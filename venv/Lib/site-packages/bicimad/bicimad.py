import requests
import zipfile
import io
import pandas as pd
from typing import TextIO


class BiciMad:
    def __init__(self, month: int, year: int, url: str = None):
        self.month = month
        self.year = year
        self.url = url
        self.data = self._load_data() if url else self.get_data(month, year)

    def _download_csv_from_zip(self) -> TextIO:
        response = requests.get(self.url)
        response.raise_for_status()
        zip_file = zipfile.ZipFile(io.BytesIO(response.content))
        csv_filename = [name for name in zip_file.namelist() if name.endswith('.csv')][0]
        with zip_file.open(csv_filename) as csv_file:
            csv_text = io.StringIO(csv_file.read().decode('utf-8'))
        return csv_text

    @staticmethod
    def get_data(month: int, year: int) -> pd.DataFrame:
        from bicimad.urlemt import UrlEMT
        url_emt = UrlEMT()
        url_emt.select_valid_urls()
        csv_file = url_emt.get_csv(month, year)

        try:
            columns_of_interest = [
                'idBike', 'fleet', 'trip_minutes', 'geolocation_unlock', 'address_unlock',
                'unlock_date', 'locktype', 'unlocktype', 'geolocation_lock', 'address_lock',
                'lock_date', 'station_unlock', 'unlock_station_name', 'station_lock', 'lock_station_name'
            ]
            df = pd.read_csv(
                csv_file,
                sep=';',
                parse_dates=['unlock_date', 'lock_date'],
                index_col='unlock_date',
                usecols=columns_of_interest
            )
        except Exception as e:
            print("Error al cargar el archivo CSV:", e)
            return pd.DataFrame()
        return df

    def clean_data(self):
        self.data.dropna(how='all', inplace=True)
        for col in ['fleet', 'idBike', 'station_lock', 'station_unlock']:
            self.data[col] = self.data[col].astype(str)

    def count_unlocked_no_lock(self) -> int:
        """Cuenta las bicicletas desbloqueadas en una estación sin bloqueo registrado."""
        unlocked_no_lock = self.data[
            (self.data['station_unlock'].notna()) & (self.data['station_lock'].isna())
            ]
        return len(unlocked_no_lock)

    def filter_regular_fleet(self) -> pd.DataFrame:
        """Filtra las bicicletas de tipo de flota '1'."""
        self.data['fleet'] = pd.to_numeric(self.data['fleet'], errors='coerce').astype('Int64')
        return self.data[self.data['fleet'] == 1]

    def day_time_usage(self) -> pd.Series:
        daily_minutes = self.data['trip_minutes'].groupby(self.data.index.date).sum()
        daily_hours = daily_minutes / 60
        daily_hours.index = pd.to_datetime(daily_hours.index)
        return daily_hours

    def weekday_time_usage(self) -> pd.Series:
        day_map = {0: 'L', 1: 'M', 2: 'X', 3: 'J', 4: 'V', 5: 'S', 6: 'D'}
        self.data['weekday'] = self.data.index.dayofweek.map(day_map)
        weekly_minutes = self.data.groupby('weekday')['trip_minutes'].sum()
        return weekly_minutes / 60

    def total_usage_by_day(self) -> pd.Series:
        daily_usage = self.data.groupby(self.data.index.date).size()
        daily_usage.index = pd.to_datetime(daily_usage.index)
        return daily_usage

    def total_usage_by_date_and_station(self) -> pd.DataFrame:
        usage_by_date_station = self.data.groupby([pd.Grouper(freq="1D"), 'station_unlock']).size()
        usage_by_date_station = usage_by_date_station.reset_index(name='total_usos')
        return usage_by_date_station

    def most_popular_stations(self) -> set:
        station_usage = self.data.groupby('address_unlock').size()
        max_usage = station_usage.max()
        return set(station_usage[station_usage == max_usage].index)

    def usage_from_most_popular_station(self) -> int:
        station_usage = self.data.groupby('address_unlock').size()
        max_usage = station_usage.max()
        return station_usage[station_usage == max_usage].sum()

    def resume(self) -> pd.Series:
        if self.data.empty:
            print("El DataFrame está vacío. No se puede generar un resumen.")
            return pd.Series()
        total_uses = len(self.data)
        total_time = self.data['trip_minutes'].sum()
        popular_station = self.data['station_lock'].mode().iloc[0]
        uses_from_popular = (self.data['station_lock'] == popular_station).sum()
        return pd.Series({
            'year': self.year,
            'month': self.month,
            'total_uses': total_uses,
            'total_time': total_time,
            'most_popular_station': popular_station,
            'uses_from_most_popular': uses_from_popular
        })

    def __str__(self):
        return str(self.data)

