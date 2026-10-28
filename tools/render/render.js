// Render Kadar posts to 1080x1920 PNG + 8s H.264 MP4 + caption.txt.
// Usage: (cd tools/render && npm install --silent) && node tools/render/render.js posts.json outDir [handle]
// posts.json: array of Kadar post objects (id, cat, text, caption, tags, q, design{tpl,bg,font,...}).
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const DIR = __dirname, NM = path.join(DIR, 'node_modules');
const [,, postsFile, outDir, handle = '@quietmanlaws'] = process.argv;
if (!postsFile || !outDir) { console.error('usage: node render.js posts.json outDir [handle]'); process.exit(1); }
const html = fs.readFileSync(path.join(DIR, 'kadar.html'), 'utf8');
let js = html.slice(html.lastIndexOf('<script>') + 8, html.lastIndexOf('</script>'));
js = js.slice(0, js.indexOf('/* ───────────────────────── Store')) + '\nwindow.R={renderPost,videoBlob,imageBlob,fullCaption,loadFonts};\n})();\n';
const F = [['Archivo',800,'archivo/files/archivo-latin-800-normal'],['Anton',400,'anton/files/anton-latin-400-normal'],['Playfair Display',600,'playfair-display/files/playfair-display-latin-600-normal'],['DM Serif Display',400,'dm-serif-display/files/dm-serif-display-latin-400-normal'],['Cormorant Garamond',600,'cormorant-garamond/files/cormorant-garamond-latin-600-normal'],['JetBrains Mono',500,'jetbrains-mono/files/jetbrains-mono-latin-500-normal']];
const css = F.map(([n,w,p]) => `@font-face{font-family:'${n}';font-weight:${w};src:url(file://${NM}/@fontsource/${p}.woff2)}`).join('');
const page = `<!doctype html><html><head><meta charset=utf-8><style>${css}</style>
<script src="file://${NM}/react/umd/react.production.min.js"></script>
<script src="file://${NM}/htm/dist/htm.umd.js"></script>
<script src="file://${NM}/mp4-muxer/build/mp4-muxer.js"></script></head><body><script>${js}</script></body></html>`;
const pagePath = path.join(DIR, '.render.html'); fs.writeFileSync(pagePath, page);
const posts = JSON.parse(fs.readFileSync(postsFile, 'utf8'));
const SET = { handle, showHandle: true, accent: '#d6bf94', cta: 'Follow us for more', emojis: '🖤🧠', noHyphens: true };
fs.mkdirSync(outDir, { recursive: true });
(async () => {
  const b = await chromium.launch(); const p = await b.newPage(); p.on('pageerror', e => console.error('page error', e.message));
  await p.goto('file://' + pagePath); await p.evaluate(() => window.R.loadFonts());
  for (const post of posts) {
    const r = await p.evaluate(async ([post, SET]) => {
      const b64 = async bl => { const u = new Uint8Array(await bl.arrayBuffer()); let s = ''; for (let i = 0; i < u.length; i += 0x8000) s += String.fromCharCode.apply(null, u.subarray(i, i + 0x8000)); return btoa(s); };
      const png = await window.R.imageBlob(post, SET, 'png'); const v = await window.R.videoBlob(post, SET, 8);
      return { png: await b64(png), mp4: await b64(v.blob), ext: v.ext, cap: window.R.fullCaption(post, SET) };
    }, [post, SET]);
    const base = path.join(outDir, post.id);
    fs.writeFileSync(base + '-post.png', Buffer.from(r.png, 'base64'));
    fs.writeFileSync(base + '-reel.' + r.ext, Buffer.from(r.mp4, 'base64'));
    fs.writeFileSync(base + '-caption.txt', r.cap);
    console.log('rendered', post.id, r.ext);
  }
  await b.close();
})();
