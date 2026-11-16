"""Render scene.html frame by frame with Playwright, then assemble the reel with ffmpeg.

    spike/envs/render/bin/python prototype/render.py            # full reel
    spike/envs/render/bin/python prototype/render.py --stills   # a few stills only
"""

import json
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
OUT = HERE / "out"
FPS = 30
TAIL_S = 1.2  # hold the end card after the voice stops

words = json.loads((OUT / "words.json").read_text())
beats = json.loads((OUT / "beats.json").read_text())
voice_end = beats[-1]["end"]
end = voice_end + TAIL_S
n_frames = int(end * FPS)
stills = "--stills" in sys.argv

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
    page.goto((HERE / "scene.html").resolve().as_uri())
    page.evaluate("document.fonts.ready")
    info = page.evaluate("d => init(d)", {"words": words, "beats": beats, "end": voice_end})
    print(f"bound {info['bound']} of {info['words']} spoken words; unbound: {info['unbound']}")

    if stills:
        for name, t in [("hook", 3.6), ("question", 7.6), ("answer_a", 15.8), ("answer_b", 27.4), ("why", 31.6), ("cta", end - 0.1)]:
            page.evaluate("t => seek(t)", t)
            page.screenshot(path=str(OUT / f"still_{name}.png"))
        browser.close()
        sys.exit()

    ffmpeg = subprocess.Popen(
        [
            "ffmpeg", "-v", "error", "-y",
            "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "png", "-i", "-",
            "-i", str(OUT / "narration.wav"),
            "-filter_complex", f"[1:a]loudnorm=I=-14:TP=-1.5:LRA=11,apad=whole_dur={end}[a]",
            "-map", "0:v", "-map", "[a]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
            "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            "-movflags", "+faststart", "-t", f"{end:.3f}",
            str(OUT / "reel.mp4"),
        ],
        stdin=subprocess.PIPE,
    )
    t0 = time.time()
    for i in range(n_frames):
        page.evaluate("t => seek(t)", i / FPS)
        ffmpeg.stdin.write(page.screenshot(type="png"))
        if i % 150 == 0:
            print(f"frame {i}/{n_frames}  {time.time() - t0:.0f}s", flush=True)
    ffmpeg.stdin.close()
    ffmpeg.wait()
    browser.close()
    print(f"rendered {n_frames} frames in {time.time() - t0:.0f}s -> {OUT / 'reel.mp4'}")
