import json
import os
from src.utils.logger import logger

class Deduplicator:
    def __init__(self, file_path):
        self.file_path = file_path
        self.seen_links = set()
        self._load()

    def _load(self):
        """Load already seen links from the JSON file."""
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    self.seen_links = set(data)
                except json.JSONDecodeError:
                    logger.warning("Failed to decode seen.json. Initializing an empty set.")
                    self.seen_links = set()
        else:
            self.seen_links = set()

    def is_new(self, link):
        """Returns True if the link hasn't been seen before."""
        return link not in self.seen_links

    def mark_seen(self, link):
        """Add link to the seen set."""
        self.seen_links.add(link)

    def save(self):
        """Persist the set back to the JSON file."""
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(list(self.seen_links), f, indent=2)
            
        logger.info(f"Saved {len(self.seen_links)} links to {self.file_path}")
