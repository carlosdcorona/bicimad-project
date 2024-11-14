import pandas as pd
from .urlemt import UrlEMT


class BiciMad:
    def __init__(self, month: int, year: int):
        self._month = month
        self._year = year
        self._data = self.get_data(month, year)

    @staticmethod
    def get_data(month: int, year: int) -> pd.DataFrame:
        url_emt = UrlEMT()
        url_emt._valid_urls = UrlEMT.select_valid_urls()
        csv_file = url_emt.get_csv(month, year)

        columns_of_interest = [
            'idBike', 'fleet', 'trip_minutes', 'geolocation_unlock', 'address_unlock',
            'unlock_date', 'locktype', 'unlocktype', 'geolocation_lock', 'address_lock',
            'lock_date', 'station_unlock', 'unlock_station_name', 'station_lock', 'lock_station_name'
        ]

        df = pd.read_csv(
            csv_file,
            sep=';',
            parse_dates=['unlock_date'],
            usecols=columns_of_interest
        )
        df.set_index('unlock_date', inplace=True)
        return df

    @property
    def data(self):
        return self._data

    def clean(self):
        self._data.dropna(how="all", inplace=True)
        for col in ['fleet', 'idBike', 'station_lock', 'station_unlock']:
            self._data[col] = self._data[col].astype(str)

    def resume(self):
        return pd.Series({
            'year': self._year,
            'month': self._month,
            'total_uses': len(self._data),
            'total_time': self._data['trip_minutes'].sum() / 60,
            'most_popular_station': self._data['address_unlock'].mode()[0] if not self._data[
                'address_unlock'].mode().empty else None,
            'uses_from_most_popular': self._data['address_unlock'].value_counts().max()
        })
