# ⚽⚡ agent-lab

A self-hosted coding & sports lab. Two services:

- **soccer-dashboard** — Serie A live standings, match results, scorer leaderboard, news feed, ML predictions
- **code-gym** — LeetCode trainer with ELO-based skill tracking and AI problem selector

---

## 🚀 Quick Start (Docker)

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/agent-lab.git
cd agent-lab
```

### 2. Start everything

```bash
docker-compose up --build -d
```

### 3. Find your URLs and tokens

```bash
docker-compose logs
```

Look for the startup banner — it prints the URLs and tokens for both services:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ⚽ soccer-dashboard → http://localhost:5050
     Token: soccer-Boris2026-SecretToken
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  💪 code-gym → http://localhost:5051
     Token: codegym-fr-2026
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 4. Open in browser

- ⚽ **soccer-dashboard** → `http://localhost:5050/?token=YOUR_TOKEN`
- 💪 **code-gym** → `http://localhost:5051/?token=YOUR_TOKEN`

---

## 🛠️ Common Tasks

### Check if services are running

```bash
docker-compose ps
```

### View logs (shows startup banner too)

```bash
docker-compose logs
```

### Stop services

```bash
docker-compose stop
```

### Restart services

```bash
docker-compose restart
```

### Rebuild after changes

```bash
docker-compose up --build -d
```

### Clean slate (remove everything)

```bash
docker-compose down -v
```

---

## 👥 For Your Sister (Cate)

```bash
# 1. Fork the repo on GitHub (click "Fork" on GitHub)

# 2. Clone her fork
git clone https://github.com/SISTER_USERNAME/agent-lab.git
cd agent-lab

# 3. Start
docker-compose up --build -d

# 4. Find tokens
docker-compose logs
```

Then open the URLs from the startup banner with the tokens shown.

To contribute:
```bash
git checkout -b add-new-feature
# ... make changes ...
git add .
git commit -m "Add amazing feature"
git push origin add-new-feature
# → Open a Pull Request on GitHub
```

---

## 🔒 Security Notes

- **Never commit `agent.env`** — it's in `.gitignore`
- **Token in URL** — fine for local use, not production-grade
- **Telegram bot token** — keep it private, rotate if exposed

---

## 📁 Project Structure

```
agent-lab/
├── docker-compose.yml          ← all services
├── .env.example               ← env template
├── .gitignore
│
├── projects/                  ← runnable projects
│   ├── soccer_dashboard/       ← ⚽ Serie A dashboard
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── soccer_dashboard.py
│   │   └── match_predictor.py
│   └── code-gym/               ← 💪 LeetCode trainer
│       ├── Dockerfile
│       ├── requirements.txt
│       ├── app/
│       │   ├── app.py
│       │   ├── models.py
│       │   ├── seed_data.py
│       │   └── templates/
│       └── agent/
│           └── problem_selector.py
│
├── concepts/                  ← agentic AI documentation
├── examples/                  ← Python code examples
├── experiments/               ← playground
├── resources/                 ← learning materials
└── issues/                    ← troubleshooting docs
```

---

_Built with 🦈 by Boris — agent-lab_