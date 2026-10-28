# ig-media

Automatic Instagram publishing for @mind.psychollogy and @quietmanlaws, run by GitHub Actions (free, no computer needed).

- `media/` images (JPG) and reels (MP4), served publicly to Instagram from raw.githubusercontent.com
- `queue/` one JSON file per scheduled post
- `stats/` daily post metrics, written by the bot
- `scripts/ig.py` publisher (Instagram API with Instagram Login)

Queue item:

```json
{
  "account": "mind",              
  "type": "POST",                 
  "media_url": "https://raw.githubusercontent.com/mariomiladinovic10-alt/ig-media/main/media/....jpg",
  "caption": "...",
  "publish_at": "2026-11-09T00:00:00Z",
  "status": "pending"
}
```

`account`: `mind` or `quietmanlaws`. `type`: `POST`, `REEL` or `STORY`. Times are UTC.
The publish workflow runs every hour and posts everything that is due.

Secrets (Settings > Secrets and variables > Actions): `IG_TOKEN_MIND`, `IG_TOKEN_QML`, optional `GH_PAT` for automatic token renewal.
