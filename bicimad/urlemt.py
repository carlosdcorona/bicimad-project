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
        pattern = r'href="(/getattachment/[a-zA-Z0-9\-]+/trips_\d{2}_\d{2}_[A-Za-z]+\.csv)"'
        links = set(re.findall(pattern, html_text))
        full_links = {f"https://opendata.emtmadrid.es{link}" for link in links}
        return full_links

    def select_valid_urls(self) -> None:
        url = UrlEMT.EMT + UrlEMT.GENERAL
        try:
            response = requests.get(url)
            response.raise_for_status()
            links = UrlEMT.get_links(response.text)
            self._valid_urls = links
            if self._valid_urls:
                print("Enlaces válidos encontrados y almacenados.")
            else:
                print("No se encontraron enlaces válidos.")
        except requests.RequestException as e:
            raise ConnectionError("Error al acceder a la página de EMT") from e

    def get_url(self, month: int, year: int) -> str:
        if month < 1 or month > 12 or year < 21 or year > 23:
            raise ValueError("Mes o año fuera de rango (mes: 1-12, año: 21-23).")
        month_str = f"{month:02d}"
        year_str = f"{year:02d}"
        for url in self._valid_urls:
            if f"trips_{year_str}_{month_str}" in url:
                print(f"Enlace encontrado para {month}/{year}.")
                return url
        raise ValueError(f"No se encontró un enlace válido para el mes {month} y año {year}.")

    def get_csv(self, month: int, year: int) -> TextIO:
        url = self.get_url(month, year)
        response = requests.get(url)
        response.raise_for_status()
        zip_file = zipfile.ZipFile(io.BytesIO(response.content))
        csv_filename = [name for name in zip_file.namelist() if name.endswith('.csv')][0]
        return io.StringIO(zip_file.read(csv_filename).decode('utf-8'))
