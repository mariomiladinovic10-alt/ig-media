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
