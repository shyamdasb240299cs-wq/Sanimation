# Elon for a Day — render it on the RTX 4060 laptop

This folder has everything needed to render the final 2:13 vertical film (1080 × 1920, 30 fps, 3,995 frames) in Blender Cycles on an NVIDIA RTX 4060. You get:

- all 10 sets
- the rigged 3D hands
- 121 placed Poly Haven props (CC0)
- the per-frame animation
- the captions, voiceover, music and sound effects

Total time: about 30 minutes of setup, then 3–6 hours of unattended rendering.

---

## 1. Requirements

| Item | Needed |
|---|---|
| GPU | NVIDIA RTX 4060 (laptop or desktop), 8 GB VRAM |
| RAM | 16 GB recommended |
| Disk | **12 GB free** on a local SSD (repo 1.5 GB, built scene 0.9 GB, frames ~3 GB, working space) |
| OS | Windows 10/11 (or Linux) |
| Blender | **5.3.0 exactly**. Other versions may not open the scene or may change the look. |
| NVIDIA driver | Latest Game Ready or Studio driver |
| Optional | `git` (to download) and `ffmpeg` (only if you want to make the MP4 on this laptop) |

---

## 2. Install the software (one time)

1. **NVIDIA driver:** open the NVIDIA App (or GeForce Experience), go to Drivers, install the latest one, and reboot.
2. **Blender 5.3.0:** go to <https://www.blender.org/download/>. If 5.3.0 is no longer the current release, use *Previous versions*, which also covers older releases. Install it to the default folder:
   `C:\Program Files\Blender Foundation\Blender 5.3\blender.exe`
   If you install it somewhere else, open each `.bat` file in Notepad and change the `set "BLENDER=..."` line at the top.
3. **(Optional) Git:** <https://git-scm.com/download/win>
4. **(Optional) ffmpeg:** open *Command Prompt* and run `winget install ffmpeg`, then close and reopen Command Prompt.

---

## 3. Get the files

**Option A, with Git (recommended):**
```
cd C:\
git clone https://github.com/shyamdasb240299cs-wq/Sanimation.git
cd Sanimation\elon4060
```
If the repository is private, Git will ask you to sign in to GitHub. Use your own account in the browser window it opens.

**Option B, without Git:** open the repository on github.com, click **Code → Download ZIP**, and extract it to `C:\Sanimation`. Use a short path with no special characters. Then open `C:\Sanimation\elon4060`.

Keep the folder structure exactly as it is. Don't move individual files out of `elon4060`.

---

## 4. One-time setup (builds `film.blend`)

`film.blend` (0.9 GB) is too big for GitHub, so it is rebuilt from the included data on this laptop.

Double-click **`setup_windows.bat`** (Linux: `bash setup_linux.sh`). It runs four steps:

1. Rejoins the large tree model that was split for GitHub.
2. Builds `film.blend`: all sets, Poly Haven materials and props, lights, camera and compositor. This takes 10–30 minutes, and the window prints progress.
3. Installs the rigged 3D hands (phone grip, thumbprint on the tablet, open-palm button press) and the final colour look.
4. Validates the kit: all 3,995 frames and every referenced file must be present.

It ends with **SETUP COMPLETE**. If it says SETUP FAILED, see Troubleshooting below.

---

## 5. Benchmark (5–10 minutes)

Double-click **`bench_windows.bat`**. It renders 15 representative frames into `bench\`.

- The log must say **`Cycles device: OPTIX`** (or `CUDA`). If it says CPU, see Troubleshooting.
- Each frame prints `... s/frame avg`. Full film time ≈ that number × 3,995, so 4 s/frame ≈ 4.2 hours.
- Open the images in `bench\` and check them. `f0690.jpg` is the thumbprint on the tablet, `f2146.jpg` the hand on the big red button, `f0100.jpg` the phone grip, `f3920.jpg` Elon tapping Subscribe in the new ending.

---

## 6. Render the film

Double-click **`run_windows.bat`**. Frames go to `frames\f0000.jpg` … `frames\f3994.jpg`.

- Plug the laptop into power and set Windows → Power mode to **Best performance**.
- Put the laptop on a hard, flat surface for airflow, and turn off sleep (Settings → System → Power → Screen and sleep → *Never* while plugged in).
- **It is resumable.** If it stops for any reason (crash, sleep, you close the window), just run `run_windows.bat` again. Finished frames are checked and skipped.
- Don't change samples or settings partway through. To try other settings, use a new empty output folder.

**Optional, from a Command Prompt in `elon4060`:**
```
run_windows.bat 0 1999 96        :: only frames 0–1999 (e.g. split the work with a second PC)
run_windows.bat 2000 3994 96     :: the rest
run_windows.bat 0 3994 64        :: fewer samples = faster, slightly softer (denoiser still on)
```

---

## 7. Make the final video

**Option A:** copy the `frames\` folder back to the authoring laptop for the final review, grade and encode.

**Option B, finish on this laptop (needs ffmpeg):** double-click **`finish\finish_windows.bat`**. It checks that all 3,995 frames exist, then writes `finish\Elon_for_a_Day_Blender.mp4` with burned-in captions and the full original audio: voiceover, music and SFX at −14 LUFS.

---

## 8. Troubleshooting

| Problem | Fix |
|---|---|
| `Cycles device: CPU` or "no supported GPU" | Update the NVIDIA driver and reboot. Then in Blender: *Edit → Preferences → System → Cycles Render Devices → OptiX*, tick the RTX 4060, and click *Save Preferences*. |
| `'blender' is not recognized` | Blender isn't at the default path. Edit the `BLENDER=` line at the top of the `.bat` files. |
| Out of memory / crash | Close other apps (browsers, games). Re-run. It resumes. Try `run_windows.bat 0 3994 64`. |
| Setup fails at step 2 | Check you have Blender **5.3.0** and that the whole `elon4060` folder (including `assets` and `data`) is present. Delete `film.blend` if it exists and re-run setup. |
| One frame looks wrong | Delete that `frames\fNNNN.jpg` and run `run_windows.bat` again. Only missing frames are rendered. |
| Very slow (>15 s/frame) | Check the GPU is used (see first row), the laptop is plugged in, and power mode is Best performance. |

---

## 9. What's in the folder

| Path | Purpose |
|---|---|
| `setup_windows.bat` / `setup_linux.sh` | One-time build of `film.blend` |
| `bench_*`, `run_*` | Benchmark and full render (resumable) |
| `build.py` | Builds all sets, materials, Poly Haven props (collision-checked), pools, lights, compositor |
| `rig_hands.py` | Rigged 3D cartoon hands: one skin mesh, bones per finger, smooth weights, nails |
| `continuous_hands.py`, `install_hands.py`, `refine_scene.py` | Hand meshes for device grips, installation, final look |
| `render_frames.py` | Per-frame renderer (camera, characters, props, screens, lights, post) |
| `validate_kit.py`, `rejoin_parts.py` | Kit check, rejoin split files |
| `data/` | Exported animation: 3,995 frame files, character images, screens, geometry |
| `assets/` | Poly Haven CC0 HDRIs, textures and 91 models (`ASSET-LICENSES.json`) |
| `finish/` | Captions, mixed audio, caption font, encode scripts |
