import re
import requests
import zipfile
import io
from typing import Set, TextIO

class UrlEMT:
    EMT = 'https://opendata.emtmadrid.es'
    GENERAL = "/Datos-estaticos/Datos-generales-(1)"

    def __init__(self):
        self._valid_urls = set()

    @staticmethod
    def get_links(html_text: str) -> Set[str]:
        # Ajuste del patrón regex para capturar URLs relativas y hacerlas absolutas
        pattern = r'href="(/getattachment/[a-zA-Z0-9\-]+/trips_\d{2}_\d{2}_[A-Za-z]+-csv\.aspx)"'
        links = set(re.findall(pattern, html_text))
        full_links = {f"https://opendata.emtmadrid.es{link}" for link in links}
        print(f"Found {len(full_links)} URLs matching the pattern.")
        for link in full_links:
            print(f"Captured URL: {link}")
        return full_links

    @staticmethod
    def select_valid_urls() -> Set[str]:
        url = UrlEMT.EMT + UrlEMT.GENERAL
        try:
            print(f"Accessing URL: {url}")
            response = requests.get(url)
            response.raise_for_status()
            print("Successfully accessed the EMT page.")
            links = UrlEMT.get_links(response.text)
            if not links:
                print("No valid URLs were captured. The page structure or pattern might have changed.")
            else:
                print("Captured valid URLs:", links)
            return links
        except requests.RequestException as e:
            print("Error accessing the EMT page:", e)
            return set()

    def get_url(self, month: int, year: int) -> str:
        if month < 1 or month > 12 or year < 21 or year > 23:
            raise ValueError("Month or year out of range (month: 1-12, year: 21-23).")
        month_str = f"{month:02d}"
        year_str = f"{year:02d}"
        for url in self._valid_urls:
            if f"trips_{year_str}_{month_str}" in url:
                return url
        raise ValueError("No valid link found for the specified month and year.")

    def get_csv(self, month: int, year: int) -> TextIO:
        url = self.get_url(month, year)
        response = requests.get(url)
        response.raise_for_status()
        zip_file = zipfile.ZipFile(io.BytesIO(response.content))
        csv_filename = [name for name in zip_file.namelist() if name.endswith('.csv')][0]
        return io.StringIO(zip_file.read(csv_filename).decode('utf-8'))