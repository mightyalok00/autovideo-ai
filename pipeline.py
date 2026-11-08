"""
Master Orchestration Pipeline for 100% Free AI Long Video Generation.
Run via:
    python pipeline.py --topic "The History of Artificial Intelligence" --duration 10
"""

import argparse
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import (  # type: ignore  # noqa: E402
    DEFAULT_VOICE,
    MUSIC_DIR,
    OUTPUT_DIR,
    TEMP_DIR,
)
from script_generator import generate_script  # type: ignore  # noqa: E402
from video_assembler import (  # type: ignore  # noqa: E402
    add_background_music_and_subtitles,
    build_image_scene_clip,
    build_video_scene_clip,
    concatenate_clips,
)
from visuals_fetcher import fetch_visual_for_scene  # type: ignore  # noqa: E402
from voiceover import generate_voice  # type: ignore  # noqa: E402


def run_pipeline(
    topic: str,
    duration_minutes: int = 5,
    script_file: str | None = None,
    voice: str = DEFAULT_VOICE,
    output_filename: str | None = None,
    burn_subs: bool = False,
) -> str:
    start_time = time.time()
    slug = "".join([c if c.isalnum() else "_" for c in topic[:30].strip().lower()])
    run_temp = TEMP_DIR / slug
    run_temp.mkdir(parents=True, exist_ok=True)

    if not output_filename:
        output_filename = f"{slug}_full_video.mp4"
    final_output = OUTPUT_DIR / output_filename

    print("\n" + "=" * 60)
    print("🎬 STARTING AI LONG VIDEO AUTOMATION")
    print(f"📌 Topic: {topic}")
    print(f"⏱️  Target Duration: {duration_minutes} minutes")
    print(f"🎙️  Voice: {voice}")
    print(f"📁 Output: {final_output}")
    print("=" * 60 + "\n")

    # 1. Generate or load script
    print(">>> STEP 1: Generating Comprehensive Long Script...")
    script_data = generate_script(topic=topic, duration_minutes=duration_minutes, script_file=script_file)
    scenes = script_data.get("scenes", [])
    if not scenes:
        raise ValueError("No scenes found in script!")
    print(f"✅ Generated {len(scenes)} scenes for '{script_data.get('title', topic)}'.\n")

    # Save script to temp
    import json

    with open(run_temp / "script.json", "w", encoding="utf-8") as f:
        json.dump(script_data, f, indent=2)

    scene_clips = []
    total_audio_duration = 0.0

    # Process each scene
    for idx, scene in enumerate(scenes, 1):
        scene_id = scene.get("scene_id", idx)
        narration = scene.get("narration", "")
        print(f"\n--- [Scene {scene_id}/{len(scenes)}] ---")
        print(f'Voiceover: "{narration[:80]}..."')

        # 2. Generate Voiceover
        audio_path = run_temp / f"audio_{scene_id:03d}.mp3"
        sub_path = run_temp / f"sub_{scene_id:03d}.srt"
        print("Generating voiceover audio...")
        dur = generate_voice(narration, str(audio_path), str(sub_path), voice=voice)
        total_audio_duration += dur
        print(f"Audio ready: {dur:.2f} seconds.")

        # 3. Fetch/Generate Visual
        visual_info = fetch_visual_for_scene(scene, run_temp)

        # 4. Render Scene Clip
        clip_path = run_temp / f"clip_{scene_id:03d}.mp4"
        print("Rendering synchronized video clip...")
        if visual_info["type"] == "video":
            build_video_scene_clip(visual_info["path"], str(audio_path), str(clip_path), dur)
        else:
            build_image_scene_clip(visual_info["path"], str(audio_path), str(clip_path), dur)

        if os.path.exists(clip_path):
            scene_clips.append(str(clip_path))
            print(f"Clip {scene_id} rendered successfully.")
        else:
            print(f"⚠️ Warning: Clip {scene_id} failed to render.")

    if not scene_clips:
        raise RuntimeError("No scene clips were generated!")

    # 5. Concatenate all scenes into master video
    print("\n>>> STEP 5: Stitching all scene clips together...")
    concat_temp = run_temp / "concatenated_raw.mp4"
    concatenate_clips(scene_clips, str(concat_temp), run_temp)
    print(f"✅ Concat completed: {len(scene_clips)} clips merged.")

    # 6. Add background music and optional subtitles
    print("\n>>> STEP 6: Finalizing Audio Mix & Mastering...")
    # Find background music if available
    bg_music = None
    music_files = list(MUSIC_DIR.glob("*.mp3")) + list(MUSIC_DIR.glob("*.wav"))
    if music_files:
        bg_music = str(music_files[0])
        print(f"Using background music track: {music_files[0].name}")
    else:
        print("No background music track placed in assets/music (skipping BGM ducking).")

    add_background_music_and_subtitles(str(concat_temp), str(final_output), bg_music_path=bg_music, subtitle_path=None)

    elapsed = time.time() - start_time
    file_size_mb = os.path.getsize(final_output) / (1024 * 1024) if os.path.exists(final_output) else 0

    print("\n" + "=" * 60)
    print("🎉 VIDEO GENERATION COMPLETE!")
    print(f"📹 Output File: {final_output}")
    print(f"⏱️  Total Duration: {total_audio_duration / 60:.2f} minutes ({total_audio_duration:.1f}s)")
    print(f"💾 File Size: {file_size_mb:.2f} MB")
    print(f"⚡ Processing Time: {elapsed:.1f} seconds")
    print("=" * 60 + "\n")

    return str(final_output)


def main():
    parser = argparse.ArgumentParser(description="100% Free AI Long Video Generator")
    parser.add_argument("--topic", type=str, default="The Mystery of Deep Sea Creatures", help="Video topic or theme")
    parser.add_argument("--duration", type=int, default=3, help="Approximate duration in minutes (e.g. 5, 10, 15)")
    parser.add_argument("--script", type=str, default=None, help="Path to custom text/markdown script file")
    parser.add_argument("--voice", type=str, default=DEFAULT_VOICE, help="Voice name (e.g. en-US-ChristopherNeural)")
    parser.add_argument("--output", type=str, default=None, help="Output MP4 filename")

    args = parser.parse_args()
    run_pipeline(
        topic=args.topic,
        duration_minutes=args.duration,
        script_file=args.script,
        voice=args.voice,
        output_filename=args.output,
    )


if __name__ == "__main__":
    main()
