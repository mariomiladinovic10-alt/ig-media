# Quiet Man Laws: master system for YouTube Shorts (adopted 1 Nov 2026)

Mario's instruction (1 Nov 2026): "od sad ovako radimo". This file merges his MASTER PROJECT prompt with the production brief format and the locked animated style. It is the operating manual for every Quiet Man Laws Short. Talk to Mario in Serbian (Latin); every script, title, caption and on screen text is natural English.

## 1. Channel
- Quiet Man Laws | Silent Power, https://www.youtube.com/@quietmanlaws. Slogan: A Quieter Mind. A Stronger Man.
- Audience: men 18 to 35 (psychology, relationships, emotional intelligence, confidence, personal development).
- Pillars: male psychology, relationships and attraction, emotional intelligence, self respect and boundaries, quiet confidence, masculinity and discipline, human behavior, psychological storytelling.
- Personality: calm, confident, mature, premium, minimalist, emotionally compelling, direct but never aggressive, mysterious but never confusing.
- Goal: an original storytelling brand, not an AI quote channel. Never promise views, subscribers or earnings.

## 2. Baseline analytics (YouTube Studio, given by Mario 1 Nov 2026)
| | Video A: They laughed at what he was building | Video B: If you have to convince her to choose you, she's already chosen |
|---|---|---|
| Format | animated micro story, 26 s | static typography, 9 s |
| Public views | ~2,500 | ~526 |
| Engaged views | ~1,800 | 127 |
| Stayed to watch | 68.2% | 23.5% |
| Avg view duration | 15 s (~58%) | 9 s (~100%) |
Possible early drop around 6 to 8 s in Video A (not confirmed).
Hypothesis to test (not proven): original animated stories with a relatable conflict and curiosity beat static statements that reveal the conclusion at once. Do not optimize for shortness. Never invent analytics or use arbitrary retention targets.

## 3. Formats
A. Psychological micro stories (relatable male character; beginning, development, satisfying outcome).
B. Relationship moments (communication, respect, boundaries; no stereotypes, no manipulative tactics).
C. Uncomfortable truths (must include an original explanation or concrete example; never a quote held on screen).
D. Quiet discipline (consistency, patience, resilience; grounded).
E. The moment everything changed (a realization or decision with a real payoff).
Starting mix hypothesis: 70% animated micro stories, 20% relationship and dialogue stories, 10% experiments. Change only on evidence.

## 4. Retention tests (every script must pass all three)
A. First second hook: works without sound, minimal readable text, a conflict, a specific problem, an unexpected situation or an open question. No logos, greetings, setup or generic phrases. Do not reveal the conclusion unless that creates a stronger reason to stay.
B. Continuous engagement: every scene advances the story (action, new information, emotional change, decision). A meaningful development inside roughly 5 to 10 s. No random effects just to add cuts.
C. Satisfying ending: a specific insight, resolution or practical lesson tied to this story. A loop back to the opening is welcome but never at the cost of clarity.

## 5. Length
Test 15 to 35 s first; choose length by the idea (observation 12 to 18 s, micro story 20 to 30 s, longer only when the story needs it). Cut filler, not story. Change target length only after real results.

## 6. Script rules
Human, calm, conversational, emotionally intelligent. No robotic narration, clichés, hype words, repeated structures, unsupported psychological claims, misogyny or manipulation. Every script: distinctive premise, audience motivation, hook, progression, memorable payoff. Each Short is written as an original piece, never a template with swapped words. No dashes in on screen text, titles or captions.

## 7. Visual system (LOCKED white glow style, see style.json; neon couple style.json for relationship stories)
- Black background, dark charcoal ground, lots of negative space, one soft volumetric spotlight from above, monochrome, subtle bloom, flat vector look.
- Hero: clean white stick figure, round head, thick uniform lines, soft white neon glow. Others: dim gray, no glow. No faces, no text in generated images.
- Overlay text: Inter ExtraBold uppercase, white with soft glow, upper third, one gold key word (#F2C46D, `*word*` in assemble scripts). Hook text visible on frame 0, never a fade from black.
- Consistency: generate the first scene with text2image, then every following scene with kling-3-omni image2image using the previous scene as reference ("keep the exact same scene, camera, table, figures; change only the poses"). This keeps one cohesive set across shots.
- Clip prompts start "One single continuous wide shot, camera locked off, no zoom, no cuts." and end with motion_suffix + "Faceless stick figures, plain round heads." PixVerse still often pushes in; trim clips before the push becomes a giant close up behind the captions.
- Every shot shows a meaningful action, emotion or change. Vary scenes between videos; never reuse the Simply Animated rock/chain or word bricks staircase.

## 8. Production pipeline (approval gates in CAPS)
1. Idea (from strategy + experiment log).
2. Hook: three alternatives scored on clarity, curiosity, emotional relevance, visual potential, honesty; recommend one.
3. Script: word for word narration with estimated duration (calm read ≈ 140 wpm).
4. Storyboard: time range, scene, character action, on screen text, narration, animation, sound, transition.
5. MARIO APPROVES the concept and script before any paid asset (OpenArt credits) is generated.
6. Visuals: OpenArt kling-3-omni (images, 10 credits) and pixverseV6 image2video 540p 5 s (50 credits); max 2 video jobs at once. Contact sheet review before animating; frame strip review after.
7. NO VOICEOVER (Mario, 1 Nov 2026: "ovo ne prolazi, više ne radimo ovako" after the voiceover Short "How to Make a Disrespectful Person Regret It, Calmly" had 6 views after ~11 h, while an image Short published 30 minutes later had 888). All videos are silent: overlay text + original music. The notes below are kept only for reference.
   Old note: calm natural English male voice. ElevenLabs is NOT connected (Highsfield has only 10 credits and blocks other TTS hosts). Working fallback: local Kokoro TTS (kokoro-onnx, model files from github.com/thewh1teagle/kokoro-onnx releases), voice am_onyx, speed 0.92, one wav per line, then place lines on a timeline with deliberate pauses. Switch to ElevenLabs when Mario connects it.
8. Edit: Remotion is not installed; current working editor is ffmpeg + Python (tools/animate/assemble.py for text only videos; the qml-anim-08 build script pattern for voiceover videos: per segment clips or stills with slow zoom, captions from text_card(), music.py bed ducked under the voice, a low hit on the key law, loudness normalized to -14 LUFS). Remotion can be added later if Mario wants it.
9. QC: opening understandable without sound, clear progression, ending delivers, captions readable and inside the safe area (out of the bottom 20% and right 15%), balanced audio, consistent visuals, nothing cut off, frame 0 not black.
10. Export: 1080x1920, H.264 MP4, 30 fps, AAC; plus title options, description, hashtags, cover frame JPG, metadata.
11. MARIO APPROVES publishing. Do not upload or schedule without his OK. (Exception only where he has given a standing approval in writing.)
12. Log the video in tools/animate/experiments.md and stories.md.

## 9. Analytics loop
After publishing, ask Mario for YouTube Studio numbers at about 24 h, 72 h and 7 days (public views, engaged views, shown in feed, stayed to watch, swiped away, avg view duration, avg % viewed, retention curve, likes, comments, shares, subscribers gained). Use only windows that exist.
Diagnostics: many swipes → first frame, topic, hook. Drop right after hook → promise vs next scene. Mid drop → pacing, repetition, visual stagnation. Drop before payoff → predictability or slow ending. AVD above length → replays. Never treat one metric as proof; compare videos of similar age and format.
Log per video: id, title, topic, hook, script, duration, format, publish date, analytics, retention notes, hypothesis, next experiment. After each batch: what improved, what declined, what is uncertain, which formats to keep testing, next changes. Never overturn the whole strategy on one video.

## 10. Monetization and originality (checked 1 Nov 2026)
- YPP: 1,000 subscribers plus 10 million qualified Shorts views in 90 days (or 4,000 long form watch hours in 12 months). YouTube says YPP updates start 1 Feb 2027 with higher criteria (figures not published on the page).
- July 2026 inauthentic content clarification: generic, repetitive or template based mass produced content (AI, CGI or templates with little variation) cannot earn; neither can content designed to be distressing or manipulative. A channel with too much of it loses monetization. → Our daily templated quote Shorts are the main originality risk; original stories are the defence.
- No reuploads, copyrighted clips, copied scripts, misleading titles or artificial engagement. Declare AI content where YouTube requires it.

## 11. Research
Study English Shorts in psychology, relationships, emotional intelligence, animated storytelling: hooks, structure, pacing, visuals, endings, titles. Verifiable sources only; never invent competitor numbers; never copy scripts, characters or animations.

## 12. Packaging standard for every video (Mario, 1 Nov 2026: "uvek imamo thumbnail, hashtagove i ostalo sve što ide")
Every finished video ships with all of this, no exceptions:
- Final MP4 1080x1920, frame 0 already shows the hook text.
- Thumbnail (cover) JPG 1080x1920 in the LOCKED cover style (Mario, 1 Nov 2026), made with `python3 tools/animate/thumb.py <scene.png> "<HEADLINE with one *gold* word>" <out.jpg> [zoom] [focus_y]`:
  - background = the story's conflict moment (the scene that makes people ask "why?"), not the ending; key figures visible below the headline box and above the bottom 20%;
  - top third: small gold "QUIET MAN LAWS" tag + thin gold rounded frame with a 2 to 5 word headline in Inter ExtraBold, white with ONE gold word;
  - headline = a conflict or open loop specific to this story (e.g. "HE CHASED. SHE *RAN.*"), never the lesson itself and never the same words as the YouTube title;
  - built from competitor research (1 Nov 2026): Simply Animated covers show one clear metaphor frame on black with tiny labels; PsycHacks uses the same framed headline box on every Short for instant recognition; Charisma on Command uses one bold accent (yellow arrow/caption) on the key element. Our frame + single gold word combines these.
  Host the cover in the repo (media/quietmanlaws/anim/<id>_cover.jpg) and pass it as videoThumbnailUrl on Instagram REEL, YouTube Short and TikTok (fallback videoCoverMilliseconds 2000). Frame 0 of the video still shows the hook text.
- YouTube title: the hook as a curiosity line, up to ~80 characters, ending " #shorts" (e.g. "The More He Chased, the Farther She Went #shorts"), plus 2 alternative titles in the report.
- Captions are written PER PLATFORM (three separate Metricool posts at the same time: Instagram, YouTube, TikTok). All start the same: line 1 the story's insight in one sentence + 1 emoji; blank line; one question inviting viewers to share their own story. Then the follow lines (Mario, 1 Nov 2026: always ask people to follow on Instagram and do everything that makes the Shorts show up to them):
  - Instagram: "Follow @quietmanlaws for a new quiet law every day 🖤🧠"
  - YouTube: question ends with "Tell me in the comments." then "Subscribe so the next Quiet Law shows up in your feed 🔔" and "Follow us on Instagram for a new post every day: @quietmanlaws (instagram.com/quietmanlaws)". First 3 hashtags are shown above the title, so order them: 2 strongest topic tags, then #shorts.
  - TikTok: "Follow for more and find us on Instagram @quietmanlaws 🖤🧠"
  Then 6 to 8 hashtags: topic tags + #stickfigure #animation #quietmanlaws. Never "-" or dashes.
- Discovery basics on every YouTube Short: the main search phrase of the topic in the title and in the first line of the description; "quiet man laws" among the tags; notifySubscribers left on (default); keep the series look (same cover frame, same end card) so returning viewers recognise it. In the end card always "Follow @quietmanlaws".
- YouTube tags: 4 topic tags + "mens psychology", "stick figure animation", "shorts"; category PEOPLE_BLOGS; madeForKids false; type short; public.
- TikTok title: the hook in sentence case (no hashtags), privacy PUBLIC_TO_EVERYONE.
- Instagram: type REEL, showReelOnFeed true.
- Scheduling: three Metricool posts (blogId 7710957) at the same time, one each for instagram, youtube and tiktok, each with its own caption; then check all three appear in getScheduledPosts.
- After scheduling: append to stories.md and experiments.md, commit and push.

## 13. Decisions (1 Nov 2026)
- Mario: "na osnovu ovog prompta pravis videe i opise ... sve sto smo pricali". This master system is the standard for all Quiet Man Laws Shorts from now on, including the Monday weekly routine.
- PENDING: updating the weekly routine to this system was blocked by a permission check on 1 Nov 2026; Mario needs to approve the routine change. Planned change: keep his standing auto publish approval (31 Oct 2026), make every main video an original animated story with full packaging (section 12), and stop YouTube Shorts versions of the static image posts (Instagram and TikTok image posts continue).

## 14. V2 upgrade (Mario's "GROWTH SYSTEM V2", 1 Nov 2026)
- Script engine: tools/animate/SCRIPT_ENGINE.md (10 ranked concepts per batch, 5 scored hooks, 0-2/2-7/7-16/16-25/25-32 s structure, storyboard rows, quality gate before any paid asset, experiment categories A to F, series).
- Editor: tools/animate/assemble2.py (caption beats every 1.5 to 3 s, per scene trim/speed/push-in, cuts, hit/whoosh accents, final line over the last scene). assemble.py is kept unchanged.
- Analytics: tools/analytics/shorts.csv (per video and age window: 24 h, 72 h, 7 d), channel.csv, experiments.csv, analyze.py (like rate, subs per 1,000 views, engaged share, averages by format, pillar, hook type, style; merges a YouTube Studio CSV export). Never invent missing numbers.
- Internal targets (not algorithm thresholds): stayed to watch 55 to 60%+, swiped below 45%, likes 3 to 4% of views, 2+ subs per 1,000 views.
- Content mix for 30 days: 60% emotional micro stories, 25% male psychology, 15% discipline.
- Voiceover from V2 section 8 is NOT used: Mario decided on 1 Nov 2026 to keep all videos silent. Test it again only if he asks.
- CTA: subtle and only when it fits ("Follow for more stories about self-respect"); the caption follow lines of section 12 stay.
