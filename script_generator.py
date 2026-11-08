"""
Script Generator Module for AI Long Video Automation.
Supports Google Gemini (Free), Groq (Free), Ollama (Local Free),
or custom text/markdown script files.
"""

import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import (  # type: ignore  # noqa: E402
    GEMINI_API_KEY,
    GROQ_API_KEY,
    OLLAMA_URL,
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL,
)

SYSTEM_PROMPT = """You are an expert documentary scriptwriter and YouTube video director.
Your job is to generate a comprehensive, highly engaging long-form video script for YouTube.
Break down the topic into cohesive scenes. Each scene should have:
1. "narration": 2 to 4 engaging, natural narrative sentences suitable for voiceover.
2. "visual_prompt": A descriptive cinematic prompt for generating high quality 16:9 4k imagery.
3. "search_query": 2 to 4 keywords to search for relevant stock footage.

CRITICAL: Return ONLY valid JSON in the following exact format without any markdown code block fences or commentary:
{
  "title": "Title of the Video",
  "scenes": [
    {
      "scene_id": 1,
      "narration": "Narration text here...",
      "visual_prompt": "Cinematic visual description, dramatic lighting, 8k...",
      "search_query": "relevant keywords"
    }
  ]
}
"""


def generate_with_gemini(topic: str, num_scenes: int) -> dict:
    """Generate script using Google Gemini API (Free tier)."""
    api_key = GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found.")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    prompt = f"Write a deep-dive long video script about '{topic}' with approximately {num_scenes} scenes.\n{SYSTEM_PROMPT}"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "response_mime_type": "application/json",
        },
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(text)


def generate_with_groq(topic: str, num_scenes: int) -> dict:
    """Generate script using Groq Free Tier API."""
    api_key = GROQ_API_KEY or os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found.")

    url = "https://api.groq.com/openai/v1/chat/completions"
    prompt = f"Write a long video script about '{topic}' with {num_scenes} scenes."

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
        "response_format": {"type": "json_object"},
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        text = data["choices"][0]["message"]["content"]
        return json.loads(text)


def get_available_ollama_model() -> str | None:
    """Detect available local Ollama models."""
    try:
        req = urllib.request.Request(f"{OLLAMA_URL}/api/tags")
        with urllib.request.urlopen(req, timeout=1.5) as r:
            data = json.loads(r.read().decode("utf-8"))
            names = [m["name"] for m in data.get("models", [])]
            for p in ["llama3.2:latest", "llama3.2:3b", "qwen2.5:3b", "mistral:7b", "deepseek-r1:7b"]:
                if p in names:
                    return p
            return names[0] if names else None
    except Exception:  # noqa: BLE001
        return None


def generate_with_ollama(topic: str, num_scenes: int, model: str | None = None) -> dict:
    """Generate script using local Ollama instance (100% offline & free)."""
    selected_model = model or get_available_ollama_model() or "llama3.2:latest"
    print(f"Generating {num_scenes}-scene script using local Ollama ({selected_model})...")
    url = f"{OLLAMA_URL}/api/generate"
    prompt = f"""You are a master YouTube documentary director.
Write a script about '{topic}'. It MUST contain {num_scenes} scenes in the scenes list.
Example format:
{{
  "title": "The Secrets of {topic}",
  "scenes": [
    {{"scene_id": 1, "narration": "Gripping spoken intro (35 words).", "visual_prompt": "Cinematic 8k photorealistic portrait, dramatic lighting", "stock_query": "dramatic portrait"}},
    {{"scene_id": 2, "narration": "Deep revelation of the mystery (35 words).", "visual_prompt": "Ancient library in shadows, golden light", "stock_query": "ancient library"}}
  ]
}}
Ensure exactly {num_scenes} scenes are included. Output ONLY raw JSON matching this format."""

    payload = {
        "model": selected_model,
        "prompt": prompt,
        "stream": False,
        "format": "json",
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        res = json.loads(data["response"])
        if "scenes" in res and len(res["scenes"]) > 0:
            return res
    raise ValueError("Ollama returned invalid scene list.")


def parse_custom_script(file_path: str) -> dict:
    """Parse user provided text or markdown script into structured scenes."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    # Check if already json
    if content.startswith("{"):
        try:
            return json.loads(content)
        except Exception:
            pass

    # Split paragraphs into scenes
    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
    scenes = []
    for idx, p in enumerate(paragraphs, 1):
        words = re.findall(r"\w+", p)
        keywords = " ".join(words[:4]) if words else "cinematic background"
        scenes.append(
            {
                "scene_id": idx,
                "narration": p,
                "visual_prompt": f"Cinematic documentary shot, {p[:120]}, dramatic lighting, 8k, photorealistic",
                "search_query": keywords,
            }
        )

    return {"title": "Custom Script Video", "scenes": scenes}


def get_demo_script(topic: str, num_scenes: int = 6, niche_id: str = "history") -> dict:
    """
    Intelligent Procedural Niche Story Engine.
    Generates rich, authentic, high-retention multi-scene documentaries
    customized specifically to the topic and niche without relying on unstable external APIs.
    """
    clean_topic = topic.strip().title()
    t_lower = topic.lower()

    # Detect niche from keywords if default
    detected_niche = niche_id
    if any(k in t_lower for k in ["stoic", "psychology", "mind", "manipulat", "dark", "ego", "aurelius", "seneca"]):
        detected_niche = "stoicism"
    elif any(k in t_lower for k in ["space", "cosmos", "universe", "black hole", "galaxy", "nasa", "planet"]):
        detected_niche = "space"
    elif any(k in t_lower for k in ["crime", "murder", "killer", "investigation", "mystery", "fbi", "heist"]):
        detected_niche = "crime"
    elif any(k in t_lower for k in ["money", "billionaire", "market", "economy", "rich", "crash", "wealth"]):
        detected_niche = "finance"
    elif any(k in t_lower for k in ["ai", "robot", "tech", "quantum", "silicon", "algorithm", "future"]):
        detected_niche = "ai"
    elif any(k in t_lower for k in ["war", "empire", "ancient", "rome", "century", "battle", "conquer"]):
        detected_niche = "history"

    narratives = {
        "stoicism": [
            (
                f"We think we understand human resilience—until we look into the shadows of {clean_topic}. Beneath the surface of calm endurance lies a far more unsettling psychological truth.",
                "Ancient Roman bust in dim flickering torchlight, shadowy marble columns, dramatic chiaroscuro lighting, photorealistic 8k, cinematic color grade",
                "ancient philosophy marble sculpture",
            ),
            (
                "Centuries ago, ancient thinkers realized that controlling one's perception wasn't merely a virtue—it was an ultimate weapon of influence. In the crucible of power, emotions became fatal vulnerabilities.",
                "Ancient scroll on weathered wooden desk, feather quill, dramatic candle flame casting long shadows, atmospheric smoke, hyperrealistic",
                "ancient scroll quill candlelight",
            ),
            (
                "This is where psychology takes a darker turn. The very techniques designed for supreme inner tranquility can be inverted—weaponized to read, predict, and disarm human behavior without uttering a sound.",
                "Silhouette of a solitary figure standing in a grand stone archway, fog drifting across the floor, moody atmospheric volumetric light, 8k",
                "shadowy silhouette contemplation hallway",
            ),
            (
                f"Look closely at those who mastered {clean_topic}. They did not suppress their inner chaos; they studied it, mapped it, and used it as armor against an unpredictable world.",
                "Dramatic close-up of sculpted marble eyes, subtle rain droplets, intense emotional stoicism, high contrast cinematic photography",
                "stoic statue face close up dramatic",
            ),
            (
                "Today, the battleground has shifted from ancient empires into our everyday modern psyche. In a world drowning in constant noise, the quietest mind holds the greatest leverage.",
                "Modern city skyline at dusk, reflections on wet glass, lone figure observing the glowing horizon, cinematic anamorphic lens, 8k",
                "modern city reflection dusk loner",
            ),
            (
                f"The ultimate revelation of {clean_topic} is simple yet profound: whoever controls your emotions controls your reality. True mastery begins when you reclaim that power.",
                "A solitary figure walking into a blinding golden dawn, ancient and modern architecture blending seamlessly, inspirational cinematic wide shot",
                "sunrise horizon triumphant dawn",
            ),
        ],
        "space": [
            (
                f"In the frozen silence of the cosmos, {clean_topic} presents an enigma that defies our fundamental laws of physics. What astronomers discovered out there changes everything.",
                "Deep cosmic void, glowing James Webb deep space nebula, swirling violet and gold stardust, event horizon, ultra-detailed 8k render",
                "deep space nebula cosmic stars",
            ),
            (
                "Millions of light-years away, incomprehensible gravitational forces twist spacetime into impossible geometries. The instruments whispered anomalies that scientists could not initially explain.",
                "Radio telescope array pointing into a starry night sky, Milky Way blazing above in vibrant colors, long exposure photography, 8k",
                "radio telescope night sky milky way",
            ),
            (
                f"As humanity peered deeper into the darkness, the true scale of {clean_topic} revealed a chilling realization: we are only scratching the surface of cosmic reality.",
                "A colossal black hole warping light around its glowing accretion disk, cosmic dust streams, cinematic Unreal Engine 5 space render",
                "black hole accretion disk interstellar",
            ),
            (
                "Every calculation pointed to an extraordinary conclusion. What happens when matter is pushed beyond the limits of known physical reality?",
                "Distant alien exoplanet horizon, glowing twin moons, strange crystalline terrain, cosmic dawn, cinematic sci-fi landscape",
                "alien planet surface dual moons",
            ),
            (
                f"The universe does not reveal its secrets easily. For every question {clean_topic} answers, an even deeper cosmic abyss opens before us.",
                "Astronaut floating tethered in high Earth orbit, gazing toward an endless starry void, photorealistic Earth curvature, 8k cinematic",
                "astronaut spacewalk earth orbit stars",
            ),
            (
                f"As we gaze into tomorrow, one truth remains: {clean_topic} is not just a distant wonder—it is a mirror reflecting humanity's endless quest for understanding.",
                "Breathtaking spiral galaxy in deep space, billions of glowing stars, radiant core, Hubble ultra deep field style, awe-inspiring",
                "spiral galaxy core glowing space",
            ),
        ],
        "history": [
            (
                f"History is written by the victors, but the true story of {clean_topic} was buried beneath centuries of forgotten records and carefully guarded secrets.",
                "Grand ancient citadel illuminated by burning torches, towering stone battlements, historic volumetric mist, photorealistic 8k, cinematic color grade",
                "ancient fortress torches historic battle",
            ),
            (
                "Long before modern civilization took shape, pivotal decisions were made behind closed doors that would seal the fate of millions for generations to come.",
                "Old map of ancient territories on aged parchment, compass, brass magnifying glass, flickering candlelight, intricate details",
                "vintage map compass ancient parchment",
            ),
            (
                "When the crisis finally broke, it came with devastating velocity. What seemed like an unshakeable empire began to crumble from the inside out.",
                "Dramatic cinematic battlefield in the aftermath of conflict, smoke rising into a stormy dusk sky, ancient banners, epic wide shot",
                "ancient battlefield smoke banners sunset",
            ),
            (
                "Eyewitness accounts speak of desperate bargains and catastrophic miscalculations that altered the course of human destiny forever.",
                "Ancient throne room in shadows, decaying marble statues, sunbeams piercing through broken stone roof, haunting historical ruins",
                "ruined palace throne room sunbeams",
            ),
            (
                f"The echoes of {clean_topic} still reverberate through our world today, hidden in the very foundations of modern law, culture, and power.",
                "Historic library with towering shelves of leather-bound manuscripts, dust motes dancing in warm sunbeam, scholarly atmosphere",
                "ancient library books sunlight dust",
            ),
            (
                f"By uncovering the truth behind {clean_topic}, we do not just unearth the past—we receive an urgent warning about our own future.",
                "Sunset over ancient Roman colosseum ruins, golden hour illumination, dramatic clouds, hyperrealistic wide angle architectural shot",
                "ancient ruins sunset golden hour",
            ),
        ],
    }

    # Pick best narrative template, defaulting to stoicism/history
    template_scenes = narratives.get(detected_niche, narratives["history"])

    # Build scene list matching num_scenes
    scenes = []
    for i in range(num_scenes):
        idx = i % len(template_scenes)
        narration, prompt, query = template_scenes[idx]
        scenes.append(
            {
                "scene_id": i + 1,
                "narration": narration,
                "visual_prompt": prompt,
                "search_query": f"{clean_topic.lower()} {query}",
            }
        )

    return {
        "title": f"The Dark Truth About {clean_topic}",
        "scenes": scenes,
    }


def generate_with_openrouter(topic: str, num_scenes: int, model: str = None) -> dict:
    """Generate script using OpenRouter API with multi-model fallback."""
    api_key = OPENROUTER_API_KEY or os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found.")

    candidate_models = [
        model or OPENROUTER_MODEL or "google/gemma-4-31b-it:free",
        "google/gemma-4-31b-it:free",
        "nvidia/nemotron-3.5-lightning:free",
        "liquid/lfm-2.5-2.6b:free",
    ]

    url = "https://openrouter.ai/api/v1/chat/completions"
    prompt = f"Write a deep-dive long video script about '{topic}' with {num_scenes} scenes.\n{SYSTEM_PROMPT}"

    last_error = None
    for m in candidate_models:
        try:
            print(f"Trying OpenRouter model: {m}...")
            payload = {
                "model": m,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.7,
            }

            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}",
                    "HTTP-Referer": "http://localhost:8501",
                    "X-Title": "AI Long Video Studio",
                },
            )
            with urllib.request.urlopen(req, timeout=35) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                raw_text = data["choices"][0]["message"]["content"].strip()
                if "```json" in raw_text:
                    raw_text = raw_text.split("```json")[1].split("```")[0].strip()
                elif "```" in raw_text:
                    raw_text = raw_text.split("```")[1].split("```")[0].strip()
                return json.loads(raw_text)
        except Exception as e:
            last_error = e
            print(f"Model {m} notice: {e}. Trying next...")

    raise RuntimeError(f"All OpenRouter models failed. Last error: {last_error}")


def generate_script(
    topic: str, duration_minutes: int = 5, script_file: str = None
) -> dict:
    """Main entry point to get or generate script."""
    if script_file and os.path.exists(script_file):
        print(f"Loading custom script from: {script_file}")
        return parse_custom_script(script_file)

    # Roughly 4 to 5 scenes per minute (each scene ~12-15 seconds)
    num_scenes = max(4, int(duration_minutes * 4.5))

    # 1. Try local Ollama FIRST if active and running
    ollama_model = get_available_ollama_model()
    if ollama_model:
        try:
            return generate_with_ollama(topic, num_scenes, model=ollama_model)
        except Exception as e:  # noqa: BLE001
            print(f"Ollama generation notice: {e}. Trying next provider...")

    # 2. Try OpenRouter if provided
    if OPENROUTER_API_KEY or os.getenv("OPENROUTER_API_KEY"):
        try:
            print(
                f"Generating {num_scenes}-scene script using OpenRouter ({OPENROUTER_MODEL})..."
            )
            return generate_with_openrouter(topic, num_scenes)
        except Exception as e:
            print(f"OpenRouter API generation failed: {e}. Trying fallback...")

    # Try Gemini
    if GEMINI_API_KEY:
        try:
            print(
                f"Generating {num_scenes}-scene script using Google Gemini (Free Tier)..."
            )
            return generate_with_gemini(topic, num_scenes)
        except Exception as e:
            print(f"Gemini API generation failed: {e}. Trying fallback...")

    # Try Groq
    if GROQ_API_KEY:
        try:
            print(f"Generating {num_scenes}-scene script using Groq Free Tier...")
            return generate_with_groq(topic, num_scenes)
        except Exception as e:
            print(f"Groq API generation failed: {e}. Trying fallback...")

    # Try Ollama
    try:
        print("Checking for local Ollama instance...")
        return generate_with_ollama(topic, num_scenes)
    except Exception:
        pass

    print("Using intelligent procedural documentary engine...")
    return get_demo_script(topic, num_scenes)
