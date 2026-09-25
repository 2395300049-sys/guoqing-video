#!/usr/bin/env python3
"""
Step 2: Dual-Engine AI Video Rendering (MiniMax-H3 / Google Veo)
Submits Shot 1 (Exploded Disassembly) and Shot 2 (Assembly & Rotation)
"""

import os
import sys
import time
import json
import urllib.request
import argparse
from pathlib import Path

def get_token():
    # 1. Check environment variable
    token = os.environ.get("METASO_API_KEY")
    if token:
        return token
    # 2. Check local or parent .env files
    env_paths = [
        Path(".env"),
        Path("../.env"),
        Path("/Users/yujialin/cx- project/vps/ComfyUI/.env")
    ]
    for p in env_paths:
        if p.exists():
            for line in p.read_text(encoding="utf-8").splitlines():
                if line.startswith("METASO_API_KEY="):
                    return line.split("=", 1)[1].strip()
    return "mk-DDADBA6FCADC5F75F74B56381CC6779B"

BASE_URL = "https://metaso.cn/api/minimax"

def upload_image(image_path: Path, token: str) -> str:
    print(f"Uploading anchor {image_path.name}...")
    boundary = "----WebKitFormBoundary" + hex(int(time.time() * 1000))[2:]
    with open(image_path, "rb") as f:
        img_bytes = f.read()

    body = bytearray()
    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(b'Content-Disposition: form-data; name="purpose"\r\n\r\nvideo_generation_input\r\n')
    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(f'Content-Disposition: form-data; name="file"; filename="{image_path.name}"\r\n'.encode("utf-8"))
    body.extend(b"Content-Type: image/jpeg\r\n\r\n")
    body.extend(img_bytes)
    body.extend(f"\r\n--{boundary}--\r\n".encode("utf-8"))

    req = urllib.request.Request(
        f"{BASE_URL}/v1/files/upload",
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/form-data; boundary={boundary}"
        }
    )
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
    
    file_id = res.get("file", {}).get("file_id")
    if not file_id:
        raise RuntimeError(f"Upload failed: {res}")
    return f"mm_file://{file_id}"

def submit_and_poll(prompt: str, images: list, duration: int, resolution: str, token: str, output_path: Path):
    content = [{"type": "text", "text": prompt}]
    for img_url in images:
        content.append({"type": "image_url", "image_url": {"url": img_url}, "role": "reference_image"})

    payload = {
        "model": "MiniMax-H3",
        "content": content,
        "resolution": resolution,
        "duration": duration,
        "ratio": "16:9"
    }

    req = urllib.request.Request(
        f"{BASE_URL}/v2/video_generation",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))

    task_id = res.get("task_id")
    print(f"Task created: {task_id}. Polling progress...")

    deadline = time.time() + 1800
    video_url = None
    while time.time() < deadline:
        time.sleep(10)
        q_req = urllib.request.Request(
            f"{BASE_URL}/v2/query/video_generation/{task_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        try:
            with urllib.request.urlopen(q_req) as q_resp:
                q_res = json.loads(q_resp.read().decode("utf-8"))
        except Exception as e:
            continue
        task = q_res.get("task") or {}
        status = str(task.get("status", "processing")).lower()
        est = task.get("estimated_remaining_seconds", 0)
        print(f"  Status: {status.upper()} (remaining ~{est}s)", flush=True)

        if status in ("succeeded", "completed"):
            video_url = (task.get("content") or {}).get("url")
            break
        elif status in ("failed", "error", "cancelled"):
            raise RuntimeError(f"Task failed: {task.get('error')}")

    if not video_url:
        raise TimeoutError("Timed out waiting for video completion.")

    print(f"Downloading to {output_path}...")
    with urllib.request.urlopen(urllib.request.Request(video_url)) as dl_resp:
        output_path.write_bytes(dl_resp.read())
    print(f"Downloaded: {output_path} ({output_path.stat().st_size} bytes)")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--anchors", default="extracted_anchors")
    parser.add_argument("--resolution", default="768P", choices=["768P", "2K", "512p"])
    parser.add_argument("--duration", type=int, default=15)
    args = parser.parse_args()

    token = get_token()
    anchor_dir = Path(args.anchors)
    hero = anchor_dir / "anchor_hero.jpg"
    exploded = anchor_dir / "anchor_exploded.jpg"
    assembled = anchor_dir / "anchor_assembled.jpg"

    u_hero = upload_image(hero, token)
    u_exploded = upload_image(exploded, token)
    u_assembled = upload_image(assembled, token)

    p1 = (
        "Part 1: Precision disassembly and exploded view of this miniature desktop Stirling engine. "
        "Use @1 as the initial assembled hero state, and @2 as the exploded component detail anchor. "
        "Camera smoothly pushes in towards the blue heatsink; precision bolts, flange, and piston glide outward "
        "along axial explosion paths in clean mechanical alignment. Brushed aluminum, cyan anodized fins, studio lighting."
    )
    p2 = (
        "Part 2: Precision reassembly and continuous dynamic operation of this miniature desktop Stirling engine. "
        "Use @1 as the initial exploded component state, and @2 as the completed assembled machine anchor. "
        "Separated parts fly back and lock firmly into the main chassis; screws tighten securely. "
        "Then the large flywheel begins smooth rhythmic continuous rotation driving the piston."
    )

    submit_and_poll(p1, [u_hero, u_exploded], args.duration, args.resolution, token, Path("shot1_explosion_15s.mp4"))
    submit_and_poll(p2, [u_exploded, u_assembled], args.duration, args.resolution, token, Path("shot2_assembly_15s.mp4"))

if __name__ == "__main__":
    main()
