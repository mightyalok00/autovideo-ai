"""Simple CLI entry point for AutoVideo AI."""

import argparse
from pathlib import Path

from autonomous_agent import run_agent


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a narrated AI video.")
    parser.add_argument("--topic", required=True, help="Video topic")
    parser.add_argument("--duration", type=int, default=3, help="Length in minutes")
    parser.add_argument("--niche", default="history", help="Niche ID (default: history)")
    parser.add_argument("--script", help="Optional custom script file")
    args = parser.parse_args()

    topic = args.topic.strip()
    if not topic:
        parser.error("--topic cannot be empty")
    if not 1 <= args.duration <= 60:
        parser.error("--duration must be between 1 and 60 minutes")
    if args.script and not Path(args.script).is_file():
        parser.error(f"Script file does not exist: {args.script}")

    result = run_agent(
        topic=topic,
        duration_minutes=args.duration,
        niche_id=args.niche,
        custom_script=args.script,
    )
    print(f"\nVideo created: {result['video_path']}")


if __name__ == "__main__":
    main()
