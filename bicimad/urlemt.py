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
        pattern = r'href="(/getattachment/[a-zA-Z0-9\-]+/trips_\d{2}_\d{2}_[A-Za-z]+-csv\.aspx)"'
        links = set(re.findall(pattern, html_text))
        full_links = {f"{UrlEMT.EMT}{link}" for link in links}
        return full_links

    def select_valid_urls(self) -> Set[str]:
        url = f"{UrlEMT.EMT}{UrlEMT.GENERAL}"
        response = requests.get(url)
        if response.status_code != 200:
            raise ConnectionError("Error al conectar con el servidor de la EMT.")
        self._valid_urls = self.get_links(response.text)
        return self._valid_urls

    def get_url(self, month: int, year: int) -> str:
        if month < 1 or month > 12 or year < 21 or year > 23:
            raise ValueError("Mes o año fuera de rango (mes: 1-12, año: 21-23).")
        month_str = f"{month:02d}"
        year_str = f"{year:02d}"
        for url in self._valid_urls:
            if f"trips_{year_str}_{month_str}" in url:
                return url
        raise ValueError("No se encontró un enlace válido para el mes y año especificados.")

    def get_csv(self, month: int, year: int) -> TextIO:
        url = self.get_url(month, year)
        print(f"Descargando archivo desde: {url}")

        response = requests.get(url)
        if response.status_code != 200:
            raise ConnectionError("Error al descargar el archivo CSV.")

        zip_file = zipfile.ZipFile(io.BytesIO(response.content))
        csv_filename = [name for name in zip_file.namelist() if name.endswith('.csv')][0]
        with zip_file.open(csv_filename) as csv_file:
            csv_text = io.StringIO(csv_file.read().decode('utf-8'))

        print("Archivo CSV descargado exitosamente.")
        return csv_text
