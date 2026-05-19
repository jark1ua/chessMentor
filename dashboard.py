"""
Local web dashboard for ChessMentor.

Serves a single-page app on http://localhost:5555 (default).
Requires Flask: pip install flask

Start modes
-----------
  python main.py --dashboard          # foreground (blocks)
  python main.py --dashboard --bg     # background thread (non-blocking)
"""
from __future__ import annotations

import threading
from typing import Optional

from profile import load_profile, load_history

try:
    from flask import Flask, jsonify
    _FLASK = True
except ImportError:
    _FLASK = False


# ---------------------------------------------------------------------------
# Stats builder
# ---------------------------------------------------------------------------

def _build_stats() -> dict:
    profile = load_profile()
    history = load_history()

    # Opening frequency across all recorded openings
    freq: dict = {}
    for color in ("white", "black"):
        for name in profile.get("openings", {}).get(color, []):
            key = f"[{color[0].upper()}] {name}"
            freq[key] = freq.get(key, 0) + 1

    # Match history (last 60)
    match_graph = [
        {
            "date":   e.get("ts", "")[:10],
            "result": e.get("result", "unknown"),
            "moves":  e.get("moves_analyzed", 0),
        }
        for e in history[-60:]
    ]

    return {
        "profile": {
            "username":       profile.get("username", "Player"),
            "rating":         profile.get("rating_estimate"),
            "games":          profile.get("total_games_analyzed", 0),
            "preferred_color": profile.get("preferred_color", "both"),
            "created_at":     (profile.get("created_at") or "")[:10],
        },
        "lessons":          profile.get("lessons", []),
        "weaknesses":        profile.get("weaknesses", []),
        "strengths":         profile.get("strengths", []),
        "coach_notes":       [n.get("note", "") for n in profile.get("coach_notes", [])[-10:]],
        "opening_frequency": freq,
        "match_history":     match_graph,
    }


# ---------------------------------------------------------------------------
# Dashboard HTML (self-contained, no static files)
# ---------------------------------------------------------------------------

_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ChessMentor Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
:root{--bg:#0d1117;--surface:#161b22;--border:#30363d;--gold:#e2b96a;
  --green:#3fb950;--red:#f85149;--blue:#58a6ff;--text:#c9d1d9;--muted:#8b949e}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;min-height:100vh}
header{background:var(--surface);border-bottom:1px solid var(--border);
  padding:1rem 2rem;display:flex;align-items:center;gap:1rem}
header h1{color:var(--gold);font-size:1.4rem;font-weight:700}
#sub{color:var(--muted);font-size:.85rem;margin-top:.2rem}
.refresh{margin-left:auto;background:transparent;color:var(--gold);border:1px solid var(--gold);
  padding:.35rem .9rem;border-radius:6px;cursor:pointer;font-size:.85rem}
.refresh:hover{background:var(--gold);color:#000}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));
  gap:1.25rem;padding:1.5rem 2rem}
.card{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:1.1rem}
.card h2{color:var(--gold);font-size:.9rem;font-weight:600;letter-spacing:.05em;
  text-transform:uppercase;border-bottom:1px solid var(--border);padding-bottom:.6rem;margin-bottom:.8rem}
.row{display:flex;justify-content:space-between;padding:.3rem 0;
  border-bottom:1px solid #21262d;font-size:.85rem}
.row .lbl{color:var(--muted)}.row .val{font-weight:600}
.tags{display:flex;flex-wrap:wrap;gap:.3rem;margin-top:.2rem}
.tag{display:inline-block;border-radius:4px;padding:.15rem .5rem;font-size:.75rem;font-weight:600}
.tag.w{background:#3d0f0f;color:var(--red)}.tag.s{background:#0f3d1a;color:var(--green)}
.tag.n{background:#1a2a3d;color:var(--blue)}
ul.lessons{list-style:none;max-height:240px;overflow-y:auto}
ul.lessons li{padding:.35rem 0;border-bottom:1px solid #21262d;font-size:.82rem;color:var(--muted)}
ul.lessons li::before{content:"♟ ";color:var(--gold)}
.note{font-size:.8rem;color:var(--muted);padding:.3rem 0;border-bottom:1px solid #21262d}
.chart-wrap{position:relative;height:200px}
em.empty{color:var(--muted);font-size:.82rem;font-style:italic}
</style>
</head>
<body>
<header>
  <span style="font-size:1.8rem">♛</span>
  <div><h1>ChessMentor Dashboard</h1><div id="sub">Loading…</div></div>
  <button class="refresh" onclick="load()">↻ Refresh</button>
</header>
<div class="grid" id="grid"></div>

<script>
const esc = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const row = (l,v) => `<div class="row"><span class="lbl">${l}</span><span class="val">${esc(v??'—')}</span></div>`;

async function load(){
  const d = await fetch('/api/stats').then(r=>r.json());
  const p = d.profile;
  document.getElementById('sub').textContent =
    `${p.username} · Rating: ${p.rating??'Unknown'} · ${p.games} games analyzed`;

  const g = document.getElementById('grid');
  g.innerHTML = '';

  // Profile
  g.insertAdjacentHTML('beforeend',`<div class="card"><h2>Player Profile</h2>
    ${row('Username',p.username)}${row('Rating',p.rating??'Unknown')}
    ${row('Games',p.games)}${row('Preferred color',p.preferred_color)}
    ${row('Member since',p.created_at||'Unknown')}</div>`);

  // Weaknesses + Strengths
  const wt = d.weaknesses.map(w=>`<span class="tag w">${esc(w)}</span>`).join('')||'<em class="empty">None yet</em>';
  const st = d.strengths.map(s=>`<span class="tag s">${esc(s)}</span>`).join('')||'<em class="empty">None yet</em>';
  g.insertAdjacentHTML('beforeend',`<div class="card"><h2>Strengths & Weaknesses</h2>
    <div style="margin-bottom:.8rem"><div style="font-size:.75rem;color:var(--red);margin-bottom:.4rem">WEAKNESSES</div>
    <div class="tags">${wt}</div></div>
    <div><div style="font-size:.75rem;color:var(--green);margin-bottom:.4rem">STRENGTHS</div>
    <div class="tags">${st}</div></div></div>`);

  // Lessons
  const ll = d.lessons.length
    ? `<ul class="lessons">${d.lessons.slice(-20).map(l=>`<li>${esc(l)}</li>`).join('')}</ul>`
    : '<em class="empty">No lessons yet</em>';
  g.insertAdjacentHTML('beforeend',`<div class="card"><h2>Lesson Library (${d.lessons.length})</h2>${ll}</div>`);

  // Coach notes
  const cn = d.coach_notes.length
    ? d.coach_notes.map(n=>`<div class="note">💬 ${esc(n)}</div>`).join('')
    : '<em class="empty">No notes yet</em>';
  g.insertAdjacentHTML('beforeend',`<div class="card"><h2>Recent Coach Notes</h2>${cn}</div>`);

  // Match history chart
  if(d.match_history.length){
    const el = document.createElement('div');
    el.className='card';
    el.innerHTML='<h2>Match History</h2><div class="chart-wrap"><canvas id="hc"></canvas></div>';
    g.appendChild(el);
    const labels=d.match_history.map((m,i)=>m.date||`G${i+1}`);
    new Chart(document.getElementById('hc'),{type:'bar',
      data:{labels,datasets:[
        {label:'Win', data:d.match_history.map(m=>m.result==='1-0'?1:0),  backgroundColor:'#3fb950'},
        {label:'Loss',data:d.match_history.map(m=>m.result==='0-1'?1:0),  backgroundColor:'#f85149'},
        {label:'Draw',data:d.match_history.map(m=>m.result==='1/2-1/2'?1:0),backgroundColor:'#8b949e'},
      ]},
      options:{responsive:true,maintainAspectRatio:false,
        plugins:{legend:{labels:{color:'#c9d1d9',boxWidth:10,font:{size:10}}}},
        scales:{x:{stacked:true,ticks:{color:'#8b949e',maxRotation:45,font:{size:9}}},
                y:{stacked:true,ticks:{color:'#8b949e'}}}}});
  }

  // Opening frequency doughnut
  const okeys=Object.keys(d.opening_frequency);
  if(okeys.length){
    const el=document.createElement('div');
    el.className='card';
    el.innerHTML='<h2>Opening Frequency</h2><div class="chart-wrap"><canvas id="oc"></canvas></div>';
    g.appendChild(el);
    const top=okeys.slice(0,10);
    const COLORS=['#e2b96a','#3fb950','#58a6ff','#f85149','#a371f7','#39d353',
                  '#fb8c00','#e879f9','#22d3ee','#a3e635'];
    new Chart(document.getElementById('oc'),{type:'doughnut',
      data:{labels:top,datasets:[{data:top.map(k=>d.opening_frequency[k]),backgroundColor:COLORS}]},
      options:{responsive:true,maintainAspectRatio:false,
        plugins:{legend:{position:'right',labels:{color:'#c9d1d9',boxWidth:10,font:{size:10}}}}}});
  }
}
load();
</script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Flask app
# ---------------------------------------------------------------------------

def create_app() -> Optional[object]:
    if not _FLASK:
        return None
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False

    @app.route("/")
    def index():
        return _HTML, 200, {"Content-Type": "text/html; charset=utf-8"}

    @app.route("/api/stats")
    def stats():
        return jsonify(_build_stats())

    return app


def run_dashboard(port: int = 5555) -> None:
    """Run the dashboard in the foreground (blocking)."""
    if not _FLASK:
        print("[ERROR] Flask not installed. Run: pip install flask")
        return
    app = create_app()
    print(f"[ChessMentor] Dashboard → http://localhost:{port}")
    app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)


def run_dashboard_background(port: int = 5555) -> "threading.Thread":
    """Start the dashboard in a daemon thread and return it."""
    t = threading.Thread(target=run_dashboard, args=(port,), daemon=True)
    t.start()
    return t
