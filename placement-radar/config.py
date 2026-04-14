import os
from dotenv import load_dotenv

# Load environment variables from .env file (for local runs)
load_dotenv()

# Telegram Configuration
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TELEGRAM_TOKEN or not CHAT_ID:
    print("Warning: TELEGRAM_TOKEN or CHAT_ID not fully configured in environment.")

# Filter Keywords
KEYWORDS = [
    "intern", "internship", "sde", "software", "developer", 
    "hackathon", "fellowship", "remote", "frontend", "backend", 
    "fullstack", "full-stack", "2025", "2026", "fresher", "grad"
]

# Database paths
SEEN_FILE = os.path.join(os.path.dirname(__file__), "data", "seen.json")
