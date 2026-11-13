#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
"${BLENDER:-blender}" -b film.blend --python-exit-code 1 --python render_frames.py -- --engine CYCLES --require-gpu 1 --samples "${3:-96}" --start "${1:-0}" --end "${2:-3994}" --out frames
