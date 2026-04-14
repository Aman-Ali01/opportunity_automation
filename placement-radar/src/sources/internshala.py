import requests
from bs4 import BeautifulSoup
from src.sources.base import BaseSource
from src.utils.logger import logger

class InternshalaSource(BaseSource):
    @property
    def source_name(self):
        return "Internshala"

    def fetch(self):
        """
        Scrape software engineering internships from Internshala.
        """
        items = []
        try:
            # We target the software-engineering-internships page
            url = "https://internshala.com/internships/software-engineering-internships/"
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                # Internshala typically wraps internships in divs with class 'internship_meta'
                job_elements = soup.find_all("div", class_="internship_meta")
                
                for job in job_elements:
                    title_elem = job.find("h3", class_="job-title-href")
                    if not title_elem:
                        # fallback if they change class names
                        title_elem = job.find("a", class_="view_detail_button")
                        
                    company_elem = job.find("a", class_="link_display_like_text")
                    
                    if title_elem and title_elem.text.strip():
                        title = title_elem.text.strip()
                        company = company_elem.text.strip() if company_elem else "Unknown Company"
                        link = title_elem.get("href", "")
                        
                        full_title = f"{title} at {company}"
                        full_link = f"https://internshala.com{link}" if link.startswith("/") else link
                        
                        items.append({
                            "title": full_title,
                            "link": full_link,
                            "source": self.source_name
                        })
            else:
                logger.warning(f"Internshala returned status {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error fetching from {self.source_name}: {e}")
            
        return items
