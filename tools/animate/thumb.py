# Quiet Man Laws Shorts cover / thumbnail (LOCKED style, 1 Nov 2026).
# Usage: python3 thumb.py bg.png "HE CHASED. SHE *RAN.*" out.jpg [zoom] [focus_y]
# Layout: brand tag + framed headline (one gold word) in the top third, the story's key moment below, bottom 20% kept clear for platform UI.
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
W, H = 1080, 1920
F_BOLD = '/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf'
F_SEMI = '/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
GOLD, WHITE = (242, 196, 109), (255, 255, 255)
STYLE = 'clean'  # LOCKED 1 Nov 2026 (Mario): no box, no tag; big glowing white text with one gold word, like the in-video captions

def cover(img, zoom, fy):
    s = max(W / img.width, H / img.height) * zoom
    img = img.resize((int(img.width * s), int(img.height * s)), Image.LANCZOS)
    x = (img.width - W) // 2
    y = int(min(max(img.height * fy - H * 0.62, 0), img.height - H))
    return img.crop((x, y, x + W, y + H))

def main():
    bg, text, out = sys.argv[1], sys.argv[2], sys.argv[3]
    zoom = float(sys.argv[4]) if len(sys.argv) > 4 else 1.35
    fy = float(sys.argv[5]) if len(sys.argv) > 5 else 0.6
    img = cover(Image.open(bg).convert('RGB'), zoom, fy)
    img = ImageEnhance.Contrast(img).enhance(1.15)
    vig = Image.new('L', (W, H), 0); ImageDraw.Draw(vig).ellipse([-W*0.35, H*0.12, W*1.35, H*1.15], fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(160))
    img = Image.composite(img, Image.new('RGB', (W, H), (0, 0, 0)), vig)
    # top shade so the headline always reads
    shade = Image.new('L', (W, H), 0); d = ImageDraw.Draw(shade)
    for yy in range(0, 900):
        d.line([(0, yy), (W, yy)], fill=int(215 * (1 - yy / 900) ** 1.6))
    img = Image.composite(Image.new('RGB', (W, H), (0, 0, 0)), img, shade)
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    # headline, auto size, max 3 lines
    words = [(w.replace('*', ''), w.startswith('*') or w.endswith('*') or w.endswith('*.') ) for w in text.split()]
    size = 112
    while True:
        f = ImageFont.truetype(F_BOLD, size); lines, cur = [], []
        for w in words:
            t = ' '.join(x for x, _ in cur + [w])
            if cur and f.getlength(t) > W - 200: lines.append(cur); cur = [w]
            else: cur.append(w)
        lines.append(cur)
        if len(lines) <= 3 or size <= 90: break
        size -= 8
    lh = int(size * 1.12); top = 300
    box_h = len(lines) * lh + 90
    if STYLE == 'box':  # old boxed look, kept only for reference
        d.rounded_rectangle([60, top - 45, W - 60, top - 45 + box_h], radius=28, outline=GOLD + (255,), width=5, fill=(0, 0, 0, 120))
    for i, ln in enumerate(lines):
        full = ' '.join(x for x, _ in ln); x = (W - f.getlength(full)) / 2; y = top + i * lh
        for wd, g in ln:
            d.text((x, y), wd, font=f, fill=GOLD if g else WHITE); x += f.getlength(wd + ' ')
    glow = layer.filter(ImageFilter.GaussianBlur(14))
    shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); shadow.putalpha(layer.getchannel('A').filter(ImageFilter.GaussianBlur(9)).point(lambda a: min(255, int(a * 0.85))))
    out_img = Image.alpha_composite(img.convert('RGBA'), shadow)
    out_img = Image.alpha_composite(out_img, glow); out_img = Image.alpha_composite(out_img, glow)
    out_img = Image.alpha_composite(out_img, layer).convert('RGB')
    out_img.save(out, quality=92)
    print('ok', out)

if __name__ == '__main__':
    main()
