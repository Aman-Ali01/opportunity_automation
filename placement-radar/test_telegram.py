from src.notify.telegram import notify_all
import sys
from config import TELEGRAM_TOKEN, CHAT_ID

if not TELEGRAM_TOKEN or not CHAT_ID:
    print("ERROR: TELEGRAM_TOKEN or CHAT_ID is missing in .env file!")
    sys.exit(1)

test_item = [
    {
        "title": "Test Internship at ACME Corp",
        "link": "https://example.com/test",
        "source": "Placement Radar Diagnostic"
    }
]

print("Sending test message to Telegram...")
success_count = notify_all(test_item)

if success_count > 0:
    print("✅ TEST SUCCESSFUL! Check your Telegram App for the message.")
else:
    print("❌ TEST FAILED. Check your bot token and chat ID.")
