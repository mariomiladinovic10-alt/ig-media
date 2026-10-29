const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs');
(async () => {
  const facts = JSON.parse(fs.readFileSync(__dirname + '/facts.json', 'utf8'));
  const only = process.argv[2];
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  fs.mkdirSync(__dirname + '/yt', { recursive: true });
  for (const [i, F] of facts.entries()) {
    if (only && only !== 'stills' && String(i) !== only) continue;
    await p.goto('file://' + __dirname + '/fact2.html');
    await p.evaluate(F => { init(F); }, F);
    await p.evaluate(() => document.fonts.ready);
    const total = await p.evaluate(() => window.TOTAL);
    const name = F.d;
    if (only === 'stills') { for (const t of [2.0, 7.5, 10.8]) { await p.evaluate(t => setT(t), t); await p.screenshot({ path: `yt/still-${name}-${t}.png` }); } if (i >= 2) break; continue; }
    const fps = 30, n = Math.ceil(total * fps);
    const ff = spawn('ffmpeg', ['-y','-loglevel','error','-f','image2pipe','-framerate',String(fps),'-i','-','-i',__dirname+'/mix1.wav','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-shortest',`yt/${name}.mp4`], { stdio: ['pipe','inherit','inherit'] });
    for (let k = 0; k < n; k++) { await p.evaluate(t => setT(t), k / fps); const buf = await p.screenshot({ type: 'jpeg', quality: 90 }); if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
    console.log('done', name);
  }
  await b.close();
})();
