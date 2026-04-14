import requests
from src.sources.base import BaseSource
from src.utils.logger import logger

class RedditSource(BaseSource):
    @property
    def source_name(self):
        return "Reddit"

    def fetch(self):
        """
        Fetch new posts from subreddits using Reddit's JSON endpoints.
        """
        items = []
        subreddits = ["developersIndia", "cscareerquestions"]
        
        # User agent is required for Reddit API to avoid 429 Too Many Requests
        headers = {
            "User-Agent": "PlacementRadar/1.0 (Automated job search scraper via Python)"
        }
        
        for sub in subreddits:
            url = f"https://www.reddit.com/r/{sub}/new.json?limit=15"
            try:
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    posts = data.get("data", {}).get("children", [])
                    for post in posts:
                        post_data = post.get("data", {})
                        title = post_data.get("title", "")
                        permalink = post_data.get("permalink", "")
                        
                        items.append({
                            "title": title,
                            "link": f"https://www.reddit.com{permalink}",
                            "source": f"{self.source_name} - r/{sub}"
                        })
                else:
                    logger.warning(f"Reddit /r/{sub} returned status {response.status_code}")
            except Exception as e:
                logger.error(f"Error fetching from {self.source_name} (r/{sub}): {e}")
                
        return items
