"""
soccer_dashboard.py
Serie A Dashboard — protetto, news, live matches, classifiche
"""

import json, os, secrets, random, string, threading
from datetime import datetime
from functools import wraps
import schedule
import time
import requests
from flask import Flask, Response, request, abort
from bs4 import BeautifulSoup

# ── Constants ──────────────────────────────────────────────────────────────────
DATA_FILE   = os.path.join(os.path.dirname(__file__), "data.json")
LOG_FILE    = os.path.join(os.path.dirname(__file__), "fetch.log")
AUTH_FILE   = os.path.join(os.path.dirname(__file__), ".auth")
CACHE_FILE  = os.path.join(os.path.dirname(__file__), "cache.json")

# ── Logging ─────────────────────────────────────────────────────────────────────
def log(msg):
    ts = datetime.now().strftime("%d/%m/%Y %H:%M")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

# ── Auth ────────────────────────────────────────────────────────────────────────
DASHBOARD_TOKEN = None
PIN             = None

def load_auth():
    global DASHBOARD_TOKEN, PIN
    if os.path.exists(AUTH_FILE):
        with open(AUTH_FILE) as f:
            lines = [l.strip() for l in f.read().splitlines() if l.strip()]
        DASHBOARD_TOKEN = lines[0]
        PIN = lines[1] if len(lines) > 1 else None
    else:
        DASHBOARD_TOKEN = secrets.token_urlsafe(32)
        PIN = "".join(random.choices(string.digits, k=4))
        with open(AUTH_FILE, "w") as f:
            f.write(DASHBOARD_TOKEN + "\n" + PIN + "\n")
        os.chmod(AUTH_FILE, 0o600)
    log(f"Token: {DASHBOARD_TOKEN} | PIN: {PIN}")

load_auth()

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        token = auth.replace("Bearer ", "").strip()
        allowed = (token == DASHBOARD_TOKEN
                   or request.args.get("token") == DASHBOARD_TOKEN
                   or request.args.get("pin") == PIN)
        if not allowed:
            abort(401)
        return f(*args, **kwargs)
    return decorated

# ── Cache ──────────────────────────────────────────────────────────────────────
def cache_get(key, max_age_seconds=300):
    """Return cached data if fresh, else None."""
    if not os.path.exists(CACHE_FILE):
        return None
    try:
        with open(CACHE_FILE) as f:
            all_cache = json.load(f)
        entry = all_cache.get(key, {})
        age = datetime.now().timestamp() - entry.get("ts", 0)
        if age < max_age_seconds:
            return entry.get("data")
    except Exception:
        pass
    return None

def cache_set(key, data):
    all_cache = {}
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE) as f:
                all_cache = json.load(f)
        except Exception:
            pass
    all_cache[key] = {"ts": datetime.now().timestamp(), "data": data}
    with open(CACHE_FILE, "w") as f:
        json.dump(all_cache, f)

# ── Static Data ─────────────────────────────────────────────────────────────────
FALLBACK_STANDINGS = [
    {"pos":"1",  "team":"Napoli",       "P":"32","W":"21","D":"7","L":"4","GF":"62","GA":"28","PTS":"70"},
    {"pos":"2",  "team":"Inter",        "P":"32","W":"20","D":"7","L":"5","GF":"63","GA":"26","PTS":"67"},
    {"pos":"3",  "team":"Atalanta",     "P":"32","W":"19","D":"8","L":"5","GF":"67","GA":"30","PTS":"65"},
    {"pos":"4",  "team":"Juventus",     "P":"32","W":"18","D":"9","L":"5","GF":"46","GA":"23","PTS":"63"},
    {"pos":"5",  "team":"Lazio",        "P":"32","W":"16","D":"9","L":"7","GF":"52","GA":"38","PTS":"57"},
    {"pos":"6",  "team":"Roma",         "P":"32","W":"15","D":"9","L":"8","GF":"49","GA":"39","PTS":"54"},
    {"pos":"7",  "team":"Fiorentina",   "P":"32","W":"14","D":"10","L":"8","GF":"48","GA":"36","PTS":"52"},
    {"pos":"8",  "team":"Bologna",      "P":"32","W":"12","D":"12","L":"8","GF":"42","GA":"35","PTS":"48"},
    {"pos":"9",  "team":"Torino",       "P":"32","W":"12","D":"10","L":"10","GF":"35","GA":"34","PTS":"46"},
    {"pos":"10", "team":"Milan",        "P":"32","W":"12","D":"9","L":"11","GF":"45","GA":"44","PTS":"45"},
    {"pos":"11", "team":"Cagliari",     "P":"32","W":"11","D":"9","L":"12","GF":"36","GA":"42","PTS":"42"},
    {"pos":"12", "team":"Genoa",        "P":"32","W":"10","D":"10","L":"12","GF":"33","GA":"40","PTS":"40"},
    {"pos":"13", "team":"Lecce",        "P":"32","W":"9", "D":"11","L":"12","GF":"31","GA":"43","PTS":"38"},
    {"pos":"14", "team":"Udinese",      "P":"32","W":"9", "D":"9", "L":"14","GF":"36","GA":"50","PTS":"36"},
    {"pos":"15", "team":"Parma",        "P":"32","W":"8", "D":"11","L":"13","GF":"38","GA":"52","PTS":"35"},
    {"pos":"16", "team":"Empoli",       "P":"32","W":"8", "D":"10","L":"14","GF":"26","GA":"41","PTS":"34"},
    {"pos":"17", "team":"Monza",        "P":"32","W":"8", "D":"8", "L":"16","GF":"32","GA":"48","PTS":"32"},
    {"pos":"18", "team":"Verona",       "P":"32","W":"7", "D":"9", "L":"16","GF":"29","GA":"50","PTS":"30"},
    {"pos":"19", "team":"Como",         "P":"32","W":"6", "D":"10","L":"16","GF":"26","GA":"50","PTS":"28"},
    {"pos":"20", "team":"Venezia",      "P":"32","W":"5", "D":"9", "L":"18","GF":"24","GA":"55","PTS":"24"},
]

# ── Fetch Functions ─────────────────────────────────────────────────────────────

def fetch_league_data():
    """Fetch standings + top scorers from Fotmob."""
    cached = cache_get("league", max_age_seconds=600)
    if cached:
        return cached

    try:
        resp = requests.get(
            "https://www.fotmob.com/api/leagues?id=55&tab=table",
            headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "it-IT,it;q=0.9"},
            timeout=15
        )
        resp.raise_for_status()
        data = resp.json()

        # Standings
        table = data.get("tableData", [])
        teams = []
        for row in table[:20]:
            stats = row.get("stats", {})
            teams.append({
                "pos": str(row.get("rank", "?")),
                "team": row.get("teamName", row.get("teamDispName", "?")),
                "P": str(stats.get("played", "?")),
                "W": str(stats.get("wins", "?")),
                "D": str(stats.get("draws", "?")),
                "L": str(stats.get("losses", "?")),
                "GF": str(stats.get("goalsFor", "?")),
                "GA": str(stats.get("goalsAgainst", "?")),
                "PTS": str(stats.get("points", "?")),
            })

        # Top scorers
        scorers = []
        top_scorers = data.get("topScorers", {}).get("players", [])
        for p in top_scorers[:10]:
            scorers.append({
                "name": p.get("name", "?"),
                "team": p.get("teamName", "?"),
                "goals": str(p.get("goals", "?")),
                "assists": str(p.get("assists", "?")),
            })

        result = {"standings": teams, "scorers": scorers, "source": "fotmob"}
        cache_set("league", result)
        return result

    except Exception as e:
        log(f"Fotmob errore: {e}")

    # Fallback standings + static scorers
    result = {
        "standings": FALLBACK_STANDINGS,
        "scorers": [
            {"name":"Lautaro Martínez","team":"Inter","goals":"20","assists":"3"},
            {"name":"Victor Osimhen","team":"Napoli","goals":"17","assists":"2"},
            {"name":"Dusan Vlahovic","team":"Juventus","goals":"15","assists":"2"},
            {"name":"Gianluca Scamacca","team":"Atalanta","goals":"14","assists":"1"},
            {"name":"Marcus Rashford","team":"Milan","goals":"12","assists":"4"},
            {"name":"Ciro Immobile","team":"Lazio","goals":"12","assists":"2"},
            {"name":"Christian Pulisic","team":"Milan","goals":"11","assists":"5"},
            {"name":"Moise Kean","team":"Fiorentina","goals":"11","assists":"1"},
            {"name":"Sébastien Haller","team":"Atalanta","goals":"10","assists":"2"},
            {"name":"Mateo Retegui","team":"Genoa","goals":"10","assists":"1"},
        ],
        "source": "fallback"
    }
    cache_set("league", result)
    return result


def fetch_matches():
    """Fetch recent + upcoming Serie A matches from Fotmob."""
    cached = cache_get("matches", max_age_seconds=600)
    if cached:
        return cached

    try:
        resp = requests.get(
            "https://www.fotmob.com/api/leagues?id=55&tab=fixtures",
            headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "it-IT,it;q=0.9"},
            timeout=15
        )
        resp.raise_for_status()
        data = resp.json()

        rounds = data.get("rounds", [])
        matches = []
        for rnd in rounds:
            for m in rnd.get("matches", []):
                matches.append({
                    "home": m.get("home", {}).get("name", "?"),
                    "away": m.get("away", {}).get("name", "?"),
                    "homeScore": m.get("homeScore", {}).get("full", "?"),
                    "awayScore": m.get("awayScore", {}).get("full", "?"),
                    "status": m.get("status", ""),
                    "time": m.get("status", ""),
                    "date": rnd.get("startDate", ""),
                    "league": "Serie A",
                })

        result = {"matches": matches[:30], "source": "fotmob"}
        cache_set("matches", result)
        return result

    except Exception as e:
        log(f"Matches errore: {e}")

    result = {
        "matches": [
            {"home":"Napoli","away":"Inter","homeScore":"2","awayScore":"2","status":"FT","time":"Finalizzato","date":"2026-04-13"},
            {"home":"Atalanta","away":"Juventus","homeScore":"1","awayScore":"0","status":"FT","time":"Finalizzato","date":"2026-04-13"},
            {"home":"Milan","away":"Roma","homeScore":"1","awayScore":"1","status":"FT","time":"Finalizzato","date":"2026-04-13"},
            {"home":"Lazio","away":"Fiorentina","homeScore":"3","awayScore":"1","status":"FT","time":"Finalizzato","date":"2026-04-14"},
            {"home":"Bologna","away":"Torino","homeScore":"2","awayScore":"0","status":"FT","time":"Finalizzato","date":"2026-04-14"},
            {"home":"Genoa","away":"Verona","homeScore":"1","awayScore":"1","status":"FT","time":"Finalizzato","date":"2026-04-14"},
            {"home":"Parma","away":"Cagliari","homeScore":"0","awayScore":"2","status":"FT","time":"Finalizzato","date":"2026-04-15"},
            {"home":"Venezia","away":"Empoli","homeScore":"1","awayScore":"0","status":"FT","time":"Finalizzato","date":"2026-04-15"},
            {"home":"Monza","away":"Lecce","homeScore":"2","awayScore":"2","status":"FT","time":"Finalizzato","date":"2026-04-15"},
            {"home":"Udinese","away":"Como","homeScore":"1","awayScore":"0","status":"FT","time":"Finalizzato","date":"2026-04-16"},
            {"home":"Inter","away":"Napoli","homeScore":"?","awayScore":"?","status":"U","time":"Lun 21:45","date":"2026-04-21"},
            {"home":"Juventus","away":"Lazio","homeScore":"?","awayScore":"?","status":"U","time":"Sab 18:30","date":"2026-04-26"},
        ],
        "source": "fallback"
    }
    cache_set("matches", result)
    return result


def fetch_news():
    """Fetch Italian football news from multiple RSS sources."""
    cached = cache_get("news", max_age_seconds=1800)
    if cached:
        return cached

    news_items = []
    sources = [
        ("Gazzetta dello Sport", "https://www.gazzetta.it/rss.xml"),
        ("Sky Sport Italia", "https://sportsky.it/feed"),
        ("Corriere dello Sport", "https://www.corrieredellosport.it/rss"),
    ]

    for name, url in sources:
        try:
            resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=8)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "xml")
            items = soup.find_all("item")[:6]
            for item in items:
                title = item.find("title")
                link = item.find("link")
                desc = item.find("description")
                pub_date = item.find("pubDate")
                news_items.append({
                    "title": title.get_text(strip=True) if title else "",
                    "link": link.get_text(strip=True) if link else "#",
                    "desc": desc.get_text(strip=True)[:120] + "..." if desc else "",
                    "source": name,
                    "date": pub_date.get_text(strip=True)[:16] if pub_date else "",
                })
        except Exception as e:
            log(f"News [{name}] errore: {e}")

    # Fallback news if all sources fail
    if not news_items:
        news_items = [
            {"title":"Napoli avanti di 3 punti sull'Inter: la corsa scudetto entra nel vivo","link":"#","desc":"A tre giornate dalla fine il campionato si decide sul campo. Il Napoli di Conte guida con 70 punti...","source":"Gazzetta","date":"19 apr"},
            {"title":"Atalanta in Champions: Gasperini ci crede ancora","link":"#","desc":"LAtalanta si avvicina alla zona Champions con una marcia impressionante: 65 punti e gioco...","source":"Sky Sport","date":"19 apr"},
            {"title":"Juventus, nouns about the title: Allegri e il futuro","link":"#","desc":"La Juventus naviga tra i primi quattro con 63 punti, ma il mercato estivo già preoccupa...","source":"Corriere","date":"18 apr"},
            {"title":"Derby di Milano: Pioli vs Inzaghi, chi vince la corsa Champions?","link":"#","desc":"Milan e Inter si affrontano nel big match della settimana: 45 punti per i rossoneri, 67 per i nerazzurri...","source":"Gazzetta","date":"18 apr"},
            {"title":"Serie A, 5 squadre per 2 posti Europa: chi va in Europa League?","link":"#","desc":"Lazio, Roma, Fiorentina, Bologna e Torino: cinque squadre raccolte in 6 punti per due posti in Europa League...","source":"Sky Sport","date":"17 apr"},
            {"title":"Retrocessione: Venezia e Como in zona UEFA, Verona out","link":"#","desc":"Con 24 punti, il Venezia è quasi fuori dalla Serie A. Il Como con 28 punti lotta per la salvezza...","source":"Corriere","date":"17 apr"},
        ]

    result = {"news": news_items[:15], "source": "rss"}
    cache_set("news", result)
    return result


def fetch_all():
    log("Fetch completo Serie A...")
    try:
        fetch_league_data()
    except Exception as e:
        log(f"Standings errore: {e}")
    try:
        fetch_matches()
    except Exception as e:
        log(f"Matches errore: {e}")
    try:
        fetch_news()
    except Exception as e:
        log(f"News errore: {e}")
    log("Fetch completo terminato")

# ── Build HTML ──────────────────────────────────────────────────────────────────
def build_html():
    league_data = fetch_league_data()
    matches_data = fetch_matches()
    news_data = fetch_news()

    standings = league_data.get("standings", FALLBACK_STANDINGS)
    scorers   = league_data.get("scorers", [])
    matches   = matches_data.get("matches", [])
    news      = news_data.get("news", [])

    # ── Standings rows
    stand_rows = ""
    for t in standings:
        p = int(t["pos"])
        cls = "top4" if p <= 4 else ("euro" if p == 5 else ("relegation" if p >= 18 else ""))
        stand_rows += f"""<tr class="{cls}" onclick="toggleRow(this)">
  <td class="pos">{t['pos']}</td>
  <td class="team">{t['team']}</td>
  <td>{t['P']}</td><td class="w">{t['W']}</td><td class="d">{t['D']}</td><td class="l">{t['L']}</td>
  <td>{t['GF']}</td><td>{t['GA']}</td>
  <td class="pts">{t['PTS']}</td>
</tr>"""

    # ── Scorers rows
    scorer_rows = ""
    for i, s in enumerate(scorers):
        scorer_rows += f"""<tr onclick="toggleRow(this)">
  <td class="pos">{i+1}</td>
  <td class="team">{s['name']}</td>
  <td class="team small">{s['team']}</td>
  <td class="pts">{s['goals']}</td>
  <td class="small">{s['assists']}</td>
</tr>"""

    # ── Match cards
    match_cards = ""
    status_icon = {"FT": "🔴", "U": "📅", "LIVE": "⚡"}
    for m in matches:
        icon = status_icon.get(m["status"], "📅")
        score = f"{m['homeScore']} - {m['awayScore']}" if m["status"] != "U" else "vs"
        cls = "live" if m["status"] == "FT" else ""
        match_cards += f"""<div class="match-card {cls}">
  <div class="match-date">{m['date'][5:]}</div>
  <div class="match-teams">
    <span class="mt">{m['home']}</span>
    <span class="score">{score}</span>
    <span class="mt">{m['away']}</span>
  </div>
  <div class="match-status">{icon} {m['time']}</div>
</div>"""

    # ── News items
    news_items = ""
    for n in news:
        news_items += f"""<a href="{n['link']}" target="_blank" class="news-item">
  <div class="news-source">{n['source']} · {n['date']}</div>
  <div class="news-title">{n['title']}</div>
  <div class="news-desc">{n['desc']}</div>
</a>"""

    # ── Prediction cards
    import subprocess, json as _json
    try:
        result = subprocess.run(
            ["python3", os.path.join(os.path.dirname(__file__), "match_predictor.py")],
            capture_output=True, text=True, timeout=30
        )
        preds_data = None
        pred_file = os.path.join(os.path.dirname(__file__), "predictions.json")
        if os.path.exists(pred_file):
            with open(pred_file) as f:
                preds_data = _json.load(f)
    except Exception:
        preds_data = None

    if preds_data and preds_data.get("predictions"):
        pred_cards = ""
        for p in preds_data["predictions"]:
            conf_class = "home-win" if p["prediction"] == "1" else ("away-win" if p["prediction"] == "2" else "draw")
            conf_icon  = "🏠" if p["prediction"] == "1" else ("✈️" if p["prediction"] == "2" else "🤝")
            f_home = "".join(f"<span class='form-{f.lower()}'>{f}</span>" for f in p.get("home_form", []))
            f_away = "".join(f"<span class='form-{f.lower()}'>{f}</span>" for f in p.get("away_form", []))
            pred_cards += f"""<div class="pred-card">
  <div class="pred-teams">
    <div class="pred-team-row home"><span>{p['home']}</span><span>{p['home'][:3].upper()}</span></div>
    <div class="pred-badge {conf_class}">{conf_icon} {p['label']} · {p['prob']}%</div>
    <div class="pred-team-row away"><span>{p['away']}</span><span>{p['away'][:3].upper()}</span></div>
  </div>
  <div class="pred-meta">
    <span>📅 {p.get('date','?')}</span>
    <span>🔮 {p['estimated_score']}</span>
    <span>{p['confidence']}</span>
  </div>
  <div class="pred-form">🏠 [{f_home}]  ✈️ [{f_away}]</div>
</div>"""
    else:
        pred_cards = "<div class='empty-state'>Nessun pronostico disponibile. Clicca ↻ per generarli.</div>"

    return f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Serie A Dashboard</title>
<style>
  *,*::before,*::after{{margin:0;padding:0;box-sizing:border-box}}
  :root{{
    --bg:#0f1923;--surface:#161f2d;--border:#1e2a36;--hover:#1a2536;
    --cyan:#00bcd4;--green:#00c853;--gold:#ffc107;--red:#ff5252;
    --teal:#1de9b6;--text:#e8eaed;--muted:#607d8b;--sub:#455a64;
  }}
  body{{font-family:'Inter','Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--text);min-height:100vh}}
  .wrap{{max-width:1100px;margin:0 auto;padding:1.5rem}}

  /* ── Header ── */
  header{{display:flex;justify-content:space-between;align-items:center;padding-bottom:1.5rem;border-bottom:1px solid var(--border);margin-bottom:2rem;flex-wrap:wrap;gap:1rem}}
  .brand{{display:flex;align-items:center;gap:.75rem}}
  .brand-icon{{font-size:2rem}}
  .brand-text h1{{font-size:1.5rem;font-weight:800;background:linear-gradient(135deg,var(--cyan),var(--teal));-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
  .brand-text p{{font-size:.7rem;color:var(--muted);margin-top:2px}}
  .meta{{text-align:right}}
  .meta .updated-value{{font-size:.8rem;color:#90a4ae;margin-top:2px}}

  /* ── Tabs ── */
  .tabs{{display:flex;gap:.5rem;margin-bottom:1.5rem;flex-wrap:wrap}}
  .tab{{padding:.6rem 1.2rem;border-radius:8px;font-size:.8rem;font-weight:600;cursor:pointer;border:none;background:var(--surface);color:var(--muted);transition:all .2s}}
  .tab.active,.tab:hover{{background:var(--cyan);color:#0f1923}}

  /* ── Predictions ── */
  .pred-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:.75rem;padding:1rem}}
  .pred-card{{background:#1a2536;border:1px solid var(--border);border-radius:12px;padding:1rem 1.2rem;cursor:pointer;transition:all .2s}}
  .pred-card:hover{{background:#212d3b;transform:translateY(-2px)}}
  .pred-card.boosted{{border-color:var(--cyan)}}
  .pred-teams{{display:flex;flex-direction:column;gap:.3rem;margin-bottom:.8rem}}
  .pred-team-row{{display:flex;justify-content:space-between;align-items:center;font-size:.9rem;font-weight:600}}
  .pred-team-row.home{{color:#cfd8dc}}
  .pred-team-row.away{{color:#90a4ae}}
  .pred-badge{{text-align:center;padding:.5rem;border-radius:8px;font-weight:800;font-size:.95rem}}
  .pred-badge.home-win{{background:rgba(0,188,212,.15);color:var(--cyan)}}
  .pred-badge.draw{{background:rgba(255,193,7,.12);color:var(--gold)}}
  .pred-badge.away-win{{background:rgba(255,82,82,.1);color:var(--red)}}
  .pred-meta{{display:flex;justify-content:space-between;font-size:.68rem;color:var(--muted);margin-top:.6rem;flex-wrap:wrap;gap:.3rem}}
  .pred-form{{font-size:.65rem;letter-spacing:.05em}}
  .form-w{{color:var(--green);font-weight:700}}
  .form-d{{color:var(--gold)}}
  .form-l{{color:var(--red)}}

  /* ── Section ── */
  .section{{display:none}}
  .section.active{{display:block}}

  /* ── Card ── */
  .card{{background:var(--surface);border:1px solid var(--border);border-radius:16px;overflow:hidden;margin-bottom:1.5rem;box-shadow:0 4px 24px rgba(0,0,0,.3)}}
  .card-top{{display:flex;justify-content:space-between;align-items:center;padding:1rem 1.25rem;border-bottom:1px solid var(--border);background:#1a2536}}
  .card-title{{font-size:.75rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--sub)}}
  .refresh-btn{{background:var(--cyan);color:#0f1923;border:none;padding:.4rem 1rem;border-radius:8px;font-size:.75rem;font-weight:700;cursor:pointer;transition:all .2s}}
  .refresh-btn:hover{{background:var(--teal);transform:translateY(-1px)}}

  /* ── Table ── */
  table{{width:100%;border-collapse:collapse}}
  th{{padding:.8rem 1rem;text-align:left;font-size:.65rem;font-weight:700;color:var(--sub);text-transform:uppercase;letter-spacing:.08em;border-bottom:1px solid var(--border)}}
  th:not(:first-child):not(:nth-child(2)){{text-align:center}}
  td{{padding:.7rem 1rem;font-size:.85rem;border-bottom:1px solid rgba(30,42,54,.5);transition:background .15s}}
  td:not(:first-child):not(:nth-child(2)){{text-align:center}}
  tr:last-child td{{border-bottom:none}}
  tr:hover td{{background:var(--hover)}}
  tr.top4 td{{background:rgba(0,188,212,.06)}}
  tr.relegation td{{background:rgba(255,82,82,.06)}}
  tr.euro td{{background:rgba(255,193,7,.05)}}
  td.pos{{color:var(--muted);font-weight:700;width:32px}}
  td.team{{font-weight:600;color:#cfd8dc}}
  td.team.small{{font-size:.78rem;color:var(--muted);font-weight:400}}
  td.w{{color:var(--green);font-weight:700}}
  td.d{{color:var(--gold)}}
  td.l{{color:var(--red)}}
  td.pts{{font-weight:800;color:var(--teal);font-size:1rem}}
  td.small{{font-size:.78rem;color:var(--muted)}}

  /* ── Match Cards ── */
  .matches-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:.75rem;padding:1rem}}
  .match-card{{background:#1a2536;border:1px solid var(--border);border-radius:10px;padding:.8rem 1rem;cursor:pointer;transition:all .2s;display:flex;flex-direction:column;gap:.4rem}}
  .match-card:hover{{background:#212d3b;transform:translateY(-2px)}}
  .match-card.live{{border-color:var(--green)}}
  .match-date{{font-size:.68rem;color:var(--muted);text-transform:uppercase;letter-spacing:.05em}}
  .match-teams{{display:flex;justify-content:space-between;align-items:center;gap:.5rem;font-size:.85rem;font-weight:600}}
  .mt{{color:#cfd8dc;flex:1;text-align:center}}
  .score{{font-size:1.1rem;font-weight:800;color:var(--teal);flex:0 0 auto}}
  .match-status{{font-size:.7rem;color:var(--muted)}}

  /* ── News ── */
  .news-list{{padding:.5rem}}
  .news-item{{display:block;padding:.9rem 1rem;border-bottom:1px solid var(--border);text-decoration:none;color:inherit;transition:background .15s}}
  .news-item:last-child{{border-bottom:none}}
  .news-item:hover{{background:var(--hover)}}
  .news-source{{font-size:.68rem;color:var(--cyan);text-transform:uppercase;letter-spacing:.06em;font-weight:700;margin-bottom:.3rem}}
  .news-title{{font-size:.88rem;font-weight:600;color:#cfd8dc;line-height:1.4;margin-bottom:.3rem}}
  .news-desc{{font-size:.75rem;color:var(--muted);line-height:1.5}}

  /* ── Scorers ── */
  .scorer-row td{{}}

  /* ── Live badge animation ── */
  @keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.5}}}}
  .live-badge{{animation:pulse 1.5s infinite;display:inline-block;width:6px;height:6px;background:var(--green);border-radius:50%;margin-right:4px}}

  /* ── No data state ── */
  .empty-state{{padding:2rem;text-align:center;color:var(--muted);font-size:.85rem}}

  @media(max-width:600px){{
    body{{padding:.5rem}}
    .brand-icon{{font-size:1.6rem}}
    .brand-text h1{{font-size:1.2rem}}
    .matches-grid{{grid-template-columns:1fr}}
    th,td{{padding:.6rem .4rem;font-size:.78rem}}
    .tab{{padding:.5rem .8rem;font-size:.75rem}}
  }}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="brand">
      <span class="brand-icon">⚽</span>
      <div class="brand-text">
        <h1>Serie A Dashboard</h1>
        <p>Stagione 2024/25 · Aggiornato alle {datetime.now().strftime('%H:%M')}</p>
      </div>
    </div>
    <div class="meta">
      <div class="updated-label" style="font-size:.65rem;color:var(--muted);text-transform:uppercase;letter-spacing:.08em">Ultimo aggiornamento</div>
      <div class="updated-value">{datetime.now().strftime('%d/%m/%Y %H:%M')}</div>
    </div>
  </header>

  <div class="tabs">
    <button class="tab active" onclick="showTab('standings')">📊 Classifica</button>
    <button class="tab" onclick="showTab('matches')">⚽ Partite</button>
    <button class="tab" onclick="showTab('scorers')">👟 Marcatori</button>
    <button class="tab" onclick="showTab('predictions')">🔮 Pronostici</button>
    <button class="tab" onclick="showTab('news')">📰 Notizie</button>
  </div>

  <!-- STANDINGS -->
  <div id="tab-standings" class="section active">
    <div class="card">
      <div class="card-top">
        <span class="card-title">Classifica Serie A — Giornata 32</span>
        <button class="refresh-btn" onclick="refresh('/update','standings')">↻ Aggiorna</button>
      </div>
      <table>
        <thead><tr>
          <th>#</th><th>Squadra</th><th>G</th><th>V</th><th>P</th><th>S</th><th>GF</th><th>GS</th><th>Pti</th>
        </tr></thead>
        <tbody>{stand_rows}</tbody>
      </table>
    </div>
    <div style="display:flex;gap:1.5rem;font-size:.75rem;color:var(--muted);margin-top:.5rem">
      <span>● <span style="color:var(--cyan)">Champions League</span></span>
      <span>● <span style="color:var(--gold)">Europa League</span></span>
      <span>● <span style="color:var(--red)">Retrocessione</span></span>
    </div>
  </div>

  <!-- MATCHES -->
  <div id="tab-matches" class="section">
    <div class="card">
      <div class="card-top">
        <span class="card-title">⚡ Risultati & Calendario</span>
        <button class="refresh-btn" onclick="refresh('/update','matches')">↻ Aggiorna</button>
      </div>
      <div class="matches-grid">{match_cards}</div>
    </div>
  </div>

  <!-- SCORERS -->
  <div id="tab-scorers" class="section">
    <div class="card">
      <div class="card-top">
        <span class="card-title">👟 Classifica Marcatori — Top 10</span>
        <button class="refresh-btn" onclick="refresh('/update','scorers')">↻ Aggiorna</button>
      </div>
      <table>
        <thead><tr><th>#</th><th>Giocatore</th><th>Squadra</th><th>Gol</th><th>Assist</th></tr></thead>
        <tbody>{scorer_rows}</tbody>
      </table>
    </div>
  </div>

  <!-- PREDICTIONS -->
  <div id="tab-predictions" class="section">
    <div class="card">
      <div class="card-top">
        <span class="card-title">🔮 Pronostici — Weekend</span>
        <button class="refresh-btn" onclick="refresh('/predict','predictions')">↻ Aggiorna</button>
      </div>
      <div class="pred-grid" id="predictions-content">{pred_cards}</div>
    </div>
  </div>

  <!-- NEWS -->
  <div id="tab-news" class="section">
    <div class="card">
      <div class="card-top">
        <span class="card-title">📰 Ultime Notizie</span>
        <button class="refresh-btn" onclick="refresh('/update','news')">↻ Aggiorna</button>
      </div>
      <div class="news-list">{news_items}</div>
    </div>
  </div>
</div>

<script>
function showTab(id){{
  document.querySelectorAll('.section').forEach(s=>s.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  document.getElementById('tab-'+id).classList.add('active');
  event.target.classList.add('active');
}}

function refresh(url, tab){{
  fetch(url+'?token={DASHBOARD_TOKEN}').then(()=>{{
    showTab(tab);
    location.reload();
  }});
}}

function refreshPreds(){{
  fetch('/predict?token={DASHBOARD_TOKEN}').then(()=>location.reload());
}}

function toggleRow(el){{
  el.style.background = el.style.background ? '' : 'rgba(0,188,212,.1)';
}}
</script>
</body>
</html>"""


# ── Flask App ───────────────────────────────────────────────────────────────────
app = Flask(__name__)

@app.route("/")
@require_auth
def index():
    return Response(build_html(), mimetype="text/html")

@app.route("/update")
@require_auth
def update():
    fetch_all()
    return "OK"

@app.route("/predict")
@require_auth
def predict():
    threading.Thread(target=run_predictor, daemon=True).start()
    return "OK"

@app.route("/health")
def health():
    return {"status": "ok", "time": datetime.now().isoformat()}

# ── Scheduler ──────────────────────────────────────────────────────────────────
def send_telegram_alert(message):
    import urllib.request, urllib.error
    token = "8735305765:AAEo4LPyaVJcpDmMNZxIV9jp0p_VfX5sX_Y"
    chat_id = "411617293"
    try:
        import json
        data = json.dumps({
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }).encode("utf-8")
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        resp = urllib.request.urlopen(req, timeout=10)
        log(f"Telegram alert inviato")
    except Exception as e:
        log(f"Telegram alert errore: {e}")

def run_predictor():
    import subprocess, json
    try:
        result = subprocess.run(
            ["python3", os.path.join(os.path.dirname(__file__), "match_predictor.py")],
            capture_output=True, text=True, timeout=30
        )
        log(f"Predizioni generate")

        # Read predictions and format Telegram message
        pred_file = os.path.join(os.path.dirname(__file__), "predictions.json")
        if os.path.exists(pred_file):
            with open(pred_file) as f:
                data = json.load(f)
            preds = data.get("predictions", [])[:5]  # top 5 only for Telegram
            lines = ["🔮 *PREVISIONI SERIE A*\n"]
            for i, p in enumerate(preds, 1):
                icon = "🏠" if p["prediction"] == "1" else ("✈️" if p["prediction"] == "2" else "🤝")
                lines.append(f"{i}. **{p['home']}** vs **{p['away']}**")
                lines.append(f"   {icon} {p['label']} ({p['prob']}%) · 🔮 {p['estimated_score']}")
            lines.append(f"\n_Aggiornato: {data.get('updated','')} | Dashboard: http://localhost:5050_")
            send_telegram_alert("\n".join(lines))
    except Exception as e:
        log(f"Predizione errore: {e}")

def run_scheduler():
    fetch_all()
    schedule.every().day.at("08:00").do(fetch_all)
    schedule.every().day.at("20:00").do(fetch_all)
    # Prediction schedule: Friday 20:00 and Monday 08:00
    schedule.every().friday.at("20:00").do(run_predictor)
    schedule.every().monday.at("08:00").do(run_predictor)
    log("Scheduler avviato — fetch 08:00/20:00 | predizioni Ven 20:00 / Lun 08:00")
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    threading.Thread(target=run_scheduler, daemon=True).start()
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  ⚽ soccer-dashboard → http://localhost:5050")
    print(f"     Token: {DASHBOARD_TOKEN}")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    log(f"Dashboard avviata → http://localhost:5050")
    app.run(host="0.0.0.0", port=5050, debug=False, threaded=True)