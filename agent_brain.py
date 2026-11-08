"""
Agent Brain & Training Knowledge Base for Long Video Automation.
Encapsulates viral retention mechanics, YouTube documentary storytelling frameworks,
cinematic visual directing prompts, and self-critique rubrics.
"""

# Specialized Agent Personas & Directing Guidelines
PERSONA_PROMPTS = {
    "documentary": {
        "name": "Cinematic Documentary Director (Ken Burns / BBC Style)",
        "tone": "Authoritative, immersive, atmospheric, philosophical, grand in scale",
        "voice": "en-US-ChristopherNeural",
        "visual_style": "35mm anamorphic film, dramatic chiaroscuro lighting, historic volumetric mist, photorealistic 8k, cinematic color grade",
        "structure": "Cold Open Hook -> The Forgotten Genesis -> Escalation of Conflict -> The Turning Point -> Climax -> The Modern Echo",
    },
    "magnates": {
        "name": "High-Stakes Corporate / Financial Thriller (MagnatesMedia Style)",
        "tone": "Suspenseful, dramatic, fast-paced, revealing corruption, wealth, and power",
        "voice": "en-US-GuyNeural",
        "visual_style": "Dark corporate noir, neon reflections in rain, moody skyscrapers, cinematic shadow play, luxury gold and deep obsidian tones",
        "structure": "The Impossible Heist/Collapse -> Humble Beginnings -> The Dangerous Gamble -> Unchecked Empire -> The Downfall -> Key Lessons",
    },
    "vox_explainer": {
        "name": "Kinetic Explainer & Modern Journalist (Vox / Johnny Harris Style)",
        "tone": "Curious, investigative, clear, fast-moving, questioning conventional wisdom",
        "voice": "en-US-JennyNeural",
        "visual_style": "Vibrant editorial imagery, dynamic perspectives, clean minimalist framing, sharp architectural contrast, macro details",
        "structure": "The Counter-Intuitive Truth -> Why Everyone Gets It Wrong -> The Hidden Mechanism -> The Real Consequences -> What Happens Next",
    },
    "mystery": {
        "name": "Unsolved Mysteries & Cosmic Horror (SunnyV2 / Lemmino Style)",
        "tone": "Eerie, contemplative, detail-oriented, suspense-building, unresolved tension",
        "voice": "en-GB-RyanNeural",
        "visual_style": "Desaturated moody palette, foggy moonlit atmospheres, deep oceanic or cosmic voids, vintage photographic grain, haunting scale",
        "structure": "The Unexplainable Incident -> The Initial Search -> Bizarre Clues That Don't Fit -> Debunked Theories -> The Chilling Possibility",
    },
}

# The 5 Golden Rules of High-Retention Scriptwriting
RETENTION_RULES = [
    "NEVER begin with greetings or channel intros; launch straight into the central mystery or conflict within 3 seconds.",
    "Plant an 'Open Loop' question in the first 45 seconds that is only answered at the very end.",
    "Alternate sentence lengths: follow two complex descriptive sentences with one punchy, short declaration.",
    "Describe physical, tangible sensations rather than abstract concepts (e.g. 'frigid salt water leaking through rivets' instead of 'they experienced difficulty').",
    "End each chapter with a forward-propelling cliffhanger into the next chapter.",
]


def evaluate_script_retention(script_data: dict) -> dict:
    """
    Self-Critique Engine: Analyzes generated script against retention rules
    and provides scores and actionable refinements.
    """
    scenes = script_data.get("scenes", [])
    if not scenes:
        return {"overall_score": 0, "critique": "Script contains no scenes."}

    first_scene = scenes[0].get("narration", "").lower()

    # 1. Hook evaluation
    hook_score = 10
    weak_starters = [
        "welcome",
        "in this video",
        "today we are",
        "hello",
        "let's dive in",
        "have you ever",
    ]
    if any(ws in first_scene for ws in weak_starters):
        hook_score -= 4
    if len(first_scene.split()) > 45:
        hook_score -= 2  # Too wordy for cold open

    # 2. Pacing evaluation
    total_words = sum(len(s.get("narration", "").split()) for s in scenes)
    avg_words_per_scene = total_words / max(1, len(scenes))
    pacing_score = 9 if 20 <= avg_words_per_scene <= 45 else 7

    # 3. Visual Prompt Richness
    visual_score = 9
    for s in scenes:
        v_prompt = s.get("visual_prompt", "")
        if len(v_prompt) < 30:
            visual_score = 6
            break

    overall_score = round((hook_score * 0.4 + pacing_score * 0.3 + visual_score * 0.3), 1)

    recommendations = []
    if hook_score < 8:
        recommendations.append(
            "Strengthen cold open: remove filler, open with the high-stakes climax or shocking fact."
        )
    if avg_words_per_scene > 50:
        recommendations.append("Trim narration per scene to prevent visual stagnation; aim for 20-35 words per cut.")
    if visual_score < 8:
        recommendations.append("Inject cinematic camera keywords (e.g. anamorphic 35mm, chiaroscuro, drone push-in).")

    return {
        "overall_score": overall_score,
        "hook_score": hook_score,
        "pacing_score": pacing_score,
        "visual_score": visual_score,
        "recommendations": recommendations,
        "passed_quality_check": overall_score >= 7.5,
    }


def refine_visual_prompt(raw_prompt: str, style_keywords: str) -> str:
    """Trains raw prompts into photographic cinematic masterpieces."""
    cleaned = raw_prompt.strip()
    return f"Cinematic film still, {cleaned}, {style_keywords}, ultra-detailed 8k, award-winning cinematography, photorealistic, Unreal Engine 5 render style, wide angle composition"
