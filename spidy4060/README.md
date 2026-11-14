# Spidy4060 — Brain Decoy character pack

31 cast entries in the same smooth, shaded 2D cartoon style as the earlier Elon character sheets:
- Masked Spider-Man, unmasked suited Peter, and civilian Peter sharing one identity profile.
- Andrew Garfield-inspired stylized Peter, Gwen Stacy, and a seven-year-old rescue child.
- 25 distinct civilians: fans, commuters, neighbors, workers, a parent, a rider, students and shoppers.
- Pip, the eight-legged red-and-blue outro spider.

## Open the studio

Node 22+ is required. Run `npm install`, then `npm start`, and open http://127.0.0.1:4173. The studio offers 14 expressions, 11 motion/gesture studies, continuous three-quarter head turns, three wrist-device states, portrait framing, pause, and transparent PNG download. No runtime network or external art assets are required.

## Deliverables

- `sheets/`: principal/civilian cast sheets and six-expression/five-angle studies for the four main designs.
- `characters/`: transparent PNGs and machine-readable cast manifest.
- `review/motion-preview.mp4`: eight-second silent character movement sample.
- `web/roman.js`: editable character geometry, wardrobe, face projection and drawing API.
- `web/toon.js`: self-contained drawing module, including inherited engine.
- `web/app.js`: deterministic animation options and interactive preview.
- `SKILL.md`: current Spidy instructions.
- `skills/elon-latest-original.md`: exact latest skill from the previous film project.
- `reference/`: original supplied brief; `audio/`: unchanged original narration.

Run `npm run build` after rig changes. `npm run capture` uses Playwright and local Chrome at `/opt/google/chrome/chrome`; set `CHROME_PATH` on other machines. Run `python3 make-sheets.py` with Pillow installed to rebuild sheets. Intermediate motion frames are intentionally excluded from Git. Encode with:

```sh
ffmpeg -framerate 30 -i review/motion/f%04d.png -vf scale=540:800 -c:v libx264 -crf 20 -pix_fmt yuv420p review/motion-preview.mp4
```

## Integrating a character

```js
import {drawCharacter} from './web/toon.js';
ctx.save();
ctx.scale(2, 2); // a 1200×2000 target with 600×1000 logical coordinates
 drawCharacter(ctx, 'spidy', {
   expr: 'shock', facing: 0.35, R: 'reach', L: 'hip', shooters: 'none'
 });
ctx.restore();
```

This is a character development pack, not the completed narrated short or a Blender skeletal rig. The old Elon pack uses 2D character cards inside 3D scenes; these assets retain that workflow. Head turns cover a stylized three-quarter range, not rear/full-profile views. The preview motions are reusable gesture studies; swinging, climbing and rescue choreography require later scene work. The actor-inspired face is a stylized interpretation, not a scanned likeness. See `review/QA.md` for validation details.
