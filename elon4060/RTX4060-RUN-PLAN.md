# RTX 4060 final draft run plan

1. Copy/extract the entire kit to a local SSD on the RTX 4060 laptop. Keep `film.blend`, `data`, `assets`, the Python scripts and `finish` together.
2. Use Blender 5.3.0. The Windows launchers expect `C:\Program Files\Blender Foundation\Blender 5.3\blender.exe`; edit their BLENDER line if installed elsewhere. Plug the laptop into power.
3. Run `bench_windows.bat` (Linux: `bash bench_linux.sh`). Confirm the console selects **OPTIX** or **CUDA**. Inspect the benchmark images, especially the phone grip, thumb signing and final beach phone. Benchmark first to measure this laptop's actual speed and memory use.
4. Run `run_windows.bat` (Linux: `bash run_linux.sh`). This renders **3755 frames at 1080 × 1920, 30 fps, 96 Cycles samples**. Keep `render-settings.json`. Rerun the same launcher to resume after interruption.
5. Once all frames exist, run `finish/finish_windows.bat` with FFmpeg installed, or copy the frames back and run `bash finish/finish_linux.sh`. This validates the sequence and encodes `finish/Elon_for_a_Day_Blender.mp4` with the original mixed audio and captions.

Do not change samples, scene, or data midway through a resumed output folder. Start a new folder for changed settings. Keep at least 10 GB free for extraction and output.

## Draft changes

- Continuous connected hands with separate nail surfaces; signing pose uses four folded fingers and an exposed opposed thumb.
- Stronger cartoon contours, warmer polished faces and brighter clothing.
- Softer shadows, controlled highlights, improved floor materials and subtle foliage movement.
- Final beach phone rests above the sand with a downward insert camera.
- 89 CC0 prop placements from the included downloaded asset library. Source and license records are in `ASSET-LICENSES.json`.

Local review images are selective reduced-resolution CPU renders. The full-resolution GPU benchmark and complete final movie review remain to be done on the RTX laptop.
