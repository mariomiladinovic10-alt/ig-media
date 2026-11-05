# Swap the small line under the final caption of a finished Short for a platform specific call to action.
# Mario, 5 Nov 2026: "dodaj to na kraju" (add a subscribe line at the end of the YouTube versions).
# Usage: python3 endcta.py story.json in.mp4 out.mp4 [yt|ig|tt] ["custom line"]
# Works on already rendered videos (no clips needed): it finds where assemble2.py drew end.sub
# (same wrap logic as text_card), covers it with a soft dark plate and draws the new line in the same look.
# The video stream is re-encoded only for the overlay; audio is copied.
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from assemble import FONT, FONT2, W, H

CTA = {  # one short line, no dashes, fits the 1080 px width at 44 px
    'yt': 'Subscribe for the next Quiet Law',
    'ig': 'Follow @quietmanlaws',
    'tt': 'Follow for the next Quiet Law',
}

def caption_lines(text, size):
    f = ImageFont.truetype(FONT, size); words = [w.strip('*') for w in text.split()]
    lines, cur = 0, []
    for w in words:
        if cur and f.getlength(' '.join(cur + [w])) > W - 160: lines += 1; cur = [w]
        else: cur.append(w)
    return lines + 1

def sub_box(story):
    end = story['end']; size = story.get('text_size', 80); y = story.get('text_y', 330)
    sy = y + caption_lines(end['text'], size) * int(size * 1.18) + 40
    old = ImageFont.truetype(FONT2, 44).getlength(end.get('sub') or '')
    return sy, old

def overlay_png(story, line, path):
    sy, old_w = sub_box(story)
    f2 = ImageFont.truetype(FONT2, 44); new_w = f2.getlength(line); w = max(old_w, new_w)
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    # plate over the old line: darker than assemble2's caption plate so the old text disappears
    m = Image.new('L', (W, H), 0)
    ImageDraw.Draw(m).rounded_rectangle([(W - w) / 2 - 40, sy - 18, (W + w) / 2 + 40, sy + 70], radius=36, fill=245)
    m = m.filter(ImageFilter.GaussianBlur(14))
    plate = Image.new('RGBA', (W, H), (8, 8, 8, 0)); plate.putalpha(m); img = Image.alpha_composite(img, plate)
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    d.text(((W - new_w) / 2, sy), line, font=f2, fill=(232, 232, 232))
    glow = layer.filter(ImageFilter.GaussianBlur(8))
    img = Image.alpha_composite(img, glow); img = Image.alpha_composite(img, layer)
    img.save(path)

def main():
    story = json.load(open(sys.argv[1])); src, out = sys.argv[2], sys.argv[3]
    plat = sys.argv[4] if len(sys.argv) > 4 else 'yt'
    line = sys.argv[5] if len(sys.argv) > 5 else story['end'].get(f'sub_{plat}', CTA[plat])
    if '-' in line or '—' in line or '–' in line: sys.exit('no dashes in on screen text')
    total = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src]).strip())
    t0 = total - story['end'].get('dur', 1.8)
    png = os.path.join(tempfile.mkdtemp(), 'cta.png'); overlay_png(story, line, png)
    r = subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-loop', '1', '-t', f'{total:.3f}', '-i', png,
                        '-filter_complex', f"[0:v][1:v]overlay=0:0:enable='gte(t,{t0:.3f})'[v]", '-map', '[v]', '-map', '0:a?',
                        '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'copy',
                        '-t', f'{total:.3f}', '-movflags', '+faststart', out], capture_output=True, text=True)
    if r.returncode: sys.exit(r.stderr[-2000:])
    print('ok', out, f'end line "{line}" from {t0:.2f}s')

if __name__ == '__main__':
    main()
