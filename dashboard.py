"""
ChessMentor web control panel.

This is now the primary user interface — a Flask SPA on localhost:5555.
It exposes:
  GET  /                    → tabbed control panel HTML
  GET  /api/stats           → profile & match-history stats
  GET  /api/state           → live runtime state (FEN, eval, opening, events)
  GET  /api/profile         → full player profile
  POST /api/profile         → patch profile fields (name, rating, color)
  GET  /api/settings        → public (sensitive-masked) settings
  POST /api/settings        → save settings
  POST /api/session/start   → start capture loop  body: {region:[L,T,W,H], clock_region?:[...]}
  POST /api/session/stop    → stop capture loop  body: {result?: "1-0"|"0-1"|"1/2-1/2"}
  POST /api/chat            → freeform coach chat  body: {message: str}
  POST /api/puzzles         → fetch tactical puzzles  body: {count?: 3}
  GET  /api/lichess/eval    → query Lichess cloud eval  ?fen=...

Requires Flask: pip install flask
"""
from __future__ import annotations

import threading
from typing import Optional

from profile import load_profile, save_profile, load_history
from app_state import STATE, start_session_thread, stop_session_thread
from settings import load_settings, save_settings, public_settings, SETTINGS_KEYS

try:
    from flask import Flask, jsonify, request
    _FLASK = True
except ImportError:
    _FLASK = False


# ---------------------------------------------------------------------------
# Coach session singleton (one per running web process)
# ---------------------------------------------------------------------------

_COACH = None
_COACH_LOCK = threading.Lock()


def _get_coach():
    global _COACH
    with _COACH_LOCK:
        if _COACH is None:
            from coach import CoachSession
            from main import initialise_providers
            profile = load_profile()
            llm     = initialise_providers(profile)
            _COACH  = CoachSession(profile, llm_provider=llm)
        return _COACH


def _reset_coach():
    """Force the coach singleton to be rebuilt (e.g. after provider settings change)."""
    global _COACH
    with _COACH_LOCK:
        _COACH = None


# ---------------------------------------------------------------------------
# Stats builder
# ---------------------------------------------------------------------------

def _build_stats() -> dict:
    profile = load_profile()
    history = load_history()

    freq: dict = {}
    for color in ("white", "black"):
        for name in profile.get("openings", {}).get(color, []):
            key = f"[{color[0].upper()}] {name}"
            freq[key] = freq.get(key, 0) + 1

    match_graph = [
        {"date": e.get("ts", "")[:10],
         "result": e.get("result", "unknown"),
         "moves": e.get("moves_analyzed", 0),
         "opening": e.get("opening")}
        for e in history[-60:]
    ]

    return {
        "profile": {
            "username":        profile.get("username", "Player"),
            "rating":          profile.get("rating_estimate"),
            "games":           profile.get("total_games_analyzed", 0),
            "preferred_color": profile.get("preferred_color", "both"),
            "created_at":      (profile.get("created_at") or "")[:10],
            "accuracy_history": profile.get("accuracy_history", []),
        },
        "lessons":           profile.get("lessons", []),
        "weaknesses":         profile.get("weaknesses", []),
        "strengths":          profile.get("strengths", []),
        "coach_notes":        [n.get("note", "") for n in profile.get("coach_notes", [])[-15:]],
        "opening_frequency":  freq,
        "match_history":      match_graph,
    }


# ---------------------------------------------------------------------------
# HTML — single-page app with tabs
# ---------------------------------------------------------------------------

_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ChessMentor Control Panel</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
:root{--bg:#0d1117;--surface:#161b22;--surface2:#1c2128;--border:#30363d;
  --gold:#e2b96a;--green:#3fb950;--red:#f85149;--blue:#58a6ff;--purple:#a371f7;
  --text:#c9d1d9;--muted:#8b949e}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;min-height:100vh;font-size:14px}
header{background:var(--surface);border-bottom:1px solid var(--border);padding:.9rem 1.6rem;
  display:flex;align-items:center;gap:1rem;position:sticky;top:0;z-index:50}
header h1{color:var(--gold);font-size:1.25rem;font-weight:700}
#sub{color:var(--muted);font-size:.8rem;margin-top:.15rem}
nav{display:flex;gap:.3rem;margin-left:auto}
nav button{background:transparent;color:var(--muted);border:1px solid transparent;
  padding:.45rem .9rem;border-radius:6px;cursor:pointer;font-size:.85rem;font-weight:600}
nav button:hover{color:var(--text);background:var(--surface2)}
nav button.active{color:var(--gold);border-color:var(--gold);background:var(--surface2)}
.status-pill{display:inline-flex;align-items:center;gap:.3rem;padding:.25rem .6rem;
  border-radius:999px;font-size:.7rem;font-weight:700;letter-spacing:.05em;text-transform:uppercase}
.status-pill.on{background:#0f3d1a;color:var(--green)}
.status-pill.off{background:#3d0f0f;color:var(--red)}
.dot{width:.5rem;height:.5rem;border-radius:50%;display:inline-block}
.dot.on{background:var(--green);box-shadow:0 0 6px var(--green)}
.dot.off{background:var(--red)}
main{padding:1.5rem 1.6rem;max-width:1500px;margin:0 auto}
.tab{display:none}.tab.active{display:block}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:1.25rem}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:1.25rem}
@media(max-width:900px){.grid-2{grid-template-columns:1fr}}
.card{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:1.1rem}
.card h2{color:var(--gold);font-size:.85rem;font-weight:600;letter-spacing:.05em;
  text-transform:uppercase;border-bottom:1px solid var(--border);padding-bottom:.6rem;margin-bottom:.8rem;
  display:flex;justify-content:space-between;align-items:center}
.row{display:flex;justify-content:space-between;padding:.3rem 0;border-bottom:1px solid #21262d;font-size:.85rem}
.row .lbl{color:var(--muted)}.row .val{font-weight:600}
.tags{display:flex;flex-wrap:wrap;gap:.3rem}
.tag{display:inline-block;border-radius:4px;padding:.15rem .55rem;font-size:.75rem;font-weight:600}
.tag.w{background:#3d0f0f;color:var(--red)}.tag.s{background:#0f3d1a;color:var(--green)}
.tag.n{background:#1a2a3d;color:var(--blue)}
ul.lessons{list-style:none;max-height:260px;overflow-y:auto}
ul.lessons li{padding:.35rem 0;border-bottom:1px solid #21262d;font-size:.82rem;color:var(--muted)}
ul.lessons li::before{content:"♟ ";color:var(--gold)}
em.empty{color:var(--muted);font-style:italic;font-size:.82rem}
.chart-wrap{position:relative;height:200px}

label{display:block;font-size:.78rem;color:var(--muted);margin:.7rem 0 .25rem;font-weight:600;letter-spacing:.04em}
input[type=text],input[type=number],input[type=password],select,textarea{
  width:100%;background:var(--bg);border:1px solid var(--border);border-radius:6px;
  padding:.55rem .7rem;color:var(--text);font-size:.85rem;font-family:inherit}
input:focus,select:focus,textarea:focus{outline:none;border-color:var(--gold)}
input[type=range]{width:100%;accent-color:var(--gold)}
.btn{background:var(--gold);color:#000;border:none;padding:.55rem 1.1rem;border-radius:6px;
  cursor:pointer;font-weight:600;font-size:.85rem;display:inline-flex;align-items:center;gap:.4rem}
.btn:hover{filter:brightness(1.1)}
.btn:disabled{opacity:.4;cursor:not-allowed}
.btn.ghost{background:transparent;color:var(--gold);border:1px solid var(--gold)}
.btn.ghost:hover{background:var(--gold);color:#000}
.btn.danger{background:var(--red);color:#fff}
.btn.green{background:var(--green);color:#000}
.slider-val{color:var(--gold);font-weight:700;float:right}
.row-flex{display:flex;gap:.6rem;align-items:center}
.row-flex>*{flex:1}
.row-flex>.fix{flex:0 0 auto}

/* Live tab */
.live-board{display:grid;grid-template-columns:repeat(8,1fr);width:280px;
  border:2px solid var(--border);border-radius:6px;overflow:hidden;margin:.5rem auto}
.sq{aspect-ratio:1;display:flex;align-items:center;justify-content:center;font-size:1.5rem;line-height:1}
.sq.light{background:#d6c39a}.sq.dark{background:#7d5a3a}
.sq span{color:#000;text-shadow:0 0 2px rgba(255,255,255,.4)}
.sq.dark span{color:#fff;text-shadow:0 0 2px rgba(0,0,0,.5)}
.eval-bar{height:14px;background:linear-gradient(90deg,#000,#fff);border-radius:3px;position:relative;margin:.5rem 0}
.eval-marker{position:absolute;top:-3px;width:3px;height:20px;background:var(--gold);transition:left .4s}
.event-feed{max-height:380px;overflow-y:auto;font-size:.8rem}
.event{padding:.45rem .6rem;border-bottom:1px solid #21262d;display:flex;gap:.6rem;align-items:flex-start}
.event .kind{font-size:.65rem;font-weight:700;letter-spacing:.05em;text-transform:uppercase;
  padding:.1rem .4rem;border-radius:3px;flex-shrink:0;margin-top:.1rem}
.kind.coach{background:#1a3d2a;color:var(--green)}
.kind.position{background:#1a2a3d;color:var(--blue)}
.kind.system{background:#3d2d1a;color:var(--gold)}
.kind.error{background:#3d0f0f;color:var(--red)}
.event-msg{color:var(--text);line-height:1.4;flex:1}

/* Chat */
.chat-window{height:480px;display:flex;flex-direction:column}
.chat-msgs{flex:1;overflow-y:auto;padding:.6rem;background:var(--bg);border-radius:6px;border:1px solid var(--border)}
.chat-msg{padding:.6rem .8rem;border-radius:8px;margin:.5rem 0;font-size:.88rem;line-height:1.45;max-width:88%;white-space:pre-wrap}
.chat-msg.user{background:var(--surface2);margin-left:auto;border:1px solid var(--border)}
.chat-msg.coach{background:#0f3d1a;color:#cfeed8;border:1px solid #1a5530}
.chat-msg.system{background:#3d2d1a;color:#e2b96a;font-size:.78rem;text-align:center;max-width:100%}
.chat-input{display:flex;gap:.5rem;margin-top:.8rem}
.chat-input textarea{resize:none;min-height:60px;font-family:inherit}

/* Settings */
.set-section{margin-bottom:1.2rem}
.set-section h3{color:var(--blue);font-size:.85rem;font-weight:600;margin-bottom:.5rem;
  padding-bottom:.3rem;border-bottom:1px solid #21262d}
small.hint{color:var(--muted);font-size:.72rem;display:block;margin-top:.2rem}

/* Puzzle */
.puzzle{background:var(--surface2);border:1px solid var(--border);border-radius:8px;
  padding:.9rem;margin:.5rem 0;font-size:.85rem}
.puzzle .head{display:flex;justify-content:space-between;color:var(--gold);font-weight:600;margin-bottom:.5rem}
.puzzle code{background:#000;padding:.15rem .4rem;border-radius:3px;font-size:.75rem;color:var(--green)}
.puzzle a{color:var(--blue);text-decoration:none}
.puzzle a:hover{text-decoration:underline}

.toast{position:fixed;bottom:1.5rem;right:1.5rem;background:var(--surface);border:1px solid var(--gold);
  color:var(--gold);padding:.7rem 1.2rem;border-radius:8px;font-weight:600;font-size:.85rem;
  box-shadow:0 4px 12px rgba(0,0,0,.5);transform:translateY(100px);opacity:0;
  transition:all .3s;pointer-events:none;z-index:100}
.toast.show{transform:translateY(0);opacity:1}
.toast.err{border-color:var(--red);color:var(--red)}
</style>
</head>
<body>
<header>
  <span style="font-size:1.7rem">♛</span>
  <div>
    <h1>ChessMentor Control Panel</h1>
    <div id="sub">Loading…</div>
  </div>
  <span id="status" class="status-pill off"><span class="dot off"></span>STOPPED</span>
  <nav>
    <button data-tab="dashboard" class="active">Dashboard</button>
    <button data-tab="live">Live</button>
    <button data-tab="chat">Chat</button>
    <button data-tab="puzzles">Puzzles</button>
    <button data-tab="settings">Settings</button>
  </nav>
</header>

<main>
  <!-- DASHBOARD TAB -->
  <section class="tab active" id="dashboard">
    <div class="grid" id="dash-grid"></div>
  </section>

  <!-- LIVE TAB -->
  <section class="tab" id="live">
    <div class="grid-2">
      <div class="card">
        <h2>Session Controls</h2>
        <label>Board region (left, top, width, height) — pixels</label>
        <div class="row-flex">
          <input type="number" id="reg-l" placeholder="left">
          <input type="number" id="reg-t" placeholder="top">
          <input type="number" id="reg-w" placeholder="width">
          <input type="number" id="reg-h" placeholder="height">
        </div>
        <label>Clock region (optional, for OCR time-pressure detection)</label>
        <div class="row-flex">
          <input type="number" id="ck-l" placeholder="left">
          <input type="number" id="ck-t" placeholder="top">
          <input type="number" id="ck-w" placeholder="width">
          <input type="number" id="ck-h" placeholder="height">
        </div>
        <div class="row-flex" style="margin-top:1rem">
          <button class="btn green" id="btn-start">▶ Start session</button>
          <select id="result-select">
            <option value="unknown">unknown</option>
            <option value="1-0">1-0 (white wins)</option>
            <option value="0-1">0-1 (black wins)</option>
            <option value="1/2-1/2">1/2-1/2 (draw)</option>
          </select>
          <button class="btn danger" id="btn-stop">■ Stop session</button>
        </div>
        <small class="hint">
          Tip: Use a screenshot tool to find your board's pixel rectangle.
          The clock region is optional but enables shortened coaching under time pressure.
        </small>
      </div>

      <div class="card">
        <h2>Live Position</h2>
        <div id="board" class="live-board"></div>
        <div class="row"><span class="lbl">FEN</span><span class="val" style="font-size:.7rem" id="cur-fen">—</span></div>
        <div class="row"><span class="lbl">Engine eval</span><span class="val" id="cur-eval">—</span></div>
        <div class="eval-bar"><div class="eval-marker" id="eval-marker" style="left:50%"></div></div>
        <div class="row"><span class="lbl">Opening</span><span class="val" id="cur-opening">—</span></div>
        <div class="row"><span class="lbl">Move count</span><span class="val" id="cur-moves">0</span></div>
        <div class="row"><span class="lbl">Source</span><span class="val" id="cur-source">—</span></div>
        <button class="btn ghost" id="btn-lichess-eval" style="margin-top:.7rem">⇄ Refetch Lichess cloud eval</button>
      </div>
    </div>

    <div class="card" style="margin-top:1.25rem">
      <h2>Event feed
        <button class="btn ghost" style="font-size:.7rem;padding:.2rem .6rem" onclick="clearFeed()">clear</button>
      </h2>
      <div class="event-feed" id="event-feed"><em class="empty">No events yet — start a session.</em></div>
    </div>
  </section>

  <!-- CHAT TAB -->
  <section class="tab" id="chat">
    <div class="card">
      <h2>Coach Chat
        <span style="color:var(--muted);font-weight:400;font-size:.72rem">
          One conversation per profile — persists across sessions
        </span>
      </h2>
      <div class="chat-window">
        <div class="chat-msgs" id="chat-msgs">
          <div class="chat-msg system">Type a message to chat with your coach.</div>
        </div>
        <div class="chat-input">
          <textarea id="chat-input" placeholder="Ask about openings, strategy, or anything chess…"></textarea>
          <button class="btn" id="btn-send">Send</button>
        </div>
      </div>
    </div>
  </section>

  <!-- PUZZLES TAB -->
  <section class="tab" id="puzzles">
    <div class="card">
      <h2>Tactical Puzzles
        <button class="btn" onclick="fetchPuzzles()">Fetch new puzzles</button>
      </h2>
      <small class="hint">Puzzles are pulled from the Lichess API and filtered by your tracked tactical weaknesses.</small>
      <div id="puzzle-list" style="margin-top:1rem"><em class="empty">Click "Fetch new puzzles" to begin.</em></div>
    </div>
  </section>

  <!-- SETTINGS TAB -->
  <section class="tab" id="settings">
    <div class="grid-2">
      <div class="card">
        <h2>Player Profile</h2>
        <label>Username</label><input type="text" id="set-username">
        <label>Estimated rating</label><input type="number" id="set-rating">
        <label>Preferred color</label>
        <select id="set-color"><option>both</option><option>white</option><option>black</option></select>
        <button class="btn" onclick="saveProfile()" style="margin-top:1rem">Save profile</button>
      </div>

      <div class="card">
        <h2>Behaviour</h2>
        <label>Capture interval (s) <span class="slider-val" id="ci-val">5</span></label>
        <input type="range" id="set-CAPTURE_INTERVAL" min="1" max="20" step="0.5">
        <label>Coaching threshold (centipawns) <span class="slider-val" id="ct-val">100</span></label>
        <input type="range" id="set-COACHING_THRESHOLD" min="30" max="300" step="10">
        <label>Engine top-moves to fetch</label>
        <input type="number" id="set-ENGINE_TOP_MOVES" min="1" max="10">
        <small class="hint">The actual per-player threshold is also adapted by rating + session accuracy.</small>
      </div>
    </div>

    <div class="grid-2" style="margin-top:1.25rem">
      <div class="card">
        <h2>LLM Provider</h2>
        <label>Active LLM provider</label>
        <select id="set-LLM_PROVIDER">
          <option>claude</option><option>openai</option><option>openrouter</option>
          <option>deepseek</option><option>ollama</option><option>fallback</option>
        </select>
        <label>Fallback chain (comma-separated; used when provider = fallback)</label>
        <input type="text" id="set-LLM_FALLBACK_CHAIN" placeholder="openrouter,claude">

        <div class="set-section" style="margin-top:1rem">
          <h3>Anthropic Claude</h3>
          <label>API key</label><input type="password" id="set-ANTHROPIC_API_KEY">
          <label>Model</label><input type="text" id="set-CLAUDE_MODEL">
        </div>
        <div class="set-section">
          <h3>OpenAI</h3>
          <label>API key</label><input type="password" id="set-OPENAI_API_KEY">
          <label>LLM model</label><input type="text" id="set-OPENAI_LLM_MODEL">
          <label>Vision model</label><input type="text" id="set-OPENAI_VISION_MODEL">
        </div>
      </div>

      <div class="card">
        <h2>Additional providers</h2>
        <div class="set-section">
          <h3>OpenRouter (200+ models, single key)</h3>
          <label>API key</label><input type="password" id="set-OPENROUTER_API_KEY">
          <label>Model</label><input type="text" id="set-OPENROUTER_MODEL" placeholder="deepseek/deepseek-chat">
        </div>
        <div class="set-section">
          <h3>DeepSeek (cheap)</h3>
          <label>API key</label><input type="password" id="set-DEEPSEEK_API_KEY">
          <label>Model</label><input type="text" id="set-DEEPSEEK_MODEL">
        </div>
        <div class="set-section">
          <h3>Gemini (vision)</h3>
          <label>API key</label><input type="password" id="set-GEMINI_API_KEY">
          <label>Vision model</label><input type="text" id="set-GEMINI_VISION_MODEL">
        </div>
        <div class="set-section">
          <h3>Ollama (local)</h3>
          <label>Base URL</label><input type="text" id="set-OLLAMA_BASE_URL">
          <label>Model</label><input type="text" id="set-OLLAMA_MODEL">
        </div>
      </div>
    </div>

    <div class="grid-2" style="margin-top:1.25rem">
      <div class="card">
        <h2>Vision provider</h2>
        <label>Provider</label>
        <select id="set-VISION_PROVIDER">
          <option>cv</option><option>claude</option><option>openai</option><option>gemini</option>
        </select>
        <label>CV model path (optional TorchScript CNN)</label>
        <input type="text" id="set-CV_MODEL_PATH" placeholder="/path/to/model.pt">
        <small class="hint">"cv" runs locally and uses zero LLM tokens for board recognition.</small>
      </div>
      <div class="card">
        <h2>Engine provider</h2>
        <label>Provider</label>
        <select id="set-ENGINE_PROVIDER">
          <option>auto</option><option>lichess</option><option>local</option>
        </select>
        <label>Stockfish binary path (for local engine)</label>
        <input type="text" id="set-STOCKFISH_PATH" placeholder="stockfish">
        <small class="hint">"auto" tries Lichess cloud first (free, fast), falls back to local Stockfish.</small>
      </div>
    </div>

    <div style="margin-top:1.25rem;text-align:center">
      <button class="btn" onclick="saveSettings()" style="padding:.7rem 2rem;font-size:.95rem">💾 Save all settings</button>
      <small class="hint">Sensitive keys are shown as "***SET***" if previously stored; leave blank to keep, type new value to replace.</small>
    </div>
  </section>
</main>

<div class="toast" id="toast"></div>

<script>
// ─── Helpers ────────────────────────────────────────────────────────────
const $=id=>document.getElementById(id);
const esc=s=>String(s??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const fetchJSON=async(url,opts={})=>{
  const r=await fetch(url,{headers:{'Content-Type':'application/json'},...opts});
  return r.json();
};
let toastTimer;
function toast(msg,err=false){
  const t=$('toast');t.textContent=msg;t.className='toast show'+(err?' err':'');
  clearTimeout(toastTimer);toastTimer=setTimeout(()=>t.className='toast'+(err?' err':''),3500);
}

// ─── Tab switching ──────────────────────────────────────────────────────
document.querySelectorAll('nav button').forEach(b=>b.onclick=()=>{
  document.querySelectorAll('nav button').forEach(x=>x.classList.toggle('active',x===b));
  document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('active',t.id===b.dataset.tab));
  if(b.dataset.tab==='dashboard')loadDashboard();
  if(b.dataset.tab==='settings')loadSettings();
});

// ─── Dashboard ──────────────────────────────────────────────────────────
async function loadDashboard(){
  const d=await fetchJSON('/api/stats');
  const p=d.profile;
  $('sub').textContent=`${p.username} · ${p.rating??'Unknown'} · ${p.games} games`;
  const g=$('dash-grid');g.innerHTML='';
  g.insertAdjacentHTML('beforeend',`<div class="card"><h2>Player Profile</h2>
    ${row('Username',p.username)}${row('Rating',p.rating??'Unknown')}${row('Games',p.games)}
    ${row('Preferred color',p.preferred_color)}${row('Member since',p.created_at||'Unknown')}</div>`);
  const wt=d.weaknesses.map(w=>`<span class="tag w">${esc(w)}</span>`).join('')||'<em class="empty">None yet</em>';
  const st=d.strengths.map(s=>`<span class="tag s">${esc(s)}</span>`).join('')||'<em class="empty">None yet</em>';
  g.insertAdjacentHTML('beforeend',`<div class="card"><h2>Strengths & Weaknesses</h2>
    <div style="margin-bottom:.8rem"><div style="font-size:.7rem;color:var(--red);margin-bottom:.4rem">WEAKNESSES</div>
    <div class="tags">${wt}</div></div>
    <div><div style="font-size:.7rem;color:var(--green);margin-bottom:.4rem">STRENGTHS</div>
    <div class="tags">${st}</div></div></div>`);
  const ll=d.lessons.length?`<ul class="lessons">${d.lessons.slice(-20).map(l=>`<li>${esc(l)}</li>`).join('')}</ul>`:'<em class="empty">No lessons yet</em>';
  g.insertAdjacentHTML('beforeend',`<div class="card"><h2>Lesson Library (${d.lessons.length})</h2>${ll}</div>`);
  const cn=d.coach_notes.length?d.coach_notes.map(n=>`<div style="font-size:.8rem;color:var(--muted);padding:.3rem 0;border-bottom:1px solid #21262d">💬 ${esc(n)}</div>`).join(''):'<em class="empty">No notes</em>';
  g.insertAdjacentHTML('beforeend',`<div class="card"><h2>Recent Coach Notes</h2>${cn}</div>`);

  if(d.match_history.length){
    const el=document.createElement('div');el.className='card';
    el.innerHTML='<h2>Match History</h2><div class="chart-wrap"><canvas id="hc"></canvas></div>';
    g.appendChild(el);
    new Chart($('hc'),{type:'bar',data:{labels:d.match_history.map((m,i)=>m.date||`G${i+1}`),datasets:[
      {label:'Win', data:d.match_history.map(m=>m.result==='1-0'?1:0),backgroundColor:'#3fb950'},
      {label:'Loss',data:d.match_history.map(m=>m.result==='0-1'?1:0),backgroundColor:'#f85149'},
      {label:'Draw',data:d.match_history.map(m=>m.result==='1/2-1/2'?1:0),backgroundColor:'#8b949e'}]},
      options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{color:'#c9d1d9',boxWidth:10,font:{size:10}}}},
        scales:{x:{stacked:true,ticks:{color:'#8b949e',font:{size:9},maxRotation:45}},y:{stacked:true,ticks:{color:'#8b949e'}}}}});
  }
  const okeys=Object.keys(d.opening_frequency);
  if(okeys.length){
    const el=document.createElement('div');el.className='card';
    el.innerHTML='<h2>Opening Frequency</h2><div class="chart-wrap"><canvas id="oc"></canvas></div>';
    g.appendChild(el);
    const top=okeys.slice(0,10);const C=['#e2b96a','#3fb950','#58a6ff','#f85149','#a371f7','#39d353','#fb8c00','#e879f9','#22d3ee','#a3e635'];
    new Chart($('oc'),{type:'doughnut',data:{labels:top,datasets:[{data:top.map(k=>d.opening_frequency[k]),backgroundColor:C}]},
      options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'right',labels:{color:'#c9d1d9',boxWidth:10,font:{size:10}}}}}});
  }
  if(p.accuracy_history && p.accuracy_history.length){
    const el=document.createElement('div');el.className='card';
    el.innerHTML='<h2>Avg Centipawn Loss (per session)</h2><div class="chart-wrap"><canvas id="ac"></canvas></div>';
    g.appendChild(el);
    new Chart($('ac'),{type:'line',data:{labels:p.accuracy_history.map((_,i)=>`S${i+1}`),datasets:[{
      label:'avg cp loss',data:p.accuracy_history,borderColor:'#e2b96a',backgroundColor:'rgba(226,185,106,.2)',tension:.3,fill:true}]},
      options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},
        scales:{x:{ticks:{color:'#8b949e'}},y:{ticks:{color:'#8b949e'}}}}});
  }
}
function row(l,v){return `<div class="row"><span class="lbl">${l}</span><span class="val">${esc(v??'—')}</span></div>`}

// ─── Live state polling ───────────────────────────────────────────────
async function pollState(){
  try{
    const s=await fetchJSON('/api/state');
    $('status').className='status-pill '+(s.running?'on':'off');
    $('status').innerHTML=`<span class="dot ${s.running?'on':'off'}"></span>${s.running?'RUNNING':'STOPPED'}`;
    if(s.fen){
      renderBoard(s.fen);
      $('cur-fen').textContent=s.fen;
      if(s.eval_mate!==null && s.eval_mate!==undefined){
        $('cur-eval').textContent=`Mate in ${Math.abs(s.eval_mate)}`;$('eval-marker').style.left=(s.eval_mate>0?100:0)+'%';
      }else if(s.eval_cp!==null && s.eval_cp!==undefined){
        const cp=s.eval_cp;$('cur-eval').textContent=(cp/100).toFixed(2)+' pawns (white)';
        const pct=Math.max(2,Math.min(98,50+cp/20));$('eval-marker').style.left=pct+'%';
      }
      $('cur-opening').textContent=s.opening?`${s.opening_eco||''} ${s.opening}`.trim():'—';
      $('cur-moves').textContent=s.move_count;
      $('cur-source').textContent=s.eval_source||'—';
    }
    const feed=$('event-feed');
    if(s.events&&s.events.length){
      feed.innerHTML=s.events.slice().reverse().map(e=>{
        const t=new Date(e.ts*1000).toLocaleTimeString();
        return `<div class="event"><span class="kind ${e.kind}">${t} ${e.kind}</span><div class="event-msg">${esc(e.message)}</div></div>`;
      }).join('');
    }
  }catch(e){}
}
function clearFeed(){$('event-feed').innerHTML='<em class="empty">cleared</em>'}

// ─── Board renderer (unicode pieces) ──────────────────────────────────
const PIECES={p:'♟',n:'♞',b:'♝',r:'♜',q:'♛',k:'♚',P:'♙',N:'♘',B:'♗',R:'♖',Q:'♕',K:'♔'};
function renderBoard(fen){
  const rows=fen.split(' ')[0].split('/');
  let html='';
  for(let r=0;r<8;r++){
    let f=0;
    for(const ch of rows[r]){
      if(/\d/.test(ch)){
        for(let i=0;i<+ch;i++){
          const dark=(r+f)%2===1;
          html+=`<div class="sq ${dark?'dark':'light'}"></div>`;f++;
        }
      }else{
        const dark=(r+f)%2===1;
        html+=`<div class="sq ${dark?'dark':'light'}"><span>${PIECES[ch]||''}</span></div>`;f++;
      }
    }
  }
  $('board').innerHTML=html;
}

// ─── Session start/stop ───────────────────────────────────────────────
$('btn-start').onclick=async()=>{
  const region=['reg-l','reg-t','reg-w','reg-h'].map(i=>+$(i).value);
  if(region.some(v=>!Number.isFinite(v))){toast('Fill in all 4 region values',true);return}
  const cr=['ck-l','ck-t','ck-w','ck-h'].map(i=>+$(i).value);
  const body={region};if(cr.every(v=>Number.isFinite(v))&&cr[2]>0&&cr[3]>0)body.clock_region=cr;
  const r=await fetchJSON('/api/session/start',{method:'POST',body:JSON.stringify(body)});
  toast(r.message||'started',!r.ok);
};
$('btn-stop').onclick=async()=>{
  const result=$('result-select').value;
  const r=await fetchJSON('/api/session/stop',{method:'POST',body:JSON.stringify({result})});
  toast(r.message||'stopped',!r.ok);
};
$('btn-lichess-eval').onclick=async()=>{
  if(!$('cur-fen').textContent||$('cur-fen').textContent==='—'){toast('no live position',true);return}
  const r=await fetchJSON('/api/lichess/eval?fen='+encodeURIComponent($('cur-fen').textContent));
  if(r.pvs&&r.pvs.length){toast(`Lichess: ${r.pvs[0].moves.split(' ')[0]} (cp ${r.pvs[0].cp??r.pvs[0].mate})`);}
  else toast('No cloud eval available',true);
};

// ─── Chat ─────────────────────────────────────────────────────────────
$('btn-send').onclick=sendChat;
$('chat-input').addEventListener('keydown',e=>{
  if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();sendChat();}
});
async function sendChat(){
  const inp=$('chat-input');const text=inp.value.trim();if(!text)return;
  appendChat('user',text);inp.value='';inp.disabled=true;$('btn-send').disabled=true;
  try{
    const r=await fetchJSON('/api/chat',{method:'POST',body:JSON.stringify({message:text})});
    if(r.error)appendChat('system','Error: '+r.error);
    else appendChat('coach',r.message);
  }catch(e){appendChat('system','Network error');}
  inp.disabled=false;$('btn-send').disabled=false;inp.focus();
}
function appendChat(kind,text){
  const m=$('chat-msgs');
  m.insertAdjacentHTML('beforeend',`<div class="chat-msg ${kind}">${esc(text)}</div>`);
  m.scrollTop=m.scrollHeight;
}

// ─── Puzzles ──────────────────────────────────────────────────────────
async function fetchPuzzles(){
  $('puzzle-list').innerHTML='<em class="empty">Fetching from Lichess…</em>';
  const r=await fetchJSON('/api/puzzles',{method:'POST',body:JSON.stringify({count:3})});
  if(!r.puzzles||!r.puzzles.length){$('puzzle-list').innerHTML='<em class="empty">No puzzles returned</em>';return}
  $('puzzle-list').innerHTML=r.puzzles.map((p,i)=>{
    const d=p.puzzle||{};const g=p.game||{};
    return `<div class="puzzle"><div class="head"><span>Puzzle ${i+1}</span><span>Rating: ${d.rating??'?'}</span></div>
      <div>Themes: ${(d.themes||[]).map(t=>`<span class="tag n">${esc(t)}</span>`).join(' ')}</div>
      <div style="margin:.5rem 0">FEN: <code>${esc(g.fen||'')}</code></div>
      ${d.id?`<a href="https://lichess.org/training/${d.id}" target="_blank">Open in Lichess →</a>`:''}</div>`;
  }).join('');
}

// ─── Settings load/save ────────────────────────────────────────────────
async function loadSettings(){
  const [s,p]=await Promise.all([fetchJSON('/api/settings'),fetchJSON('/api/profile')]);
  for(const k in s){const el=$('set-'+k);if(el)el.value=s[k]||''}
  $('set-username').value=p.username||'';
  $('set-rating').value=p.rating_estimate||'';
  $('set-color').value=p.preferred_color||'both';
  if($('set-CAPTURE_INTERVAL').value)$('ci-val').textContent=$('set-CAPTURE_INTERVAL').value;
  if($('set-COACHING_THRESHOLD').value)$('ct-val').textContent=$('set-COACHING_THRESHOLD').value;
}
$('set-CAPTURE_INTERVAL').oninput=e=>$('ci-val').textContent=e.target.value;
$('set-COACHING_THRESHOLD').oninput=e=>$('ct-val').textContent=e.target.value;

async function saveProfile(){
  const r=await fetchJSON('/api/profile',{method:'POST',body:JSON.stringify({
    username:$('set-username').value,
    rating_estimate:+$('set-rating').value||null,
    preferred_color:$('set-color').value})});
  toast(r.ok?'Profile saved':'Save failed',!r.ok);
}
async function saveSettings(){
  const KEYS=["LLM_PROVIDER","LLM_FALLBACK_CHAIN","CLAUDE_MODEL","ANTHROPIC_API_KEY",
    "OPENAI_API_KEY","OPENAI_LLM_MODEL","OPENAI_VISION_MODEL",
    "OPENROUTER_API_KEY","OPENROUTER_MODEL","DEEPSEEK_API_KEY","DEEPSEEK_MODEL",
    "GEMINI_API_KEY","GEMINI_VISION_MODEL","OLLAMA_BASE_URL","OLLAMA_MODEL",
    "VISION_PROVIDER","CV_MODEL_PATH","ENGINE_PROVIDER","STOCKFISH_PATH",
    "ENGINE_TOP_MOVES","CAPTURE_INTERVAL","COACHING_THRESHOLD"];
  const body={};
  for(const k of KEYS){
    const el=$('set-'+k);if(!el)continue;
    const v=el.value;
    if(v==='***SET***')continue;  // unchanged sensitive
    body[k]=v;
  }
  const r=await fetchJSON('/api/settings',{method:'POST',body:JSON.stringify(body)});
  toast(r.ok?'Settings saved (some changes need restart)':'Save failed',!r.ok);
}

// ─── Boot ──────────────────────────────────────────────────────────────
loadDashboard();
setInterval(pollState,2500);
pollState();
</script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Flask app + routes
# ---------------------------------------------------------------------------

def create_app() -> Optional[object]:
    if not _FLASK:
        return None
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False

    # ----- HTML -----
    @app.route("/")
    def index():
        return _HTML, 200, {"Content-Type": "text/html; charset=utf-8"}

    # ----- Stats / profile -----
    @app.route("/api/stats")
    def stats():
        return jsonify(_build_stats())

    @app.route("/api/profile", methods=["GET"])
    def profile_get():
        return jsonify(load_profile())

    @app.route("/api/profile", methods=["POST"])
    def profile_post():
        data = request.get_json() or {}
        profile = load_profile()
        for key in ("username", "preferred_color"):
            if key in data and data[key] is not None:
                profile[key] = data[key]
        if "rating_estimate" in data:
            profile["rating_estimate"] = data["rating_estimate"]
        save_profile(profile)
        return jsonify({"ok": True, "profile": profile})

    # ----- Settings -----
    @app.route("/api/settings", methods=["GET"])
    def settings_get():
        return jsonify(public_settings())

    @app.route("/api/settings", methods=["POST"])
    def settings_post():
        data = request.get_json() or {}
        valid = {k: v for k, v in data.items() if k in SETTINGS_KEYS}
        save_settings(valid)
        _reset_coach()  # provider settings may have changed
        return jsonify({"ok": True, "settings": public_settings()})

    # ----- Live state / session control -----
    @app.route("/api/state")
    def state_get():
        return jsonify(STATE.snapshot())

    @app.route("/api/session/start", methods=["POST"])
    def session_start():
        data = request.get_json() or {}
        region = data.get("region")
        if not region or len(region) != 4:
            return jsonify({"ok": False, "message": "region required: [L,T,W,H]"}), 400
        clock_region = data.get("clock_region")
        if clock_region and len(clock_region) != 4:
            clock_region = None
        try:
            ok, msg = start_session_thread(tuple(region), tuple(clock_region) if clock_region else None)
            return jsonify({"ok": ok, "message": msg})
        except Exception as e:
            return jsonify({"ok": False, "message": f"failed: {e}"}), 500

    @app.route("/api/session/stop", methods=["POST"])
    def session_stop():
        data = request.get_json() or {}
        result = data.get("result", "unknown")
        ok, msg = stop_session_thread(result)
        return jsonify({"ok": ok, "message": msg})

    # ----- Chat -----
    @app.route("/api/chat", methods=["POST"])
    def chat_post():
        data = request.get_json() or {}
        msg = (data.get("message") or "").strip()
        if not msg:
            return jsonify({"error": "empty message"}), 400
        try:
            cs = _get_coach()
            reply = cs.chat(msg)
            return jsonify({"message": reply})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # ----- Puzzles -----
    @app.route("/api/puzzles", methods=["POST"])
    def puzzles_post():
        from puzzles import fetch_puzzles_for_player
        data = request.get_json() or {}
        count = int(data.get("count", 3))
        try:
            puzzles = fetch_puzzles_for_player(load_profile(), count=count)
            return jsonify({"puzzles": puzzles})
        except Exception as e:
            return jsonify({"error": str(e), "puzzles": []}), 500

    # ----- Lichess cloud eval passthrough -----
    @app.route("/api/lichess/eval")
    def lichess_eval():
        import requests as _r
        fen = request.args.get("fen", "")
        if not fen:
            return jsonify({"error": "fen required"}), 400
        try:
            r = _r.get("https://lichess.org/api/cloud-eval",
                       params={"fen": fen, "multiPv": 3}, timeout=8)
            if r.status_code == 200:
                return jsonify(r.json())
            return jsonify({"error": "no eval available", "status": r.status_code}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app


def run_dashboard(port: int = 5555) -> None:
    """Run the control panel in the foreground (blocking)."""
    if not _FLASK:
        print("[ERROR] Flask not installed. Run: pip install flask")
        return
    app = create_app()
    print(f"[ChessMentor] Control panel → http://localhost:{port}")
    app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False, threaded=True)


def run_dashboard_background(port: int = 5555) -> "threading.Thread":
    t = threading.Thread(target=run_dashboard, args=(port,), daemon=True)
    t.start()
    return t
