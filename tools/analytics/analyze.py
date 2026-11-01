# Quiet Man Laws Shorts analytics. Usage: python3 analyze.py [studio_export.csv]
# Reads shorts.csv (one row per video and age window). Optional: merge a YouTube Studio "Content" export
# (columns like "Content","Video title","Views","Engaged views","Likes","Subscribers gained","Average view duration").
# Never invents numbers: empty cells stay empty and are skipped in averages.
import csv, sys, os, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(HERE, 'shorts.csv'))))
def num(x):
    try: return float(str(x).replace(',', '').replace('%', ''))
    except: return None
if len(sys.argv) > 1:
    ex = list(csv.DictReader(open(sys.argv[1], encoding='utf-8-sig')))
    by_id = {r['video_id']: r for r in rows}
    for e in ex:
        vid = e.get('Content') or e.get('Video')
        if not vid or vid == 'Total': continue
        r = by_id.get(vid) or {'video_id': vid, 'title': e.get('Video title', ''), 'window': 'export'}
        for k_src, k in [('Views', 'views'), ('Engaged views', 'engaged_views'), ('Likes', 'likes'), ('Subscribers gained', 'subs_gained'), ('Comments added', 'comments'), ('Shares', 'shares'), ('Stayed to watch (%)', 'stayed_pct'), ('Average percentage viewed (%)', 'avg_pct_viewed')]:
            if e.get(k_src) not in (None, ''): r[k] = e[k_src]
        if vid not in by_id: rows.append(r); by_id[vid] = r
    with open(os.path.join(HERE, 'shorts.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); [w.writerow({k: r.get(k, '') for k in rows[0].keys()}) for r in rows]
for r in rows:
    v, e, l, s = num(r.get('views')), num(r.get('engaged_views')), num(r.get('likes')), num(r.get('subs_gained'))
    r['like_rate_pct'] = round(l / v * 100, 2) if v and l is not None else None
    r['subs_per_1k'] = round(s / v * 1000, 2) if v and s is not None else None
    r['engaged_share_pct'] = round(e / v * 100, 1) if v and e is not None else None
print('video | window | views | stayed% | avg%viewed | like% | subs/1k | engaged share%')
for r in rows:
    print(' | '.join(str(x) for x in [r['title'][:40], r.get('window'), r.get('views'), r.get('stayed_pct'), r.get('avg_pct_viewed'), r['like_rate_pct'], r['subs_per_1k'], r['engaged_share_pct']]))
for key in ['format', 'pillar', 'hook_type', 'visual_style', 'voice']:
    groups = {}
    for r in rows:
        x = num(r.get('stayed_pct'))
        if x is not None: groups.setdefault(r.get(key, ''), []).append(x)
    if groups:
        print(f'\nstayed% by {key}: ' + ', '.join(f'{g or "?"}: {st.mean(v):.1f} (n={len(v)})' for g, v in groups.items()))
print('\nSmall samples: treat differences as hypotheses, not proof.')
