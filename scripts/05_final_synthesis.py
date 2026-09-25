#!/usr/bin/env python3
"""
Step 5: Multi-Track Synthesis (BGM Ducking, Logo Overlay, Outro Card Fade)
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

def synthesize(video: Path, logo: Path, outro: Path, bgm: Path, voice_dir: Path, output: Path):
    ffmpeg = get_ffmpeg()
    
    # Inputs:
    # 0: video
    # 1: logo (transparent PNG)
    # 2: outro (endcard)
    # 3: bgm
    # 4..8: voice_1..voice_5
    v1 = voice_dir / "voice_1.mp3"
    v2 = voice_dir / "voice_2.mp3"
    v3 = voice_dir / "voice_3.mp3"
    v4 = voice_dir / "voice_4.mp3"
    v5 = voice_dir / "voice_5.mp3"

    filter_complex = """
    [1:v]scale=180:-1[logo_scaled];
    [0:v][logo_scaled]overlay=35:30:enable='between(t,0,26.0)'[v_main];
    [2:v]scale=1280:720,format=rgba,fade=t=in:st=26.0:d=0.8:alpha=1[outro_fade];
    [v_main][outro_fade]overlay=0:0:enable='gte(t,26.0)'[out_video];

    [3:a]volume=0.35,afade=t=out:st=29.0:d=1.0[bgm];
    [0:a]volume=0.20[ambience];
    [4:a]adelay=800|800,volume=1.3[v1];
    [5:a]adelay=6500|6500,volume=1.3[v2];
    [6:a]adelay=14200|14200,volume=1.3[v3];
    [7:a]adelay=21000|21000,volume=1.3[v4];
    [8:a]adelay=26000|26000,volume=1.3[v5];

    [bgm][ambience][v1][v2][v3][v4][v5]amix=inputs=7:duration=first:dropout_transition=2[out_audio]
    """

    cmd = [
        ffmpeg, "-y",
        "-t", "30.0",
        "-i", str(video),
        "-i", str(logo),
        "-loop", "1", "-t", "30.0", "-i", str(outro),
        "-i", str(bgm),
        "-i", str(v1),
        "-i", str(v2),
        "-i", str(v3),
        "-i", str(v4),
        "-i", str(v5),
        "-filter_complex", filter_complex.strip(),
        "-map", "[out_video]",
        "-map", "[out_audio]",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "256k",
        "-t", "30.0",
        str(output)
    ]
    print(f"Synthesizing full commercial -> {output.name}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Synthesis failed: {res.stderr}")
    print(f"Synthesis complete! Output: {output} ({output.stat().st_size} bytes)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", default="spliced_30s_720p.mp4")
    parser.add_argument("--logo", default="logo.png")
    parser.add_argument("--outro", default="outro_card.png")
    parser.add_argument("--bgm", default="best_friend.m4a")
    parser.add_argument("--voice-dir", default="voiceover_clips")
    parser.add_argument("--output", default="synthesized_commercial.mp4")
    args = parser.parse_args()

    synthesize(Path(args.video), Path(args.logo), Path(args.outro), Path(args.bgm), Path(args.voice_dir), Path(args.output))
