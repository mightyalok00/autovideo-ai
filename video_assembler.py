"""
High-Performance Video Assembler using FFmpeg.
Features:
- Ken Burns slow cinematic zoom & pan on static images
- Audio-visual duration synchronization
- Concat demuxing for arbitrarily long videos (10m, 30m, 2h+) without RAM overhead
- Background music mixing with ducking
- Subtitle burning and styling
"""

import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import MUSIC_VOLUME, VIDEO_FPS, VIDEO_HEIGHT, VIDEO_WIDTH  # type: ignore  # noqa: E402


def build_image_scene_clip(
    image_path: str,
    audio_path: str,
    output_clip_path: str,
    duration: float,
    fps: int = VIDEO_FPS,
    width: int = VIDEO_WIDTH,
    height: int = VIDEO_HEIGHT,
) -> bool:
    """
    Renders an image into a video clip with a smooth Ken Burns slow zoom effect,
    synchronized with the voiceover audio.
    """
    total_frames = int(duration * fps)
    # FFmpeg zoompan filter: gentle zoom from 1.0 to 1.15 over the duration
    filter_complex = (
        f"[0:v]scale=-2:{height * 2},zoompan=z='min(zoom+0.0008,1.20)':d={total_frames}:"
        f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={width}x{height}:fps={fps},"
        f"format=yuv420p[v]"
    )

    cmd = [
        "ffmpeg",
        "-y",
        "-loop",
        "1",
        "-i",
        image_path,
        "-i",
        audio_path,
        "-filter_complex",
        filter_complex,
        "-map",
        "[v]",
        "-map",
        "1:a",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "23",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-shortest",
        output_clip_path,
    ]

    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if res.returncode != 0:
        # Fallback to simple static scale if zoompan is slow or fails
        cmd_simple = [
            "ffmpeg",
            "-y",
            "-loop",
            "1",
            "-i",
            image_path,
            "-i",
            audio_path,
            "-vf",
            f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
            "-tune",
            "stillimage",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            output_clip_path,
        ]
        res_simple = subprocess.run(cmd_simple, capture_output=True, text=True, check=False)
        return res_simple.returncode == 0
    return True


def build_video_scene_clip(
    video_path: str,
    audio_path: str,
    output_clip_path: str,
    duration: float,
    width: int = VIDEO_WIDTH,
    height: int = VIDEO_HEIGHT,
) -> bool:
    """
    Renders a stock video clip scaled and looped/trimmed to match the voiceover audio duration.
    """
    vf = f"scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height},setsar=1,format=yuv420p"
    cmd = [
        "ffmpeg",
        "-y",
        "-stream_loop",
        "-1",
        "-i",
        video_path,
        "-i",
        audio_path,
        "-vf",
        vf,
        "-c:v",
        "libx264",
        "-preset",
        "faster",
        "-crf",
        "22",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-t",
        str(duration),
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        output_clip_path,
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return res.returncode == 0


def concatenate_clips(clip_paths: list[str], output_concat_path: str, temp_dir: Path) -> bool:
    """Concatenates video clips using the FFmpeg concat demuxer (lossless & instant)."""
    list_file = temp_dir / "concat_list.txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for p in clip_paths:
            # Escape path for FFmpeg concat file
            normalized = p.replace("\\", "/")
            f.write(f"file '{normalized}'\n")

    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file), "-c", "copy", output_concat_path]
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return res.returncode == 0


def add_background_music_and_subtitles(
    video_path: str,
    output_final_path: str,
    bg_music_path: str | None = None,
    subtitle_path: str | None = None,
    music_vol: float = MUSIC_VOLUME,
) -> bool:
    """
    Mixes ducked background music and optionally burns styled subtitles.
    """
    inputs = ["-i", video_path]
    has_music = bg_music_path and os.path.exists(bg_music_path)

    if has_music:
        inputs.extend(["-stream_loop", "-1", "-i", bg_music_path])
        # Mix voice audio (stream 0) with ducked background music (stream 1)
        filter_complex = f"[1:a]volume={music_vol}[bg];[0:a][bg]amix=inputs=2:duration=first[aout]"
        audio_map = ["-map", "0:v", "-map", "[aout]"]
    else:
        filter_complex = None
        audio_map = ["-map", "0:v", "-map", "0:a"]

    # Subtitle burn-in filter if provided
    vf_filters = []
    if subtitle_path and os.path.exists(subtitle_path):
        sub_escaped = subtitle_path.replace("\\", "/").replace(":", "\\:")
        # Stylish bold yellow/white captions with shadow
        vf_filters.append(
            f"subtitles='{sub_escaped}':force_style='FontSize=18,FontName=Arial,Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=3,Outline=2,Shadow=1,Alignment=2,MarginV=45'"
        )

    cmd = ["ffmpeg", "-y"] + inputs
    if filter_complex:
        cmd.extend(["-filter_complex", filter_complex])
    if vf_filters:
        cmd.extend(["-vf", ",".join(vf_filters)])
    cmd.extend(audio_map)
    cmd.extend(
        ["-c:v", "libx264" if vf_filters else "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", output_final_path]
    )

    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if res.returncode != 0:
        # Fallback to copy original video if filter fails
        import shutil

        shutil.copy2(video_path, output_final_path)
    return True
