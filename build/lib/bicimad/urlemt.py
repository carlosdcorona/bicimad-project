import re
import requests
import zipfile
import io
from typing import Set, TextIO


class UrlEMT:
    EMT = 'https://opendata.emtmadrid.es'
    GENERAL = "/Datos-estaticos/Datos-generales-(1)"

    def __init__(self):
        """
        Inicializa un objeto de la clase UrlEMT.

        Attributes:
        - _valid_urls (set): Conjunto de enlaces válidos desde la página de la EMT.
        """
        self._valid_urls = set()

    @staticmethod
    def get_links(html_text: str) -> Set[str]:
        """
        Extrae todos los enlaces que coinciden con el patrón de datos de uso de bicicletas.

        Parameters:
        - html_text (str): Texto HTML de la página de la EMT.

        Returns:
        - Set[str]: Conjunto de enlaces absolutos válidos.
        """
        pattern = r'href="(/getattachment/[a-zA-Z0-9\-]+/trips_\d{2}_\d{2}_[A-Za-z]+\.csv)"'
        links = set(re.findall(pattern, html_text))
        full_links = {f"https://opendata.emtmadrid.es{link}" for link in links}
        return full_links

    def select_valid_urls(self) -> None:
        """
        Actualiza el conjunto de enlaces válidos desde la página de EMT. Si la petición falla, lanza una ConnectionError.
        """
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
        """
        Obtiene el enlace correspondiente al mes y año especificados.

        Parameters:
        - month (int): Mes en formato numérico (1-12).
        - year (int): Año en formato numérico corto (21-23).

        Returns:
        - str: La URL correspondiente al mes y año.

        Raises:
        - ValueError: Si el mes o año están fuera de rango o si no existe un enlace válido para la fecha especificada.
        """
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
        """
        Descarga y extrae el archivo CSV correspondiente al mes y año especificados.

        Parameters:
        - month (int): Mes en formato numérico (1-12).
        - year (int): Año en formato numérico corto (21-23).

        Returns:
        - TextIO: Archivo CSV en formato de texto.

        Raises:
        - ValueError: Si no existe un enlace válido para la fecha especificada.
        - ConnectionError: Si la petición de descarga falla.
        """
        url = self.get_url(month, year)
        try:
            response = requests.get(url)
            response.raise_for_status()
            zip_file = zipfile.ZipFile(io.BytesIO(response.content))
            csv_filename = [name for name in zip_file.namelist() if name.endswith('.csv')][0]
            return io.StringIO(zip_file.read(csv_filename).decode('utf-8'))
        except requests.RequestException as e:
            raise ConnectionError("Error al descargar el archivo CSV") from e
