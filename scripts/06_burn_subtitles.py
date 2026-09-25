#!/usr/bin/env python3
"""
Step 6: Burn Bilingual ASS Subtitles into Commercial Video
"""

import argparse
import subprocess
from pathlib import Path

def get_ffmpeg():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"

def burn_subtitles(video_in: Path, ass_file: Path, video_out: Path):
    ffmpeg = get_ffmpeg()
    cmd = [
        ffmpeg, "-y",
        "-i", str(video_in),
        "-vf", f"subtitles={ass_file}",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        str(video_out)
    ]
    print(f"Burning subtitles from {ass_file.name} into {video_out.name}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Subtitle burn failed: {res.stderr}")
    print(f"Burn complete! Output file: {video_out} ({video_out.stat().st_size} bytes)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="synthesized_commercial.mp4")
    parser.add_argument("--subtitles", default="templates/commercial_subtitles.ass")
    parser.add_argument("--output", default="final_commercial_bilingual.mp4")
    args = parser.parse_args()

    burn_subtitles(Path(args.input), Path(args.subtitles), Path(args.output))
