#!/usr/bin/env python3
"""
Step 1: Extract Keyframe Anchors from 3D White-Model / Clay Video
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

def extract_anchors(video_path: Path, output_dir: Path):
    ffmpeg = get_ffmpeg()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Standard 3-anchor positions for 30s mechanical animations:
    # 1. Initial Hero Assembly (~2s)
    # 2. Maximum Exploded/Disassembly Detail (~7s)
    # 3. Reassembled Operation (~28s)
    anchors = [
        (2.0, "anchor_hero.jpg", "全景亮相基准"),
        (7.0, "anchor_exploded.jpg", "结构解构爆炸基准"),
        (28.0, "anchor_assembled.jpg", "重构运转基准")
    ]
    
    print(f"Extracting anchors from: {video_path}")
    for timestamp, filename, desc in anchors:
        out_file = output_dir / filename
        cmd = [
            ffmpeg, "-y",
            "-ss", str(timestamp),
            "-i", str(video_path),
            "-vframes", "1",
            "-q:v", "2",
            str(out_file)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"  [OK] {filename} ({desc}) @ {timestamp}s -> {out_file}")
        else:
            print(f"  [FAIL] Failed extracting {filename}: {res.stderr}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract Keyframe Anchors from Video")
    parser.add_argument("--input", default="e758d18ed47db0cbaf0dfe55a09a73ae_raw.mp4", help="Path to raw white-model video")
    parser.add_argument("--output", default="extracted_anchors", help="Output directory for anchors")
    args = parser.parse_args()
    
    extract_anchors(Path(args.input), Path(args.output))
