# 🎬 AutoVideo AI — Autonomous 100% Free Long-Form Video Producer

> **Turn any idea into a broadcast-ready 1080p YouTube documentary with zero API subscriptions.**

AutoVideo AI is a self-directing video production engine. It writes multi-scene documentary scripts, synthesizes natural neural voice acting, sources high-resolution imagery, and edits master 1080p MP4 videos with dynamic Ken Burns pan/zoom and background music ducking.

---

## 🌟 Key Highlights

- 🧠 **Local Intelligence:** Directly integrates with local **Ollama** (`llama3.2`, `mistral`, `deepseek-r1`, `qwen2.5`) with cloud fallbacks (OpenRouter, Gemini, Groq).
- 🎙️ **Natural Neural Narration:** Broadcast-quality voices powered by Microsoft Edge Neural Speech synthesis.
- 🎞️ **Cinematic Assembly:** Automatic lossless FFmpeg stitching with Ken Burns slow zooms, pan effects, and audio duration synchronization.
- 🖼️ **Visual Asset Pipeline:** AI image generation combined with authentic museum-grade archival photos via Wikimedia.
- 🎵 **Adaptive Sound Design:** Mixes ambient background scores with intelligent voice ducking.
- 📦 **YouTube Launch Kit:** Instant 1280x720 high-CTR thumbnail generation, timestamped chapters, and SEO tags.
- 🌐 **Interactive Studio:** Sleek web dashboard on `http://localhost:8501`.

---

## 🚀 Quick Start

### 1. Prerequisites
- **Python 3.10+**
- **FFmpeg** installed and on system `PATH`
- *(Optional but recommended)* **[Ollama](https://ollama.com)** running locally (`ollama run llama3.2`)

### 2. Installation
```bash
git clone https://github.com/mightyalok00/autovideo-ai.git
cd autovideo-ai
pip install -r requirements.txt
```

### 3. Launch Web Studio
```bash
python app.py
```
Open **`http://localhost:8501`** in your browser.

### 4. Or Run Headless via CLI
```bash
python -c "from autonomous_agent import run_agent; run_agent('The Untold Story of Stoicism', duration_minutes=3, niche_id='stoicism')"
```

---

## 📁 Project Architecture

```text
├── app.py                  # Web Studio Server & Interactive Dashboard
├── autonomous_agent.py     # 6-Stage Autonomous Director Production Loop
├── agent_brain.py          # Viral Retention & Pacing Heuristics Engine
├── script_generator.py     # Multi-Provider Scriptwriter (Ollama, OpenRouter, Niche Engine)
├── voiceover.py            # Microsoft Neural Voice Synthesizer
├── visuals_fetcher.py      # AI Image & Archival Photo Pipeline
├── video_assembler.py      # FFmpeg Pan/Zoom Lossless Video Concat Engine
├── thumbnail_generator.py  # 1280x720 High-CTR Thumbnail Designer
├── seo_optimizer.py        # YouTube Titles, Chapters & Description Generator
├── niche_engine.py         # 10 Specialized Video Niche Blueprints
├── config.py               # Core System Paths & Production Settings
└── assets/music/           # Cinematic Atmospheric Soundtrack
```

---

## 📜 License

MIT License — free for personal and commercial content creation.
