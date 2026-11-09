# AutoVideo AI

**Turn a topic into a narrated YouTube video with free tools and a simple Python workflow.**

AutoVideo AI generates scripts, narration, visuals, MP4 videos, thumbnails, and YouTube metadata. It runs locally and uses FFmpeg for rendering.

## Features

- Script generation with Ollama or a configured AI provider
- Microsoft Edge text-to-speech narration
- Scene visuals from supported sources
- FFmpeg video rendering and background music
- Thumbnail and YouTube SEO metadata generation

## Quick start

### Install

Requirements: Python 3.10+, [FFmpeg](https://ffmpeg.org/download.html), and optionally [Ollama](https://ollama.com).

```bash
git clone https://github.com/mightyalok00/autovideo-ai.git
cd autovideo-ai
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Generate a video

Run the simplified CLI:

```bash
python pipeline.py --topic "Deep Space Mysteries" --duration 3 --niche space
```

Or start the web studio:

```bash
python app.py
```

Open **http://localhost:8501**.

### Optional local AI

```bash
ollama pull llama3.2
```

No cloud API key is needed for local script generation. Optional provider keys are configured in `.env`; see `.env.example`.

## Project structure

| File | Responsibility |
|---|---|
| `pipeline.py` | CLI and input validation |
| `autonomous_agent.py` | Main production workflow |
| `script_generator.py` | Script generation |
| `voiceover.py` | Narration |
| `visuals_fetcher.py` | Scene visuals |
| `video_assembler.py` | FFmpeg rendering |
| `thumbnail_generator.py` | Thumbnail creation |
| `seo_optimizer.py` | YouTube metadata |
| `config.py` | Defaults and paths |

## Troubleshooting

- **FFmpeg not found:** Install FFmpeg and add it to PATH.
- **Ollama unavailable:** Start Ollama and verify the model is installed, or configure another provider.
- **Generation fails:** Check terminal logs and available disk space.

Keep API keys in `.env`, never in source code.

## License

MIT. See [LICENSE](LICENSE).
