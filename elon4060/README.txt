ELON FOR A DAY — POLISHED BLENDER DRAFT / RTX 4060 HANDOFF
=======================================================

Use this complete folder. The original kit and finished v2 MP4 remain separate.
The film is 1080 x 1920, 30 fps, frames 0–3754. Original narration and caption timing are retained.

WHAT CHANGED
  Stronger plum character contours, brighter cloth highlights, wrapped fingers,
  defined shoe soles/toes, continuous Blender hand meshes with shaped nails,
  warmer polished faces, softer face lighting,
  broader sun shadows, restrained bloom, richer color, reduced photographic texture
  noise, 89 downloaded CC0 prop placements, and subtle deterministic foliage sway.
  See dressing_report.txt for placements and rejected obstructions.
  Source/license links for the included 65 models, 31 materials and 6 HDRIs are
  recorded in ASSET-LICENSES.json. Inclusion in the library does not imply every
  model appears on camera. Story-specific geometry/screens remain custom.

SETUP
  Blender 5.3.0 is the version used on the authoring laptop.
  Default Windows path: C:\Program Files\Blender Foundation\Blender 5.3\blender.exe
  Edit the BLENDER line in the .bat launchers if needed, or put blender on PATH.
  Extract the whole folder onto a fast local drive. Keep data/, assets/ and finish/.
  Have at least 10 GB free for the kit, renders and final video.

1. BENCHMARK / REVIEW ON THE RTX 4060
  Double-click bench_windows.bat (or run bash bench_linux.sh).
  It renders 14 representative shots at 96 Cycles samples and full resolution.
  Confirm the log says "Cycles device: OPTIX" or "CUDA" and inspect bench/.
  The launcher stops if no supported GPU is found. It will not silently start
  a full CPU render. Render duration depends on laptop power, cooling and scenes;
  use the printed benchmark timing to estimate the full 3755-frame run.

2. FULL RENDER
  Double-click run_windows.bat (or run bash run_linux.sh).
  frames/f0000.jpg ... frames/f3754.jpg. Re-run to continue after interruption.
  Completed JPEGs are checked before skipping. Keep the render-settings.json file.

  Optional ranges and samples:
     run_windows.bat 0 1999 96
     run_windows.bat 2000 3754 96
  Samples/resolution/settings are tracked. Use an empty output folder if changing
  them; the renderer refuses to mix settings in an existing folder.

3. FINISH
  Copy frames/ back to the authoring laptop, or install ffmpeg on this laptop and
  run finish/finish_windows.bat (bash finish/finish_linux.sh on Linux).
  It checks that all 3755 frames exist, then makes
  finish/Elon_for_a_Day_Blender.mp4 with globally timed captions and continuous
  original narration, music and SFX. Do not concatenate independently cut audio.

CONTENTS
  film.blend, data/, assets/, render_frames.py  Required render inputs
  continuous_hands.py / install_hands.py      Native connected hand geometry
  build.py                                   Rebuilds the scene from data/assets
  validate_kit.py                             Checks frame/asset dependencies
  review/                                    Local Blender preview evidence
  finish/                                    Mixed audio, captions, fonts, encoder
  ASSET-LICENSES.json                         Free asset source/license manifest

TROUBLESHOOTING
  GPU not found: update NVIDIA driver and check Blender > Preferences > System.
  Out of GPU memory: close GPU-heavy apps and restart the benchmark. Lower sample
  count primarily changes time/noise and is not a general VRAM fix.
  A frame needs replacement: delete only that JPEG, keep render-settings.json,
  and run the same render settings again.
  The local previews are selective CPU tests; the full RTX render still needs
  its benchmark and final video QA after completion.
