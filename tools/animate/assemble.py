# Assemble OpenArt clips into a finished 1080x1920 Reel / Short in the locked Quiet Man Laws animated style.
# Usage: python3 assemble.py story.json clips_dir out.mp4
# story.json: {"id","seed","scenes":[{"clip":"c1.mp4","text":"THEY *LAUGHED*."}...],"end":"WORK IN *SILENCE*.","handle":"@quietmanlaws"}
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS, XF = 1080, 1920, 30, 0.4
FONT = '/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf'
FONT2 = '/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
GOLD, WHITE = (242, 196, 109), (255, 255, 255)
HERE = os.path.dirname(os.path.abspath(__file__))

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: sys.exit(r.stderr[-3000:])
    return r.stdout

def dur(p):
    return float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]).strip())

def text_card(text, path, size=78, y=360, sub=None):
    """Uppercase glowing text, *word* rendered in gold. Transparent PNG."""
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    f = ImageFont.truetype(FONT, size)
    words = [(w.strip('*'), w.startswith('*')) for w in text.split()]
    lines, cur, maxw = [], [], W - 160
    for w in words:
        test = ' '.join(x for x, _ in cur + [w])
        if cur and f.getlength(test) > maxw: lines.append(cur); cur = [w]
        else: cur.append(w)
    lines.append(cur)
    lh = int(size * 1.18)
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    for i, ln in enumerate(lines):
        full = ' '.join(x for x, _ in ln); x = (W - f.getlength(full)) / 2; yy = y + i * lh
        for wd, gold in ln:
            d.text((x, yy), wd, font=f, fill=GOLD if gold else WHITE)
            x += f.getlength(wd + ' ')
    if sub:
        f2 = ImageFont.truetype(FONT2, 44)
        d.text(((W - f2.getlength(sub)) / 2, y + len(lines) * lh + 40), sub, font=f2, fill=(220, 220, 220))
    glow = layer.filter(ImageFilter.GaussianBlur(14))
    img = Image.alpha_composite(img, glow); img = Image.alpha_composite(img, glow)
    shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    shadow.paste((0, 0, 0, 170), mask=layer.split()[3].filter(ImageFilter.GaussianBlur(6)))
    img = Image.alpha_composite(shadow, img); img = Image.alpha_composite(img, layer)
    img.save(path)

def main():
    story, cdir, out = json.load(open(sys.argv[1])), sys.argv[2], sys.argv[3]
    tmp = tempfile.mkdtemp()
    scenes = story['scenes']; n = len(scenes)
    lens = [min(dur(os.path.join(cdir, s['clip'])), 5.0) for s in scenes]
    END = 2.4
    # timeline: scene i starts at sum(lens[:i]) - i*XF
    starts = [sum(lens[:i]) - i * XF for i in range(n)]
    total_scenes = starts[-1] + lens[-1]
    total = total_scenes - XF + END
    inputs, fc = [], []
    for i, s in enumerate(scenes):
        inputs += ['-i', os.path.join(cdir, s['clip'])]
        # cover-scale to 1080x1920, subtle glow (screen-blended blur), slight contrast
        fc.append(f'[{i}:v]trim=0:{lens[i]},setpts=PTS-STARTPTS,fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},'
                  f'hue=s=0,eq=contrast=1.08:brightness=-0.01,format=gbrp,split[a{i}][b{i}];[b{i}]gblur=sigma=18[g{i}];'
                  f'[a{i}][g{i}]blend=all_mode=screen:all_opacity=0.45,format=yuv420p,setsar=1[v{i}]')
    # end card: black with soft vignette light
    inputs += ['-f', 'lavfi', '-i', f'color=c=black:s={W}x{H}:r={FPS}:d={END}']
    fc.append(f'[{n}:v]format=yuv420p,setsar=1[vend]')
    prev = 'v0'
    for i in range(1, n):
        fc.append(f'[{prev}][v{i}]xfade=transition=fade:duration={XF}:offset={starts[i]:.3f}[x{i}]'); prev = f'x{i}'
    fc.append(f'[{prev}][vend]xfade=transition=fade:duration={XF}:offset={total_scenes - XF:.3f}[base]')
    # text overlays
    k = n + 1; prev = 'base'
    cards = []
    for i, s in enumerate(scenes):
        p = os.path.join(tmp, f't{i}.png'); text_card(s['text'], p, size=84 if i == 0 else 76)
        t0 = 0 if i == 0 else starts[i] + 0.25; t1 = starts[i] + lens[i] - 0.15
        cards.append((p, t0, t1, i == 0))
    p = os.path.join(tmp, 'tend.png'); text_card(story['end'], p, size=96, y=820, sub='Follow ' + story.get('handle', '@quietmanlaws'))
    cards.append((p, total_scenes - XF + 0.1, total, False))
    for p, t0, t1, hook in cards:
        inputs += ['-loop', '1', '-t', f'{total:.3f}', '-i', p]
        fin = '' if hook else f'fade=t=in:st={t0:.3f}:d=0.35:alpha=1,'
        fc.append(f'[{k}:v]format=rgba,{fin}fade=t=out:st={t1 - 0.3:.3f}:d=0.3:alpha=1[o{k}]')
        fc.append(f'[{prev}][o{k}]overlay=0:0:shortest=1[y{k}]'); prev = f'y{k}'; k += 1
    fc.append(f'[{prev}]trim=0:{total:.3f},format=yuv420p[vout]')
    music = os.path.join(tmp, 'm.wav')
    run(['python3', os.path.join(HERE, 'music.py'), music, f'{total + 0.2:.2f}', str(story.get('seed', 1))])
    inputs += ['-i', music]
    fc.append(f'[{k}:a]atrim=0:{total:.3f},loudnorm=I=-16:TP=-1.5:LRA=11,aresample=44100[aout]')
    run(['ffmpeg', '-y', '-loglevel', 'error', *inputs, '-filter_complex', ';'.join(fc), '-map', '[vout]', '-map', '[aout]',
         '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-r', str(FPS), '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k',
         '-movflags', '+faststart', out])
    print('done', out, f'{total:.2f}s')

if __name__ == '__main__':
    main()
