import requests
from src.sources.base import BaseSource
from src.utils.logger import logger

class UnstopSource(BaseSource):
    @property
    def source_name(self):
        return "Unstop"

    def fetch(self):
        """
        Fetch hackathons and internships from Unstop public API.
        The Unstop public API often changes but there is a search/opportunity endpoint.
        """
        items = []
        try:
            # Using their opportunities api endpoint
            # Type list: 1=quizzes, 2=hackathons, 3=scholarships, 4=internships, 5=jobs
            # We want internships(4), jobs(5), and hackathons(2)
            url = "https://unstop.com/api/public/opportunity/search-result"
            params = {
                "opportunity": "hackathons,internships,jobs,contest,challenge",
                "per_page": 15,
                "oppstatus": "open"
            }
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "application/json"
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                opportunities = data.get("data", {}).get("data", [])
                
                for opp in opportunities:
                    title = opp.get("title", "")
                    seo_url = opp.get("seo_url", "")
                    
                    if title and seo_url:
                        # Construct link based on opportunity type (or just rely on seo_url if it's the full slug)
                        # Usually Unstop URLs look like: unstop.com/hackathons/seo_url
                        # If seo_url already has the prefix, we just append to base
                        items.append({
                            "title": title,
                            "link": f"https://unstop.com/{seo_url}",
                            "source": self.source_name
                        })
            else:
                logger.warning(f"Unstop returned status {response.status_code}. Response: {response.text[:100]}")
                
        except Exception as e:
            logger.error(f"Error fetching from {self.source_name}: {e}")
            
        return items
