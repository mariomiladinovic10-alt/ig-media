# Pulling Shorts numbers from YouTube Studio (no API needed)

The built-in browser is signed in to YouTube Studio for the Quiet Man Laws channel (UCm3aKJtsH6hyKWOvyttDMVw).
1. Video ids: open studio.youtube.com/channel/UCm3aKJtsH6hyKWOvyttDMVw/videos/short and run
   `[...document.querySelectorAll('ytcp-video-row')].map(r=>r.querySelector('a[href*="/video/"]').getAttribute('href').split('/')[2]+' '+r.innerText.replace(/\s*\n\s*/g,' | ').slice(0,200))`
2. Per video: open studio.youtube.com/video/<ID>/analytics/tab-overview/period-default, wait until "views since" and "Stayed to watch" (or "No audience retention data") appear, then read
   views ("This Short has had N views"), Subscribers, Stayed to watch %, Average view duration, length ("0:00 / 0:24").
   Two videos per browser_batch call keeps each call under the 50 s limit.
3. Append one row per video and window (24 h, 72 h, 7 d, lifetime@date) to tools/analytics/shorts.csv; never type a number that was not on the page.
4. Or export: Studio > Analytics > Advanced mode > Export current view (CSV) and run `python3 tools/analytics/analyze.py export.csv`.
