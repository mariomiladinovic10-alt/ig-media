# Text video backgrounds without OpenArt credits (9 Nov 2026 weekly run).
# Draws the locked white glow look procedurally: black, charcoal ground, one soft spotlight from above,
# and a clean glowing white stick figure (round head, thick uniform lines, no face) in a simple pose,
# plus optional dim gray props (bench, door, window, phone, second figure).
# Usage: python3 txtbg.py out.png pose [props comma separated] [x]
#   poses: stand, stand_phone, sit, sit_phone, sit_headdown, walk, stand_back
#   props: bench, door, window, table, other (dim gray second figure facing him), phone_on_bench
import sys, math
from PIL import Image, ImageDraw, ImageFilter
W, H, GY = 1080, 1920, 1390  # ground line
LW, HR = 15, 36              # line width, head radius

def spotlight(img, cx):
    beam = Image.new('L', (W, H), 0); d = ImageDraw.Draw(beam)
    d.polygon([(cx - 40, 0), (cx + 40, 0), (cx + 260, GY), (cx - 260, GY)], fill=38)
    beam = beam.filter(ImageFilter.GaussianBlur(70))
    pool = Image.new('L', (W, H), 0); ImageDraw.Draw(pool).ellipse([cx - 330, GY - 40, cx + 330, GY + 70], fill=95)
    pool = pool.filter(ImageFilter.GaussianBlur(45))
    core = Image.new('L', (W, H), 0); ImageDraw.Draw(core).rectangle([cx - 6, 0, cx + 6, GY], fill=40)
    core = core.filter(ImageFilter.GaussianBlur(22))
    for m in (beam, pool, core):
        img.paste((255, 255, 255), mask=m)

def P(x0, y0, pts):  # pose points relative to hip (x0, y0)
    return {k: (x0 + v[0], y0 + v[1]) for k, v in pts.items()}

def pose_pts(name, x):
    hip_y = GY - 170
    if name.startswith('sit'): hip_y = GY - 120
    base = {'neck': (0, -165), 'head': (0, -165 - HR - 6), 'hip': (0, 0)}
    if name == 'stand':
        b = dict(base, la=(-55, -40), ra=(55, -40), lh=(-62, 30), rh=(62, 30), lk=(-25, 85), rk=(25, 85), lf=(-35, 170), rf=(35, 170), le=(-45, -100), re=(45, -100))
    elif name == 'stand_back':  # hands in pockets, slight lean
        b = dict(base, le=(-48, -95), re=(48, -95), la=(-30, -20), ra=(30, -20), lh=(-18, 5), rh=(18, 5), lk=(-22, 85), rk=(22, 85), lf=(-34, 170), rf=(34, 170))
    elif name == 'stand_phone':
        b = dict(base, head=(8, -165 - HR - 2), le=(-45, -100), re=(40, -95), la=(-50, -40), ra=(30, -125), lh=(-55, 30), rh=(30, -125), lk=(-25, 85), rk=(25, 85), lf=(-35, 170), rf=(35, 170))
    elif name == 'walk':
        b = dict(base, le=(-40, -100), re=(40, -100), la=(-60, -55), ra=(60, -30), lh=(-80, -5), rh=(75, 25), lk=(-50, 80), rk=(40, 85), lf=(-95, 165), rf=(60, 170))
    elif name in ('sit', 'sit_phone', 'sit_headdown'):
        b = dict(base, lk=(80, 0), rk=(90, 6), lf=(85, 120), rf=(100, 120), le=(-30, -95), re=(30, -95))
        if name == 'sit':
            b.update(la=(10, -40), ra=(40, -35), lh=(70, -5), rh=(85, 0))
        elif name == 'sit_phone':
            b.update(head=(18, -160 - HR - 2), neck=(8, -160), la=(40, -70), ra=(55, -60), lh=(80, -95), rh=(85, -92))
        else:
            b.update(head=(45, -140 - HR + 6), neck=(22, -150), la=(45, -55), ra=(55, -50), lh=(80, -10), rh=(88, -5))
    else:
        raise SystemExit('unknown pose ' + name)
    return P(x, hip_y, b), hip_y

def draw_figure(layer, pts, col, lw=LW):
    d = ImageDraw.Draw(layer)
    segs = [('neck', 'hip'), ('neck', 'le'), ('le', 'la'), ('la', 'lh'), ('neck', 're'), ('re', 'ra'), ('ra', 'rh'),
            ('hip', 'lk'), ('lk', 'lf'), ('hip', 'rk'), ('rk', 'rf')]
    # shoulders: arm chain starts at neck, upper arm point 'le' then forearm to hand ('la' used as elbow when given)
    for a, b in segs:
        if a in pts and b in pts:
            d.line([pts[a], pts[b]], fill=col, width=lw, joint='curve')
            for p in (pts[a], pts[b]):
                d.ellipse([p[0] - lw / 2, p[1] - lw / 2, p[0] + lw / 2, p[1] + lw / 2], fill=col)
    hx, hy = pts['head']; d.ellipse([hx - HR, hy - HR, hx + HR, hy + HR], fill=col)

def main():
    out, pose = sys.argv[1], sys.argv[2]
    props = [p for p in (sys.argv[3].split(',') if len(sys.argv) > 3 else []) if p]
    x = int(sys.argv[4]) if len(sys.argv) > 4 else 540
    img = Image.new('RGB', (W, H), (0, 0, 0))
    ImageDraw.Draw(img).rectangle([0, GY, W, H], fill=(22, 22, 23))
    spotlight(img, x)
    dim = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(dim); g = (88, 88, 92, 255)
    if 'bench' in props or pose.startswith('sit'):
        dd.rectangle([x - 70, GY - 120, x + 120, GY - 104], fill=g)
        dd.rectangle([x - 60, GY - 104, x - 48, GY], fill=g); dd.rectangle([x + 98, GY - 104, x + 110, GY], fill=g)
    if 'door' in props:
        dx = x + 300 if x < 700 else x - 420
        dd.rectangle([dx, GY - 430, dx + 170, GY], outline=g, width=10)
        lt = Image.new('L', (W, H), 0); ImageDraw.Draw(lt).rectangle([dx + 12, GY - 418, dx + 158, GY], fill=70)
        img.paste((255, 255, 255), mask=lt.filter(ImageFilter.GaussianBlur(6)))
    if 'window' in props:
        wx = 140 if x > 400 else 780
        dd.rectangle([wx, GY - 760, wx + 190, GY - 480], outline=g, width=9)
        dd.line([(wx + 95, GY - 760), (wx + 95, GY - 480)], fill=g, width=6); dd.line([(wx, GY - 620), (wx + 190, GY - 620)], fill=g, width=6)
    if 'table' in props:
        dd.rectangle([x + 140, GY - 150, x + 330, GY - 136], fill=g); dd.rectangle([x + 228, GY - 136, x + 242, GY], fill=g)
    if 'other' in props:
        ox = x + 300 if x < 700 else x - 300
        opts, _ = pose_pts('stand_back', ox); draw_figure(dim, opts, (70, 70, 74, 255), 13)
    if 'phone_on_bench' in props:
        dd.rectangle([x + 60, GY - 132, x + 100, GY - 121], fill=(150, 150, 150, 255))
    img = Image.alpha_composite(img.convert('RGBA'), dim)
    pts, _ = pose_pts(pose, x)
    fig = Image.new('RGBA', (W, H), (0, 0, 0, 0)); draw_figure(fig, pts, (255, 255, 255, 255))
    if pose.endswith('phone'):
        px, py = pts['rh']; ImageDraw.Draw(fig).rounded_rectangle([px - 14, py - 30, px + 14, py + 14], 5, fill=(255, 255, 255, 255))
    glow = fig.split()[3].filter(ImageFilter.GaussianBlur(22)).point(lambda a: min(255, int(a * 1.6)))
    halo = Image.new('RGBA', (W, H), (255, 255, 255, 0)); halo.putalpha(glow.point(lambda a: int(a * 0.55)))
    img = Image.alpha_composite(img, halo); img = Image.alpha_composite(img, fig)
    img.convert('RGB').save(out)

if __name__ == '__main__':
    main()
