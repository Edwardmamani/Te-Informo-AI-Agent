
import requests
from typing import Optional

class NewsSearchTool:
    def __init__(self):
        self.base_url = "https://scraper.rendoaltar.dev/api/search"
        self.default_max_results = 3

    def _run(self, query: str, max_results: Optional[int] = 3) -> str:
        """
        Esta petición puede demorar hasta 2 minutos en responder.
        """
        if max_results is None:
            max_results = self.default_max_results
        params = {
            "q": query,
            "max_results": max_results
        }
        response = requests.get(self.base_url, params=params, timeout=120)  # Hasta 2 min de espera
        response.raise_for_status()
        return str(response.json())
