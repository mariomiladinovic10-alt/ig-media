# Quiet Man Laws visual, subtitle and audio guide (V3, 5 Nov 2026)

Builds on the LOCKED white glow style (tools/animate/style.json, MASTER.md section 7). Nothing here replaces it; it adds rules so every scene is directed, not generated at random.

## 1. Look
- Palette: black #000, charcoal ground #141414 to #1c1c1c, white glow hero, dim gray others, ONE accent: muted gold #F2C46D (key word, a single object that matters in the story: the phone screen, the ring, the hoodie). Ivory #EDE6D6 allowed for warm memory scenes only.
- Light: one soft volumetric spotlight from above, or one practical light inside the scene (phone screen, window, street lamp). Never two competing light sources.
- Composition 9:16: the hero sits in the lower 55% of the frame; upper third stays dark and empty for captions; nothing important in the bottom 20% (Shorts UI) or the right 15% (buttons).
- Characters: the hero is always the same white glowing figure with a round head; recurring partner figure = dim gray with a short ponytail (she) so viewers learn the cast. No faces, no text in images.
- Motion: every 2 to 3 s something changes: a new action, a cut to a new angle of the same set, a push in (assemble2 push 1.00 to 1.08), or a light change. Never a still frame where only the caption changes for more than 3 s.
- No stock footage, no random scenes, no effects for their own sake. Each scene shows exactly what the caption at that moment says, or the reaction to it.

## 2. Scene prompt templates (OpenArt kling-3-omni, then pixverseV6 image2video)
Image (first scene, text2image 9:16):
```
{style_prefix} {SETTING: one sentence, concrete place and time}. {HERO ACTION: what the hero does, body language}. {OTHERS: who else, where, dim gray}. {ACCENT: the one object glowing muted gold, if any}. Camera: {wide / medium / over the shoulder}, eye level. {style_suffix}
```
Next scenes (image2image from the previous scene, keeps the set): 
```
Keep the exact same scene, camera, set, lighting and figures. Change only: {pose or action}. {accent object state}. {style_suffix}
```
Clip (image2video 5 s, 540p):
```
One single continuous wide shot, camera locked off, no zoom, no cuts. {ONE action, 3 to 5 s, e.g. "the hero slowly lowers the phone and puts it face down on the table"}. {motion_suffix} Faceless stick figures, plain round heads.
```
Budget per Short: 4 to 5 images (40 to 50 credits) + 2 to 3 clips (100 to 150) ≈ 150 to 200 credits; stills with push in fill the rest.

## 3. Subtitles (on screen lines)
- Inter ExtraBold uppercase, 80 px, white with soft glow, centred at y 330 (upper third), soft dark plate (assemble2 default). One gold key word per line.
- Max 8 words, about 1.5 to 3 s per line (reading speed ~3 words/s). A new line when the picture changes, not on a fixed clock.
- Series tag on frame 0: Inter SemiBold 40 px, letter spaced, gray #BDBDBD, 70 px above the hook ("REAL SCENARIOS").
- Final line in the last 2 to 3 s, CTA under it at 44 px: YouTube "Subscribe for the next Quiet Law", Instagram "Follow @quietmanlaws", TikTok "Follow for the next Quiet Law" (endcta.CTA; per story override end.sub_yt etc.).

## 4. Cover
thumb.py clean style, unchanged. Headline = the conflict, never the lesson, never the title words. Note: YouTube rejects custom thumbnails until the channel is verified; the first frame is the YouTube cover, so frame 0 must work as a cover.

## 5. Audio
- Default stays SILENT narration (Mario, 1 Nov 2026): music2.py original score, piano and strings, build to the turn at ~62%, loudness normalised to -14 LUFS (assemble2) with true peak -1 dB.
- Accents: whoosh on scene changes that matter, one low hit on the turn. Max 3 accents per Short.
- Music sits under the story: quiet first 2 s so the hook reads as calm, not hype.

## 6. Voice (only as an approved experiment)
The only voice test so far (1 Nov) was 49 s long and published at 00:30, so it does not prove that voice fails. If Mario approves, test once:
- same story rendered twice: silent version and narrated version, published 24 h apart in the same 22:00 slot;
- voice: calm natural male, about 140 words per minute, pauses of 0.4 to 0.8 s before the turn and before the payoff, no hype, no vocal fry, narration never just reads the caption word for word (captions stay short, voice adds the human detail);
- engine: local Kokoro am_onyx at speed 0.92 (free) or ElevenLabs if connected; music ducked 10 to 12 dB under the voice, voice peaks at -1 dB, whole mix -14 LUFS;
- compare stayed to watch, AVD and subs/1k at 24 h and 72 h. One test is a hint, not proof.
