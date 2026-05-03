"""
Problem Selector Agent
Reads user ELO profile and history, selects the optimal next problem.
Run from code-gym/ directory: PYTHONPATH=. python3 agent/problem_selector.py
"""
import json
import os
import sys
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # code-gym/
APP_DIR = os.path.join(BASE_DIR, "app")  # code-gym/app/
if APP_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)  # so 'app' package resolves

from app.database import get_session
from app.models import User, TopicElo, Attempt, Problem

# ── ELO helpers ────────────────────────────────────────────────────────────────
INITIAL_ELO = 1200
MIN_ELO, MAX_ELO = 800, 2400
TARGET_ELO_MINUS, TARGET_ELO_PLUS = 50, 150

_ELO_CFG = {
    "Easy":   dict(fast_attempts=1, fast_time=15, norm_attempts=2, norm_time=30,
                   win_fast=20,  win_norm=10, win_slow=5,  lose=-10),
    "Medium": dict(fast_attempts=1, fast_time=25, norm_attempts=3, norm_time=50,
                   win_fast=35,  win_norm=18, win_slow=8,  lose=-15),
    "Hard":   dict(fast_attempts=2, fast_time=45, norm_attempts=5, norm_time=90,
                   win_fast=50,  win_norm=25, win_slow=10, lose=-10),
}

def compute_elo_change(difficulty, attempts_count, time_minutes, gave_up, solved):
    cfg = _ELO_CFG.get(difficulty, _ELO_CFG["Medium"])
    if not solved:
        return cfg["lose"]
    if attempts_count <= cfg["fast_attempts"] and time_minutes <= cfg["fast_time"]:
        return cfg["win_fast"]
    if attempts_count <= cfg["norm_attempts"] and time_minutes <= cfg["norm_time"]:
        return cfg["win_norm"]
    return cfg["win_slow"]


def topic_from_elo(elo):
    if elo >= 1800: return "Master"
    if elo >= 1500: return "Advanced"
    if elo >= 1300: return "Intermediate"
    if elo >= 1100: return "Novice"
    return "Beginner"


def difficulty_from_elo(elo):
    if elo < 1000: return "Easy"
    if elo < 1300: return "Easy+Medium"
    if elo < 1600: return "Medium"
    if elo < 1900: return "Medium+Hard"
    return "Hard"


def get_user_profile(user_id):
    session = get_session()
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        return None

    topic_elos = {t.topic: t.elo for t in session.query(TopicElo).filter_by(user_id=user_id).all()}

    recent_attempts = (
        session.query(Attempt, Problem)
        .join(Problem)
        .filter(Attempt.user_id == user_id)
        .order_by(Attempt.created_at.desc())
        .limit(20)
        .all()
    )

    recent_problems = []
    for attempt, problem in recent_attempts:
        topics = problem.topics.split(",") if problem.topics else []
        recent_problems.append({
            "title": problem.title,
            "slug": problem.slug,
            "difficulty": problem.difficulty.value if hasattr(problem.difficulty, 'value') else problem.difficulty,
            "topics": topics,
            "solved": attempt.solved,
            "gave_up": attempt.gave_up,
            "attempts": attempt.attempts_count,
            "time_minutes": attempt.time_minutes,
            "elo_change": (attempt.elo_after or 0) - (attempt.elo_before or INITIAL_ELO),
        })

    solved = (
        session.query(Problem)
        .join(Attempt)
        .filter(Attempt.user_id == user_id, Attempt.solved == True)
        .all()
    )
    solved_slugs = {p.slug for p in solved}

    overall = user.overall_elo()

    return {
        "user_id": user_id,
        "user_name": user.name,
        "overall_elo": round(overall),
        "skill_level": topic_from_elo(overall),
        "topic_elos": topic_elos,
        "recent_problems": recent_problems,
        "solved_slugs": solved_slugs,
        "total_solved": len(solved_slugs),
    }


def get_recommendation(user_id, skipped_slugs=None):
    profile = get_user_profile(user_id)
    if not profile:
        return None, "No user found"

    session = get_session()
    excluded = profile["solved_slugs"] | set(skipped_slugs or [])

    # Weakest topics
    sorted_topics = sorted(profile["topic_elos"].items(), key=lambda x: x[1])
    weak_topics = [t for t, _ in sorted_topics[:3]]

    # No history → pick a high-importance Easy problem
    if not profile["topic_elos"]:
        fallback = (
            session.query(Problem)
            .filter_by(difficulty="Easy")
            .order_by(Problem.importance.desc())
            .first()
        )
        return fallback, "Welcome! Starting with an Easy classic."

    # Try to find unsolved, non-skipped problem in a weak topic
    for topic in weak_topics:
        user_elo = profile["topic_elos"].get(topic, INITIAL_ELO)

        unsolved_in_topic = (
            session.query(Problem)
            .filter(~Problem.slug.in_(excluded))
            .filter(Problem.topics.contains(topic))
            .order_by(Problem.importance.desc())
            .all()
        )

        if unsolved_in_topic:
            return unsolved_in_topic[0], f"Weak area: {topic} (ELO: {user_elo}). Focus here."

    # Fallback: any unsolved, non-skipped high-importance problem
    unsolved = (
        session.query(Problem)
        .filter(~Problem.slug.in_(excluded))
        .order_by(Problem.importance.desc())
        .first()
    )
    if unsolved:
        return unsolved, "All weak topics covered. High-importance problem next."

    # All non-skipped problems exhausted — ignore skips and try again
    if skipped_slugs:
        return get_recommendation(user_id, skipped_slugs=None)

    return None, "🎉 You've solved all seeded problems!"


def format_recommendation(profile, problem, reason):
    lines = [
        f"📊 *{profile['user_name']}'s Profile*",
        f"   Overall ELO: *{profile['overall_elo']}* ({profile['skill_level']})",
        f"   Solved: {profile['total_solved']} problems",
        "",
        f"🎯 *Next Problem Recommended*",
        "",
        f"📌 *{problem.title}*",
        f"   Difficulty: {problem.difficulty}",
        f"   Topics: {problem.topics}",
        f"   Companies: {problem.companies}",
        f"   Hint: {problem.pattern_hint}",
        f"   → https://leetcode.com/problems/{problem.slug}/",
        "",
        f"_Why: {reason}_",
    ]

    sorted_topics = sorted(profile["topic_elos"].items(), key=lambda x: x[1])[:3]
    if sorted_topics:
        lines.append("")
        lines.append("⚠️ *Weak areas:*")
        for topic, elo in sorted_topics:
            level = topic_from_elo(elo)
            lines.append(f"   {topic}: {elo} ({level})")

    return "\n".join(lines)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="CodeGym Problem Selector Agent")
    parser.add_argument("--user-id", type=int, default=1)
    parser.add_argument("--format", default="text", choices=["text", "json"])
    args = parser.parse_args()

    profile = get_user_profile(args.user_id)
    if not profile:
        print("User not found")
        sys.exit(1)

    problem, reason = get_recommendation(args.user_id)

    if args.format == "json":
        print(json.dumps({
            "profile": profile,
            "recommended_problem": {
                "title": problem.title if problem else None,
                "slug": problem.slug if problem else None,
                "difficulty": problem.difficulty if problem else None,
                "topics": problem.topics if problem else None,
                "companies": problem.companies if problem else None,
                "importance": problem.importance if problem else None,
                "pattern_hint": problem.pattern_hint if problem else None,
                "leetcode_url": problem.leetcode_url if problem else None,
            },
            "reason": reason,
        }, indent=2))
    else:
        print(format_recommendation(profile, problem, reason))
