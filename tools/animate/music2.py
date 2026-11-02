# Original cinematic score for Quiet Man Laws Shorts (V2, 2 Nov 2026). Royalty free, synthesized from scratch.
# Usage: python3 music2.py out.wav seconds [seed]
# Structure follows the video: soft piano intro, strings and pulse build, full "drop" at ~62% (the turn),
# warm resolve for the payoff line. Louder and fuller than music.py (Mario: "moramo neku muziku da ubacimo").
import sys, numpy as np, wave
out, secs = sys.argv[1], float(sys.argv[2]); seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
rng = np.random.default_rng(seed); sr = 44100; n = int(secs * sr) + 1; t = np.arange(n) / sr
def hz(m): return 440 * 2 ** ((m - 69) / 12)
progs = [[[57,60,64],[53,57,60],[48,52,55],[55,59,62]],   # Am F C G
         [[50,53,57],[46,50,53],[53,57,60],[48,52,55]],   # Dm Bb F C
         [[52,55,59],[48,52,55],[55,59,62],[50,54,57]],   # Em C G D
         [[57,60,64],[52,55,59],[53,57,60],[55,59,62]],   # Am Em F G
         [[48,52,55],[55,59,62],[57,60,64],[53,57,60]]]   # C G Am F
prog = [[m + (seed % 3) - 1 for m in ch] for ch in progs[seed % 5]]
bpm = [76, 80, 84, 72, 88][seed % 5]; beat = 60 / bpm; bar = beat * 4
drop = secs * 0.62
L = np.zeros(n); R = np.zeros(n)
def add(sig, start, pan=0.0, amp=1.0):
    i0 = int(start * sr)
    if i0 >= n: return
    sig = sig[:n - i0] * amp
    L[i0:i0 + len(sig)] += sig * (1 - pan) ; R[i0:i0 + len(sig)] += sig * (1 + pan)
def piano(f, dur, vel):
    tt = np.arange(int(dur * sr)) / sr
    env = np.exp(-tt * 1.8) * (1 - np.exp(-tt * 400))
    s = sum(a * np.sin(2 * np.pi * f * k * tt + k) * np.exp(-tt * k * .6) for k, a in [(1, 1), (2, .5), (3, .22), (4, .1), (5, .05)])
    return vel * env * s
def strings(freqs, dur, vel, att=1.2):
    tt = np.arange(int(dur * sr)) / sr
    env = np.minimum(1, tt / att) * np.minimum(1, (dur - tt) / .9)
    s = np.zeros(len(tt))
    for f in freqs:
        for d in (-0.004, 0, 0.005):  # detuned ensemble
            ff = f * (1 + d); vib = 1 + .003 * np.sin(2 * np.pi * 5.2 * tt + d * 900)
            s += sum((1 / k) * np.sin(2 * np.pi * ff * k * tt * vib) for k in range(1, 7))
    return vel * env * s / (len(freqs) * 3)
def kick(vel):
    tt = np.arange(int(.5 * sr)) / sr
    f = 45 + 75 * np.exp(-tt * 28)
    return vel * np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-tt * 7)
def tick(vel):
    nz = rng.standard_normal(int(.06 * sr)); nz = np.diff(nz, prepend=0)  # bright
    return vel * nz * np.exp(-np.arange(len(nz)) / sr * 60)
def sub(f, dur, vel):
    tt = np.arange(int(dur * sr)) / sr
    return vel * np.sin(2 * np.pi * f * tt) * np.minimum(1, tt / .05) * np.minimum(1, (dur - tt) / .2)
k = 0; s = 0.0
while s < secs:
    ch = prog[k % 4]
    phase = 0 if s < 2.5 else (1 if s < drop else 2)
    # piano arpeggio (8ths), always
    pat = [ch[0], ch[2], ch[1] + 12, ch[2], ch[0] + 12, ch[2], ch[1] + 12, ch[2]]
    for j, m in enumerate(pat):
        add(piano(hz(m + 12), 2.2, .16 if phase < 2 else .2), s + j * beat / 2, pan=(-.3 if j % 2 else .3))
    add(piano(hz(ch[0] - 12), bar, .22), s)  # left hand
    if phase >= 1:  # strings + soft pulse
        add(strings([hz(m) for m in ch], bar + .4, .22 if phase == 1 else .34, att=1.5 if phase == 1 else .4), s, pan=-.15)
        add(strings([hz(ch[0] + 12), hz(ch[2] + 12)], bar + .4, .10 if phase == 1 else .2), s, pan=.2)
        for b in range(4):
            if phase == 2 or b % 2 == 0: add(kick(.55 if phase == 2 else .35), s + b * beat)
            if phase == 2: add(tick(.05), s + b * beat + beat / 2, pan=.4)
        add(sub(hz(ch[0] - 24), bar, .22 if phase == 2 else .12), s)
    s += bar; k += 1
# riser into the drop + impact
rl = min(2.0, drop - .2)
if rl > .5:
    tt = np.arange(int(rl * sr)) / sr
    nz = rng.standard_normal(len(tt)); nz = np.convolve(nz, np.ones(6) / 6, 'same')
    add(nz * (tt / rl) ** 2 * .12, drop - rl)
    add(kick(.9), drop); add(strings([hz(prog[0][0] - 12)], 2.5, .3, att=.02), drop)
mix = np.stack([L, R], 1)
# room reverb
ir = rng.standard_normal(int(2.2 * sr)) * np.exp(-np.arange(int(2.2 * sr)) / sr * 2.6)
for c in range(2):
    mix[:, c] += np.convolve(mix[:, c], ir)[:n] * .012
fade = np.minimum(1, t / .25) * np.minimum(1, (secs - t) / 1.5)
mix *= fade[:, None]
mix = np.tanh(mix / (np.max(np.abs(mix)) + 1e-9) * 1.6) * .9   # gentle glue/saturation
with wave.open(out, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((mix * 32767).astype('<i2').tobytes())
print('ok', out, f'{bpm}bpm drop@{drop:.1f}s')
