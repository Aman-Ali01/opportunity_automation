# Placement Radar - Setup & Walkthrough

I have implemented the complete **Placement Radar** system, spanning 5 distinct scrapers, normalizer/filter mechanics, duplicate tracking, and automated Telegram alerts.

> [!TIP]
> The system is currently scheduled to run every 2 hours via GitHub actions to strike a balance between speed and avoiding strict rate limit/IP bans from GitHub's runner networks. You can change this to 1 hour (`0 * * * *`) inside `.github/workflows/cron.yml` if you desire.

## Component Overview

1. **Sources module** (`src/sources/`):
   - `github.py`: Searches the official GitHub Issues search API for internship/fresher opportunities across all repositories.
   - `unstop.py`: Queries Unstop's public `search-result` JSON endpoint to fetch hackathons and internships bypassing traditional scraper blockers.
   - `linkedin.py`: Scrapes LinkedIn's guest job search API. Includes header-spoofing to avoid immediate blocks. 
   - `internshala.py`: Scrapes the dedicated software engineering internships page using `BeautifulSoup`.
   - `reddit.py`: Reads the open `.json` API wrapper over `r/developersIndia` and `r/cscareerquestions`.

2. **Smart Filters** (`src/core/filters.py`): Matches item titles against a configurable list of keywords in `config.py` (e.g., *SDE, Intern, Hackathon, 2025, Remote*).
3. **Data Storage** (`data/seen.json`): We use an embedded, auto-updated JSON array to keep track of already sent links preventing duplicate notifications.
4. **Notifier** (`src/notify/telegram.py`): Pushes formatted HTML links to your Telegram bot.
5. **Main Runner** (`main.py`): Triggers everything sequentially and gracefully skips failing sources.

> [!WARNING]
> While these scripts attempt to appear as legitimate browsers (using User-Agents), websites like *LinkedIn* and *Internshala* aggressively block commercial scraping. Occasional failures are common in these sites. The script uses robust `try/except` to prevent these from crashing the entire program.

---

## 🚀 How to Run Locally

### 1. Set Up Telegram Bot
1. Go to Telegram and search for **@BotFather**. Use `/newbot` to create your bot and get the `HTTP API Token`.
2. Open a chat with your new bot and send it a message like "Hello".
3. Get your chat ID: Go to `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates` and look for `"chat":{"id": <YOUR_CHAT_ID>}`.

### 2. Configure Local Environment
1. In `placement-radar`, create a `.env` file by copying the example:
   ```bash
   cd projects/automation/placement-radar
   cp .env.example .env
   ```
2. Update `.env` with the details from step 1:
   ```env
   TELEGRAM_TOKEN=your_token_from_botfather
   CHAT_ID=123456789
   ```

### 3. Run It!
Ensure you have the requirements, and then trigger the run:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

Check your Telegram—you will receive formatted links from the first successful scraping pass! 
Run `python main.py` again; you'll see it output `Found 0 NEW relevant opportunities` because it correctly populated `data/seen.json`.

---

## ☁️ How to Run 24/7 on GitHub Actions (100% Free)

We have packaged the `.github/workflows/cron.yml` to automate execution directly on GitHub infrastructure.

1. **Push your code** to a GitHub repository. 
2. Go to your GitHub repository -> **Settings** -> **Secrets and variables** -> **Actions** -> **New repository secret**.
   - Create `TELEGRAM_TOKEN` and paste your bot token.
   - Create `CHAT_ID` and paste your chat ID.
3. Your bot will now automatically run every 2 hours.
4. After every successful run, the bot will `git commit` the latest `seen.json` directly back into your repository to ensure memory permanence between jobs.

> [!IMPORTANT]
> Since GitHub Actions commits `seen.json` directly to the `master/main` branch, **always run `git pull`** before doing further development locally to prevent merge conflicts!

> [!TIP]
> **WhatsApp Forwarding**: On your Android phone, set up **Tasker**, **AutoResponder**, or **MacroDroid** to monitor Telegram notifications from your bot and automatically reply back to groups or WhatsApp contacts.
