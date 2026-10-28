"""Instagram publisher for the ig-media repo.

Runs inside GitHub Actions. Uses the official Instagram API with Instagram Login
(graph.instagram.com). Access tokens come from repository secrets and are never
written to the repo.

Commands:
  python scripts/ig.py check     -> verify every configured token, print the username
  python scripts/ig.py publish   -> publish every queue item whose time has come
  python scripts/ig.py stats     -> save recent post metrics to stats/<account>.json
  python scripts/ig.py refresh   -> refresh long-lived tokens (needs GH_PAT to store them)
"""
import datetime as dt
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://graph.instagram.com/v21.0"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, "queue")
STATS = os.path.join(ROOT, "stats")

# account key -> secret name holding its long-lived Instagram access token
ACCOUNTS = {
    "mind": "IG_TOKEN_MIND",          # @mind.psychollogy
    "quietmanlaws": "IG_TOKEN_QML",    # @quietmanlaws
}


def token_for(account):
    return os.environ.get(ACCOUNTS.get(account, ""), "").strip()


def call(method, path, params=None, token=""):
    params = dict(params or {})
    params["access_token"] = token
    url = path if path.startswith("http") else f"{API}/{path}"
    data = None
    if method == "GET":
        url += "?" + urllib.parse.urlencode(params)
    else:
        data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(url, data=data, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise RuntimeError(f"{method} {path} -> {e.code}: {body[:400]}") from None


def now_utc():
    return dt.datetime.now(dt.timezone.utc)


def parse_time(s):
    t = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    if t.tzinfo is None:
        t = t.replace(tzinfo=dt.timezone.utc)
    return t


def load_queue():
    items = []
    if not os.path.isdir(QUEUE):
        return items
    for name in sorted(os.listdir(QUEUE)):
        if name.endswith(".json"):
            path = os.path.join(QUEUE, name)
            with open(path, encoding="utf-8") as f:
                items.append((path, json.load(f)))
    return items


def save(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def wait_ready(container, token, limit=600):
    start = time.time()
    while time.time() - start < limit:
        st = call("GET", container, {"fields": "status_code,status"}, token)
        code = st.get("status_code")
        if code == "FINISHED":
            return
        if code in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"container {container} failed: {st}")
        time.sleep(10)
    raise RuntimeError(f"container {container} not ready after {limit}s")


def publish_item(item):
    token = token_for(item["account"])
    if not token:
        raise RuntimeError(f"no token for account {item['account']} (secret {ACCOUNTS.get(item['account'])})")
    me = call("GET", "me", {"fields": "user_id,username"}, token)
    uid = me.get("user_id") or me.get("id")
    kind = item.get("type", "POST").upper()
    params = {"caption": item.get("caption", "")}
    if kind == "REEL":
        params.update({"media_type": "REELS", "video_url": item["media_url"], "share_to_feed": "true"})
        if item.get("cover_url"):
            params["cover_url"] = item["cover_url"]
    elif kind == "STORY":
        if item["media_url"].lower().endswith(".mp4"):
            params = {"media_type": "STORIES", "video_url": item["media_url"]}
        else:
            params = {"media_type": "STORIES", "image_url": item["media_url"]}
    else:
        params["image_url"] = item["media_url"]
    container = call("POST", f"{uid}/media", params, token)["id"]
    wait_ready(container, token)
    published = call("POST", f"{uid}/media_publish", {"creation_id": container}, token)
    return published["id"], me.get("username")


def cmd_publish():
    changed = False
    max_per_run = int(os.environ.get("MAX_PER_RUN", "4"))
    done = 0
    for path, item in load_queue():
        if item.get("status") != "pending":
            continue
        if parse_time(item["publish_at"]) > now_utc():
            continue
        if done >= max_per_run:
            break
        try:
            media_id, username = publish_item(item)
            item.update(status="published", media_id=media_id, published_at=now_utc().isoformat(), username=username)
            print(f"published {os.path.basename(path)} -> @{username} {media_id}")
        except Exception as e:  # keep going with the rest of the queue
            item["attempts"] = item.get("attempts", 0) + 1
            item["last_error"] = str(e)[:500]
            if item["attempts"] >= 3:
                item["status"] = "failed"
            print(f"ERROR {os.path.basename(path)}: {e}", file=sys.stderr)
        save(path, item)
        changed = True
        done += 1
    print("changed" if changed else "nothing due")


def cmd_check():
    ok = True
    for account, secret in ACCOUNTS.items():
        token = token_for(account)
        if not token:
            print(f"{account}: secret {secret} not set")
            continue
        try:
            me = call("GET", "me", {"fields": "user_id,username,account_type,media_count"}, token)
            print(f"{account}: OK @{me.get('username')} ({me.get('account_type')}, {me.get('media_count')} posts)")
        except Exception as e:
            ok = False
            print(f"{account}: FAILED {e}")
    sys.exit(0 if ok else 1)


def cmd_stats():
    os.makedirs(STATS, exist_ok=True)
    for account in ACCOUNTS:
        token = token_for(account)
        if not token:
            continue
        try:
            me = call("GET", "me", {"fields": "user_id,username,followers_count,media_count"}, token)
            media = call("GET", "me/media", {"fields": "id,caption,media_type,media_product_type,timestamp,permalink,like_count,comments_count", "limit": 50}, token).get("data", [])
            for m in media:
                metrics = "reach,saved,shares,views,total_interactions"
                try:
                    ins = call("GET", f"{m['id']}/insights", {"metric": metrics}, token).get("data", [])
                    m["insights"] = {d["name"]: (d.get("values") or [{}])[0].get("value", d.get("total_value", {}).get("value")) for d in ins}
                except Exception as e:
                    m["insights_error"] = str(e)[:200]
            save(os.path.join(STATS, f"{account}.json"), {"collected_at": now_utc().isoformat(), "profile": me, "media": media})
            print(f"{account}: saved {len(media)} posts")
        except Exception as e:
            print(f"{account}: stats FAILED {e}", file=sys.stderr)


def cmd_refresh():
    pat = os.environ.get("GH_PAT", "").strip()
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    for account, secret in ACCOUNTS.items():
        token = token_for(account)
        if not token:
            continue
        try:
            res = call("GET", "https://graph.instagram.com/refresh_access_token", {"grant_type": "ig_refresh_token"}, token)
            new = res.get("access_token")
            days = int(res.get("expires_in", 0)) // 86400
            if new and pat and repo:
                env = dict(os.environ, GH_TOKEN=pat)
                subprocess.run(["gh", "secret", "set", secret, "--repo", repo, "--body", new], check=True, env=env, capture_output=True)
                print(f"{account}: token refreshed and saved, valid {days} days")
            else:
                print(f"{account}: token refreshed on Instagram's side (valid {days} days); add GH_PAT to store new tokens automatically")
        except Exception as e:
            print(f"{account}: refresh FAILED {e}", file=sys.stderr)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "publish"
    {"publish": cmd_publish, "check": cmd_check, "stats": cmd_stats, "refresh": cmd_refresh}[cmd]()
