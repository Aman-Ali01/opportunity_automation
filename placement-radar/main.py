import sys
from config import SEEN_FILE
from src.utils.logger import logger
from src.core.deduplicator import Deduplicator
from src.core.filters import filter_items
from src.notify.telegram import notify_all as notify_telegram
from src.notify.whatsapp import notify_all_whatsapp

# Import all sources
from src.sources.github import GitHubJobsSource
from src.sources.reddit import RedditSource
from src.sources.unstop import UnstopSource
from src.sources.internshala import InternshalaSource
from src.sources.linkedin import LinkedInJobsSource

def main():
    logger.info("Starting Placement Radar pipeline...")
    
    # Initialize components
    dedup = Deduplicator(SEEN_FILE)
    
    sources = [
        GitHubJobsSource(),
        RedditSource(),
        UnstopSource(),
        InternshalaSource(),
        LinkedInJobsSource()
    ]
    
    all_items = []
    
    # Step 1: Fetch from all sources
    for source in sources:
        logger.info(f"Fetching from {source.source_name}...")
        try:
            items = source.fetch()
            logger.info(f"Found {len(items)} items from {source.source_name}")
            all_items.extend(items)
        except Exception as e:
            logger.error(f"Source {source.source_name} completely failed: {e}")
            
    if not all_items:
        logger.info("No items fetched from any sources. Exiting.")
        sys.exit(0)
        
    # Step 2: Filter relevant items
    filtered_items = filter_items(all_items)
    
    # Step 3: Deduplicate
    new_items = []
    for item in filtered_items:
        if dedup.is_new(item.get("link", "")):
            new_items.append(item)
            
    logger.info(f"Found {len(new_items)} NEW relevant opportunities across all sources.")
    
    # Step 4: Notify & Record
    if new_items:
        # Send via Telegram
        notify_telegram(new_items)
        
        # Send via WhatsApp (CallMeBot)
        notify_all_whatsapp(new_items)
        
        # Only mark as seen if we successfully found them and potentially notified them
        # Alternatively, mark all as seen regardless of notification success
        # Here we mark all new_items as seen so we don't spam errors infinitely
        for item in new_items:
            if item.get("link"):
                dedup.mark_seen(item.get("link"))
                
        dedup.save()
    else:
        logger.info("No fresh items to notify.")
        
    logger.info("Pipeline run complete.")

if __name__ == "__main__":
    main()
