"""
Visuals Fetcher & Generator Module for 100% Free AI Video Production.
Sources:
1. Pollinations.ai (100% Free AI Image Generation with Flux / SDXL, No API key needed).
2. Pexels Free Stock Videos & Photos (Optional API Key).
3. Offline Procedural Canvas Generator (Works 100% offline).
"""

import json
import os
import socket
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import PEXELS_API_KEY, VIDEO_HEIGHT, VIDEO_WIDTH  # type: ignore  # noqa: E402


def is_online() -> bool:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        s.connect(("1.1.1.1", 53))
        s.close()
        return True
    except OSError:
        return False


def download_pollinations_image(
    prompt: str, output_path: str, width: int = VIDEO_WIDTH, height: int = VIDEO_HEIGHT
) -> bool:
    """Download 100% free AI-generated image from Pollinations.ai (Flux/SDXL)."""
    if not is_online():
        return False
    try:
        clean_prompt = prompt.strip().replace("\n", " ")
        encoded_prompt = urllib.parse.quote(clean_prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&seed={abs(hash(prompt)) % 100000}"

        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=20) as resp, open(output_path, "wb") as f:
            f.write(resp.read())

        return os.path.exists(output_path) and os.path.getsize(output_path) > 1024
    except Exception as e:  # noqa: BLE001
        print(f"Pollinations fetch notice: {e}")
        return False


def download_pexels_video(query: str, output_path: str) -> bool:
    """Download free HD stock video from Pexels API."""
    if not PEXELS_API_KEY or not is_online():
        return False

    try:
        encoded_query = urllib.parse.quote(query)
        url = f"https://api.pexels.com/videos/search?query={encoded_query}&per_page=5&orientation=landscape"

        req = urllib.request.Request(url, headers={"Authorization": PEXELS_API_KEY})
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        videos = data.get("videos", [])
        if not videos:
            return False

        video_files = videos[0].get("video_files", [])
        selected_file = None
        for vf in video_files:
            if vf.get("width") == 1920 or vf.get("quality") == "hd":
                selected_file = vf.get("link")
                break
        if not selected_file and video_files:
            selected_file = video_files[0].get("link")

        if selected_file:
            req_dl = urllib.request.Request(selected_file, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req_dl, timeout=20) as v_resp, open(output_path, "wb") as vf:
                vf.write(v_resp.read())
            return True
    except Exception as e:  # noqa: BLE001
        print(f"Pexels fetch notice: {e}")
    return False


def generate_offline_backdrop(
    title: str, scene_num: int, output_path: str, width: int = VIDEO_WIDTH, height: int = VIDEO_HEIGHT
):
    """Generate high-res procedural cinematic backdrop using Pillow or FFmpeg (100% Offline)."""
    try:
        from PIL import Image, ImageDraw

        img = Image.new("RGB", (width, height), color=(15, 23, 42))
        draw = ImageDraw.Draw(img)

        for i in range(height):
            r = int(15 + (i / height) * 20)
            g = int(23 + (i / height) * 25)
            b = int(42 + (i / height) * 45)
            draw.line([(0, i), (width, i)], fill=(r, g, b))

        draw.rectangle([40, 40, width - 40, height - 40], outline=(56, 189, 248, 120), width=3)
        draw.text((100, height - 200), f"SCENE {scene_num}", fill=(241, 245, 249))
        draw.text((100, height - 150), title[:60], fill=(148, 163, 184))
        img.save(output_path, quality=95)
        return True
    except Exception:  # noqa: BLE001
        import subprocess

        subprocess.run(
            ["ffmpeg", "-y", "-f", "lavfi", "-i", f"color=c=#0f172a:s={width}x{height}", "-vframes", "1", output_path],
            check=False,
            capture_output=True,
        )
        return True


def download_wikipedia_image(query: str, output_path: str) -> bool:
    """Download 100% free authentic archival high-res photo from Wikipedia / Wikimedia."""
    if not is_online():
        return False
    try:
        # Extract meaningful subject words (last 2-3 content words usually define the scene)
        stop_words = {"the", "and", "for", "with", "story", "origin", "untold", "about", "scene", "shot", "cinematic"}
        meaningful = [w for w in query.replace(",", " ").split() if len(w) > 2 and w.lower() not in stop_words]

        # Try key phrases: last 2 words first, then first 2 words
        candidates = []
        if len(meaningful) >= 2:
            candidates.append(" ".join(meaningful[-2:]))
        if len(meaningful) >= 1:
            candidates.append(" ".join(meaningful[:2]))

        for term in candidates:
            encoded = urllib.parse.quote(term.strip())
            url = f"https://en.wikipedia.org/w/api.php?action=query&generator=search&gsrsearch={encoded}&gsrlimit=3&prop=pageimages&pithumbsize=1280&format=json"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            pages = data.get("query", {}).get("pages", {})
            for _, page in pages.items():
                thumb_url = page.get("thumbnail", {}).get("source")
                if thumb_url and (thumb_url.endswith(".jpg") or thumb_url.endswith(".png") or thumb_url.endswith(".jpeg")):
                    req_img = urllib.request.Request(thumb_url, headers={"User-Agent": "Mozilla/5.0"})
                    with urllib.request.urlopen(req_img, timeout=12) as img_resp, open(output_path, "wb") as f:
                        f.write(img_resp.read())
                    if os.path.exists(output_path) and os.path.getsize(output_path) > 3000:
                        return True
    except Exception as e:  # noqa: BLE001
        print(f"Wikimedia search notice: {e}")
    return False


def fetch_visual_for_scene(scene: dict, output_dir: Path) -> dict:
    """Fetch or generate visual asset (video clip or high-res image) for a scene."""
    scene_id = scene.get("scene_id", 1)
    prompt = scene.get("visual_prompt", "")
    query = scene.get("search_query", "cinematic landscape")

    video_path = output_dir / f"scene_{scene_id:03d}.mp4"
    image_path = output_dir / f"scene_{scene_id:03d}.jpg"

    if PEXELS_API_KEY:
        print(f"Scene {scene_id}: Searching Pexels for stock video: '{query}'...")
        if download_pexels_video(query, str(video_path)):
            return {"type": "video", "path": str(video_path)}

    print(f"Scene {scene_id}: Generating AI visual from prompt...")
    if download_pollinations_image(prompt, str(image_path)):
        return {"type": "image", "path": str(image_path)}

    print(f"Scene {scene_id}: Fetching authentic archival imagery for '{query}'...")
    if download_wikipedia_image(query, str(image_path)):
        return {"type": "image", "path": str(image_path)}

    print(f"Scene {scene_id}: Creating cinematic backdrop...")
    generate_offline_backdrop(prompt, scene_id, str(image_path))
    return {"type": "image", "path": str(image_path)}
