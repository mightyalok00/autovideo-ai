# Configuration file for AI Long Video Automation (100% Free)

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
ASSETS_DIR = BASE_DIR / "assets"
MUSIC_DIR = ASSETS_DIR / "music"
TEMP_DIR = BASE_DIR / "temp"

# Ensure directories exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MUSIC_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# Video Dimensions
# 1920x1080 for standard YouTube long-form (16:9)
# 1080x1920 for YouTube Shorts / TikTok / Reels (9:16)
VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
THUMBNAIL_WIDTH = 1280
THUMBNAIL_HEIGHT = 720
VIDEO_FPS = 30

# Visual Settings
IMAGE_DURATION = 6.0  # seconds per scene if image
TRANSITION_DURATION = 1.0  # crossfade duration in seconds

# Free TTS Settings (Microsoft Edge Neural Voices)
# Popular high-quality English voices:
# - en-US-ChristopherNeural (Authoritative, documentary style)
# - en-US-GuyNeural (Casual, informative explainer)
# - en-US-JennyNeural (Warm, expressive narrative)
# - en-GB-RyanNeural (British documentary narrator)
# - en-US-AriaNeural (Clear news / storytelling)
DEFAULT_VOICE = "en-US-ChristopherNeural"
VOICE_RATE = "+0%"
VOICE_PITCH = "+0Hz"

# Free Visual Sources
# Pexels API: Free key from https://www.pexels.com/api/ (20,000 free requests/month)
# If empty, pipeline automatically falls back to Pollinations.ai (100% Free AI image generator, NO KEY NEEDED)
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")

# Free LLM Settings
# OpenRouter API key (get from https://openrouter.ai/workspaces/default/keys)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "nvidia/nemotron-3.5-lightning:free")

# Gemini free tier API key (get from https://aistudio.google.com/ for free)
# Groq free tier API key (get from https://console.groq.com/ for free)
# Ollama endpoint: http://localhost:11434/api/generate (completely local & free)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

# Background Music Settings
MUSIC_VOLUME = 0.12  # Background music volume relative to voiceover (ducked)
