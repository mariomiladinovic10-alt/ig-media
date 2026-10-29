# Synthesize a royalty free, original cinematic piano + pad bed. Usage: python3 music.py out.wav seconds [seed]
import sys, numpy as np, wave
out, secs = sys.argv[1], float(sys.argv[2]); seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
rng = np.random.default_rng(seed); sr = 44100; n = int(secs * sr); t = np.arange(n) / sr
def hz(m): return 440 * 2 ** ((m - 69) / 12)
progs = [[[57,60,64],[53,57,60],[48,52,55],[55,59,62]],   # Am F C G
         [[50,53,57],[46,50,53],[53,57,60],[48,52,55]],   # Dm Bb F C
         [[52,55,59],[48,52,55],[55,59,62],[50,54,57]]]   # Em C G D
prog = progs[seed % 3]; bar = 3.0
mix = np.zeros(n)
def piano(f, start, dur, amp):
    i0 = int(start * sr); L = min(int(dur * sr), n - i0)
    if L <= 0: return
    tt = np.arange(L) / sr
    env = np.exp(-tt * 2.2) * (1 - np.exp(-tt * 300))
    s = sum(a * np.sin(2 * np.pi * f * k * tt) for k, a in [(1, 1), (2, .45), (3, .18), (4, .08)])
    mix[i0:i0 + L] += amp * env * s
k = 0; s = 0.0
while s < secs:
    ch = prog[k % 4]
    piano(hz(ch[0] - 12), s, bar, .28)                       # bass
    for j, m in enumerate([ch[0], ch[1], ch[2], ch[1] + 12, ch[2], ch[1]]):   # arpeggio
        if s > 1.5: piano(hz(m + 12), s + j * bar / 6, 1.8, .12)
    # pad
    i0 = int(s * sr); L = min(int(bar * sr), n - i0)
    if L > 0:
        tt = np.arange(L) / sr; env = np.minimum(1, tt / .8) * np.minimum(1, (bar - tt) / .8)
        mix[i0:i0 + L] += .05 * env * sum(np.sin(2 * np.pi * hz(m) * tt) + .5 * np.sin(2 * np.pi * hz(m) * 1.003 * tt) for m in ch)
    s += bar; k += 1
# reverb: convolve with decaying noise
ir = rng.standard_normal(int(1.8 * sr)) * np.exp(-np.arange(int(1.8 * sr)) / sr * 3.2)
wet = np.convolve(mix, ir)[:n] * .015
y = mix + wet
y *= np.minimum(1, t / 1.0) * np.minimum(1, (secs - t) / 2.0)   # fade in/out
y /= np.max(np.abs(y)) + 1e-9; y *= .8
st = np.stack([y, np.roll(y, 220)], 1)
with wave.open(out, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((st * 32767).astype('<i2').tobytes())
print('ok', out)
