#!/bin/zsh
# Make the prototype reel: voice -> word timings -> render -> out/reel.mp4
# Run ./setup.sh once first.
set -euo pipefail
cd "${0:A:h}"
PY=.venv/bin/python
[[ -x $PY ]] || { echo "Run ./setup.sh first."; exit 1; }

echo "1/3 Voice"
$PY voice.py 2>&1 | grep -E "^model load|^\{" || true
echo "2/3 Word timings"
$PY timings.py 2>&1 | grep -E "words in" || true
echo "3/3 Render"
$PY render.py 2>&1 | grep -E "bound|rendered"
echo "Done: $(pwd)/out/reel.mp4"
