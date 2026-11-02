# Replace the audio of a finished Short with the V2 original score (music2.py) + optional story sfx.
# Usage: python3 remix.py in.mp4 out.mp4 seed [story.json]
import json, os, subprocess, sys, tempfile
import numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
src, out, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])
story = json.load(open(sys.argv[4])) if len(sys.argv) > 4 else {}
dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src]).strip())
tmp = tempfile.mkdtemp(); mus = os.path.join(tmp, 'm.wav')
subprocess.run(['python3', os.path.join(HERE, 'music2.py'), mus, f'{dur:.2f}', str(seed)], check=True, capture_output=True)
m, sr = sf.read(mus)
if story.get('sfx'):
    from assemble2 import sfx_track
    fx = sfx_track(story['sfx'], dur, sr)[:len(m)]
    m[:len(fx)] += (fx * 0.8)[:, None]
m = m / max(1e-9, np.abs(m).max()) * 0.9
aw = os.path.join(tmp, 'a.wav'); sf.write(aw, m, sr)
r = subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-i', aw, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-af', 'loudnorm=I=-13:TP=-1.0:LRA=9', '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-t', f'{dur:.3f}', '-movflags', '+faststart', out],
                   capture_output=True, text=True)
if r.returncode: sys.exit(r.stderr[-2000:])
print('ok', out, f'{dur:.1f}s')
