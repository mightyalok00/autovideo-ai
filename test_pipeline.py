import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from video_assembler import build_image_scene_clip  # type: ignore  # noqa: E402
from visuals_fetcher import generate_offline_backdrop  # type: ignore  # noqa: E402
from voiceover import generate_voice  # type: ignore  # noqa: E402


def test():
    test_dir = Path("temp/test_run")
    test_dir.mkdir(parents=True, exist_ok=True)
    audio_file = str(test_dir / "test_audio.mp3")
    img_file = str(test_dir / "test_img.jpg")
    clip_file = str(test_dir / "test_clip.mp4")

    print("[1/3] Testing voice generation...")
    dur = generate_voice("Welcome to this automated long documentary demonstration.", audio_file)
    print(f"--> Audio generated: {dur:.2f}s")

    print("[2/3] Testing visual backdrop generator...")
    generate_offline_backdrop("AI Video Automation", 1, img_file)
    print(f"--> Image generated: {os.path.exists(img_file)}")

    print("[3/3] Testing video assembler with FFmpeg...")
    success = build_image_scene_clip(img_file, audio_file, clip_file, dur)
    print(f"--> Clip rendered successfully: {success}")
    if os.path.exists(clip_file):
        print(f"--> Clip file size: {os.path.getsize(clip_file) / 1024:.1f} KB")


if __name__ == "__main__":
    test()
