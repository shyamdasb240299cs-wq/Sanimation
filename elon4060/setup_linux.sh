#!/bin/bash
# ONE-TIME SETUP: rejoin split assets, build film.blend, apply hand/look refinements, validate.
set -e
cd "$(dirname "$0")"
BLENDER=${BLENDER:-blender}
echo "[1/4] Rejoining large asset files..."; "$BLENDER" -b --factory-startup --python-exit-code 1 --python rejoin_parts.py
echo "[2/4] Building film.blend (10-30 min)..."; "$BLENDER" -b --factory-startup --python-exit-code 1 --python build.py
echo "[3/4] Installing the rigged hands and final look..."; "$BLENDER" -b film.blend --python-exit-code 1 --python refine_scene.py
echo "[4/4] Validating the kit..."; "$BLENDER" -b --factory-startup --python-exit-code 1 --python validate_kit.py
echo "SETUP COMPLETE. Next: bash bench_linux.sh"
