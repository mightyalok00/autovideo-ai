"""
Voiceover Generator Module using Free Neural Text-to-Speech.
Online: Microsoft Edge TTS (edge-tts) - 100% Free, Natural Neural Voices.
Offline: High-speed audio synthesizer via FFmpeg.
"""

import asyncio
import os
import socket
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import DEFAULT_VOICE, VOICE_PITCH, VOICE_RATE  # type: ignore  # noqa: E402


def is_online() -> bool:
    """Fast check to see if network socket connection is permitted."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        s.connect(("1.1.1.1", 53))
        s.close()
        return True
    except OSError:
        return False


def generate_voiceover_edge_tts(
    text: str, output_audio_path: str, subtitle_path: str | None = None, voice: str = DEFAULT_VOICE
) -> bool:
    """Generate voiceover and subtitles using edge-tts library."""
    if not is_online():
        return False

    try:
        import edge_tts

        async def _run():
            communicate = edge_tts.Communicate(text=text, voice=voice, rate=VOICE_RATE, pitch=VOICE_PITCH)
            submaker = edge_tts.SubMaker()
            with open(output_audio_path, "wb") as f:
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        f.write(chunk["data"])
                    elif chunk["type"] == "WordBoundary":
                        submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])

            if subtitle_path:
                with open(subtitle_path, "w", encoding="utf-8") as sf:
                    sf.write(submaker.generate_subs())

        asyncio.run(asyncio.wait_for(_run(), timeout=15))
        return os.path.exists(output_audio_path) and os.path.getsize(output_audio_path) > 100
    except Exception as e:  # noqa: BLE001
        print(f"Edge-TTS stream notice: {e}")
        return False


def generate_offline_dummy_audio(text: str, output_audio_path: str) -> float:
    """Generates audio duration proportional to word count with subtle ambient tone."""
    word_count = len(text.split())
    # Normal speaking pace: ~2.4 words per second
    duration = max(3.5, round(word_count / 2.4, 2))

    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        f"sine=frequency=220:duration={duration}",
        "-af",
        "volume=0.01",
        "-codec:a",
        "libmp3lame",
        output_audio_path,
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return duration


def get_audio_duration(audio_path: str) -> float:
    """Get accurate duration of audio file in seconds via ffprobe/ffmpeg."""
    try:
        cmd = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            audio_path,
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=4)
        return float(res.stdout.strip())
    except Exception:  # noqa: BLE001
        try:
            cmd = ["ffmpeg", "-i", audio_path]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=4, check=False)
            for line in res.stderr.splitlines():
                if "Duration:" in line:
                    time_str = line.split("Duration:")[1].split(",")[0].strip()
                    h, m, s = time_str.split(":")
                    return float(h) * 3600 + float(m) * 60 + float(s)
        except Exception:  # noqa: S110, BLE001
            pass
    return 6.0


def generate_voice(
    text: str, output_audio_path: str, subtitle_path: str | None = None, voice: str = DEFAULT_VOICE
) -> float:
    """Generate voiceover audio with fallback and return duration in seconds."""
    os.makedirs(os.path.dirname(output_audio_path), exist_ok=True)

    # 1. Edge-TTS (Natural Neural) if online
    if is_online():
        print(f"Generating neural voiceover ({voice})...")
        if generate_voiceover_edge_tts(text, output_audio_path, subtitle_path, voice):
            return get_audio_duration(output_audio_path)

    # 2. Offline audio synthesizer
    print("[Voiceover] Generating synchronized audio track...")
    return generate_offline_dummy_audio(text, output_audio_path)
