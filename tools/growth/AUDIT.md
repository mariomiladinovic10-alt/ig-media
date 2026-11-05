# Quiet Man Laws: channel audit (5 Nov 2026)

Source: YouTube Studio, read through the built-in browser on 5 Nov 2026 about 21:00 UTC (channel overview, content list, per video overview pages). Nothing below is estimated; empty cells mean Studio had no data yet. Per video rows are in `tools/analytics/shorts.csv`; run `python3 tools/analytics/analyze.py`.

## 1. Channel numbers
- Last 28 days (8 Oct to 4 Nov): 18,403 views, 35.4 watch hours, +13 subscribers. 3,649 views in the last 48 h.
- 19 Shorts published 29 Oct to 5 Nov (about 2 per day): 7 animated stories, 12 static quote images (9 s).
- Traffic: 92 to 98% Shorts feed on every video checked. Search 3 to 8%.
- Subscribers per 1,000 views: 0.82 across all videos.

## 2. What the data says
| | animated stories (n=5 with retention) | static quotes (n=10) |
|---|---|---|
| median views | ~1,080 (best 2,758) | ~1,050 (worst 324) |
| mean stayed to watch | 54.7% | 30.8% |
| average view duration | 13 to 26 s | 7 to 10 s |
| average % viewed | 50 to 90% | 78 to 111% (short loops inflate it) |

Strongest: They laughed at what he was building (67.7% stayed, 2,758 views), The Text He Wrote at 2 AM (58.5%, 1,821), The More He Chased (57.0%, 90% viewed).
Weakest: Walking away calmly (11.2%, 324 views), Work in silence quote (15.1%), If you have to convince her (24.4%, 538), No contact quote (25.1%).

Diagnosis (evidence, not certainty; samples are small):
1. Almost every Short gets one test batch of about 1,000 feed impressions and then stops. The only one that clearly broke out also had the highest stayed to watch. Stayed to watch is the gate to watch first. No sign of a shadowban: distribution, traffic mix and comment activity are normal for a 1 week old channel.
2. Static quotes lose 70% of viewers on frame 1. The conclusion is readable at once, so there is no reason to stay. They also add mass produced, templated looking content to the channel (YouTube's inauthentic content policy, July 2026 clarification).
3. Stories hold the swipe but lose people mid video (avg 50 to 70% viewed on 21 to 29 s). Drop points to check: right after the hook (2 to 4 s) and the static middle where captions change but the picture does not.
4. Subscriber conversion is the weakest link (about 1 per 1,000 views). Causes: no series identity, no recurring character, the end card said "Follow @quietmanlaws" (an Instagram instruction) instead of a YouTube reason to subscribe, and two very different formats make the channel promise unclear.
5. Story Shorts with a situation or conflict hook (He kept chasing, 2 AM, They laughed) beat statement hooks by roughly 20 points of stayed to watch.
6. Packaging: YouTube Studio rejects custom thumbnails ("Could not upload video thumbnail"): the channel is not verified for custom thumbnails, so covers do not show on YouTube. Titles of quote Shorts are the full quote (they give away the payoff).
7. Operational: TikTok post on 5 Nov failed with "TikTok was disconnected" in Metricool. Needs reconnecting.

## 3. Prioritized improvements
| # | change | expected benefit | how to test |
|---|---|---|---|
| 1 | Stop publishing static quote Shorts on YouTube (keep them on Instagram and TikTok). Replace the 18:00 slot with a second story or a text story video. | removes the 30% stayed videos that drag the channel signal; less template content | compare channel stayed median and views per Short, 14 days before vs after |
| 2 | Subscribe line at the end of every YouTube version ("Subscribe for the next Quiet Law") plus a series promise | more subs per 1,000 views | subs/1k on the 7, 9, 11 Nov videos (CTA) vs earlier stories |
| 3 | Three named series (Emotional Truth, Real Scenarios, Psychology Reframes) with a consistent series tag line on frame 0 and the cover | recognisable channel, reason to come back | subs/1k and returning viewers per series after 14 days |
| 4 | Visual change at least every 2 to 3 s, never a still frame with only text changing; development by 5 to 7 s | higher avg % viewed | retention curve drop at 3 to 8 s vs earlier stories |
| 5 | Payoff earned in the last 3 s, with a loop line back to frame 0 where natural | replays, AVD above length | avg % viewed > 100% on stories |
| 6 | Verify the channel (phone verification in YouTube Studio settings) so custom covers work | better first impression in search and channel page | Mario action |
| 7 | Controlled voice test (see STYLE_GUIDE.md section 6), only if Mario approves | find out whether calm narration lifts AVD | one story in two versions, same slot, 24 h apart |
| 8 | Reconnect TikTok in Metricool | posts publish again | Mario action |

## 4. What is preserved
White glow style, assemble2.py, music2.py, thumb.py, Metricool scheduling, 2 Shorts per day at 18:00 and 22:00 Belgrade, retention rule (no early payoff), no dashes, approval gates. Nothing published or deleted by this audit.
