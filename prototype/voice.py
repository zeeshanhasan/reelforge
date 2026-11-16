"""Voice each beat with Kokoro, then join them with short gaps.

Run with the spike voice env:
    spike/envs/voice/bin/python prototype/voice.py
"""

import json
import time
from pathlib import Path

import numpy as np
import soundfile as sf
from mlx_audio.tts.utils import load_model

HERE = Path(__file__).parent
OUT = HERE / "out"
SR = 24_000
GAP_S = 0.35  # pause between beats

reel = json.loads((HERE / "reel.json").read_text())
OUT.mkdir(exist_ok=True)

t0 = time.time()
model = load_model("mlx-community/Kokoro-82M-bf16")
load_s = time.time() - t0

timeline = []
chunks = []
cursor = 0.0
for beat in reel["beats"]:
    parts = [
        np.asarray(r.audio, dtype=np.float32).reshape(-1)
        for r in model.generate(
            text=beat["narration"], voice=reel["voice"], speed=reel["speed"], lang_code="a"
        )
    ]
    audio = np.concatenate(parts)
    sf.write(OUT / f"beat_{beat['id']}.wav", audio, SR)
    dur = len(audio) / SR
    timeline.append({"id": beat["id"], "start": round(cursor, 3), "end": round(cursor + dur, 3)})
    chunks += [audio, np.zeros(int(GAP_S * SR), dtype=np.float32)]
    cursor += dur + GAP_S

full = np.concatenate(chunks)
sf.write(OUT / "narration.wav", full, SR)
(OUT / "beats.json").write_text(json.dumps(timeline, indent=2))
print(f"model load {load_s:.1f}s, total {time.time() - t0:.1f}s, audio {len(full) / SR:.1f}s")
for b in timeline:
    print(b)
