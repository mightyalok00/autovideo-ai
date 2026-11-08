"""
Autonomous AI Video Director & Producer Agent - All-Niche Edition.
Full end-to-end production loop:
1. Niche & Directing Strategy Selection (All 10 Categories)
2. Script Generation with Retention Formulas
3. Self-Critique Quality Evaluation (Scores 1-10)
4. Cinematic Visual Prompt Tuning
5. Neural Voiceover & FFmpeg Assembly
6. High-CTR Thumbnail Creation
7. YouTube SEO Package (Titles, Descriptions, Chapters, Tags)
8. Persistent Memory Logging (agent_memory.json)
"""

import json
import os
import sys
import time
from pathlib import Path

# Ensure local directory is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from agent_brain import evaluate_script_retention, refine_visual_prompt  # type: ignore  # noqa: E402
from config import BASE_DIR, DEFAULT_VOICE, OUTPUT_DIR, TEMP_DIR  # type: ignore  # noqa: E402
from niche_engine import NICHES  # type: ignore  # noqa: E402
from script_generator import generate_script  # type: ignore  # noqa: E402
from seo_optimizer import generate_youtube_metadata  # type: ignore  # noqa: E402
from thumbnail_generator import create_youtube_thumbnail  # type: ignore  # noqa: E402
from video_assembler import (  # type: ignore  # noqa: E402
    add_background_music_and_subtitles,
    build_image_scene_clip,
    build_video_scene_clip,
    concatenate_clips,
)
from visuals_fetcher import fetch_visual_for_scene  # type: ignore  # noqa: E402
from voiceover import generate_voice  # type: ignore  # noqa: E402

MEMORY_FILE = BASE_DIR / "agent_memory.json"


def load_memory() -> dict:
    if MEMORY_FILE.exists():
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):  # noqa: S110, BLE001
            pass
    return {"total_videos_created": 0, "history": []}


def save_memory(entry: dict):
    mem = load_memory()
    mem["total_videos_created"] += 1
    mem["history"].append(entry)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(mem, f, indent=2)


def run_agent(
    topic: str, duration_minutes: int = 5, niche_id: str = "history", custom_script: str | None = None
) -> dict:
    start_time = time.time()
    niche = NICHES.get(niche_id, NICHES["history"])
    slug = "".join([c if c.isalnum() else "_" for c in topic[:30].strip().lower()])
    run_temp = TEMP_DIR / slug
    run_temp.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 70)
    print("🤖 ALL-NICHE AUTONOMOUS AI VIDEO AGENT ENGAGED")
    print(f"🎯 Mission: Full-Length Video Production for '{topic}'")
    print(f"📁 Niche Category: {niche['icon']} {niche['name']}")
    print(f"⏱️  Target Length: {duration_minutes} minutes")
    print("=" * 70 + "\n")

    # STAGE 1: SCRIPTWRITING
    print(f">>> [STAGE 1/6] Scriptwriting for {niche['name']}...")
    script_data = generate_script(topic=topic, duration_minutes=duration_minutes, script_file=custom_script)
    scenes = script_data.get("scenes", [])
    print(f"Drafted {len(scenes)} scenes.")

    # STAGE 2: SELF-CRITIQUE & RETENTION AUDIT
    print("\n>>> [STAGE 2/6] Running Self-Critique & Retention Score Audit...")
    audit = evaluate_script_retention(script_data)
    print(f"📊 Quality Score: {audit['overall_score']}/10")
    print(f"   - Hook Score: {audit['hook_score']}/10")
    print(f"   - Pacing Score: {audit['pacing_score']}/10")
    print(f"   - Visual Richness: {audit['visual_score']}/10")

    # STAGE 3: PROMPT REFINEMENT WITH NICHE CINEMATOGRAPHY
    print(f"\n>>> [STAGE 3/6] Applying {niche['name']} Cinematography & Camera Lenses...")
    for s in scenes:
        raw_v = s.get("visual_prompt", "")
        s["visual_prompt"] = refine_visual_prompt(raw_v, niche["visual_style"])

    # STAGE 4: PRODUCTION (VOICEOVER & VISUALS)
    print("\n>>> [STAGE 4/6] Rendering Neural Voiceover & Assembling Scenes...")
    scene_clips = []
    durations = []
    voice = niche.get("voice", DEFAULT_VOICE)

    for idx, scene in enumerate(scenes, 1):
        scene_id = scene.get("scene_id", idx)
        narration = scene.get("narration", "")
        audio_path = run_temp / f"audio_{scene_id:03d}.mp3"

        # Audio
        dur = generate_voice(narration, str(audio_path), voice=voice)
        durations.append(dur)

        # Visual
        visual_info = fetch_visual_for_scene(scene, run_temp)

        # Scene Clip
        clip_path = run_temp / f"clip_{scene_id:03d}.mp4"
        if visual_info["type"] == "video":
            build_video_scene_clip(visual_info["path"], str(audio_path), str(clip_path), dur)
        else:
            build_image_scene_clip(visual_info["path"], str(audio_path), str(clip_path), dur)

        if os.path.exists(clip_path):
            scene_clips.append(str(clip_path))

    # STAGE 5: CONCAT & FINAL MASTER
    print("\n>>> [STAGE 5/6] Finalizing Master Video...")
    concat_temp = run_temp / "raw_concat.mp4"
    concatenate_clips(scene_clips, str(concat_temp), run_temp)

    final_video_path = OUTPUT_DIR / f"{slug}_master.mp4"
    bg_music = BASE_DIR / "assets" / "music" / "cinematic_ambient.mp3"
    music_arg = str(bg_music) if bg_music.exists() else None
    add_background_music_and_subtitles(str(concat_temp), str(final_video_path), bg_music_path=music_arg)

    # STAGE 6: PACKAGING (THUMBNAIL & YOUTUBE SEO)
    print("\n>>> [STAGE 6/6] Generating High-CTR Thumbnail & YouTube Metadata Package...")
    thumbnail_path = OUTPUT_DIR / f"{slug}_thumbnail.jpg"
    create_youtube_thumbnail(topic, str(thumbnail_path))

    seo_package = generate_youtube_metadata(topic, scenes, durations)
    metadata_path = OUTPUT_DIR / f"{slug}_youtube_package.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(seo_package, f, indent=2)

    total_duration = sum(durations)
    elapsed = time.time() - start_time

    # Save to agent memory
    memory_entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "topic": topic,
        "niche": niche["name"],
        "duration_seconds": total_duration,
        "quality_score": audit["overall_score"],
        "video_path": str(final_video_path),
        "thumbnail_path": str(thumbnail_path),
    }
    save_memory(memory_entry)

    print("\n" + "=" * 70)
    print("🏆 ALL-NICHE AGENT PRODUCTION COMPLETE!")
    print(f"🎬 Master Video: {final_video_path}")
    print(f"🖼️  Thumbnail:    {thumbnail_path}")
    print(f"📜 SEO Package:  {metadata_path}")
    print(f"⏱️  Duration:     {total_duration / 60:.2f} mins")
    print(f"⭐ Audit Score:  {audit['overall_score']}/10")
    print(f"⚡ Render Time:  {elapsed:.1f}s")
    print("=" * 70 + "\n")

    return {
        "video_path": str(final_video_path),
        "thumbnail_path": str(thumbnail_path),
        "seo_package": seo_package,
        "audit": audit,
    }


if __name__ == "__main__":
    import sys

    topic = sys.argv[1] if len(sys.argv) > 1 else "The Untold Secrets of the Deep Cosmos"
    niche = sys.argv[2] if len(sys.argv) > 2 else "space"
    run_agent(topic=topic, duration_minutes=2, niche_id=niche)
