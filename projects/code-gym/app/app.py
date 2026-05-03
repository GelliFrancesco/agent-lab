"""
code-gym — Flask Web App
"""
import os, sys, subprocess, threading
from datetime import datetime
from functools import wraps

from flask import Flask, render_template, request, jsonify, redirect, url_for, Response
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

# ── Auth ─────────────────────────────────────────────────────────────────────
AUTH_TOKEN = os.environ.get("CODEGYM_TOKEN", "codegym-fr-2026")
AUTH_FILE = os.path.join(BASE_DIR, ".auth")

def load_auth():
    if os.path.exists(AUTH_FILE):
        with open(AUTH_FILE) as f:
            return [l.strip() for l in f if l.strip()]
    tokens = [AUTH_TOKEN]
    pin = "7391"
    with open(AUTH_FILE, "w") as f:
        f.write("\n".join(tokens + [pin]))
    return tokens

AUTH_TOKENS = load_auth()
PIN = AUTH_TOKENS[1] if len(AUTH_TOKENS) > 1 else "7391"

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get("token", "").strip()
        if token not in AUTH_TOKENS:
            return Response("Unauthorized", 401)
        return f(*args, **kwargs)
    return decorated

# ── Database ────────────────────────────────────────────────────────────────
from models import Base, User, TopicElo, Attempt, Problem, Difficulty

DB_PATH = os.path.join(DATA_DIR, "codegym.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
Base.metadata.create_all(engine)
Session = scoped_session(sessionmaker(bind=engine))

def get_db():
    return Session()

# ── Seed problems on first run ───────────────────────────────────────────────
def seed_problems():
    db = get_db()
    if db.query(Problem).count() > 0:
        return
    sys.path.insert(0, BASE_DIR)
    from seed_data import PROBLEMS
    for p_data in PROBLEMS:
        p = Problem(
            title=p_data["title"],
            slug=p_data["slug"],
            difficulty=Difficulty[p_data["difficulty"].upper()],
            topics=p_data["topics"],
            companies=p_data["companies"],
            importance=p_data["importance"],
            leetcode_number=p_data.get("leetcode_number"),
            leetcode_url=f"https://leetcode.com/problems/{p_data['slug']}/",
            description=p_data.get("description", ""),
            pattern_hint=p_data.get("pattern_hint", ""),
        )
        db.add(p)
    db.commit()
    print(f"[{datetime.now().strftime('%H:%M')}] Seeded {len(PROBLEMS)} problems")

# ── Seed default users ──────────────────────────────────────────────────────
def seed_users():
    db = get_db()
    if db.query(User).count() > 0:
        return
    default_users = ["Francesco", "Francesca"]  # Francesco + sister
    for name in default_users:
        user = User(name=name, username=name.lower())
        db.add(user)
        db.commit()
        # Initialize topic ELOs
        for topic in ["arrays","strings","linked-lists","trees","graphs",
                       "dynamic-programming","binary-search","sorting","greedy",
                       "recursion","stacks","queues","heaps","tries","bit-manipulation"]:
            db.add(TopicElo(user_id=user.id, topic=topic, elo=1200))
        db.commit()
    print(f"[{datetime.now().strftime('%H:%M')}] Seeded {len(default_users)} users")

def migrate_db():
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE attempts ADD COLUMN with_help BOOLEAN DEFAULT 0"))
            conn.commit()
        except Exception:
            pass

seed_problems()
seed_users()
migrate_db()

# ── ELO helpers ─────────────────────────────────────────────────────────────
INITIAL_ELO = 1200
MIN_ELO, MAX_ELO = 800, 2400

# Thresholds and gains per difficulty level.
# "Fast" requires BOTH attempt and time conditions to be met.
_ELO_CFG = {
    "Easy":   dict(fast_attempts=1, fast_time=15, norm_attempts=2, norm_time=30,
                   win_fast=20,  win_norm=10, win_slow=5,  lose=-10),
    "Medium": dict(fast_attempts=1, fast_time=25, norm_attempts=3, norm_time=50,
                   win_fast=35,  win_norm=18, win_slow=8,  lose=-15),
    "Hard":   dict(fast_attempts=2, fast_time=45, norm_attempts=5, norm_time=90,
                   win_fast=50,  win_norm=25, win_slow=10, lose=-10),
}

def compute_elo_delta(difficulty, attempts_count, time_minutes, gave_up, solved, with_help=False):
    cfg = _ELO_CFG.get(difficulty, _ELO_CFG["Medium"])
    if not solved:
        return cfg["lose"]
    if with_help:
        return cfg["win_slow"]
    if attempts_count <= cfg["fast_attempts"] and time_minutes <= cfg["fast_time"]:
        return cfg["win_fast"]
    if attempts_count <= cfg["norm_attempts"] and time_minutes <= cfg["norm_time"]:
        return cfg["win_norm"]
    return cfg["win_slow"]

def time_rating(difficulty, time_minutes):
    cfg = _ELO_CFG.get(difficulty, _ELO_CFG["Medium"])
    if time_minutes <= cfg["fast_time"]:
        return "fast"
    if time_minutes <= cfg["norm_time"]:
        return "norm"
    return "slow"

def update_elo(user_id, topic, delta):
    db = get_db()
    te = db.query(TopicElo).filter_by(user_id=user_id, topic=topic).first()
    if not te:
        te = TopicElo(user_id=user_id, topic=topic, elo=INITIAL_ELO)
        db.add(te)
    te.elo = max(MIN_ELO, min(MAX_ELO, te.elo + delta))
    if delta > 0:
        te.problems_solved += 1
    elif delta < 0:
        te.problems_given_up += 1
    db.commit()
    return te.elo

def topic_from_elo(elo):
    if elo >= 1800: return "Master"
    if elo >= 1500: return "Advanced"
    if elo >= 1300: return "Intermediate"
    if elo >= 1100: return "Novice"
    return "Beginner"

# ── Interview Readiness ──────────────────────────────────────────────────────

COMPANY_PROFILES = {
    # Tier 1 – FAANG / Big Tech
    "Google":    {"elo_target": 1600, "tier": 1, "topics": ["arrays","graphs","dynamic-programming","strings","trees","binary-search"]},
    "Meta":      {"elo_target": 1550, "tier": 1, "topics": ["arrays","trees","dynamic-programming","strings","graphs"]},
    "Amazon":    {"elo_target": 1450, "tier": 1, "topics": ["arrays","trees","greedy","graphs","strings"]},
    "Apple":     {"elo_target": 1450, "tier": 1, "topics": ["arrays","strings","trees","binary-search"]},
    "Microsoft": {"elo_target": 1400, "tier": 1, "topics": ["arrays","strings","trees","dynamic-programming"]},
    # Tier 2 – Top growth tech
    "Netflix":   {"elo_target": 1500, "tier": 2, "topics": ["arrays","strings","dynamic-programming","trees","graphs"]},
    "Stripe":    {"elo_target": 1500, "tier": 2, "topics": ["arrays","strings","dynamic-programming","trees"]},
    "Airbnb":    {"elo_target": 1400, "tier": 2, "topics": ["arrays","trees","graphs","strings"]},
    "Uber":      {"elo_target": 1450, "tier": 2, "topics": ["arrays","graphs","strings","greedy"]},
    "LinkedIn":  {"elo_target": 1400, "tier": 2, "topics": ["arrays","strings","graphs","trees"]},
}

_READINESS_LABELS = [
    (80, "Very Likely Ready",   "#3fb950"),
    (65, "Strong Candidate",    "#58a6ff"),
    (50, "Getting There",       "#d29922"),
    (35, "Needs More Practice", "#db6d28"),
    (0,  "Early Stage",         "#f85149"),
]

def score_label(score):
    for threshold, label, color in _READINESS_LABELS:
        if score >= threshold:
            return label, color
    return "Early Stage", "#f85149"

def readiness_paragraph(score, weak_topics, approx_problems, company_name=None):
    target = f"{company_name}" if company_name else "a general tech interview"
    if score >= 80:
        opener = f"You're in great shape for {target}."
        detail = "Your skills are strong across key areas. Keep the momentum with a problem a day."
    elif score >= 65:
        opener = f"You're a competitive candidate for {target}."
        gaps = ", ".join(weak_topics[:2]) if weak_topics else "advanced topics"
        detail = f"A bit more depth in {gaps} would make you even stronger."
    elif score >= 50:
        opener = f"You're on the right track for {target}, but there's room to grow."
        gaps = ", ".join(weak_topics[:2]) if weak_topics else "medium difficulty problems"
        detail = f"Focus on building consistency in {gaps}."
    elif score >= 35:
        opener = f"More practice is needed before targeting {target}."
        gaps = ", ".join(weak_topics[:2]) if weak_topics else "core data structures"
        detail = f"Prioritize {gaps} — these appear in almost every loop."
    else:
        opener = f"You're in the early stages of interview prep."
        detail = "Start with Easy problems to build confidence, then move to Mediums."
    if approx_problems > 0:
        days = max(5, approx_problems)
        est = f" Roughly {approx_problems} more focused problems could close the gap — about {days} days at one problem a day."
    else:
        est = " Keep maintaining your skills with regular practice."
    return f"{opener} {detail}{est}"

def compute_readiness(user_id):
    db = get_db()
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        return None

    topic_elos = {te.topic: te.elo for te in db.query(TopicElo).filter_by(user_id=user_id).all()}
    all_problems = db.query(Problem).all()

    # Build solved / helped sets (problem_id based)
    solved_ids, helped_ids = set(), set()
    for a in db.query(Attempt).filter_by(user_id=user_id, solved=True).all():
        (helped_ids if a.with_help else solved_ids).add(a.problem_id)

    def weighted_coverage(problems):
        if not problems:
            return 0.0, 0, 0
        ws = sum(p.importance * (1.0 if p.id in solved_ids else 0.5 if p.id in helped_ids else 0)
                 for p in problems)
        wt = sum(p.importance for p in problems)
        touched = sum(1 for p in problems if p.id in solved_ids or p.id in helped_ids)
        return (ws / wt * 100) if wt else 0.0, touched, len(problems)

    def elo_component(avg_elo, target_elo):
        return min(100, max(0, (avg_elo - MIN_ELO) / (target_elo - MIN_ELO) * 100))

    # Per-company scores
    companies_out = {}
    for name, profile in COMPANY_PROFILES.items():
        key_topics = profile["topics"]
        target_elo = profile["elo_target"]

        topic_elo_vals = [topic_elos.get(t, INITIAL_ELO) for t in key_topics]
        avg_elo = sum(topic_elo_vals) / len(topic_elo_vals)
        elo_pct = elo_component(avg_elo, target_elo)

        # Coverage only for companies present in DB
        co_problems = [p for p in all_problems if name in (p.companies or "").split(",")]
        cov_pct, touched, total = weighted_coverage(co_problems)

        score = round(0.5 * elo_pct + 0.5 * cov_pct) if total > 0 else round(elo_pct)

        # Weak topics for this company (biggest ELO gap vs target)
        topic_gaps = sorted([(t, target_elo - topic_elos.get(t, INITIAL_ELO)) for t in key_topics],
                            key=lambda x: x[1], reverse=True)
        weak = [t for t, gap in topic_gaps if gap > 80][:3]

        approx = max(0, int((target_elo - avg_elo) / 15)) if avg_elo < target_elo else 0
        label, color = score_label(score)
        companies_out[name] = {
            "score": score, "label": label, "color": color,
            "elo_pct": round(elo_pct), "coverage": round(cov_pct),
            "avg_elo": round(avg_elo), "elo_target": target_elo,
            "solved": touched, "total": total,
            "weak_topics": weak, "approx_problems": approx,
            "tier": profile["tier"],
            "summary": readiness_paragraph(score, weak, approx, name),
        }

    # Overall score
    overall_elo = user.overall_elo()
    overall_elo_pct = elo_component(overall_elo, 1500)
    overall_cov, total_touched, total_probs = weighted_coverage(all_problems)
    overall_score = round(0.5 * overall_elo_pct + 0.5 * overall_cov)

    practiced = [t for t, e in topic_elos.items() if e > INITIAL_ELO + 50]
    all_weak = sorted(topic_elos.items(), key=lambda x: x[1])
    overall_weak = [t for t, e in all_weak if e < INITIAL_ELO + 100][:3]
    approx_overall = max(0, int((1500 - overall_elo) / 15)) if overall_elo < 1500 else 0

    label, color = score_label(overall_score)
    return {
        "overall_score": overall_score, "overall_label": label, "overall_color": color,
        "overall_elo": round(overall_elo), "overall_coverage": round(overall_cov),
        "solved": total_touched, "total": total_probs,
        "practiced_topics": len(practiced), "total_topics": len(topic_elos),
        "weak_topics": overall_weak, "approx_problems": approx_overall,
        "summary": readiness_paragraph(overall_score, overall_weak, approx_overall),
        "companies": companies_out,
    }

# ── Problem Selector ────────────────────────────────────────────────────────
def select_next_problem(user_id, skipped_slugs=None):
    """Run problem selector directly (no subprocess)."""
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    try:
        from agent.problem_selector import get_user_profile, get_recommendation
        profile = get_user_profile(user_id)
        if not profile:
            return None
        # Remove non-serializable fields from profile
        clean_profile = {k: v for k, v in profile.items() if k != "solved_slugs"}
        problem, reason = get_recommendation(user_id, skipped_slugs=skipped_slugs)
        if not problem:
            return {"reason": reason, "profile": clean_profile}
        return {
            "title": problem.title,
            "slug": problem.slug,
            "difficulty": problem.difficulty.value if hasattr(problem.difficulty, 'value') else problem.difficulty,
            "topics": problem.topics,
            "companies": problem.companies,
            "pattern_hint": problem.pattern_hint,
            "leetcode_url": problem.leetcode_url,
            "reason": reason,
            "profile": clean_profile,
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return None

# ── Flask App ───────────────────────────────────────────────────────────────
app = Flask(__name__)

@app.route("/")
@require_auth
def index():
    db = get_db()
    users = db.query(User).all()
    return render_template("index.html", users=users, token=request.args.get("token",""))

@app.route("/user/<int:user_id>")
@require_auth
def user_dashboard(user_id):
    db = get_db()
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        return "User not found", 404

    # Topic ELOs
    topic_elos = db.query(TopicElo).filter_by(user_id=user_id).order_by(TopicElo.elo).all()

    # Recent attempts
    attempts = (
        db.query(Attempt, Problem)
        .join(Problem)
        .filter(Attempt.user_id == user_id)
        .order_by(Attempt.created_at.desc())
        .limit(20)
        .all()
    )

    # Solved count
    solved_count = db.query(Attempt).filter_by(user_id=user_id, solved=True).count()
    giveups = db.query(Attempt).filter_by(user_id=user_id, gave_up=True).count()

    # Top topics (highest ELO)
    strong_topics = sorted(topic_elos, key=lambda x: x.elo, reverse=True)[:3]
    weak_topics = sorted(topic_elos, key=lambda x: x.elo)[:3]

    overall = user.overall_elo()
    skill = topic_from_elo(overall)

    return render_template("user_dashboard.html",
        user=user, topic_elos=topic_elos, attempts=attempts,
        solved_count=solved_count, giveups=giveups,
        strong_topics=strong_topics, weak_topics=weak_topics,
        overall_elo=round(overall), skill=skill,
        token=request.args.get("token",""),
        min_elo=MIN_ELO, max_elo=MAX_ELO,
        topic_from_elo=topic_from_elo
    )

@app.route("/api/recommend/<int:user_id>")
@require_auth
def api_recommend(user_id):
    skipped = [s for s in request.args.get("skipped", "").split(",") if s]
    result = select_next_problem(user_id, skipped_slugs=skipped)
    if result:
        return jsonify(result)
    return jsonify({"error": "Could not generate recommendation"}), 500

@app.route("/api/log_attempt/<int:user_id>", methods=["POST"])
@require_auth
def api_log_attempt(user_id):
    db = get_db()
    data = request.json
    slug = data.get("slug")
    attempts_count = int(data.get("attempts_count", 1))
    time_minutes = int(data.get("time_minutes", 0))
    gave_up = bool(data.get("gave_up", False))
    solved = bool(data.get("solved", False))
    with_help = bool(data.get("with_help", False))

    problem = db.query(Problem).filter_by(slug=slug).first()
    if not problem:
        return jsonify({"error": "Problem not found"}), 404

    # Get primary topic (first listed)
    primary_topic = (problem.topics.split(",")[0] if problem.topics else "arrays")

    # Get current ELO
    te = db.query(TopicElo).filter_by(user_id=user_id, topic=primary_topic).first()
    elo_before = te.elo if te else INITIAL_ELO

    # Calculate delta — scaled by difficulty
    difficulty_str = problem.difficulty.value if hasattr(problem.difficulty, 'value') else str(problem.difficulty)
    delta = compute_elo_delta(difficulty_str, attempts_count, time_minutes, gave_up, solved, with_help)

    elo_after = update_elo(user_id, primary_topic, delta)

    # Log attempt
    attempt = Attempt(
        user_id=user_id,
        problem_id=problem.id,
        attempts_count=attempts_count,
        time_minutes=time_minutes,
        gave_up=gave_up,
        solved=solved,
        with_help=with_help,
        elo_before=elo_before,
        elo_after=elo_after,
    )
    db.add(attempt)
    db.commit()

    rating = time_rating(difficulty_str, time_minutes) if solved and not with_help else None
    return jsonify({
        "elo_before": elo_before,
        "elo_after": elo_after,
        "delta": delta,
        "new_level": topic_from_elo(elo_after),
        "rating": rating,
        "with_help": with_help,
    })

@app.route("/api/readiness/<int:user_id>")
@require_auth
def api_readiness(user_id):
    result = compute_readiness(user_id)
    if not result:
        return jsonify({"error": "User not found"}), 404
    return jsonify(result)

@app.route("/api/problems")
@require_auth
def api_problems():
    db = get_db()
    difficulty = request.args.get("difficulty")
    topic = request.args.get("topic")

    q = db.query(Problem)
    if difficulty:
        q = q.filter_by(difficulty=Difficulty[difficulty.upper()])
    if topic:
        q = q.filter(Problem.topics.contains(topic))

    problems = q.order_by(Problem.importance.desc()).all()
    return jsonify([{
        "title": p.title,
        "slug": p.slug,
        "difficulty": p.difficulty.value,
        "topics": p.topics,
        "companies": p.companies,
        "importance": p.importance,
        "leetcode_url": p.leetcode_url,
        "pattern_hint": p.pattern_hint,
    } for p in problems])

@app.route("/api/profile/<int:user_id>")
@require_auth
def api_profile(user_id):
    db = get_db()
    user = db.query(User).filter_by(id=user_id).first_or_404()
    topic_elos = db.query(TopicElo).filter_by(user_id=user_id).all()

    solved = db.query(Attempt).filter_by(user_id=user_id, solved=True).count()
    giveups = db.query(Attempt).filter_by(user_id=user_id, gave_up=True).count()

    return jsonify({
        "name": user.name,
        "overall_elo": round(user.overall_elo()),
        "skill_level": topic_from_elo(user.overall_elo()),
        "topic_elos": {t.topic: t.elo for t in topic_elos},
        "solved": solved,
        "giveups": giveups,
    })

@app.route("/api/leaderboard")
@require_auth
def api_leaderboard():
    db = get_db()
    users = db.query(User).all()
    rows = []
    for u in users:
        solved = db.query(Attempt).filter_by(user_id=u.id, solved=True).count()
        rows.append({
            "id": u.id,
            "name": u.name,
            "elo": round(u.overall_elo()),
            "level": topic_from_elo(u.overall_elo()),
            "solved": solved,
        })
    rows.sort(key=lambda x: x["elo"], reverse=True)
    return jsonify(rows)

@app.route("/health")
def health():
    return {"status": "ok", "time": datetime.now().isoformat()}

if __name__ == "__main__":
    threading.Thread(target=lambda: None, daemon=True).start()
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  💪 code-gym → http://localhost:5051")
    print(f"     Token: {AUTH_TOKENS[0]}")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"🚀 CodeGym running → http://localhost:5051")
    app.run(host="0.0.0.0", port=5051, debug=False, threaded=True)
