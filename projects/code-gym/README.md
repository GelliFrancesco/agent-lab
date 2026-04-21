# Code Gym

A smart LeetCode trainer with ELO-based skill tracking and an AI agent that picks your next problem based on your weaknesses.

## Concept

Stop grinding random problems. Code Gym learns your weak spots and sends you the exact problem you need to level up — just like a personal coding coach.

**Core loop:**
1. Agent selects a problem matched to your skill level
2. You solve it → log attempts, time, whether you gave up
3. Your ELO per topic adjusts
4. Agent analyzes your gaps and picks the next challenge

## Architecture

```
code-gym/
├── app/
│   ├── app.py              ← Flask web app
│   ├── models.py           ← SQLAlchemy models
│   ├── database.py         ← DB setup
│   ├── seed_data.py        ← Curated problem set
│   └── routes.py           ← API routes
├── agent/
│   └── problem_selector.py ← AI subagent: picks next problem
├── migrations/             ← DB migrations
├── Dockerfile
├── requirements.txt
└── docker-compose.yml
```

## ELO System

| Event | ELO Change |
|-------|-----------|
| Solve quickly, 1 attempt | +30 |
| Solve, 2-3 attempts | +15 |
| Solve after hints/struggling | +5 |
| Give up | -20 |
| Too slow (>45min) | -10 |

**Starting ELO:** 1200 per topic  
**Provisional period:** First 3 problems per topic (ELO swings are doubled)

## Topic Tags

`arrays`, `strings`, `linked-lists`, `trees`, `graphs`, `dynamic-programming`, `binary-search`, `sorting`, `greedy`, `recursion`, `stacks`, `queues`, `heaps`, `tries`, `bit-manipulation`

## Problem Sources

1. **Curated seed list** (~100 hand-picked problems from top tech companies)
2. **LeetCode API** (future: auto-sync new problems)
3. **User can add problems manually**

## Agent Behavior

The agent reads:
- User's ELO per topic
- Recent problem history (what they struggled with)
- Solved vs. unsolved streak per topic

The agent recommends:
- "You're weak in Dynamic Programming — here's a medium that's exactly at your DP skill level"
- "You've been grinding strings — here's a tree problem to refresh"
- "You've been on a 3-problem streak in binary search — keep going or pivot?"

Agent delivers recommendations via:
- Dashboard "Next Problem" card
- Telegram notification (like the soccer dashboard)

## User Stories

- Francesco practices every evening → ELO climbs steadily
- Sister joins → separate profile, separate ELOs
- Francesco's agent notices weak graphs ELO → sends him a graphs problem
- Both Francesco and sister compete on weekly leaderboard (same problems, different ELOs)

## Tech Stack

- **Flask** — web UI
- **SQLite** — persistence (file-based, zero setup)
- **OpenClaw subagent** — problem selection intelligence
- **Telegram bot** — push notifications (reuse from soccer dashboard)

## Design Principles

- Minimal, dark UI — like a coding IDE
- Problems are the product — UI serves them
- Agent is the differentiator — not just a database of problems
- ELO is the scoreboard — visible progress, visible gaps