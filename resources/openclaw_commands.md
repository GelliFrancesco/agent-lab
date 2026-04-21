# OpenClaw — Comandi Utili

Raccolta di comandi OpenClaw per gestire agenti, sessioni, cron, e il gateway.

> Per tutti i comandi: `openclaw --help`
> Per help specifico: `openclaw <comando> --help`

---

## 🚀 Gateway

```bash
# Avviare il gateway
openclaw gateway start

# Status del gateway
openclaw status

# Riavviare il gateway
openclaw gateway restart

# Stoppare il gateway
openclaw gateway stop

# Verificare che il gateway sia raggiungibile
openclaw status
```

---

## 🤖 Agenti

```bash
# Lista tutti gli agenti configurati
openclaw agents list

# Aggiungere un nuovo agente isolato
openclaw agents add --name <nome> --workspace <path>

# Eliminare un agente
openclaw agents delete <agent-id>

# Vedere i bindings di routing
openclaw agents bindings

# Impostare identità (nome, emoji, theme)
openclaw agents set-identity <agent-id> --name "Boris" --emoji "🦈"
```

---

## 💬 Sessioni

```bash
# Lista sessioni attive (ultimi 30 minuti)
openclaw sessions list

# Lista sessioni filtrate per canale
openclaw sessions list --channel telegram

# Vedere cronologia di una sessione specifica
openclaw sessions history <session-key>

# Inviare un messaggio a una sessione
openclaw sessions send <session-key> --message "Ciao"
```

---

## ⏰ Cron Job

```bash
# Lista tutti i cron job
openclaw cron list

# Aggiungere un cron job
openclaw cron add --name "predictions" --schedule "0 8 * * 1,5" --task "python3 ~/predictions.py"

# Eliminare un cron job
openclaw cron delete <job-id>

# Testare un cron job manualmente
openclaw cron run <job-id>
```

---

## 🔌 Channels

```bash
# Configurare un canale (Telegram, Discord, etc.)
openclaw channels add telegram --bot-token <TOKEN>

# Lista canali configurati
openclaw channels list

# Status canale
openclaw channels status telegram
```

---

## 🔑 Pairing & Auth

```bash
# Lista pairing pendenti
openclaw pairing list

# Approvare un pairing
openclaw pairing approve telegram <CODE>

# Revocare un pairing
openclaw pairing revoke telegram <peer-id>
```

---

## 📋 Task & Subagents

```bash
# Lista task attivi
openclaw tasks list

# Vedere dettagli di un task
openclaw tasks get <task-id>

# Killare un task
openclaw tasks kill <task-id>

# Lista subagent attivi
openclaw subagents list
```

---

## 🛠️ Utility

```bash
# Backup
openclaw backup create

# Restore backup
openclaw backup restore <backup-id>

# Audit sicurezza locale
openclaw security audit

# Update OpenClaw
openclaw update

# Log in tempo reale
openclaw logs

# Cercare nei log
openclaw logs --grep "error"

# Ricaricare secretsruntime
openclaw secrets reload
```

---

## 🧠 Logs & Debug

```bash
# Tailing logs del gateway
openclaw logs

# Log con filtro
openclaw logs --grep "telegram" --level info

# Verificare configurazione
openclaw config show

# Validare config
openclaw config validate
```

---

## ⚙️ Configurazione

```bash
# Aprire il wizard di configurazione
openclaw configure

# Setup iniziale
openclaw setup

# Reset configurazione (WARNING: distrugge la config)
openclaw setup --reset

# Variabili d'ambiente
# Telegran bot token:
export TELEGRAM_BOT_TOKEN="..."
# Api key Anthropic:
export ANTHROPIC_API_KEY="sk-ant-..."
```

---

## 🔍 Links Utili

- Docs: https://docs.openclaw.ai
- Changelog: https://docs.openclaw.ai/changelog
- CLI reference: https://docs.openclaw.ai/cli
- Skill registry: https://clawhub.ai

---

*Generato: 2026-04-19*