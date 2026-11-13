#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
python3 check_frames.py
ffmpeg -n -framerate 30 -i ../frames/f%04d.jpg -i mix.wav -vf "ass=captions.ass:fontsdir=fonts" -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -c:a aac -b:a 256k -movflags +faststart Elon_for_a_Day_Blender.mp4
