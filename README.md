# AutoVideo AI

**Turn a topic into a narrated YouTube video—using free tools and a simple Python workflow.**

AutoVideo AI creates scripts, voiceovers, visuals, MP4 videos, thumbnails, and YouTube metadata. It runs locally and uses FFmpeg for rendering.

## What it does

- Generates a video script with a local Ollama model or configured AI provider.
- Creates narration with Microsoft Edge TTS.
- Finds or generates scene visuals.
- Renders scenes and narration into an MP4 with FFmpeg.
- Creates a thumbnail and SEO-ready title, description, tags, and chapters.

## Quick start

### 1. Install

Requirements: Python 3.10+, [FFmpeg](https://ffmpeg.org/download.html), and optionally [Ollama](https://ollama.com).

```bash
git clone https://github.com/mightyalok00/autovideo-ai.git
cd autovideo-ai
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
```

### 2. Generate a video

Start the local studio:

```bash
python app.py
```

Open **http://localhost:8501**.

Or run directly:

```bash
python -c "from autonomous_agent import run_agent; run_agent('The Hidden Secrets of Deep Space', duration_minutes=3, niche_id='space')"
```

### 3. Optional: use Ollama

Install Ollama, then pull a model:

```bash
ollama pull llama3.2
```

No cloud API key is required for local script generation. Optional provider keys can be set in a `.env` file; see `.env.example`.

## Project map

| File | Purpose |
|---|---|
| `app.py` | Local web studio |
| `autonomous_agent.py` | Runs the production workflow |
| `script_generator.py` | Script generation |
| `voiceover.py` | Narration |
| `visuals_fetcher.py` | Scene images |
| `video_assembler.py` | FFmpeg rendering |
| `thumbnail_generator.py` | Thumbnail creation |
| `seo_optimizer.py` | YouTube metadata |
| `config.py` | Defaults and paths |

## Output

Generated files are saved in the project's output directory. Keep your API keys in `.env`—never commit secrets.

## Troubleshooting

- **FFmpeg not found:** Install FFmpeg and add it to your system PATH.
- **Ollama unavailable:** Start Ollama and confirm the selected model is installed, or configure another provider.
- **Video generation fails:** Check the terminal output and ensure enough disk space is available.

## License

MIT. See [LICENSE](LICENSE).
