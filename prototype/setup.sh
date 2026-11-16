#!/bin/zsh
# One-time setup for the prototype reel. Safe to run again: it skips what is already there.
# Prints PASS or FAIL per step and stops at the first failure.
set -uo pipefail
cd "${0:A:h}"

step() { printf "%-52s" "$1"; }
pass() { print -P "%F{green}PASS%f ${1:-}"; }
fail() { print -P "%F{red}FAIL%f $1"; exit 1; }

step "Apple Silicon Mac"
[[ "$(uname -s)/$(uname -m)" == "Darwin/arm64" ]] && pass || fail "needs an Apple Silicon Mac (M1 or later)"

step "Homebrew"
command -v brew >/dev/null && pass || fail "install it from https://brew.sh, then run this again"

step "ffmpeg"
command -v ffmpeg >/dev/null || brew install ffmpeg >/dev/null 2>&1
command -v ffmpeg >/dev/null && pass || fail "brew install ffmpeg did not work"

step "uv (Python installer)"
command -v uv >/dev/null || brew install uv >/dev/null 2>&1
command -v uv >/dev/null && pass || fail "brew install uv did not work"

step "Python 3.11 environment (.venv)"
[[ -x .venv/bin/python ]] || uv venv -q -p 3.11 .venv >/dev/null 2>&1
[[ -x .venv/bin/python ]] && pass || fail "uv venv -p 3.11 .venv did not work"

step "Python packages"
uv pip install -q -p .venv/bin/python -r requirements.txt >/tmp/reelforge-setup.log 2>&1 \
  && pass || fail "see /tmp/reelforge-setup.log"

step "Headless browser for rendering"
.venv/bin/python -m playwright install chromium >>/tmp/reelforge-setup.log 2>&1 \
  && pass || fail "see /tmp/reelforge-setup.log"

step "Voice model (Kokoro, first time downloads it)"
.venv/bin/python -c "from mlx_audio.tts.utils import load_model; load_model('mlx-community/Kokoro-82M-bf16')" \
  >>/tmp/reelforge-setup.log 2>&1 && pass || fail "see /tmp/reelforge-setup.log"

step "Timing model (Whisper, first time downloads it)"
.venv/bin/python -c "from huggingface_hub import snapshot_download as d; d('mlx-community/whisper-small.en-mlx')" \
  >>/tmp/reelforge-setup.log 2>&1 && pass || fail "see /tmp/reelforge-setup.log"

print "\nSetup done. Make the reel with: ./make_reel.sh"
