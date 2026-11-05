# Quiet Man Laws script engine V2 (1 Nov 2026)

Use this for every Short, by hand or in routines. Output language for content: natural English. Report to Mario in Serbian. Videos are SILENT (no voiceover, Mario 1 Nov 2026): the story is told by animation + on screen lines (subtitle beats) + original music + small sound accents.

## 1. Concept card (10 per batch, ranked)
working title · topic · pillar (micro story 60% / male psychology 25% / discipline 15%) · series · audience emotion · visual hook (what is on frame 0) · premise · conflict · payoff · duration · experiment category (A to F, section 6) · reason for rank (prefer topics with proven views in our channel data, then competitor proven topics; never generic AI confidence).
Never repeat a theme from stories.md.

## 2. Five hooks, scored 1 to 10 (editorial judgment, not a prediction)
Criteria: clarity without context · curiosity · emotional relevance · visual potential (can frame 0 show it?) · originality · fit with the story. Total out of 60. Pick the highest; ties go to visual potential. A hook states a situation or tension, never the lesson ("He never answered the insult.", not "Silence is power."). 3 to 7 words on screen. Do not reuse lines from earlier videos.

## 3. Timing structure (adapt to the story, never stretch)
| time | job | on screen |
|---|---|---|
| 0 to 2 s | HOOK: understandable without context, frame 0 already shows it | hook line, visual matches it |
| 2 to 7 s | SETUP: who, where, why it matters | 1 to 2 short lines |
| 7 to 16 s | CONFLICT: stakes rise, the viewer wonders what happens | 2 to 3 lines |
| 16 to 25 s | TWIST / INSIGHT: earned, believable | 1 to 2 lines |
| 25 to 32 s | ENDING: memorable final line, may echo frame 0 | final line + "Follow @quietmanlaws" |
A focused idea can end at 15 to 20 s. Caption beats every 1.5 to 3 s; a visual change (new action, reaction, push-in, cut) at least every 3 s.

## 3b. Retention rule (Mario, 1 Nov 2026)
People must stay on the video: reveal the story line by line, never show the whole message or the lesson early, payoff only in the last 2 to 3 s. Titles, cover and caption line 1 tease the conflict, never the ending. Quality gate: PACING and ENDING fail (under 7) if the lesson is readable before the end.

## 4. Storyboard row (one per beat)
time range · scene/visual · character action · on screen line (gold word in *asterisks*, max 8 words, no dashes) · animation (clip, trim, speed, push) · sound (music, hit, whoosh) · transition (cut by default).

## 5. Quality gate BEFORE generating any paid asset (score 1 to 10 each)
HOOK · STORY (reason to keep watching) · EMOTION · VISUALS (understood with sound off) · PACING (every beat moves the story) · ENDING (earned payoff) · ORIGINALITY (vs stories.md and competitors) · BRAND (calm, mature, never misogynistic or manipulative) · ACCURACY (no invented statistics or pseudo science).
Rule: revise any criterion under 7; reject the concept if HOOK, STORY or ENDING stays under 7 after one revision. Write the scores into experiments.csv (column gate_scores). Scores are editorial, never presented as success odds.

## 6. Experiment categories
A story vs statement · B first frame visual hook type · C short (15 to 20 s) vs long (25 to 35 s) · D relationship vs discipline theme · E type of payoff (reversal, realization, quiet win) · F subtle CTA line vs none. Change one variable per comparison.

## 7. Series (recurring reason to come back)
The Quiet Man's Lessons · Stories of Self-Respect · Psychology of Silence · The Discipline Series · Lessons Men Learn Too Late. Put the series name small in the cover tag area or the caption, never as an intro.

## 8. Production (existing pipeline, unchanged tools)
OpenArt kling-3-omni text2image for scene 1, then image2image from it for every next scene (consistency) · pixverseV6 image2video 540p 5 s (prompt starts "One single continuous wide shot, camera locked off, no zoom, no cuts.") · contact sheet + frame strip review · assemble2.py (beats, trims, push-ins, accents, final line over the last scene) · thumb.py cover · packaging per MASTER.md section 12 · QC: 1080x1920, frame 0 not black, captions inside the safe area, loudness about -14 LUFS, no corrupted frames.
Cost per Short about 300 to 450 OpenArt credits; ask Mario before batches that exceed what he has authorised.

## 9. V3 changes (5 Nov 2026, Mario's growth brief; these override sections 1 to 3 where they differ)
Evidence behind them: tools/growth/AUDIT.md (stories 54.7% stayed vs static quotes 30.8%; conflict and situation hooks beat statements).

### 9a. Three series (rotate A, B, C; one series per Short)
- A. EMOTIONAL TRUTH: relatable relationship experiences, heartbreak, self respect, attachment, emotional maturity. Micro story, one man, one moment.
- B. REAL SCENARIOS: one specific dating or relationship situation, then a realistic, practical response the viewer can use tonight.
- C. PSYCHOLOGY REFRAMES: a popular belief, a concrete example that breaks it, the healthier or more accurate way to think. No invented statistics; name a concept only if it is well established, never a number we cannot source.
Frame 0 carries a small series tag line above the hook (e.g. "REAL SCENARIOS") in the cover and video, same position every time.

### 9b. Structure (adapt, never stretch)
| time | job |
|---|---|
| 0 to 2 s | SCROLL STOPPING HOOK: a specific conflict, curiosity gap, relatable problem or useful promise. Readable without sound. |
| 2 to 7 s | EMOTIONAL CONNECTION: a realistic situation the viewer recognises from his own life. |
| 7 to 17 s | STORY / INSIGHT: develop it, introduce one useful distinction, keep curiosity, no filler. |
| 17 to 26 s | PAYOFF: the real lesson, practical response or insight the hook promised. |
| 26 to 30 s | ENDING: a memorable line or a natural question, then the platform CTA under it (endcta.py / assemble2.py yt). |
Length buckets to test: 15 to 25 s (default), 25 to 35 s, occasionally 35 to 45 s when the story needs it. Log the bucket in shorts.csv duration_s.

### 9c. Hooks
At least three alternatives per Short (five when time allows), ranked by specificity, clarity, curiosity, emotional relevance (1 to 5 each, total out of 20). Write the ranking into the production pack. A hook is a situation or a tension, never the lesson.

### 9d. Never
Generic motivational quotes; sigma or alpha clichés; empty dramatic statements; long intros; narration that repeats what the picture shows; engagement bait ("comment YES"); misleading or unverified psychological claims; negative generalisations about women or men; dashes in on screen text, titles or captions.

### 9e. Quality control (automatic)
Run `python3 tools/growth/qc_script.py pack.json` on every production pack before any paid asset. It fails on: dashes, banned phrases, fewer than 3 hooks, an on screen line over 8 words or unreadable in 1.5 s, the payoff word set appearing before the last 30% of the timeline, a missing CTA line, a total outside 15 to 45 s, a missing hypothesis. Editorial gate scores (section 5) stay.
