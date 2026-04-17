import requests
from bs4 import BeautifulSoup
from src.sources.base import BaseSource
from src.utils.logger import logger

class GitHubJobsSource(BaseSource):
    @property
    def source_name(self):
        return "GitHub"

    def fetch(self):
        """
        Search for popular repos matching our internship/job needs.
        We can use GitHub's API to search for newly created issues or repos.
        For simplicity and no-auth, we use GitHub Search API.
        Rate limits are 10 req/minute unauthenticated.
        """
        items = []
        try:
            # Look for recent repos or issues containing internship links
            # Searching issues in the past 7 days with keywords
            # e.g.: "internship 2025" or "off-campus placement"
            url = "https://api.github.com/search/issues"
            params = {
                "q": "internship OR hiring OR LFX OR \"open source\" state:open",
                "sort": "created",
                "order": "desc",
                "per_page": 10
            }
            
            headers = {
                "Accept": "application/vnd.github.v3+json"
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                for issue in data.get("items", []):
                    items.append({
                        "title": f"[{issue['repository_url'].split('/')[-1]}] {issue['title']}",
                        "link": issue["html_url"],
                        "source": self.source_name
                    })
            else:
                logger.warning(f"GitHub API returned status {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error fetching from {self.source_name}: {e}")
            
        return items
