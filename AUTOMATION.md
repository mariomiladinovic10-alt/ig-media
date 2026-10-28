# Weekly / monthly automation

## @quietmanlaws (cloud, weekly)
1. Analytics: connector "Metricool quietmanlaws", brand 7710957 (timezone Europe/Belgrade).
2. Library: Kadar Reels Studio https://claude.ai/artifact/NeW6g3Rx1KgmRQ12zWG86e, ArtifactData collection `data/users/me/reels/posts_en`.
3. Render: `cd tools/render && npm install --silent && cd ../.. && node tools/render/render.js posts.json out @quietmanlaws`
   -> `<id>-post.png`, `<id>-reel.mp4`, `<id>-caption.txt`
4. Upload to `media/quietmanlaws/<YYYY-MM-DD>/` and push. Public URL:
   `https://raw.githubusercontent.com/mariomiladinovic10-alt/ig-media/main/media/quietmanlaws/<date>/<file>`
5. Schedule with createScheduledPost (blogId 7710957): image POST 01:00 and REEL 18:00 Europe/Belgrade, one each per day.

## @mind.psychollogy (computer on, monthly)
Old Metricool account (mariomiladinovic10@gmail.com), brand 7697579, userId 6011984, reached through the Claude app's built-in browser.
Scheduling uses the page's own API with the X-Mc-Auth token from localStorage `global.authData`:
- `GET /api/actions/normalize/image/url?url=<public media url>&blogId=7697579&userId=6011984` -> Metricool media URL (works for mp4 too)
- `POST /api/v2/scheduler/posts?blogId=7697579&userId=6011984` with the createScheduledPost JSON body.
Image POST 01:00, REEL 18:00 Europe/Belgrade.
STORY 19:00 Europe/Belgrade daily: media = that day's REEL mp4 (already normalized Metricool URL), empty text, instagramData {autoPublish: true, type: "STORY"}.
List: `GET /api/v2/scheduler/posts?blogId=7697579&userId=6011984&start=YYYY-MM-DDT00:00:00&end=...&timezone=Europe/Belgrade&extendedRange=true`
Monthly run also does a competitor/trend scan (read only) before writing.
