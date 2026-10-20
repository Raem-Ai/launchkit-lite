# Reel Factory pipeline (open source, MIT)

The ffmpeg + Playwright + Whisper pipeline behind the daily "$100 → $10,000" challenge reels (carlosg.ai/challenge). Turns a folder of generated clips and voice lines into a finished vertical reel with dissolves, word-keyed motion graphics, burned-in captions, a ducked music bed and SFX.

Run order (from a working folder containing `intro.mp4`, `hf/become.mp4`, `hf/<shot>.mp4`, `sfx/`, `brand/`):

1. `trimsync.py` cut each shot to its own speech (keeps the model's lip-sync)
2. `assemble.py` timeline + base track
3. `xfade.py` dissolves / hard cuts
4. `words.py` Whisper word timestamps → `caps.py` caption chunks
5. `plan.py` graphics + SFX cues keyed to spoken words (edit per episode)
6. `build.py` render `overlay.html` to 30 fps frames (`part N 4` for 4 workers)
7. `mix.py` voices + music + SFX, loudnorm
8. `compose.py` final mp4

`lipcheck.py` prints mouth-motion vs audio bars to find the crop; the real check is a face strip:
`ffmpeg -i final.mp4 -vf "fps=5,crop=W:H:X:Y,scale=120:-1,tile=13x2" -frames:v 1 strip.png`

Requirements: Python 3.10+, ffmpeg, `pip install faster-whisper playwright numpy scipy` and `playwright install chromium`. Fonts (Inter, Michroma) are OFL.

The full method, the generation prompts that keep characters and lip-sync consistent, the sound-design recipe, and a worked example are in the Reel Factory kit: https://raem.gumroad.com/l/reel-factory
