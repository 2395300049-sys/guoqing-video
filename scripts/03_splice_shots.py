#!/usr/bin/env python3
"""
Step 3: Seamless Shot Splicing via FFmpeg (720P / 1080P)
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

def splice(shot1: Path, shot2: Path, output: Path, width=1280, height=720):
    ffmpeg = get_ffmpeg()
    filter_str = (
        f"[0:v]scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1[v0];"
        f"[1:v]scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1[v1];"
        f"[v0][0:a][v1][1:a]concat=n=2:v=1:a=1[outv][outa]"
    )
    cmd = [
        ffmpeg, "-y",
        "-i", str(shot1),
        "-i", str(shot2),
        "-filter_complex", filter_str,
        "-map", "[outv]",
        "-map", "[outa]",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "20",
        "-c:a", "aac",
        "-b:a", "192k",
        str(output)
    ]
    print(f"Splicing {shot1.name} and {shot2.name} -> {output.name}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg error: {res.stderr}")
    print(f"Splice complete: {output} ({output.stat().st_size} bytes)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--shot1", default="shot1_explosion_15s.mp4")
    parser.add_argument("--shot2", default="shot2_assembly_15s.mp4")
    parser.add_argument("--output", default="spliced_30s_720p.mp4")
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=720)
    args = parser.parse_args()

    splice(Path(args.shot1), Path(args.shot2), Path(args.output), args.width, args.height)
