# Character pack QA — 2026-11-14

Two visual review passes plus a final arm correction were performed on rendered character assets.

- First pass: inspected principal cast and Peter's five facing positions. Shared face/hair projection stays attached across the supported turn range.
- Refinements: red segmented boots, Gwen's headband, more mask-lens expression variation, child portrait crop corrected for the smaller rig.
- Second pass: inspected the child expression grid, civilian ensemble, and hero gesture frame. Removed a redundant straight forearm stroke which protruded from the curved hip arm, and added extended index/pinky fingers to the web gesture.
- Automated render matrix: 21 entries × 14 expressions × 3 facing boundaries, plus 5 principal/outro designs × 11 motions × 6 frame positions = 1,212 renders. No browser exceptions. This checks rendering coverage, not anatomical perfection or film choreography.
- Preserved narration duration: 81.3975 seconds. Original skill and voiceover copied unchanged; SHA-256 hashes in `input-hashes.txt`.
- Three wrist states are exposed independently of character identity. Full/empty states are explicit options; callers must set them according to story timing.

Scope: vector character sheets and 2.5D-ready drawing code. Not a finished 3D character mesh, full rotation model, audio-aligned film, or completed rescue/swing sequence. Motion reel contains deterministic gesture samples with no narration. Tiny spider leg motion is implemented in the studio; the lens web / CTA composition belongs to later scene work.

## Civilian expansion

Added civilian16–civilian25, bringing the ensemble to 25 civilians / 31 total entries. Each addition has an independent face profile, wardrobe, and hairstyle. First-pass sheet review caught the inherited vest insignia; it was removed from the new civilian designs. Final validation covers 31 × 14 × 3 expression/facing renders plus 15 × 11 × 6 motion frames (2,292 total). The original four-character motion reel is unchanged. `sheets/city-additions.jpg` presents the ten additions separately; `sheets/city-cast.jpg` includes all 25 civilians.
