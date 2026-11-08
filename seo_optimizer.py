"""
YouTube SEO & Viral Packaging Engine.
Automatically drafts high-CTR titles, timestamps/chapters, descriptions, and tags.
"""


def generate_youtube_metadata(topic: str, scenes: list, scene_durations: list) -> dict:
    """Generates complete YouTube video package with chapters, titles, and SEO tags."""
    title_options = [
        f"The Untold Truth About {topic.title()}",
        f"Why Nobody Talks About The Real {topic.title()}",
        f"The Dark Secret Behind {topic.title()}",
        f"How {topic.title()} Changed History Forever",
        f"The Impossible Mystery of {topic.title()} Explained",
    ]

    # Calculate chapters / timestamps
    current_seconds = 0.0
    chapters = []
    for idx, (scene, dur) in enumerate(zip(scenes, scene_durations), 1):
        minutes = int(current_seconds // 60)
        seconds = int(current_seconds % 60)
        timestamp = f"{minutes:02d}:{seconds:02d}"

        # Chapter name from search query or scene title
        q = scene.get("search_query", f"Chapter {idx}").title()
        chapters.append(f"{timestamp} - {q}")
        current_seconds += dur

    chapter_text = "\n".join(chapters)

    description = f"""In this deep-dive documentary, we explore the extraordinary story of {topic.title()}.

📌 CHAPTERS:
{chapter_text}

🔔 Subscribe for more in-depth investigative documentaries and explainers.
Leave your thoughts in the comments below: Which part of this story surprised you the most?

#Documentary #History #Education #DeepDive #{topic.replace(" ", "")}
"""

    tags = [
        topic.lower(),
        f"{topic.lower()} documentary",
        f"{topic.lower()} explained",
        f"history of {topic.lower()}",
        "full documentary",
        "deep dive",
        "educational video",
        "viral explainer",
    ]

    return {
        "title_options": title_options,
        "selected_title": title_options[0],
        "description": description.strip(),
        "chapters": chapters,
        "tags": tags,
        "pinned_comment": f"What was the most shocking revelation about {topic.title()}? Let us know in the comments below! 👇",
    }
