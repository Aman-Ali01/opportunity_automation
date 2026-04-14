import requests
import time
from config import TELEGRAM_TOKEN, CHAT_ID
from src.utils.logger import logger

def format_message(item):
    """
    Formats the item dictionary into a visually appealing string.
    Message format:
    🚀 Title
    🌐 Source
    🔗 Link
    """
    title = item.get('title', 'Unknown Title')
    source = item.get('source', 'Unknown Source')
    link = item.get('link', '#')
    
    message = (
        f"🚀 <b>{title}</b>\n"
        f"🌐 <i>{source}</i>\n"
        f"🔗 <a href='{link}'>Apply Here</a>"
    )
    return message

def send_telegram_message(message, retries=3):
    """
    Sends a formatted message to Telegram via the Bot API.
    Used HTML parse mode to allow bolding and links.
    """
    if not TELEGRAM_TOKEN or not CHAT_ID:
        logger.error("Telegram credentials missing. Skipping notification.")
        return False
        
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    
    for attempt in range(retries):
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info("Successfully sent message to Telegram")
            # To avoid hitting Telegram API rate limits (e.g. 30 messages/sec max)
            time.sleep(1)
            return True
        except requests.exceptions.RequestException as e:
            logger.warning(f"Attempt {attempt+1}/{retries} failed to send Telegram message: {e}")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                logger.error(f"Failed to send Telegram message after {retries} attempts.")
                return False

def notify_all(items):
    """
    Processes a list of items and sends them through Telegram.
    """
    success_count = 0
    for item in items:
        msg = format_message(item)
        if send_telegram_message(msg):
            success_count += 1
            
    logger.info(f"Successfully notified {success_count} out of {len(items)} items")
    return success_count
