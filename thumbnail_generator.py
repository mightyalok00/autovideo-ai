"""
YouTube High-CTR Thumbnail Generator Module.
Generates 1280x720 cinematic thumbnail with high contrast, bold typography,
vignettes, and visual emphasis for maximum CTR.
"""

import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import THUMBNAIL_HEIGHT, THUMBNAIL_WIDTH  # type: ignore  # noqa: E402
from visuals_fetcher import (  # type: ignore  # noqa: E402
    download_pollinations_image,
    download_wikipedia_image,
    generate_offline_backdrop,
)


def create_youtube_thumbnail(
    topic: str,
    output_path: str,
    punchy_text: str | None = None,
    width: int = THUMBNAIL_WIDTH,
    height: int = THUMBNAIL_HEIGHT,
) -> str:
    """Creates a high-CTR YouTube thumbnail using AI imagery and typography overlays."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    temp_bg = output_path.replace(".jpg", "_bg_temp.jpg")

    # 1. Generate dramatic background
    prompt = (
        f"YouTube thumbnail hero shot for {topic}, intense drama, cinematic lighting, "
        "hyper-detailed, high contrast, clean focal point, award winning composition"
    )
    if not download_pollinations_image(prompt, temp_bg, width=width, height=height):
        if not download_wikipedia_image(topic, temp_bg):
            generate_offline_backdrop(topic, 1, temp_bg, width=width, height=height)

    if not punchy_text:
        words = topic.split()
        if len(words) <= 3:
            punchy_text = topic.upper()
        else:
            punchy_text = f"THE TRUTH ABOUT\n{words[-2].upper()} {words[-1].upper()}"

    # 2. Add dramatic dark gradient and bold typography with Pillow
    try:
        from PIL import Image, ImageDraw, ImageFont

        img = Image.open(temp_bg).convert("RGBA")
        if img.size != (width, height):
            img = img.resize((width, height), Image.Resampling.LANCZOS)

        overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw_ov = ImageDraw.Draw(overlay)

        # Vignette & left-side shadow for text readability
        for x in range(int(width * 0.7)):
            alpha = int(180 * (1 - x / (width * 0.7)))
            draw_ov.line([(x, 0), (x, height)], fill=(0, 0, 0, alpha))

        img = Image.alpha_composite(img, overlay)
        draw = ImageDraw.Draw(img)

        # Draw high-contrast text with shadow
        text_lines = punchy_text.split("\n")
        font = None
        font_size = 72
        font_paths = [
            "C:/Windows/Fonts/impact.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/arial.ttf",
        ]
        for fp in font_paths:
            if os.path.exists(fp):
                try:
                    font = ImageFont.truetype(fp, font_size)
                    break
                except OSError:
                    continue

        if not font:
            font = ImageFont.load_default()

        y = int(height * 0.3)
        for line in text_lines:
            x = 80
            # Outline / Drop Shadow
            for offset_x in [-4, -2, 0, 2, 4]:
                for offset_y in [-4, -2, 0, 2, 4]:
                    draw.text((x + offset_x, y + offset_y), line, font=font, fill=(0, 0, 0))
            # Main bold text (Vibrant Yellow / White)
            draw.text((x, y), line, font=font, fill=(254, 240, 138))
            y += int(font_size * 1.3)

        rgb_img = img.convert("RGB")
        rgb_img.save(output_path, "JPEG", quality=95)

        if os.path.exists(temp_bg):
            os.remove(temp_bg)
        return output_path
    except Exception as e:  # noqa: BLE001
        print(f"Pillow thumbnail styling error: {e}. Using raw image.")
        if os.path.exists(temp_bg):
            shutil.move(temp_bg, output_path)
        return output_path
