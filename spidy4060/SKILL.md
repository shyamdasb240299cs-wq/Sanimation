---
name: spidy-character-animation
description: Use the Spidy cast and the latest shared cartoon rig to create consistent character sheets and motion studies, or integrate these characters into the Brain Decoy short.
---
# Spidy character workflow

Use `web/roman.js` as the character source. Run `npm run build` after edits. `web/toonbase.js` is the inherited drawing engine; `web/toon.js` is the generated portable module. Do not rebuild from the old Elon source. The exact latest previous project skill is preserved in `skills/elon-latest-original.md`; its Elon-specific durations, captions and cast are historical context, not instructions for this project.

Current task scope is character assets, sheets, code, and reusable motion studies. Do not interpret the attached production brief as a request to render the full film. The user's direct request adds Gwen, an unmasked Andrew Garfield-inspired Peter, and civilian variants; it takes precedence over the attached brief's optional unmasking / likeness direction.

Use `drawCharacter(context, key, options)` on a 600×1000 design canvas. Full-size exports are 1080×1600 transparent PNG. Adult soles sit at y=975; the child uses a 0.7 scale anchored to the same floor. Actor keys are in `characters/manifest.json`. Reuse `peter` identity for masked, suit-unmasked and casual forms. Preserve red/blue panels, eye frames, emblem, child yellow coat / teal backpack / blue shoes, and eight tiny-spider legs.

Options: `expr`, `facing` (-1 to +1, stylized three-quarter range), `L`/`R` arm poses, `step`, `stride`, `bob`, `tilt`, `headTilt`, `jump`, `blink`, `talk`, `hairPhase`, `shooters` (`none`, `full`, `empty`), and `time`. Use `studio.options(frame, overrides)` for deterministic motion. Keep facial layers in the shared ellipsoid transform. Keep devices in the wrist transform. Never flip a character texture to simulate turns when it contains readable props.

These are 2D vector rigs suitable for 2.5D cards, not Blender skeletal meshes. `swingPose` and `webPose` are gesture studies: the eventual film still needs fixed web anchors, pendulum paths, contact poses, camera motion, and action-specific animation. Procedural talk is not phoneme lip sync. Do not claim complete choreography from these samples.

Validation: run `npm run capture`, then `python3 make-sheets.py`. Inspect principal and civilian sheets, all expression and turn sheets, device states, and successive reel frames. Capture an initial pass, fix visual problems, and inspect the final pass. Preserve review findings in `review/QA.md`.

Narration is `audio/voiceover-original.mp3`, verified 81.3975 seconds. Keep it byte-for-byte intact. The original brief is reference material. When building the later film, no wrist devices on the first jump; full cartridges after retrieval; empty devices remain attached after depletion and during rescue. Gwen is available for the love/normal-life reflection but has no additional spoken dialogue.

The cast now has 31 entries, including 25 civilians. Added civilian16–civilian25 have independent identity profiles in `CITY_ADDITIONS`. Select sheets by `group` rather than array offsets so future additions remain included. `SKIP_MOTION=1 npm run capture` refreshes exports and validation while preserving the unchanged principal motion reel.
