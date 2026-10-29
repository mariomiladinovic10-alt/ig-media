---
name: animate
description: Use when Mario types /animate (optionally with a topic or a count): make original animated stick figure Reels and YouTube Shorts for @quietmanlaws in the LOCKED glowing minimalist style through OpenArt, assemble them with text and original music, show them to Mario, and schedule after his approval.
---

# /animate: Quiet Man Laws animated Reels and Shorts

Talk to Mario in Serbian. Every on screen text, title and caption is in English. Never use dashes in on screen text or captions.

## Locked style (never change without Mario's explicit approval)
Repo: `mariomiladinovic10-alt/ig-media`, folder `tools/animate/` (style.json, assemble.py, music.py).
- Minimalist 2D stick figures, pure black background, dark charcoal ground, lots of negative space.
- Hero: clean white stick figure, round head, thick uniform lines, soft white neon glow. Others: dim gray, no glow.
- One soft volumetric spotlight from above, monochrome, subtle bloom, flat vector look, no faces, no text in the image.
- Image prompt = `style_prefix` + scene + `style_suffix` from style.json, with the hero and others lines verbatim.
- Clip prompt must start with "One single continuous wide shot, camera locked off, no zoom, no cuts" (PixVerse otherwise jump zooms) and end with the motion_suffix plus "Faceless stick figures, plain round heads".
- Overlay text: Inter ExtraBold uppercase, white with glow, one gold key word marked `*like this*`, upper third. Hook text visible from frame 0.
- Music: original synthesized piano and pad from music.py (seed per video). No copyrighted audio.
- End card: one short line + "Follow @quietmanlaws". Length about 25s (5 scenes of 5s, 0.4s crossfades, 2.4s end card).

## Story rules
- Original stories only. Use competitor research for themes, never copy scenes, scripts or characters (do not reuse the "your past" rock and chain, or the word bricks staircase from Simply Animated).
- Themes that perform best in this niche (Simply Animated, 273k subs): prove it to yourself (17M), never miss your chance (9.4M), trust you can achieve it (8.6M), be authentic (7.1M), work in silence (4.6M), stop waiting (4.3M), prove them wrong (4.1M), act like you made it (3.4M), your potential (2.9M), discipline (2.3M), growth when nobody watches (2.1M).
- Structure: hook in the first 2 seconds, problem, struggle, turn, payoff line. 5 scenes, one short sentence per scene.
- Check `tools/animate/stories.md` so a theme is never repeated.

## Pipeline
1. `openart_account_get`: report credits. Cost per video: 5 images x 10 (kling-3-omni text2image 9:16 1k) + 5 clips x 50 (pixverseV6 image2video 540p 5s) = 300, plus retries. Stop and tell Mario when credits run short (give upgradeUrl).
2. Generate the 5 images (max about 4 jobs in parallel; on PARALLEL_LIMIT_EXCEEDED wait and resubmit). Review them on a contact sheet before animating.
3. Animate each image with image2video (startFrame = the image resource id and url). Review frame strips; redo a clip only if it is clearly broken (faces, goggles, color shift, extra limbs).
4. Download from cdn.openart.ai, write story json, run `python3 tools/animate/assemble.py story.json clips_dir out.mp4`.
5. SendUserFile the mp4s to Mario and wait for his OK. Never publish without it.
6. After approval: copy to `media/quietmanlaws/anim/`, push, and schedule with the Metricool quietmanlaws connector (blogId 7710957, timezone Europe/Belgrade) as one post with providers instagram (REEL) and youtube (short, madeForKids false, category PEOPLE_BLOGS, title ends with #shorts). Caption style: English, emojis, ends with "Follow us for more". Slot: 16:00 America/New_York (YouTube Shorts peak, Instagram still strong), one per day; that is 21:00 Belgrade while the US is on daylight time and 22:00 Belgrade after the US switches to winter time (first Sunday of November until the last Sunday of October in Europe).
7. Append the story to `tools/animate/stories.md` and commit.
