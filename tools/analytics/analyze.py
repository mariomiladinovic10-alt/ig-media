# Quiet Man Laws Shorts analytics (V3, 5 Nov 2026).
# Usage:
#   python3 analyze.py                      summary + baseline + per video diagnosis
#   python3 analyze.py studio_export.csv    merge a YouTube Studio "Content" CSV export first, then summarise
#   python3 analyze.py --report VIDEO_ID    one video report (markdown) against the channel baseline
#   python3 analyze.py --next               topic / format recommendation for the next batch
# Reads shorts.csv (one row per video and age window). The LATEST row per video is used for baselines.
# Never invents numbers: empty cells stay empty and are skipped. Small samples are hypotheses, not proof.
import csv, sys, os, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, 'shorts.csv')
rows = list(csv.DictReader(open(PATH)))

def num(x):
    try: return float(str(x).replace(',', '').replace('%', ''))
    except (TypeError, ValueError): return None

def merge_export(path):
    ex = list(csv.DictReader(open(path, encoding='utf-8-sig')))
    by_id = {r['video_id']: r for r in rows}
    for e in ex:
        vid = e.get('Content') or e.get('Video')
        if not vid or vid == 'Total': continue
        r = by_id.get(vid) or {'video_id': vid, 'title': e.get('Video title', ''), 'window': 'export'}
        for k_src, k in [('Views', 'views'), ('Engaged views', 'engaged_views'), ('Likes', 'likes'), ('Subscribers gained', 'subs_gained'),
                         ('Comments added', 'comments'), ('Shares', 'shares'), ('Stayed to watch (%)', 'stayed_pct'),
                         ('Average percentage viewed (%)', 'avg_pct_viewed')]:
            if e.get(k_src) not in (None, ''): r[k] = e[k_src]
        if vid not in by_id: rows.append(r); by_id[vid] = r
    with open(PATH, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader()
        for r in rows: w.writerow({k: r.get(k, '') for k in rows[0].keys()})

def latest():
    """Latest row per video (rows are appended in time order)."""
    out = {}
    for r in rows: out[r['video_id']] = r
    return list(out.values())

def enrich(r):
    v, e, l, s = num(r.get('views')), num(r.get('engaged_views')), num(r.get('likes')), num(r.get('subs_gained'))
    sh, avd, d = num(r.get('shares')), num(r.get('avd_s')), num(r.get('duration_s'))
    r['like_rate_pct'] = round(l / v * 100, 2) if v and l is not None else None
    r['share_rate_pct'] = round(sh / v * 100, 2) if v and sh is not None else None
    r['subs_per_1k'] = round(s / v * 1000, 2) if v and s is not None else None
    r['engaged_share_pct'] = round(e / v * 100, 1) if v and e is not None else None
    # average view duration (seconds) and average percentage viewed are different things: keep both
    if r.get('avg_pct_viewed') in (None, '') and avd and d: r['avg_pct_viewed'] = round(avd / d * 100, 1)
    return r

def baseline(rs, key):
    vals = [num(r.get(key)) for r in rs if num(r.get(key)) is not None]
    return (st.median(vals), len(vals)) if vals else (None, 0)

def format_base(r, rs, base):
    """Baseline from videos of the same format when there are at least 3, else the channel baseline.
    A 9 s quote and a 26 s story are not comparable on average % viewed."""
    same = [x for x in rs if x.get('format') == r.get('format')]
    if len([x for x in same if num(x.get('stayed_pct')) is not None]) >= 3:
        return {k: baseline(same, k) for k in base}
    return base

def diagnose(r, base, rs=None):
    """Rules from the growth brief. Compares with this channel's own medians, never with fixed promises."""
    if rs: base = format_base(r, rs, base)
    out = []
    stayed, apv, v = num(r.get('stayed_pct')), num(r.get('avg_pct_viewed')), num(r.get('views'))
    b_st, b_apv, b_v = base['stayed_pct'][0], base['avg_pct_viewed'][0], base['views'][0]
    shr, b_sh = num(r.get('share_rate_pct')), base['share_rate_pct'][0]
    if stayed is None: return ['no retention data yet (Studio needs up to 2 days)']
    if b_st and stayed < b_st * 0.9:
        out.append('stayed to watch below baseline: test the first frame and the hook (topic, frame 0 text, visual)')
    elif apv is not None and b_apv and apv < b_apv * 0.9:
        out.append('first frame holds, retention weak: test pacing, length, story development and payoff')
    elif shr is not None and b_sh is not None and shr < b_sh:
        out.append('good retention, weak sharing: test topic relevance, usefulness and originality')
    elif v is not None and b_v and v < b_v and stayed >= (b_st or 0):
        out.append('good metrics, limited distribution: check audience fit, sample size, upload time; do not assume a shadowban')
    else:
        out.append('at or above baseline: keep the variable, change one other thing next time')
    return out

def summary():
    rs = [enrich(r) for r in latest()]
    keys = ['views', 'stayed_pct', 'avd_s', 'avg_pct_viewed', 'subs_per_1k', 'like_rate_pct', 'share_rate_pct']
    base = {k: baseline(rs, k) for k in keys}
    print('CHANNEL BASELINE (median of latest row per video)')
    for k in keys: print(f'  {k}: {base[k][0]} (n={base[k][1]})')
    print('\nvideo | dur | views | stayed% | AVD s | avg % viewed | subs/1k | diagnosis')
    for r in sorted(rs, key=lambda r: r.get('published', '')):
        print(' | '.join(str(x) for x in [r['title'][:38], r.get('duration_s'), r.get('views'), r.get('stayed_pct'), r.get('avd_s'),
                                          r.get('avg_pct_viewed'), r['subs_per_1k'], '; '.join(diagnose(r, base, rs))]))
    for key in ['format', 'pillar', 'hook_type', 'visual_style', 'voice']:
        groups = {}
        for r in rs:
            x = num(r.get('stayed_pct'))
            if x is not None: groups.setdefault(r.get(key, ''), []).append(x)
        if groups:
            print(f'\nstayed% by {key}: ' + ', '.join(f'{g or "?"}: {st.mean(v):.1f} (n={len(v)})' for g, v in groups.items()))
    tv = sum(num(r.get('views')) or 0 for r in rs); ts = sum(num(r.get('subs_gained')) or 0 for r in rs)
    if tv: print(f'\nsubscribers per 1,000 views (all videos): {ts / tv * 1000:.2f}')
    print('\nSmall samples: treat differences as hypotheses, not proof.')
    return rs, base

def report(vid):
    rs, base = [enrich(r) for r in latest()], None
    base = {k: baseline(rs, k) for k in ['views', 'stayed_pct', 'avd_s', 'avg_pct_viewed', 'subs_per_1k', 'like_rate_pct', 'share_rate_pct']}
    hist = [enrich(dict(r)) for r in rows if r['video_id'] == vid]
    if not hist: sys.exit(f'{vid} not in shorts.csv')
    r = hist[-1]
    print(f"# Report: {r['title']} ({vid})\n")
    print(f"Published {r.get('published')} · {r.get('duration_s')} s · {r.get('format')} · pillar {r.get('pillar')} · hook {r.get('hook_type')}\n")
    print('| metric | ' + ' | '.join(h.get('window', '') for h in hist) + ' | channel median |')
    print('|---|' + '---|' * (len(hist) + 1))
    for k, label in [('views', 'public views'), ('engaged_views', 'engaged views'), ('stayed_pct', 'stayed to watch %'), ('swiped_pct', 'swiped away %'),
                     ('avd_s', 'average view duration (s)'), ('avg_pct_viewed', 'average % viewed'), ('likes', 'likes'), ('comments', 'comments'),
                     ('shares', 'shares'), ('subs_gained', 'subscribers gained'), ('subs_per_1k', 'subs per 1,000 views')]:
        b = base.get(k, (None,))[0] if k in base else ''
        print(f'| {label} | ' + ' | '.join(str(h.get(k) if h.get(k) not in (None, '') else '') for h in hist) + f' | {b if b is not None else ""} |')
    print('\n## Diagnosis (vs same format baseline when n>=3)\n- ' + '\n- '.join(diagnose(r, base, rs)))
    print('\n## Hypothesis tested\n(from experiments.csv / plan)\n\n## Decision\nkeep / change one variable / drop')

def next_batch():
    rs = [enrich(r) for r in latest()]
    def score(group_key):
        g = {}
        for r in rs:
            x = num(r.get('stayed_pct'))
            if x is not None: g.setdefault(r.get(group_key) or '?', []).append(x)
        return sorted(((st.mean(v), len(v), k) for k, v in g.items()), reverse=True)
    print('Recommendation for the next batch (evidence so far, small samples):')
    for key in ['format', 'hook_type', 'pillar']:
        s = score(key)
        if s: print(f'- {key}: best {s[0][2]} ({s[0][0]:.1f}% stayed, n={s[0][1]}); weakest {s[-1][2]} ({s[-1][0]:.1f}%, n={s[-1][1]})')
    top = sorted([r for r in rs if num(r.get('stayed_pct')) is not None], key=lambda r: -num(r['stayed_pct']))[:3]
    print('- strongest videos to learn from: ' + '; '.join(f"{r['title'][:40]} ({r['stayed_pct']}%)" for r in top))
    print('- rule: write new concepts that share the strongest videos\' hook type and pillar, change one variable per test (experiments.csv).')

if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == '--report': report(a[1])
    elif a and a[0] == '--next': next_batch()
    else:
        if a: merge_export(a[0])
        summary()
