---
name: cartoon-audio-short
description: Make a vertical animated cartoon short (single 20-30s clip or multi-part 60-90s+ story). Offers ideas, writes the script, designs custom 2D characters and 3D worlds, runs a mandatory multi-pass visual look-check on contact sheets, and turns the user's voiceover into a finished 1080x1920 MP4 with synthesized music and SFX via audio.py and finish.sh.
---

# Cartoon short: idea -> script -> voiceover -> finished MP4

The look: smoothly shaded 2D cartoon characters on canvas-drawn cards in a colourful 3D world with painted textures, depth-of-field and gliding cameras. Keep the rounded bean bodies, slender limbs and plum outlines; give faces, hair, clothes and props soft painted volume with clean analytic gradients. Character surfaces should stay smooth at close-up scale, without random grain or noisy texture overlays. The output is 1080x1920, 30 fps, exactly as long as the voiceover. The user's voice is unchanged. The music bed and SFX are synthesized in `audio.py` with automatic voice-envelope ducking and normalized to −14 LUFS by `finish.sh`. Proven on "The Soldier Who Never Left" (19.7 s, 8 shots).

## Rules
- Stories, characters and shots are always original. Never recreate another creator's video shot for shot. Offer an original take on the same idea instead.
- For this cast, the user's visual reference is [Ricks Clips — How Mine Salting Worked](https://www.youtube.com/shorts/TRUkQ1wbV2E). Study its soft shading, rounded heads, bean bodies, slender limbs, plum outlines and painted 3D environments. Apply that level of finish to the original Elon story, cast and staging.
- Public figures, celebrities, tech founders (e.g., Elon Musk), and parody/satirical brand references (e.g., SpaceX, Tesla, X) ARE allowed for "What If", parody, educational, and commentary stories. Design recognizable custom outfits, hairstyles, and props for them in `web/roman.js` and `web/paint.js`.
- **This Elon project requires captions:** the user explicitly requested proper captions matching the supplied voiceover. Preserve the spoken words and timing; use `script.txt`, `captions/captions.srt` / `captions/captions.vtt` and reviewed `captions/words.json`. Render the captions into the actual video, not only a sidecar. For other projects, use captions when requested. Diegetic text (a carved message, a sign, a phone screen, a stock ticker, a building logo) is fine, and it must read correctly (not mirrored).
- Never edit or re-time the voice. The picture is timed to it, and every visual reaction lands 0-3 frames before its word.
- **Audio pipeline (`audio.py` -> `mix_raw.wav` -> `finish.sh`):** Note that `mix.py` is not used in this kit. Instead, `audio.py` synthesizes the music bed and frame-accurate SFX cues, applies an envelope-follower ducking curve (`duck = 1 - 0.45 * np.clip(ve / (ve.max() * 0.25), 0, 1)`) so the music sits cleanly under the narration, and writes `mix_raw.wav`. Then `bash finish.sh "Title"` normalizes the master audio (`loudnorm=I=-14:TP=-1.5:LRA=7`) into `mix.wav` and muxes it with the rendered frames.
- **Multi-part support for 60s–90s+ videos & storage hygiene:** For videos longer than 30 seconds (such as a 90-second / 1:30 story), split the project into 20-25 second parts (~650-750 frames per part). Share the same `web/toon.js` and `web/paint.js` across all parts so character rigs and textures remain 100% consistent. To respect tight disk limits (e.g., 10 GB free space), delete `frames/*.jpg` after each part's `.mp4` passes QA, then concatenate the finished part MP4s at the end using `ffmpeg -f concat`.
- Keep the user informed with a task list. Always run the **2-Pass Visual Look Check** (Stage 4.6) and inspect the contact sheet before starting the full frame render.

## Character-only previews (before voiceover)
When the user asks to inspect characters, palettes, expressions, turn studies, or motion samples, build the preview directly. No story intake or voiceover is required. Use the root `roman.js` for the rig and principal cast, plus `cast-extras.js` for the ensemble profiles, outfits and labels. Preserve the story roles, wardrobe continuity and props when refining the designs.

This workspace includes a ready example in `character-palette/`:
- `npm run build` strips the vendored `vendor/toon.ts` using Node's `stripTypeScriptTypes(..., {mode: 'strip'})`, combines root `roman.js` and `cast-extras.js` into `web/roman.js`, then concatenates that cast with the base engine into `web/toon.js`.
- `npm start` serves the local preview at `http://127.0.0.1:4173`. The expanded cast has 31 entries grouped into Story (10), Board (10), Office (5), Everyday (5) and Family (1). It includes fourteen expressions, six continuous motion studies, full-body/portrait framing, facing/prop controls, and transparent 1200x2000 PNG downloads. Its design canvas is 600x1000, rendered at 2× resolution.
- Use shared identity profiles across wardrobe changes: `elon` and `elonBeach` share Elon's face; `heroBroke`, `heroCEO` and `heroBurnout` share the hero's face. The engineer, executive, moderator, bodyguard and senator each have their own head contour, feature proportions and body silhouette.
- The ensemble adds ten board members in coordinated suits, five office colleagues, five everyday civilians and an American middle-class mom in a cardigan, tee, jeans and sneakers. Each has its own profile, hair, wardrobe and expression studies; do not vary only clothing color.
- The deterministic story sample is 30 seconds / 900 frames, three seconds per original cast entry, with a smooth move from the full body into a portrait. Save the corrected rig's sample as `out/cast-sample-v3.mp4` and refresh `out/cast-sample.mp4` after QA. Preserve the original rig and reel in `archive/roman-v1.js`, `archive/toon-v1.js` and `out/cast-sample-v1.mp4`.
- Run `npm run check` with local Chrome (or `CHROME_PATH`) for the character/expression matrix and UI checks.
- `render.text` is JavaScript source: copy it to a project's `render.mjs`. The example already has an executable `character-palette/render.mjs` copy. It supports Canvas 2D and WebGL through the same `window.ready`, `window.err`, `window.renderFrame(f)` and `canvas#c` contract.
- Run both visual passes below for samples too. The expanded review includes `stills/ensemble-sheet.jpg`, `stills/board-sheet.jpg`, `stills/turn-review.jpg` and `stills/mom.png`. Inspect the entire facing range: head, hair, glasses and hats must rotate together; hats must sit on the head, headset bands must remain behind the scalp, and ties must stay attached. Also check identity continuity, face detail, hand/prop contact and smooth motion. Preview UI screenshots alone do not replace inspection of the actual character frames.
- Character samples use the supplied 2D rig directly. A full narrated film additionally needs the 3D world, lighting, camera, audio, and timing stages below.

## Stage 1: Intake (for a narrated film)
For this project, the user has already provided `audio/voiceover.mp3` (125.152625 seconds). Skip intake and script invention: use the recording, `script.txt` and the caption assets as the current production input. Check `audio/voiceover-info.json` for transcription/timing quality notes and review uncertain words against the recording. In other projects, if an audio file is already attached, skip to Stage 4; use a supplied script for timing.
Otherwise ask one AskUserQuestion (or plain text if that tool is missing): **"Where are you starting from?"**
- **Voiceover ready**: ask them to upload it, plus the script text if they have it (the script makes the timing exact). Go to Stage 4 when it arrives.
- **I have a script, need the voiceover**: tighten the script per Stage 3 if needed, give it back with recording tips, ask for the upload, then go to Stage 4.
- **Need video ideas and a script**: go to Stage 2.
Also ask the target length if they haven't said. The default is 20-30 s; 60-90 s+ is supported by splitting into 20-25 s parts.

## Stage 2: 10 video ideas (or custom concept development)
If the user already has a concept (e.g., "What if you became Elon Musk for a day"), skip the 10-idea list and directly develop their concept into a structured multi-part story and shot plan. Otherwise, give 10 numbered ideas:
- **Title** (5-8 words, curiosity-driven, e.g. "The Soldier Who Never Left").
- **Hook line**: the first spoken sentence, a paradox or high-stakes premise stated as fact.
- **The twist** in one line (the ironic payoff that ends the video).
- **Why it animates well**: the 2-3 big visual moments (a collapse, a reveal, a chase, a transformation).
- **True, legend, or what-if**: state whether it is documented history, folklore, or a speculative "what-if" scenario.

What makes an idea "perfect" for this format:
- One surprising story with a physical cause and effect you can show literally in 2.5D.
- A clear protagonist, stakes that escalate rapidly, and an ironic twist in the last line.
- A setting that can be built from clean 3D primitives plus cartoon cards (apartments, penthouses, rocket launchpads, highways, bridges, ships, castles, labs, beaches).

## Stage 3: Script (after they pick)
Write the narration only (no stage directions in the spoken text), sized at about 3.7 words/s:
- 20-23 s part ≈ 75-85 words
- 30 s short ≈ 110 words
- 60 s short ≈ 220 words (split into 3 parts of ~20 s)
- 90 s (1:30) video ≈ 330 words (split into 4 parts of ~22.5 s / ~82 words each)

Formula across the story:
1. **Hook** (sentence 1, no setup): the immediate high-stakes premise or absurd fact.
2. **Setting & Inciting Event** in 1-2 lines: when, where, who, and the concrete physical trigger.
3. **Escalation**, 2-4 beats, each bigger. Use visual contrast and one exaggeration joke.
4. **Climax / Overload**: the hidden catch or runaway consequence of the premise.
5. **Twist / Payoff**: short, ironic, and the last words of the video.
Use plain spoken English, contractions, sentences around 8-15 words, and numbers written as words. Never describe what the viewer already sees.

Then reply with:
- The script in copyable blocks (broken by Part if 60-90 s+), with word count and estimated length.
- A shot-by-shot visual plan (the 3D sets, character outfits, props, and camera moves you'll animate).
- Recording tips: one steady, warm narrator voice; ElevenLabs works well (e.g., *Adam - Radio Announcer*, speed about 1.05-1.1, stability about 45-55 %). Mp3 or wav is fine. Leave natural pauses at sentence ends. Export without music.
- The ask: **"Upload the voiceover (or Part 1's voiceover) when it's ready and I'll build the video."**

## Stage 4: Build the video (after the voiceover is uploaded)
Do everything from here without stopping. Ask only if the timing cannot be resolved.

### 4.0 Get the kit & configure GPU/CPU rendering
For this portable handoff, run `node tools/create-film-project.mjs film-project` from the handoff root. It copies the local kit, current cast, narration, transcript and caption assets without network setup. Do not run the original network setup script or replace the current cast. The following describes the original reference setup only: locate `cartoon-short-kit/` and run `bash <kit>/tools/setup.sh ~/shorts/<slug>` when building an unrelated project without the portable helper.
- `setup.sh` copies `engine/*.js`, `engine/index.html`, `example/soldier/story.js`, `example/soldier/audio.py`, and `tools/*` into the project folder.
- On first run, `setup.sh` fetches `three@0.160.0` (`web/lib/three.module.js`) and clones `github.com/mromidev/claude-animated-shorts` to strip types from `toon.ts` into `web/toonbase.js`, then concatenates `web/toonbase.js` + `web/roman.js` into `web/toon.js`.
- **Hardware WebGL vs. CPU SwiftShader (`render.mjs`):**
  - The updated `render.mjs` requests hardware WebGL first (`--ignore-gpu-blocklist --enable-gpu-rasterization --enable-webgl`) and logs the detected renderer. Initialization or first-frame failures retry with CPU SwiftShader (`--use-angle=swiftshader`); `USE_CPU=1` forces that attempt. Browsers may choose software rendering even on the initial attempt. Canvas 2D character previews report their own engine and need no WebGL context. Actual speed depends on the scene and machine.
  - Note: Resolution and scene settings are preserved across backends, but GPU drivers and software rendering can differ. Inspect frames from the active backend; do not promise pixel-identical results or fixed speedups. The character-only sample uses Canvas 2D, with no 3D shadows or depth-of-field.

### 4.1 Timing
For this Elon project, use `audio/voiceover.mp3`, `script.txt` and the supplied caption timing files. Listen to verify words and boundaries before treating automatic transcription as final. If realignment is needed, run `python3 timing.py audio/voiceover.mp3 script.txt --out work`. Update the reference `audio.py` to read this canonical audio path instead of its example `voice.mp3`.
- With whisper or faster-whisper installed, it uses word timestamps.
- Otherwise it aligns script phrases (split at punctuation) to silence-detected speech segments using dynamic programming that matches syllables to duration.
- Check `work/phrases.json`: pauses should fall at sentence ends. Total frames = `round(duration * 30)`. The current recording is 125.152625 seconds, giving 3,755 picture frames at 30 fps (0–3,754). Keep the full original audio at mux; the final picture frame covers the fractional frame.

### 4.1a Required captions for this film
- Use the exact spoken narration; correct uncertain ASR words/names/numbers by listening. Never shorten, paraphrase or add words for the caption text. Respect actual speech pauses and cue boundaries.
- Use natural 2–5-word groups, at most two lines, bold white letters with a dark high-contrast stroke/shadow. Place them in the lower-middle 9:16 safe area, above platform controls and clear of faces, hands and focal props; adjust individual shots when necessary.
- Drive caption display by absolute audio time in preview and `renderFrame(f)`. Optional active-word color emphasis must follow reviewed word timestamps; never estimate each word with a constant reading rate.
- Captions must be burned into the final exported video. Draw them into the captured canvas/composite or burn them in during encoding; a separate HTML overlay will be missing from canvas-only captures. SRT/VTT sidecars are included for editing/accessibility but do not replace visible captions. Preserve one global caption timeline across render parts; avoid repeated/dropped words at boundaries.
- Inspect a captioned playback sample, the first/last cue, long words, line breaks, pauses and every part transition. Automatic timestamps require this final listening check.

### 4.2 Shot plan (`work/PLAN.md` before code)
Make one row per shot: frames, words, caption cue range, 3D setting, light preset, camera move, characters/outfits/poses/expressions, 3D props/effects, and SFX cue.
- Frame 0 is already the hook image (never start on a blank or slow fade-in).
- Usually one shot per phrase. Merge tiny phrases into the next shot.
- Illustrate every sentence literally. Props and environment animations carry the comedy and scale.
- Vary shot sizes across every part: hook MCU -> wide 3D environment reveal -> two-shot interaction -> extreme close-up insert on key prop/screen -> reaction close-up -> dynamic crane/orbit payoff.
- Use light presets for emotional beats: `day` for normal, `golden` for wealth/drama, `night`/`neon` for tech/control rooms, `redAlert` for panic. A time or location jump gets a 6-frame white flash.
- The twist line gets a sting (music stops, low hit, push-in with roll). The last shot's physical payoff lands on the final word.

### 4.3 World (`web/main.js` & `web/paint.js`)
Keep the core engine sections in `web/main.js`: toon materials, ink contract, `add`/`tbox`, sky, lights, cards, render targets/post, `applyLight`, `drawActors`, `swapForNd`, `renderFrame`. Replace the example Roman bridge world between `// ---------- world ----------` and `// ---------- cards ----------`, plus the story parts of `worldState()`.
- Build rich environments from 3D primitives with painted canvas textures (`paint.js`: planks, beams, stone, grass, dirt, plaster, roof tiles, marble, banners, carved/printed text, plus modern textures like brushed steel, carbon grid, asphalt, glass skyscraper windows, glowing screens). Write new painters in `paint.js` using the same flat-with-dark-seams style.
- Use `tbox` for constant texel density, a 2-step toon gradient, and fog = horizon colour.
- Set pieces (rockets launching, cars moving, stock arrows bursting through floors, doors opening, piles of paper growing) are pivoted Three.js `Group` objects driven by `0..1` progress from `worldAt(f)` with eased (`M.smooth`, `M.back`, `M.spring`) and staggered parts.
- Diegetic text on phones, tablets, signs, or buildings must be checked on the contact sheet to ensure it is not mirrored.

### 4.4 Cast (`web/roman.js` -> `web/toon.js`)
- `romanFront(p, outfitKey, opts)` draws on a `600x1000` design canvas (`1200x2000` transparent texture) with soles at `y=975`. The card is `2.25 m` tall in 3D space (`1 canvas unit = 0.00225 m`). Preserve this card contract when redesigning the cast.
- `OUTFITS` chooses wardrobe and accessories; `CHARACTER_PROFILES` controls each identity's head contour, cheeks, jaw, chin, eyes, nose, mouth, neck and torso proportions. Elon's business and beach variants share the `elon` profile and swept hair. The hero's three wardrobe variants share the `hero` profile. Keep the supporting cast visibly distinct in silhouette as well as color.
- Build volume with layered Canvas paths, radial skin gradients, directional cloth gradients, soft cheek/nose planes, hair highlights and restrained seams. Keep the bean torso and slender articulated limbs. Draw outfits, glasses, badges and hand props live so they follow the rig rather than becoming static bitmap replacements. `headBounds(outfitKey)` provides a safe crop for expression studies, including hats.
- Use the shared ellipsoid projection for every head layer, including the face, hair, glasses and hats; independent horizontal offsets cause visible drift in turns. Keep the beach hat seated on the scalp and the engineer's headset bridge behind the hair. Draw tie knot and blade in one attachment transform so even a loose tie stays coherent.
- Arm poses: `hang`, `spear`, `point`, `up`, `wave`, `hip`, `belly`, `temple` (+swirl), `lift`, `reach` (+lift), `cheek`, `shield`, `cross`, `thumb`.
- Expressions: `roman.js` explicitly defines the modern aliases missing from the base engine: `happy`, `sad`, `angry`, `smirk`, `wink`, and `worried`, plus `snore`, `stubborn`, `squint`, `exhausted`, and `hyped`. `neutral`, `shock`, and `laugh` are in the base. The exported `EXPRESSIONS` array is the preview list. Eye kinds must be supported by the engine (`dot`, `small`, `lid`, `slit`, `happy`, `dash`, `squeeze`, `shock`, `shockHalf`, `spiral`); **`open` is invalid and falls through to a spiral eye**. Unknown expression names fall back to neutral.
- The redesigned rig draws its sculpted faces directly, while preserving those aliases for legacy helpers. Animate speaking with the continuous `opts.talk` mouth parameter while retaining the selected expression, eye pose and identity. Never simulate speech by cycling whole-face expressions. The preview's procedural Talk study is not audio lip sync.
- **Rebuild after every edit** with `cat web/toonbase.js web/roman.js > web/toon.js`. In the character sample, edit root `roman.js` for the shared rig or root `cast-extras.js` for ensemble data, then run `npm run build` from `character-palette/` so the copied cast and bundle stay synchronized.
- Detached props or floating UI cards (e.g. a lifted helmet, a floating `$340B` net-worth counter, speech icons) are separate billboard cards aligned with `headCenter(seed)`: `y = DECK + (partY - hc) * 0.00225`.

### 4.5 Motion: smooth and alive (`web/motion.js`)
- **Cameras**: `camFromKeys(keys, f, {kicks})`. Use `smooth` glides (18-45 f), `easeOut` for reveals and whips, and `path` via-points (Catmull-Rom splines) for curved 3D orbits. Every hold creeps (`creep = 0.0012`) so the frame is never static for 4+ frames. Use 3-5° rolls on drama and 7-frame `kicks` on impacts/launches.
- **Characters never freeze**: apply `idle(f, seed)` to every visible character card, `blinkAt(f, seed)` for natural blinking, and head bobs on stressed words.
- The rig also supports continuous head turns, articulated walk cycles, waving, hair sway, prop tilt and eased pose entry. Keep these small secondary movements coherent with the body; check them in playback as well as stills.
- **Actions**: anticipation (`M.anticip`) -> overshoot (`M.back`) -> spring settle (`M.spring`).
- **Secondary motion**: floating notification cards, smoke/fire plumes, cash particles, sweat drops, or drifting clouds so the scene always feels alive.
- **Lens**: DOF on close-ups and mediums (`cInf` 8-14 px), focused on the speaking character's eyes. Wide shots stay sharp. Focus racks take ~14 frames.

### 4.6 Mandatory 2-Pass Visual Look Check (before the full render)
Never launch a full frame render blindly. You MUST visually inspect the rendered scenes first:
1. **Pass 1 — Initial Contact Sheet**:
   - Render 10-16 representative stills (the middle of each shot plus key transitions and prop actions):
     `node render.mjs stills/a "5,45,95,140,200,260,330,400,470,540,610,660"`
   - Build the contact sheet:
     `python3 sheet.py stills/a stills/sheet_a.jpg`
   - **Visually view `stills/sheet_a.jpg`** and audit every frame for these 6 visual traps:
     1. *Narrow vertical framing (`1080x1920`)*: Are characters cut off at the left/right edges? (At 4 m distance and FOV 40°, horizontal half-width is only `±0.8 m`—stage multiple characters in depth rather than wide horizontal lines).
     2. *Obstructions*: Are 3D railings, desks, cars, or pillars blocking a character's face or body?
     3. *Camera clipping*: Does the camera path intersect walls, roofs, ground planes, or props?
     4. *Mirrored or unreadable text*: Do diegetic signs, screens, or labels read left-to-right clearly with high contrast?
     5. *Detached prop alignment*: Are floating cards or held props aligned properly with the character's hands/head?
     6. *Visual energy & composition*: Does every shot have clear depth (foreground, subject, 3D background) and distinct lighting?
2. **Pass 2 — Fix & Verify (`sheet_b.jpg`)**:
   - Adjust camera coordinates, FOV, prop positions, or character poses in `web/story.js` and `web/main.js` to fix any issues spotted in Pass 1.
   - Re-render the affected frames into `stills/b` and run `python3 sheet.py stills/b stills/sheet_b.jpg` to confirm the fixes look clean before starting the full render.

### 4.7 Sound (`audio.py` -> `mix_raw.wav`)
Edit `audio.py` to match the shot timings (`F = lambda f: f / 30`) and emotional beats of the part:
- **Music bed**: synthesized rhythmic loop that builds energy during escalation and cuts out cleanly at the twist line (leaving a low ambient drone or environment sound).
- **SFX cues**: place frame-accurate procedural hits (`whoosh` on camera whips, `thunk` on stamps/knocks, `ting` on money/reveals, `rumble`+`crash` on launches/impacts, `sting` on the twist, `water`/`leaves` on outdoor scenes).
- Run `python3 audio.py` to generate `mix_raw.wav` (which mixes the unchanged `audio/voiceover.mp3`, the ducked music bed, and SFX). The reference example may still use `voice.mp3`; update that path and its soldier-specific duration/cue table before running it.

### 4.8 Render + Finish + Multi-Part Concat
1. **Render all frames**:
   - Run `node render.mjs frames "0-<TOTAL-1>"` (`RESUME=1` resumes safely if interrupted).
2. **Encode and QA (`finish.sh`)**:
   - Run `bash finish.sh "Part1"`. It normalizes `mix_raw.wav` to `-14 LUFS` (`mix.wav`), encodes `out/Part1.mp4` (`libx264 -preset slow -crf 17`), checks for frozen spans (`>=0.4s`) or black frames, and outputs `out/qa_sheet.jpg`.
   - Inspect `out/qa_sheet.jpg` to confirm the full render is clean.
3. **Storage cleanup (for multi-part projects)**:
   - Once `out/Part1.mp4` is verified, run `rm -rf frames/*.jpg` to free disk space before rendering Part 2.
4. **Combine parts (when building a multi-part 60s–90s video)**:
   - Create `concat.txt` listing each finished part (`file 'Part1.mp4'`, etc.) and run:
     `ffmpeg -y -f concat -safe 0 -i concat.txt -c copy Final_Master.mp4`


For this 125.152625-second film, prefer rendering picture-only chunks at reviewed sentence/shot boundaries, joining them, then muxing one continuous full-length audio master. Keep captions on a global timebase. Do not cut or independently re-encode the narration at arbitrary ~20-second boundaries; that can drop syllables, create encoder gaps and drift caption sync.
