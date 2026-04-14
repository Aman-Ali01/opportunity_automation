import requests
import time
import urllib.parse
from config import CALLMEBOT_PHONE, CALLMEBOT_API_KEY
from src.utils.logger import logger

def format_whatsapp_message(item):
    """
    Formats the item dictionary into a string suitable for WhatsApp.
    Message format:
    🚀 *Title*
    🌐 _Source_
    🔗 Link
    """
    title = item.get('title', 'Unknown Title')
    source = item.get('source', 'Unknown Source')
    link = item.get('link', '#')
    
    # WhatsApp text formatting uses * for bold and _ for italics
    message = (
        f"🚀 *{title}*\n"
        f"🌐 _{source}_\n"
        f"🔗 {link}"
    )
    return message

def send_whatsapp_message(message, retries=3):
    """
    Sends a formatted message to WhatsApp using CallMeBot API.
    """
    if not CALLMEBOT_PHONE or not CALLMEBOT_API_KEY:
        logger.error("CallMeBot credentials missing. Skipping WhatsApp notification.")
        return False
        
    encoded_message = urllib.parse.quote(message)
    # The CallMeBot API endpoint requires phone and apikey parameters
    url = f"https://api.callmebot.com/whatsapp.php?phone={CALLMEBOT_PHONE}&text={encoded_message}&apikey={CALLMEBOT_API_KEY}"
    
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=15)
            
            # The CallMeBot API returns 200 on success, anything else means failure.
            # Sometimes their API might return 200 but text contains "Error"
            if response.status_code == 200 and "Message queued" in response.text or "Error" not in response.text:
                logger.info("Successfully sent message to WhatsApp via CallMeBot")
                # Sleep to respect CallMeBot API rate limits (avoid spam bans)
                time.sleep(2)
                return True
            else:
                logger.warning(f"CallMeBot returned an unexpected response: {response.text[:200]}")
                time.sleep(2 ** attempt)
        except requests.exceptions.RequestException as e:
            logger.warning(f"Attempt {attempt+1}/{retries} failed to send WhatsApp message: {e}")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                logger.error(f"Failed to send WhatsApp message after {retries} attempts.")
                return False

def notify_all_whatsapp(items):
    """
    Processes a list of items and sends them through WhatsApp.
    """
    success_count = 0
    for item in items:
        msg = format_whatsapp_message(item)
        if send_whatsapp_message(msg):
            success_count += 1
            
    logger.info(f"Successfully sent {success_count} out of {len(items)} items to WhatsApp")
    return success_count
