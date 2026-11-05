# V2 assembler for Quiet Man Laws Shorts (1 Nov 2026). assemble.py stays as it was.
# Usage: python3 assemble2.py story.json clips_dir out.mp4 [yt|ig|tt]
#   optional platform: swaps end.sub for that platform's call to action (end.sub_yt etc., else endcta.CTA)
#   (Mario 5 Nov 2026: YouTube versions end with a subscribe line). Without it nothing changes.
# story.json:
# {"id": "qml-anim-10", "seed": 10,
#  "scenes": [ {"clip": "c1.mp4", "start": 0.0, "dur": 3.0, "speed": 1.0, "push": [1.00, 1.06],
#               "beats": [ {"t": 0.0, "text": "HE NEVER *ANSWERED* THE INSULT."} ] }, ...],
#  "sfx": [ {"t": 7.2, "type": "hit"}, {"t": 12.0, "type": "whoosh"} ],
#  "end": {"text": "SILENCE IS AN *ANSWER* TOO.", "sub": "Follow @quietmanlaws", "dur": 1.8} }
# Changes vs assemble.py:
#  - several caption beats per scene (a new line every 1.5 to 3 s instead of one per 5 s scene)
#  - each scene can trim and slow a clip (start, dur, speed) and adds a slow push-in so the frame never sits still
#  - hard cuts by default (crossfade only if "xf" is given), so the story moves faster
#  - the final line sits over the last scene (no black end card) unless end.card is true
#  - optional synthesized sound accents (hit, whoosh), music ducked under nothing (silent videos)
import json, os, subprocess, sys, tempfile
import numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from assemble import text_card, GOLD  # same locked caption look
from PIL import Image, ImageDraw, ImageFilter
W, H, FPS = 1080, 1920, 30

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: sys.exit(r.stderr[-3000:])

def scene_clip(src, sc, out):
    st, d, sp = sc.get('start', 0.0), sc['dur'], sc.get('speed', 1.0)
    z0, z1 = sc.get('push', [1.0, 1.06]); cy = sc.get('cy', 0.5)
    n = int(round(d * FPS))
    zoom = f"{z0}+({z1}-{z0})*min(1\\,n/{max(n-1,1)})"
    vf = (f"trim=start={st},setpts=(PTS-STARTPTS)*{sp},fps={FPS},"
          f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
          f"tpad=stop_mode=clone:stop_duration={d + 1:.2f},"
          f"scale=w='iw*({zoom})':h='ih*({zoom})':eval=frame,crop={W}:{H}:(iw-{W})/2:(ih-{H})*{cy},"
          f"hue=s=0,{sc.get('grade', 'null')},eq=contrast=1.08:brightness=-0.01,format=gbrp,split[a][b];[b]gblur=sigma=18[g];"
          f"[a][g]blend=all_mode=screen:all_opacity=0.45,format=yuv420p,setsar=1")
    run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-filter_complex', vf, '-frames:v', str(n), '-an',
         '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-r', str(FPS), out])

def add_plate(png, strength=150):
    # soft dark plate behind the caption so it stays readable on bright scenes (V2 subtitle contrast rule)
    im = Image.open(png).convert('RGBA'); bb = im.getchannel('A').point(lambda a: 255 if a > 40 else 0).getbbox()
    if not bb: return
    pad = 60; m = Image.new('L', im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([bb[0]-pad, bb[1]-pad//2, bb[2]+pad, bb[3]+pad//2], radius=50, fill=strength)
    m = m.filter(ImageFilter.GaussianBlur(28))
    plate = Image.new('RGBA', im.size, (0, 0, 0, 0)); plate.putalpha(m)
    Image.alpha_composite(plate, im).save(png)

def series_tag(text, path, y):
    # small letter spaced series label above the hook on the first scene (V3, 5 Nov 2026)
    from assemble import FONT2
    from PIL import ImageFont
    f = ImageFont.truetype(FONT2, 38); sp = 6
    w = sum(f.getlength(ch) + sp for ch in text) - sp
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img); x = (W - w) / 2
    for ch in text:
        d.text((x, y), ch, font=f, fill=(189, 189, 189)); x += f.getlength(ch) + sp
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.paste((0, 0, 0, 200), mask=img.split()[3].filter(ImageFilter.GaussianBlur(5)))
    Image.alpha_composite(sh, img).save(path)

def sfx_track(events, total, sr=44100):
    a = np.zeros(int(sr * (total + 1)))
    for e in events:
        i0 = int(e['t'] * sr)
        if e['type'] == 'hit':
            t = np.arange(int(sr * 1.6)) / sr
            s = (np.sin(2*np.pi*50*t) + .35*np.sin(2*np.pi*100*t)) * np.exp(-t*3.5) * (1-np.exp(-t*400)) * .55
        else:  # whoosh: band limited noise swell
            t = np.arange(int(sr * .7)) / sr
            nz = np.random.default_rng(int(e['t']*100)).standard_normal(len(t))
            nz = np.convolve(nz, np.ones(40)/40, mode='same')
            s = nz * np.sin(np.pi * t / t[-1]) ** 2 * .12
        a[i0:i0 + len(s)] += s[:max(0, len(a) - i0)]
    return a

def main():
    story, cdir, out = json.load(open(sys.argv[1])), sys.argv[2], sys.argv[3]
    if len(sys.argv) > 4 and story.get('end', {}).get('text'):
        from endcta import CTA
        story['end']['sub'] = story['end'].get(f'sub_{sys.argv[4]}', CTA[sys.argv[4]])
    tmp = tempfile.mkdtemp(); parts = []; t = 0.0; caps = []
    for i, sc in enumerate(story['scenes']):
        if story.get('grade'): sc.setdefault('grade', story['grade'])  # extra filter, e.g. curves to turn old neon clips into the white glow look
        p = os.path.join(tmp, f's{i}.mp4'); scene_clip(os.path.join(cdir, sc['clip']), sc, p); parts.append(p)
        beats = sc.get('beats', [])
        for j, b in enumerate(beats):
            b1 = beats[j + 1]['t'] if j + 1 < len(beats) else sc['dur']
            caps.append((t + b['t'], t + b1, b['text']))
        t += sc['dur']
    end = story.get('end', {}); total = t
    if end.get('card'):
        d = end.get('dur', 2.0)
        p = os.path.join(tmp, 'end.mp4')
        run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', f'color=c=black:s={W}x{H}:r={FPS}:d={d}', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', p]); parts.append(p)
        total += d
    lst = os.path.join(tmp, 'l.txt'); open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
    raw = os.path.join(tmp, 'raw.mp4')
    run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', raw])
    # captions (+ final line over the last seconds)
    if end.get('text'):
        d = end.get('dur', 1.8)
        caps = [c if c[1] <= total - d else (c[0], total - d, c[2]) for c in caps if c[0] < total - d]
        caps.append((total - d, total, end['text'], end.get('sub')))
    inputs = ['-i', raw]; fc = []; prev = '0:v'
    for k, c in enumerate(caps):
        png = os.path.join(tmp, f'c{k}.png')
        y = story.get('text_y', 330)
        text_card(c[2], png, size=story.get('text_size', 80), y=y, sub=c[3] if len(c) > 3 else None)
        if story.get('plate', True): add_plate(png)
        inputs += ['-loop', '1', '-t', f'{total:.3f}', '-i', png]
        fc.append(f"[{prev}][{k+1}:v]overlay=0:0:enable='between(t,{c[0]:.3f},{c[1]-0.001:.3f})'[v{k}]"); prev = f'v{k}'
    if story.get('series'):
        png = os.path.join(tmp, 'series.png'); series_tag(story['series'], png, story.get('text_y', 330) - 80)
        k = len(caps); inputs += ['-loop', '1', '-t', f'{total:.3f}', '-i', png]
        t1 = story['scenes'][0]['dur']
        fc.append(f"[{prev}][{k+1}:v]overlay=0:0:enable='between(t,0,{t1:.3f})'[vs]"); prev = 'vs'
    vout = os.path.join(tmp, 'v.mp4')
    run(['ffmpeg', '-y', '-loglevel', 'error', *inputs, '-filter_complex', ';'.join(fc), '-map', f'[{prev}]', '-t', f'{total:.3f}',
         '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-r', str(FPS), '-pix_fmt', 'yuv420p', vout])
    # audio: original music + accents
    mus = os.path.join(tmp, 'm.wav'); run(['python3', os.path.join(HERE, 'music2.py'), mus, f'{total + 0.3:.2f}', str(story.get('seed', 1))])
    m, sr = sf.read(mus); m = m if m.ndim == 1 else m.mean(1)
    fx = sfx_track(story.get('sfx', []), total, sr)[:len(m)]
    mix = m[:len(fx)] + fx; mix = mix / max(1e-9, np.abs(mix).max()) * 0.9
    aw = os.path.join(tmp, 'a.wav'); sf.write(aw, mix, sr)
    run(['ffmpeg', '-y', '-loglevel', 'error', '-i', vout, '-i', aw, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
         '-af', 'loudnorm=I=-14:TP=-1.0:LRA=11', '-c:a', 'aac', '-b:a', '160k', '-t', f'{total:.3f}', '-movflags', '+faststart', out])
    print('done', out, f'{total:.2f}s', f'{len(caps)} caption beats')

if __name__ == '__main__':
    main()
