#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
"${BLENDER:-blender}" -b film.blend --python-exit-code 1 --python render_frames.py -- --engine CYCLES --require-gpu 1 --samples "${3:-96}" --only 100,300,450,690,1180,1345,1560,2080,2146,2265,2460,2880,3050,3340,3690 --out bench
