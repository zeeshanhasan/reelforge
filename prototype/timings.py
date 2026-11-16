"""Word-level timings for the narration with mlx-whisper.

Run with the spike voice env:
    spike/envs/voice/bin/python prototype/timings.py
"""

import json
import time
from pathlib import Path

import mlx_whisper

HERE = Path(__file__).parent
OUT = HERE / "out"
MODEL = "mlx-community/whisper-small.en-mlx"

reel = json.loads((HERE / "reel.json").read_text())
script = " ".join(b["narration"] for b in reel["beats"])

t0 = time.time()
result = mlx_whisper.transcribe(
    str(OUT / "narration.wav"),
    path_or_hf_repo=MODEL,
    word_timestamps=True,
    initial_prompt=script,  # spelling hints: Prept, rollbacks
    language="en",
)
words = [
    {"w": w["word"].strip(), "start": round(w["start"], 3), "end": round(w["end"], 3)}
    for seg in result["segments"]
    for w in seg["words"]
]
(OUT / "words.json").write_text(json.dumps(words, indent=1))
print(f"{len(words)} words in {time.time() - t0:.1f}s (script has {len(script.split())})")
print(" ".join(w["w"] for w in words))
