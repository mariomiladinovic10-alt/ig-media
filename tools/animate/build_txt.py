# Build credit free text videos from a week's txt/meta.json (weekly run, 16 Nov 2026).
# Usage: python3 tools/animate/build_txt.py media/quietmanlaws/<week>/txt/meta.json media/quietmanlaws/<week>
# Per entry: txtbg.py scenes -> story-<id>.json -> assemble2.py (music2 score, beats) -> thumb.py cover.
# No _yt version: text videos go to Instagram and TikTok only (Mario, 10 Nov 2026).
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
meta, out = json.load(open(sys.argv[1])), sys.argv[2]
tdir = os.path.dirname(os.path.abspath(sys.argv[1]))
only = sys.argv[3:]
for m in meta:
    if only and m['id'] not in only: continue
    d = os.path.join(tdir, m['id']); os.makedirs(d, exist_ok=True)
    for i, (pose, props, x) in enumerate(m['bgs']):
        subprocess.run(['python3', f'{HERE}/txtbg.py', f'{d}/bg{i+1}.png', pose, props, str(x)], check=True)
    durs, push = [4.2, 6.3, 6.8], [[1.0, 1.05], [1.05, 1.1], [1.1, 1.15]]
    scenes = [{'clip': f'bg{i+1}.png', 'dur': durs[i], 'push': push[i], 'cy': 0.62,
               'beats': [{'t': round(2.1 * j, 1), 'text': t} for j, t in enumerate(lines)]}
              for i, lines in enumerate(m['s'])]
    story = {'id': m['id'], 'seed': int(m['id'][-4:]), 'text_y': 560, 'series': m['series'], 'scenes': scenes,
             'sfx': [{'t': 4.2, 'type': 'whoosh'}, {'t': 10.5, 'type': 'whoosh'}, {'t': 14.7, 'type': 'hit'}],
             'end': {'text': m['end'], 'sub': 'Follow @quietmanlaws', 'dur': 2.6}}
    sp = f'{HERE}/story-{m["id"]}.json'; json.dump(story, open(sp, 'w'), indent=1)
    subprocess.run(['python3', f'{HERE}/assemble2.py', sp, d, f'{out}/{m["id"]}.mp4'], check=True)
    subprocess.run(['python3', f'{HERE}/thumb.py', f'{d}/bg1.png', m['cover'], f'{out}/{m["id"]}_cover.jpg', '1.15', '0.62'], check=True)
    print('built', m['id'])
