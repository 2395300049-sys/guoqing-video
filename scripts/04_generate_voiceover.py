#!/usr/bin/env python3
"""
Step 4: Neural English Commercial Voiceover Generation via edge-tts
"""

import asyncio
import argparse
from pathlib import Path

DEFAULT_LINES = [
    ("voice_1.mp3", "Precision engineering. Global scale."),
    ("voice_2.mp3", "From intricate design to worldwide markets, every detail matters."),
    ("voice_3.mp3", "Shutiao Global empowers enterprises to expand seamlessly across the globe."),
    ("voice_4.mp3", "Accelerate your global journey with confidence."),
    ("voice_5.mp3", "Shutiao Global. Going global made simple.")
]

async def generate_voice(output_dir: Path, voice_name="en-US-ChristopherNeural"):
    import edge_tts
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Generating voiceover clips using voice: {voice_name}")
    for filename, text in DEFAULT_LINES:
        out_path = output_dir / filename
        communicate = edge_tts.Communicate(text, voice_name, rate="+0%", pitch="+0Hz")
        await communicate.save(str(out_path))
        print(f"  [OK] {filename}: \"{text}\"")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="voiceover_clips")
    parser.add_argument("--voice", default="en-US-ChristopherNeural")
    args = parser.parse_args()

    asyncio.run(generate_voice(Path(args.output_dir), args.voice))
