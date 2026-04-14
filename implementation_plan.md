# Placement Radar Implementation Plan

This document outlines the architecture and implementation steps for building the Placement Radar system, a fully automated pipeline to discover and push job opportunities.

## Goal

Build a free, modular, and extendable Python system that fetches opportunities from Unstop, Internshala, LinkedIn, GitHub, and Reddit, filters them using smart heuristics, deduplicates them locally, and pushes notifications via the Telegram Bot API. The system will be scheduled to run every hour via GitHub Actions.

## Proposed Architecture & Structure

The codebase will be organized inside `placement-radar/` and divided into modular components:

### Core Configuration & Pipeline
- **`config.py`**: Loads environment variables (`TELEGRAM_TOKEN`, `CHAT_ID`) using `python-dotenv`.
- **`main.py`**: The orchestration script. Instantiates sources, aggregates results, applies filtering, deduplicates, and sends valid items via the notifier.

### Sources (`src/sources/`)
Each source will expose a `fetch()` function that returns a standard list of dictionaries: `{"title": str, "link": str, "source": str}`.
- **`unstop.py`**: Scrapes Unstop for hackathons/contests (using RSS or public APIs if available, or basic web scraping).
- **`internshala.py`**: Scrapes Internshala for software-related internships.
- **`linkedin.py`**: Uses basic HTTP requests to fetch LinkedIn jobs (e.g., via their guest jobs search endpoint).
- **`github.py`**: Searches GitHub API for hiring/internship issues or repos.
- **`reddit.py`**: Reads `r/developersIndia` and `r/cscareerquestions` using Reddit's open `.json` endpoints (no API auth required).

### Core Logic (`src/core/`)
- **`filters.py`**: Implements smart filtering using keywords (configurable list of keywords like "intern", "sde", "hackathon", "remote", "2025", "2026"). Allows scoring/ranking mechanisms.
- **`deduplicator.py`**: Reads from and writes to `data/seen.json`. Ensures that `is_new(link)` checks are efficient (set-based processing).

### Notifications (`src/notify/`)
- **`telegram.py`**: Implements the Telegram Bot API client. Includes formatting logic (HTML/Markdown, emojis) and uses retry-logic for robustness. WhatsApp forwarding relies on the user's local Tasker/AutoResponder setup triggered by these Telegram notifications.

### Utilities (`src/utils/`)
- **`logger.py`**: Common logging configuration to output pipeline statuses and error messages cleanly.

### Deployment & Infra
- **`.github/workflows/cron.yml`**: GitHub Actions workflow. Runs `main.py` on ```cron: '0 * * * *'```. Uses repository secrets for `TELEGRAM_TOKEN` and `CHAT_ID`, and commits back the updated `data/seen.json` via the GitHub Action bot.
- **`requirements.txt`**: Project dependencies (`requests`, `beautifulsoup4`, `python-dotenv`).

## Open Questions

> [!IMPORTANT]
> **Scraping Protections**: Sites like LinkedIn and Internshala often block aggressive scraping. I will implement basic unauthenticated scraping/RSS/JSON fallbacks. In production, these might occasionally fail or require proxies if blocked by the hosting provider's IP range (e.g. GitHub Action runner IPs). I will add robust `try-except` blocks to ensure one failing source does not stop the entire pipeline. Is this acceptable?

> [!WARNING]
> **GitHub Actions Committing Data**: To maintain `data/seen.json` across GitHub Actions runs, the workflow must commit changes back to the repository after every run. This means your Git history will have an automated commit every hour. Is this acceptable, or would you prefer me to disable the auto-commit and just print duplicate logs for local tracking initially? (I will proceed with auto-commit as it is a common pattern for 100% free scraping setups).

## Verification Plan

### Automated Tests/Checks
- Perform a local dry-run without Telegram token to verify that scraping, normalization, filtering, and deduplication logic behave correctly.
- Verify `seen.json` captures hashes/links properly.
- Ensure logging correctly identifies failures and skips them gracefully.

### Manual Verification
- You will be provided with instructions to cd into `placement-radar`, set `.env` with actual Telegram Bot details, and run `python main.py` locally to see live Telegram messages.
- Add workflow to GitHub repository to verify the Action executes correctly.
