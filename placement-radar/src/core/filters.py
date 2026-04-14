import re
from config import KEYWORDS
from src.utils.logger import logger

def is_relevant(item, keywords=KEYWORDS):
    """
    Checks if a given opportunity item matches the desired keywords.
    item is a dict containing {"title": ..., "link": ..., "source": ...}
    We'll do a simple case-insensitive regex search against the title.
    """
    title = item.get("title", "").lower()
    
    # If no keywords are provided, assume everything is relevant
    if not keywords:
        return True

    # Check if any keyword is present in the title
    for kw in keywords:
        # Match keyword as distinct word or part of it
        if kw.lower() in title:
            return True
        
    return False

def filter_items(items):
    """
    Filters a list of items based on relevance.
    """
    filtered = []
    for item in items:
        if is_relevant(item):
            filtered.append(item)
    
    if len(items) > 0:
        logger.info(f"Filtering kept {len(filtered)} out of {len(items)} items from {items[0].get('source') if items else 'Unknown'}")
        
    return filtered
