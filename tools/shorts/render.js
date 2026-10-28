const { chromium } = require('playwright');
const { spawn } = require('child_process');
(async () => {
  const mode = process.argv[2] || 'video';
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + __dirname + '/short.html');
  await p.evaluate(() => document.fonts.ready);
  const total = await p.evaluate(() => window.TOTAL);
  if (mode === 'stills') {
    for (const t of [1.5, 4.5, 15.5]) { await p.evaluate(t => setT(t), t); await p.screenshot({ path: `still-${t}.png` }); }
    console.log('total', total); await b.close(); return;
  }
  const fps = 30, n = Math.ceil(total * fps);
  const ff = spawn('ffmpeg', ['-y','-loglevel','error','-f','image2pipe','-framerate',String(fps),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','video.mp4'], { stdio: ['pipe','inherit','inherit'] });
  for (let i = 0; i < n; i++) {
    await p.evaluate(t => setT(t), i / fps);
    const buf = await p.screenshot({ type: 'jpeg', quality: 92 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
  console.log('frames', n, 'total', total); await b.close();
})();
