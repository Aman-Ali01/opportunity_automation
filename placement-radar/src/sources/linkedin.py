import requests
import urllib.parse
from bs4 import BeautifulSoup
from src.sources.base import BaseSource
from src.utils.logger import logger

class LinkedInJobsSource(BaseSource):
    @property
    def source_name(self):
        return "LinkedIn"

    def fetch(self):
        """
        Scrape LinkedIn guest jobs search endpoint.
        This endpoint often changes and can rate-limit heavily, 
        so we wrap it in safety mechanisms.
        """
        items = []
        try:
            keywords = urllib.parse.quote("software engineer OR intern OR developer OR LFX OR placement OR research")
            location = urllib.parse.quote("India OR Remote")
            url = f"https://www.linkedin.com/jobs/search?keywords={keywords}&location={location}&f_TPR=r86400&position=1&pageNum=0"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept-Language": "en-US,en;q=0.9",
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                job_cards = soup.find_all("div", class_="base-card")
                
                for job in job_cards:
                    title_elem = job.find("h3", class_="base-search-card__title")
                    link_elem = job.find("a", class_="base-card__full-link")
                    company_elem = job.find("h4", class_="base-search-card__subtitle")
                    
                    if title_elem and link_elem:
                        title = title_elem.text.strip()
                        company = company_elem.text.strip() if company_elem else ""
                        link = link_elem.get("href", "").split("?")[0] # remove tracking params
                        
                        full_title = f"{title} at {company}" if company else title
                        
                        items.append({
                            "title": full_title,
                            "link": link,
                            "source": self.source_name
                        })
            else:
                logger.warning(f"LinkedIn returned status {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error fetching from {self.source_name}: {e}")
            
        return items
