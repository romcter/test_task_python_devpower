import aiohttp
from bs4 import BeautifulSoup

class DataFetcher:
    WIKIPEDIA_URL = "https://en.wikipedia.org/w/index.php?title=List_of_countries_by_population_(United_Nations)&oldid=1215058959"
    STATISTICSTIMES_URL = "https://statisticstimes.com/demographics/countries-by-population.php"

    def __init__(self, source: str):
        self.source = source.lower()

    async def fetch_data(self) -> list[dict]:
        async with aiohttp.ClientSession() as session:
            if self.source == "wikipedia":
                return await self._fetch_wikipedia(session)
            elif self.source == "statisticstimes":
                return await self._fetch_statisticstimes(session)
            else:
                raise ValueError(f"Unknown data source: {self.source}")

    async def _fetch_wikipedia(self, session: aiohttp.ClientSession) -> list[dict]:
        async with session.get(self.WIKIPEDIA_URL) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find("table", {"class": "wikitable"})
            rows = table.find_all("tr")[2:]
            countries = []
            for row in rows:
                cells = row.find_all("td")
                if len(cells) < 5:
                    continue
                name = cells[0].text.strip()
                pop_text = cells[2].text.strip().replace(",", "")
                population = int(pop_text) if pop_text != "N/A" else 0
                region = cells[4].text.strip()
                subregion = cells[3].text.strip()
                countries.append({
                    "name": name,
                    "population": population,
                    "region": region,
                    "subregion": subregion
                })
            return countries

    async def _fetch_statisticstimes(self, session: aiohttp.ClientSession) -> list[dict]:
        async with session.get(self.STATISTICSTIMES_URL) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find("table", {"id": "table_id"})
            rows = table.find_all("tr")[1:]
            countries = []
            for row in rows:
                cells = row.find_all("td")
                if len(cells) < 7:
                    continue
                name = cells[1].text.strip()
                pop_text = cells[2].text.strip().replace(",", "")
                population = int(pop_text) if pop_text != "N/A" else 0
                region = cells[6].text.strip()
                countries.append({
                    "name": name,
                    "population": population,
                    "region": region,
                    "subregion": None
                })
            return countries