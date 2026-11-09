"""
Universal All-Niche Video Studio with Intelligent Topic Search & Discovery.
Features:
- Live Search & Discovery for ANY Niche (Finance, Space, Crime, AI, History, Stoicism, Horror, Health, etc.)
- 10 Specialized Video Production Niches
- Instant Viral Hook & Angle Generator
- 1-Click "Select & Create" Pipeline
- Transparent Agent Thought Stream & Stepper
- YouTube Launch Package & High-CTR Thumbnail
"""

import http.server
import json
import os
import socketserver
import sys
import threading
import urllib.parse
from pathlib import Path

# Ensure local directory is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from autonomous_agent import run_agent  # type: ignore  # noqa: E402
from config import OUTPUT_DIR  # type: ignore  # noqa: E402
from niche_engine import search_niche_ideas  # type: ignore  # noqa: E402

PORT = 8501
STATUS_LOCK = threading.Lock()
GENERATION_LOCK = threading.Lock()
STATUS = {
    "state": "idle",
    "step": 0,
    "thought": "Universal Agent ready. Search any topic or pick a niche below.",
    "score": None,
    "audit_details": None,
    "video_url": None,
    "thumbnail_url": None,
    "seo": None,
}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Universal Video Studio - Search & Create for All Niches</title>
    <style>
        :root {
            --bg: #070a12;
            --surface: #111827;
            --surface-hover: #1a2338;
            --primary: #38bdf8;
            --primary-glow: rgba(56, 189, 248, 0.25);
            --text: #f8fafc;
            --text-dim: #94a3b8;
            --border: #1f293d;
            --success: #34d399;
            --accent: #fbbf24;
            --purple: #a855f7;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        body { background: var(--bg); color: var(--text); padding: 30px 20px; min-height: 100vh; }
        .container { max-width: 1050px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 25px; }
        .badge { display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; background: rgba(56, 189, 248, 0.12); color: var(--primary); border-radius: 9999px; font-size: 13px; font-weight: 600; margin-bottom: 12px; border: 1px solid var(--border); }
        h1 { font-size: 2.3rem; font-weight: 800; letter-spacing: -0.5px; margin-bottom: 6px; }
        p.subtitle { color: var(--text-dim); font-size: 15px; }
        
        /* SEARCH & DISCOVERY BOX */
        .search-card { background: linear-gradient(180deg, #131c31, #0f172a); border: 1px solid #293859; border-radius: 16px; padding: 22px; margin-bottom: 25px; box-shadow: 0 8px 25px rgba(0,0,0,0.4); }
        .search-row { display: flex; gap: 12px; margin-bottom: 12px; }
        .search-input { flex: 1; background: #090e1a; border: 1px solid var(--border); border-radius: 10px; color: #fff; padding: 14px 18px; font-size: 16px; outline: none; transition: 0.2s border; }
        .search-input:focus { border-color: var(--primary); box-shadow: 0 0 0 3px var(--primary-glow); }
        .btn-search { background: #0284c7; color: #fff; border: none; padding: 0 24px; border-radius: 10px; font-size: 15px; font-weight: 700; cursor: pointer; transition: 0.2s; }
        .btn-search:hover { background: #0369a1; }
        
        .niche-chips { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px; }
        .chip { background: #090e1a; border: 1px solid var(--border); color: var(--text-dim); padding: 5px 12px; border-radius: 16px; font-size: 12px; cursor: pointer; transition: 0.2s; font-weight: 500; }
        .chip:hover { border-color: var(--primary); color: #fff; background: #1a253d; }
        
        /* SEARCH RESULTS */
        .search-results { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 18px; }
        .result-card { background: #090e1a; border: 1px solid var(--border); border-radius: 12px; padding: 14px; display: flex; flex-direction: column; justify-content: space-between; transition: 0.2s; }
        .result-card:hover { border-color: var(--primary); transform: translateY(-2px); }
        .result-title { font-size: 14px; font-weight: 700; color: #fff; margin-bottom: 6px; }
        .result-hook { font-size: 12px; color: var(--text-dim); line-height: 1.4; margin-bottom: 12px; }
        .btn-select { background: rgba(56, 189, 248, 0.15); color: var(--primary); border: 1px solid rgba(56, 189, 248, 0.3); padding: 6px 12px; border-radius: 8px; font-size: 12px; font-weight: 700; cursor: pointer; width: 100%; transition: 0.2s; }
        .btn-select:hover { background: var(--primary); color: #000; }
        
        /* STUDIO FORM */
        .card { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 26px; margin-bottom: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
        .form-group { margin-bottom: 20px; }
        label { display: flex; justify-content: space-between; font-size: 14px; font-weight: 600; margin-bottom: 8px; color: var(--text); }
        label span.hint { font-weight: 400; color: var(--text-dim); font-size: 12px; }
        input[type="text"], select {
            width: 100%; background: #0b1120; border: 1px solid var(--border); border-radius: 10px; color: #fff; padding: 12px 16px; font-size: 15px; outline: none; transition: 0.2s border;
        }
        input[type="text"]:focus, select:focus { border-color: var(--primary); box-shadow: 0 0 0 3px var(--primary-glow); }
        .row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
        
        button.btn-generate {
            width: 100%; background: linear-gradient(135deg, #0284c7, #38bdf8); color: #fff; border: none; padding: 16px; border-radius: 12px; font-size: 16px; font-weight: 800; cursor: pointer; transition: 0.2s; box-shadow: 0 4px 15px var(--primary-glow); letter-spacing: 0.3px;
        }
        button.btn-generate:hover { transform: translateY(-1px); opacity: 0.95; }
        button.btn-generate:disabled { background: #334155; cursor: not-allowed; transform: none; box-shadow: none; }
        
        /* Stepper & Thoughts */
        .stepper { display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; margin: 20px 0; text-align: center; }
        .step-item { background: #0b1120; padding: 10px 6px; border-radius: 8px; border: 1px solid var(--border); font-size: 11px; color: var(--text-dim); transition: 0.3s; }
        .step-item.active { border-color: var(--primary); color: #fff; background: rgba(56, 189, 248, 0.1); font-weight: 700; }
        .step-item.done { border-color: var(--success); color: var(--success); }
        
        .thought-box { background: #070b14; border: 1px solid #1e293b; border-radius: 12px; padding: 16px; margin-top: 15px; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 13px; line-height: 1.5; color: #38bdf8; display: flex; align-items: center; gap: 10px; }
        
        /* Quality Scores */
        .scores-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 20px 0; }
        .score-card { background: #0b1120; border: 1px solid var(--border); border-radius: 10px; padding: 14px; text-align: center; }
        .score-val { font-size: 1.8rem; font-weight: 800; color: var(--success); }
        .score-title { font-size: 12px; color: var(--text-dim); margin-top: 4px; font-weight: 600; }
        
        .media-preview { display: grid; grid-template-columns: 3fr 2fr; gap: 16px; margin-top: 20px; }
        video { width: 100%; border-radius: 12px; border: 1px solid var(--border); background: #000; }
        img.thumb-img { width: 100%; border-radius: 12px; border: 1px solid var(--border); object-fit: cover; }
        
        .seo-box { background: #0b1120; border: 1px solid var(--border); border-radius: 12px; padding: 18px; margin-top: 20px; }
        .seo-box h3 { font-size: 14px; color: var(--accent); margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
        .copy-btn { background: #1e293b; color: #fff; border: 1px solid var(--border); padding: 4px 10px; border-radius: 6px; font-size: 11px; cursor: pointer; }
        .seo-box pre { white-space: pre-wrap; color: var(--text-dim); background: #070b14; padding: 14px; border-radius: 8px; font-size: 12px; max-height: 250px; overflow-y: auto; }
        
        .spinner { display: inline-block; width: 14px; height: 14px; border: 2px solid rgba(255,255,255,0.3); border-radius: 50%; border-top-color: var(--primary); animation: spin 1s linear infinite; }
        @keyframes spin { to { transform: rotate(360deg); } }

        /* GITHUB ACTIONS CLOUD DISPATCH (DESKTOP & MOBILE) */
        .github-runner-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.95));
            border: 1px solid rgba(56, 189, 248, 0.35);
            border-radius: 14px;
            padding: 16px 20px;
            margin-bottom: 22px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            box-shadow: 0 4px 20px rgba(56, 189, 248, 0.08);
        }
        .runner-left { display: flex; align-items: center; gap: 14px; }
        .runner-icon {
            font-size: 22px;
            background: rgba(56, 189, 248, 0.15);
            border: 1px solid rgba(56, 189, 248, 0.4);
            border-radius: 10px;
            width: 44px;
            height: 44px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }
        .runner-title { font-size: 15px; font-weight: 700; color: #fff; margin-bottom: 3px; }
        .runner-desc { font-size: 12px; color: var(--text-dim); line-height: 1.4; }
        .runner-actions { display: flex; gap: 10px; flex-shrink: 0; }
        .btn-github-run {
            background: linear-gradient(135deg, #0284c7, #2563eb);
            color: #fff;
            text-decoration: none;
            padding: 10px 18px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: 0.2s;
            box-shadow: 0 2px 10px rgba(2, 132, 199, 0.3);
        }
        .btn-github-run:hover { transform: translateY(-1px); box-shadow: 0 4px 15px rgba(2, 132, 199, 0.5); }
        .btn-github-repo {
            background: #1e293b;
            color: #cbd5e1;
            text-decoration: none;
            padding: 10px 14px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            border: 1px solid var(--border);
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: 0.2s;
        }
        .btn-github-repo:hover { border-color: var(--primary); color: #fff; }

        @media (max-width: 768px) {
            body { padding: 15px 10px; }
            h1 { font-size: 1.8rem; }
            .github-runner-card { flex-direction: column; align-items: stretch; text-align: left; }
            .runner-actions { display: grid; grid-template-columns: 1fr 1fr; width: 100%; margin-top: 6px; }
            .btn-github-run, .btn-github-repo { justify-content: center; padding: 12px; font-size: 13px; }
            .search-row { flex-direction: column; }
            .btn-search { padding: 12px; width: 100%; }
            .search-results { grid-template-columns: 1fr; }
            .row { grid-template-columns: 1fr !important; }
            .preview-grid { grid-template-columns: 1fr !important; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="badge">🌐 Universal Video Engine</div>
            <h1>Autonomous Video Director Studio</h1>
            <p class="subtitle">Search, discover, and produce viral long-form videos across every niche.</p>
        </div>

        <!-- GITHUB ACTIONS CLOUD DISPATCH RUNNER (MOBILE & DESKTOP) -->
        <div class="github-runner-card">
            <div class="runner-left">
                <div class="runner-icon">⚡</div>
                <div>
                    <div class="runner-title">Run in Cloud: Desktop & Mobile Dispatch</div>
                    <div class="runner-desc">Directly trigger autonomous video rendering on GitHub Actions from your phone (GitHub Mobile app) or browser. No local hardware required.</div>
                </div>
            </div>
            <div class="runner-actions">
                <a href="https://github.com/mightyalok00/autovideo-ai/actions/workflows/generate-video.yml" target="_blank" rel="noopener" class="btn-github-run">
                    <span>▶</span> Run on GitHub Actions
                </a>
                <a href="https://github.com/mightyalok00/autovideo-ai" target="_blank" rel="noopener" class="btn-github-repo">
                    <span>★</span> GitHub Repo
                </a>
            </div>
        </div>

        <!-- SEARCH & IDEA DISCOVERY ENGINE -->
        <div class="search-card">
            <div style="font-size: 14px; font-weight: 700; margin-bottom: 8px; display: flex; align-items: center; gap: 6px;">
                <span>🔎</span>
                <span>Viral Topic Discovery & Niche Search</span>
            </div>
            <div class="search-row">
                <input type="text" id="search-query" class="search-input" placeholder="Search any topic (e.g. Space, Marcus Aurelius, AI, Wall Street, Deep Sea, Ancient Egypt)...">
                <button class="btn-search" onclick="doSearch()">Search & Brainstorm</button>
            </div>
            <div class="niche-chips">
                <span style="font-size: 12px; color: var(--text-dim); align-self: center;">Popular Niches:</span>
                <span class="chip" onclick="quickSearch('Space & Black Holes')">🌌 Space & Cosmos</span>
                <span class="chip" onclick="quickSearch('Ancient Rome & Egypt')">📜 Ancient History</span>
                <span class="chip" onclick="quickSearch('Billionaire Heists & Finance')">💰 Finance & Money</span>
                <span class="chip" onclick="quickSearch('Unsolved Disappearances')">🔍 True Crime</span>
                <span class="chip" onclick="quickSearch('Stoicism & Dark Psychology')">🧘 Stoicism & Mind</span>
                <span class="chip" onclick="quickSearch('Artificial Intelligence & Singularity')">🤖 AI & Future Tech</span>
                <span class="chip" onclick="quickSearch('Horror & Creepy Legends')">👻 Horror & Urban Myths</span>
                <span class="chip" onclick="quickSearch('Longevity & Biohacking')">🩺 Health & Longevity</span>
                <span class="chip" onclick="quickSearch('Border Anomalies & Geopolitics')">🌍 Geopolitics</span>
                <span class="chip" onclick="quickSearch('Gaming Lore & Secrets')">🎮 Gaming Lore</span>
            </div>

            <!-- DYNAMIC SEARCH RESULTS CARDS -->
            <div class="search-results" id="search-results"></div>
        </div>

        <!-- MAIN PRODUCTION STUDIO -->
        <div class="card">
            <div class="form-group">
                <label>
                    Target Video Topic
                    <span class="hint">Click any search card above or enter your custom topic</span>
                </label>
                <input type="text" id="topic" value="The Bronze Age Collapse: When Civilization Vanished">
            </div>

            <div class="row">
                <div class="form-group">
                    <label>
                        Video Niche & Cinematography Style
                        <span class="hint">Directs camera lenses, voice actor & tone</span>
                    </label>
                    <select id="niche_id">
                        <option value="history" selected>📜 History & Ancient Civilizations (Ken Burns / 35mm)</option>
                        <option value="space">🌌 Science, Space & Cosmos (James Webb / Cosmic Synth)</option>
                        <option value="finance">💰 Finance, Wealth & Scandals (Corporate Noir / Wall St)</option>
                        <option value="crime">🔍 True Crime & Cold Cases (Desaturated Rain / Suspense)</option>
                        <option value="tech">🤖 AI, Tech & Future Singularity (Cyberpunk / High Tech)</option>
                        <option value="psychology">🧘 Stoicism, Psychology & Mind (Marble Chiaroscuro / Cello)</option>
                        <option value="horror">👻 Horror & Folklore (Grainy 16mm / Haunting Strings)</option>
                        <option value="health">🩺 Health, Longevity & Biology (Editorial Medical / Clean)</option>
                        <option value="geopolitics">🌍 Geopolitics & Border Anomalies (War Room / Satellites)</option>
                        <option value="gaming">🎮 Gaming Lore & Pop Culture (Unreal Engine 5 / Action)</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>
                        Target Video Duration
                        <span class="hint">Multi-chapter automatic scene pacing</span>
                    </label>
                    <select id="duration">
                        <option value="2">2 Minutes (Quick Concept Preview)</option>
                        <option value="5" selected>5 Minutes (Standard YouTube Explainer)</option>
                        <option value="10">10 Minutes (Deep Dive Documentary)</option>
                        <option value="15">15 Minutes (Extended Feature)</option>
                        <option value="30">30 Minutes (Masterclass Longform)</option>
                    </select>
                </div>
            </div>

            <div class="form-group" style="margin-top: -5px;">
                <label>
                    <span>🔑 OpenRouter API Key (Optional)</span>
                    <span class="hint">Unlocks free models (Llama 3.3 70B, DeepSeek R1). Get key at <a href="https://openrouter.ai/workspaces/default/keys" target="_blank" style="color: var(--primary); text-decoration: none;">openrouter.ai/keys ↗</a></span>
                </label>
                <input type="password" id="openrouter_key" placeholder="sk-or-v1-... (Paste your key here or leave blank for built-in free templates)">
            </div>

            <button class="btn-generate" id="btn-generate" onclick="startGeneration()">⚡ Direct & Produce Video for this Niche</button>

            <!-- Production Pipeline Stepper -->
            <div class="stepper" id="stepper">
                <div class="step-item" id="step-1">1. Research & Niche Hooks</div>
                <div class="step-item" id="step-2">2. Script Critique</div>
                <div class="step-item" id="step-3">3. Cinematography</div>
                <div class="step-item" id="step-4">4. Neural Voice & Cut</div>
                <div class="step-item" id="step-5">5. YouTube Launch Kit</div>
            </div>

            <!-- Live Agent Thought Stream -->
            <div class="thought-box" id="thought-box">
                <span id="thought-icon">💡</span>
                <span id="thought-text">Universal Agent ready. Select a topic or search any niche above.</span>
            </div>

            <!-- Results Section -->
            <div id="results-container" style="display: none; margin-top: 25px;">
                <!-- Retention Scores -->
                <div class="scores-grid">
                    <div class="score-card">
                        <div class="score-val" id="score-hook">10/10</div>
                        <div class="score-title">🎯 Hook Strength (First 5s)</div>
                        <div style="font-size: 11px; color: var(--text-dim); margin-top: 3px;">Captures curiosity without fluff</div>
                    </div>
                    <div class="score-card">
                        <div class="score-val" id="score-pacing">9.2/10</div>
                        <div class="score-title">⏱️ Retention Pacing</div>
                        <div style="font-size: 11px; color: var(--text-dim); margin-top: 3px;">~28 words per visual cut</div>
                    </div>
                    <div class="score-card">
                        <div class="score-val" id="score-visual">9.5/10</div>
                        <div class="score-title">🎨 Niche Visual Richness</div>
                        <div style="font-size: 11px; color: var(--text-dim); margin-top: 3px;">Cinematic lighting & lenses</div>
                    </div>
                </div>

                <div class="media-preview">
                    <div>
                        <label>🎬 Final Master Video (1080p MP4)</label>
                        <video id="player" controls></video>
                        <a id="video-download" href="#" download style="display: inline-block; margin-top: 8px; font-size: 13px; color: var(--primary); text-decoration: none; font-weight: 600;">⬇️ Download Master Video</a>
                    </div>
                    <div>
                        <label>🖼️ High-CTR Thumbnail (1280x720)</label>
                        <img id="thumb-preview" class="thumb-img" alt="Thumbnail Preview">
                        <a id="thumb-download" href="#" download style="display: inline-block; margin-top: 8px; font-size: 13px; color: var(--primary); text-decoration: none; font-weight: 600;">⬇️ Download Thumbnail</a>
                    </div>
                </div>

                <!-- YouTube Launch Kit -->
                <div class="seo-box">
                    <h3>
                        <span>📦 YouTube Studio Launch Package</span>
                        <button class="copy-btn" onclick="copySEO()">📋 Copy to Clipboard</button>
                    </h3>
                    <pre id="seo-display"></pre>
                </div>
            </div>
        </div>
    </div>

    <script>
        function quickSearch(k) {
            document.getElementById('search-query').value = k;
            doSearch();
        }

        function doSearch() {
            const q = document.getElementById('search-query').value.trim();
            if (!q) return;

            const resDiv = document.getElementById('search-results');
            resDiv.innerHTML = '<div style="color: var(--primary); font-size: 13px;"><span class="spinner"></span> Brainstorming viral angles for ' + q + '...</div>';

            fetch('/api/search?q=' + encodeURIComponent(q))
                .then(r => r.json())
                .then(items => {
                    resDiv.innerHTML = '';
                    if (!items || items.length === 0) {
                        resDiv.innerHTML = '<div style="color: var(--text-dim); font-size: 13px;">No results found. Try another search keyword.</div>';
                        return;
                    }
                    items.forEach(item => {
                        const card = document.createElement('div');
                        card.className = 'result-card';
                        card.innerHTML = `
                            <div>
                                <div style="font-size: 11px; color: var(--accent); margin-bottom: 4px; font-weight: 600;">${item.icon || '📌'} ${item.niche_name || ''}</div>
                                <div class="result-title">${item.title}</div>
                                <div class="result-hook">"${item.hook}"</div>
                            </div>
                            <button class="btn-select" onclick="selectTopic('${item.title.replace(/'/g, "\\'")}', '${item.niche_id}', ${item.duration || 5})">⚡ Select & Create</button>
                        `;
                        resDiv.appendChild(card);
                    });
                });
        }

        function selectTopic(title, niche_id, dur) {
            document.getElementById('topic').value = title;
            if (niche_id) document.getElementById('niche_id').value = niche_id;
            if (dur) document.getElementById('duration').value = dur;
            window.scrollTo({top: 450, behavior: 'smooth'});
        }

        function updateStepper(step) {
            for (let i = 1; i <= 5; i++) {
                const el = document.getElementById('step-' + i);
                el.className = 'step-item';
                if (i < step) el.classList.add('done');
                else if (i === step) el.classList.add('active');
            }
        }

        function checkStatus() {
            fetch('/api/status')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('thought-text').innerText = data.thought || 'Processing...';
                    if (data.state === 'running') {
                        document.getElementById('btn-generate').disabled = true;
                        document.getElementById('thought-icon').innerHTML = '<span class="spinner"></span>';
                        updateStepper(data.step || 3);
                        setTimeout(checkStatus, 2500);
                    } else if (data.state === 'done') {
                        document.getElementById('btn-generate').disabled = false;
                        document.getElementById('thought-icon').innerText = '✅';
                        updateStepper(5);
                        
                        document.getElementById('results-container').style.display = 'block';
                        document.getElementById('player').src = data.video_url;
                        document.getElementById('video-download').href = data.video_url;
                        
                        document.getElementById('thumb-preview').src = data.thumbnail_url;
                        document.getElementById('thumb-download').href = data.thumbnail_url;
                        
                        if (data.audit_details) {
                            document.getElementById('score-hook').innerText = (data.audit_details.hook_score || 10) + '/10';
                            document.getElementById('score-pacing').innerText = (data.audit_details.pacing_score || 9) + '/10';
                            document.getElementById('score-visual').innerText = (data.audit_details.visual_score || 9) + '/10';
                        }
                        
                        if (data.seo) {
                            let text = "========================================\\nRECOMMENDED VIRAL TITLES (Ranked by CTR):\\n========================================\\n";
                            data.seo.title_options.forEach((t, i) => { text += `[Option ${i+1}] ${t}\\n`; });
                            text += "\\n========================================\\nDESCRIPTION & CHAPTERS:\\n========================================\\n" + data.seo.description;
                            text += "\\n\\n========================================\\nTAGS:\\n========================================\\n" + data.seo.tags.join(", ");
                            document.getElementById('seo-display').innerText = text;
                        }
                    } else {
                        document.getElementById('btn-generate').disabled = false;
                        document.getElementById('thought-icon').innerText = '💡';
                    }
                });
        }

        function startGeneration() {
            const topic = document.getElementById('topic').value;
            const duration = document.getElementById('duration').value;
            const niche_id = document.getElementById('niche_id').value;
            const openrouter_key = document.getElementById('openrouter_key').value.trim();

            document.getElementById('btn-generate').disabled = true;
            document.getElementById('results-container').style.display = 'none';
            updateStepper(1);

            fetch('/api/generate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({topic, duration, niche_id, openrouter_key})
            }).then(() => {
                checkStatus();
            });
        }

        function copySEO() {
            const text = document.getElementById('seo-display').innerText;
            navigator.clipboard.writeText(text).then(() => {
                alert("YouTube Launch Kit copied to clipboard!");
            });
        }

        // Run default search on load
        window.onload = function() {
            doSearch();
        };
    </script>
</body>
</html>
"""


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode("utf-8"))
        elif path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(STATUS).encode("utf-8"))
        elif path == "/api/search":
            qs = urllib.parse.parse_qs(parsed.query)
            q = qs.get("q", ["history"])[0]
            results = search_niche_ideas(q)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(results).encode("utf-8"))
        elif path.startswith("/output/"):
            filename = urllib.parse.unquote(path.split("/output/")[1])
            file_path = OUTPUT_DIR / filename
            if file_path.exists():
                mime = "video/mp4" if filename.endswith(".mp4") else "image/jpeg"
                self.send_response(200)
                self.send_header("Content-Type", mime)
                self.send_header("Content-Length", str(file_path.stat().st_size))
                self.end_headers()
                with open(file_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "File not found")
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/api/generate":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)

            topic = data.get("topic", "The Bronze Age Collapse")
            duration = int(data.get("duration", 5))
            niche_id = data.get("niche_id", "history")
            openrouter_key = data.get("openrouter_key", "").strip()
            if openrouter_key:
                os.environ["OPENROUTER_API_KEY"] = openrouter_key

            def _worker():
                try:
                    STATUS["state"] = "running"
                    STATUS["step"] = 1
                    STATUS["thought"] = (
                        f"Agent researching '{topic}' and structuring narrative for {niche_id.title()}..."
                    )

                    STATUS["step"] = 2
                    STATUS["thought"] = "Auditing retention hook and word density against viral benchmarks..."

                    res = run_agent(topic=topic, duration_minutes=duration, niche_id=niche_id)

                    STATUS["step"] = 5
                    video_name = Path(res["video_path"]).name
                    thumb_name = Path(res["thumbnail_path"]).name

                    STATUS["state"] = "done"
                    STATUS["thought"] = f"Production complete! Quality score: {res['audit']['overall_score']}/10."
                    STATUS["score"] = res["audit"]["overall_score"]
                    STATUS["audit_details"] = res["audit"]
                    STATUS["video_url"] = f"/output/{video_name}"
                    STATUS["thumbnail_url"] = f"/output/{thumb_name}"
                    STATUS["seo"] = res["seo_package"]
                except Exception as e:  # noqa: BLE001
                    STATUS["state"] = "error"
                    STATUS["thought"] = f"Error: {e!s}"

            threading.Thread(target=_worker, daemon=True).start()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode("utf-8"))


def start_server():
    server = socketserver.TCPServer(("", PORT), RequestHandler)
    print(f"\n🌐 Universal All-Niche Video Studio running at: http://localhost:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    start_server()
