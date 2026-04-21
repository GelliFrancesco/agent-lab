"""
match_predictor.py
Subagent: analizza le partite della Serie A e produce predizioni con confidenza.
Usalo come spawn isolato quando vuoi predizioni fresche.
"""

import json, os, sys
from datetime import datetime, timedelta
import requests

# ── Config ─────────────────────────────────────────────────────────────────────
DATA_FILE  = os.path.join(os.path.dirname(__file__), "..", "soccer_dashboard", "data.json")
CACHE_FILE = os.path.join(os.path.dirname(__file__), "..", "soccer_dashboard", "cache.json")
Fotmob     = "https://www.fotmob.com/api/leagues?id=55&tab=fixtures"
HEADERS    = {"User-Agent": "Mozilla/5.0", "Accept-Language": "it-IT,it;q=0.9"}

# ── Forme recenti (fallback statico realistic) ─────────────────────────────────
FORM_CACHE = {
    "Napoli":      ["W","W","D","W","W"],
    "Inter":       ["W","W","L","W","D"],
    "Atalanta":    ["D","W","W","W","L"],
    "Juventus":    ["W","D","W","W","D"],
    "Lazio":       ["L","W","L","W","W"],
    "Roma":        ["D","W","D","L","W"],
    "Fiorentina":  ["W","D","W","D","L"],
    "Bologna":     ["D","L","W","D","D"],
    "Torino":      ["W","L","D","L","W"],
    "Milan":       ["D","W","L","D","W"],
    "Cagliari":    ["L","W","D","W","L"],
    "Genoa":       ["D","D","L","W","D"],
    "Lecce":       ["L","L","D","W","L"],
    "Udinese":     ["D","L","W","D","L"],
    "Parma":       ["L","D","L","D","W"],
    "Empoli":      ["D","L","W","D","L"],
    "Monza":       ["L","L","D","L","D"],
    "Verona":      ["L","L","D","L","W"],
    "Como":        ["D","L","L","D","L"],
    "Venezia":     ["L","L","L","W","L"],
}

# ── H2H precalcolati (ultime 3 stagioni, parziali) ─────────────────────────────
H2H = {
    ("Napoli","Inter"):     {"h2h":["D","W","W","D","L"], "home_dominant": True},
    ("Inter","Napoli"):     {"h2h":["D","L","D","W","W"], "home_dominant": False},
    ("Atalanta","Juventus"):{"h2h":["L","D","W","D","W"], "home_dominant": False},
    ("Juventus","Atalanta"):{"h2h":["W","D","L","W","D"], "home_dominant": True},
    ("Milan","Roma"):       {"h2h":["D","W","D","L","D"], "home_dominant": True},
    ("Roma","Milan"):       {"h2h":["D","W","D","W","D"], "home_dominant": False},
    ("Lazio","Fiorentina"): {"h2h":["W","W","D","L","W"], "home_dominant": True},
    ("Fiorentina","Lazio"): {"h2h":["L","D","W","W","D"], "home_dominant": False},
    ("Lazio","Juventus"):   {"h2h":["L","D","L","W","L"], "home_dominant": True},
}

# ── Home advantage fattori (gol fatti in casa vs fuori) ───────────────────────
HOME_ADV = {
    "Napoli":1.25, "Inter":1.2, "Atalanta":1.15, "Juventus":1.18,
    "Lazio":1.1, "Roma":1.12, "Fiorentina":1.08, "Bologna":1.05,
    "Torino":1.1, "Milan":1.05, "Cagliari":0.95, "Genoa":1.0,
    "Lecce":0.9, "Udinese":0.95, "Parma":0.9, "Empoli":0.85,
    "Monza":0.85, "Verona":0.8, "Como":0.75, "Venezia":0.8,
}

FORM_WEIGHT   = {"W": 3, "D": 1, "L": 0}
CONFIDENCE_RANGES = {
    (0.70, 1.00): "🔴 Alta",
    (0.55, 0.70): "🟡 Media",
    (0.40, 0.55): "🟢 Bassa",
}

# ── Load data ───────────────────────────────────────────────────────────────────
def load_matches():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE) as f:
                cache = json.load(f)
            if "matches" in cache:
                return cache["matches"]["data"]["matches"]
        except Exception:
            pass
    return []

def load_standings():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE) as f:
                return json.load(f)["teams"]
        except Exception:
            pass
    return []

# ── Scoring helpers ──────────────────────────────────────────────────────────────
def form_score(form_list):
    return sum(FORM_WEIGHT[f] for f in form_list) / len(form_list)

def h2h_boost(team_a, team_b, is_home):
    key = (team_a, team_b)
    if key in H2H:
        h2h = H2H[key]["h2h"]
        wins = h2h.count("W")
        if is_home and H2H[key].get("home_dominant"):
            return 0.1
        return wins / max(len(h2h), 1) * 0.08
    key2 = (team_b, team_a)
    if key2 in H2H:
        return -0.05  # opponent has history
    return 0

def points_boost(team, standings):
    pts = 0
    for s in standings:
        if s["team"] == team:
            try: pts = int(s["PTS"])
            except: pass
            break
    # Normalizza: 70+ = alto boost, 30- = basso
    return (pts - 30) / 100  # range approx -0.3 to 0.4

# ── Core predictor ─────────────────────────────────────────────────────────────
def predict(home, away, is_home=True):
    form_a = FORM_CACHE.get(home, ["D","D","D","D","D"])
    form_b = FORM_CACHE.get(away, ["D","D","D","D","D"])

    base = 0.45 if is_home else 0.38  # away always harder

    base += form_score(form_a) / 10 * 0.25
    base -= form_score(form_b) / 10 * 0.15

    base += HOME_ADV.get(home, 1.0) * 0.05
    base -= HOME_ADV.get(away, 1.0) * 0.03

    base += h2h_boost(home, away, is_home)

    standings = load_standings()
    base += points_boost(home, standings) * 0.1
    base -= points_boost(away, standings) * 0.05

    # Cap within [0.25, 0.75]
    prob = max(0.25, min(0.75, base))

    if prob >= 0.55:
        prediction = "1" if is_home else "2"
        confident = "Home Win" if is_home else "Away Win"
    elif prob <= 0.42:
        prediction = "2" if is_home else "1"
        confident = "Away Win" if is_home else "Home Win"
    else:
        prediction = "X"
        confident = "Pareggio"

    confidence_label = next(
        label for (lo, hi), label in CONFIDENCE_RANGES.items()
        if lo <= prob <= hi
    )

    # Goal estimate: poisson-ish
    home_goals = round(prob * 2.2 + (FORM_CACHE.get(home, ["D"]*5).count("W") * 0.15))
    away_goals = round((1 - prob) * 1.6 + (FORM_CACHE.get(away, ["D"]*5).count("W") * 0.1))
    home_goals = max(0, min(4, home_goals))
    away_goals = max(0, min(4, away_goals))

    return {
        "home": home,
        "away": away,
        "prediction": prediction,
        "label": confident,
        "confidence": confidence_label,
        "prob": round(prob * 100),
        "estimated_score": f"{home_goals}-{away_goals}",
        "home_form": form_a,
        "away_form": form_b,
    }

# ── Build all predictions ───────────────────────────────────────────────────────
def predict_all():
    matches = load_matches()
    upcoming = [m for m in matches if m.get("status") == "U"]

    # Fallback match list if cache empty
    if not upcoming:
        # Use ALL fallback matches (not just those without a result)
        all_fallback = [
            {"home":"Inter","away":"Napoli","date":"2026-04-21"},
            {"home":"Juventus","away":"Lazio","date":"2026-04-26"},
            {"home":"Milan","away":"Roma","date":"2026-04-26"},
            {"home":"Atalanta","away":"Bologna","date":"2026-04-26"},
            {"home":"Fiorentina","away":"Torino","date":"2026-04-26"},
            {"home":"Genoa","away":"Cagliari","date":"2026-04-27"},
            {"home":"Verona","away":"Venezia","date":"2026-04-27"},
            {"home":"Udinese","away":"Monza","date":"2026-04-27"},
            {"home":"Lecce","away":"Parma","date":"2026-04-27"},
            {"home":"Como","away":"Empoli","date":"2026-04-27"},
        ]
        upcoming = all_fallback

    results = []
    for m in upcoming[:10]:
        home, away = m["home"], m["away"]
        pred = predict(home, away, is_home=True)
        pred["date"] = m.get("date", "?")
        results.append(pred)

    return results

# ── Human readable output ───────────────────────────────────────────────────────
def format_predictions(preds):
    lines = ["⚽ **PREVISIONI SERIE A**\n"]

    for i, p in enumerate(preds, 1):
        f_home = "".join(p["home_form"])
        f_away = "".join(p["away_form"])
        lines.append(
            f"{i}. **{p['home']}** vs **{p['away']}**\n"
            f"   📅 {p['date']}  |  {p['label']} ({p['prob']}%) {p['confidence']}\n"
            f"   🏠 Forma: [{f_home}]  vs  [{f_away}]\n"
            f"   🔮 Score stimato: {p['estimated_score']}\n"
        )

    lines.append("\n_Le predizioni sono basate su forma, H2H e vantaggio casa._")
    return "\n".join(lines)

# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    preds = predict_all()
    output = format_predictions(preds)
    print(output)

    # Save to predictions.json for dashboard to read
    out_file = os.path.join(os.path.dirname(__file__), "predictions.json")
    with open(out_file, "w") as f:
        json.dump({"updated": datetime.now().strftime("%d/%m/%Y %H:%M"), "predictions": preds}, f, indent=2)
    print(f"\n💾 Salvato in {out_file}")