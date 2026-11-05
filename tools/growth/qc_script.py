# Script quality control for Quiet Man Laws production packs (V3, 5 Nov 2026).
# Usage: python3 qc_script.py pack.json [pack2.json ...]     exit code 1 if any pack fails
# A pack is the JSON written for each Short (see tools/growth/shorts/*.json). Its "story" block is the exact
# assemble2.py story, so what passes here is what gets rendered.
import json, re, sys

BANNED = ['sigma', 'alpha male', 'beta male', 'high value man', 'grindset', 'comment yes', 'type yes', 'like and subscribe',
          'women are', 'women always', 'all women', 'men are trash', 'females', 'red pill', 'never trust a woman',
          'studies show', 'science says', 'scientifically proven', '% of men', '% of women']
DASHES = ['-', '–', '—']
WPS = 3.3  # comfortable reading speed for short uppercase lines (words per second)

def words(s): return re.findall(r"[A-Za-z0-9']+", s.replace('*', ''))

def check(pack):
    errs, warns = [], []
    st = pack.get('story', {}); scenes = st.get('scenes', [])
    if not scenes: return ['no story.scenes'], warns
    total = sum(s['dur'] for s in scenes) + (st.get('end', {}).get('dur', 0) if st.get('end', {}).get('card') else 0)
    if not 15 <= total <= 45: errs.append(f'total {total:.1f}s outside 15 to 45 s')
    # all on screen lines with absolute times
    lines, t = [], 0.0
    for s in scenes:
        bs = s.get('beats', [])
        for j, b in enumerate(bs):
            b1 = bs[j + 1]['t'] if j + 1 < len(bs) else s['dur']
            lines.append((t + b['t'], t + b1, b['text']))
        t += s['dur']
    end = st.get('end', {})
    if not end.get('text'): errs.append('no end line')
    else: lines.append((total - end.get('dur', 1.8), total, end['text']))
    if not lines or lines[0][0] > 0.01: errs.append('no caption on frame 0 (hook must be visible at once)')
    for a, b, txt in lines:
        n = len(words(txt))
        if n > 8: errs.append(f'line over 8 words: "{txt}"')
        if (b - a) < n / WPS: warns.append(f'line on screen {b - a:.1f}s, needs ~{n / WPS:.1f}s to read: "{txt}"')
        if txt.count('*') not in (0, 2): errs.append(f'gold marker must wrap one key word or phrase: "{txt}"')
    # visual change at least every 3.5 s (a new scene or a push)
    for s in scenes:
        if s['dur'] > 3.5 and abs(s.get('push', [1, 1.06])[1] - s.get('push', [1, 1.06])[0]) < 0.03:
            warns.append(f'scene {s["clip"]} {s["dur"]}s with almost no motion')
    # retention rule: payoff words only in the last 30%
    pk = [w.lower() for w in pack.get('payoff_keywords', [])]
    if not pk: errs.append('payoff_keywords missing (needed to check the retention rule)')
    for a, b, txt in lines[:-1]:
        if a < total * 0.7 and any(k in txt.lower().replace('*', '') for k in pk):
            errs.append(f'payoff revealed early at {a:.1f}s: "{txt}"')
    # copy checks
    copy = ' '.join([pack.get('title', ''), *pack.get('title_alts', []), pack.get('description', ''), pack.get('pinned_comment', ''),
                     pack.get('cover', {}).get('headline', ''), *[l[2] for l in lines]])
    for d in DASHES:
        if d in copy.replace('#shorts', ''): errs.append(f'dash character {d!r} in copy or on screen text')
    low = copy.lower()
    for b in BANNED:
        if b in low: errs.append(f'banned phrase: "{b}"')
    hooks = pack.get('hooks', [])
    if len(hooks) < 3: errs.append('fewer than 3 hook alternatives')
    for h in hooks:
        if len(words(h['text'])) > 8: errs.append(f'hook over 8 words: "{h["text"]}"')
    if not pack.get('hypothesis'): errs.append('no hypothesis')
    if not pack.get('series') in ('EMOTIONAL TRUTH', 'REAL SCENARIOS', 'PSYCHOLOGY REFRAMES'): errs.append('series must be one of the three')
    if pack.get('cover', {}).get('headline', '').replace('*', '').strip().upper() == pack.get('title', '').replace(' #shorts', '').upper():
        errs.append('cover headline must differ from the title')
    if len(pack.get('title', '')) > 100: errs.append('title over 100 characters')
    return errs, warns

def main():
    bad = 0
    for p in sys.argv[1:]:
        e, w = check(json.load(open(p)))
        print(('FAIL ' if e else 'PASS ') + p)
        for x in e: print('  error:', x)
        for x in w: print('  warn: ', x)
        bad += bool(e)
    sys.exit(1 if bad else 0)

if __name__ == '__main__':
    main()
