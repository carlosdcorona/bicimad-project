import pandas as pd


class BiciMad:
    def __init__(self, month: int, year: int, test_mode: bool = False):
        """
        Inicializa un objeto BiciMad.

        Parameters:
        - month (int): Mes en el que se desea obtener los datos.
        - year (int): Año en el que se desea obtener los datos.
        - test_mode (bool): Si es True, carga datos de prueba en lugar de datos reales.
        """
        self.month = month
        self.year = year
        if test_mode:
            # Datos de prueba para modo de test
            self.data = pd.DataFrame({
                'idBike': [1, 2],
                'fleet': ['A', 'B'],
                'trip_minutes': [15, 20],
                'geolocation_unlock': ['loc1', 'loc2'],
                'address_unlock': ['addr1', 'addr2'],
                'unlock_date': pd.to_datetime(['2023-02-01', '2023-02-02']),
                'locktype': ['type1', 'type2'],
                'unlocktype': ['type1', 'type2'],
                'geolocation_lock': ['loc3', 'loc4'],
                'address_lock': ['addr3', 'addr4'],
                'lock_date': pd.to_datetime(['2023-02-01', '2023-02-02']),
                'station_unlock': [101, 102],
                'unlock_station_name': ['Station1', 'Station2'],
                'station_lock': [201, 202],
                'lock_station_name': ['Station3', 'Station4'],
            })
        else:
            # Cargar los datos reales usando el método get_data
            self.data = self.get_data(month, year)

    @staticmethod
    def get_data(month: int, year: int) -> pd.DataFrame:
        """
        Método estático que obtiene los datos del mes y año especificados.

        Returns:
        - pd.DataFrame: DataFrame con los datos del mes y año especificados.
        """
        # Aquí agregarías la lógica para cargar los datos reales, por ejemplo, descargando de una fuente
        # Por simplicidad, retorna un DataFrame vacío si no está en modo de prueba
        return pd.DataFrame()

    @property
    def data(self) -> pd.DataFrame:
        """
        Acceso al atributo de datos.

        Returns:
        - pd.DataFrame: DataFrame con los datos de uso de bicicletas.
        """
        return self._data

    @data.setter
    def data(self, value: pd.DataFrame):
        """
        Establece el DataFrame para los datos de uso de bicicletas.

        Parameters:
        - value (pd.DataFrame): DataFrame con los datos.
        """
        self._data = value

    def clean(self):
        """
        Realiza la limpieza del DataFrame de datos. Modifica el DataFrame en lugar de retornar uno nuevo.
        - Elimina filas con todos sus valores NaN.
        - Convierte las columnas 'fleet', 'idBike', 'station_lock', y 'station_unlock' a tipo str.
        """
        self.data.dropna(how='all', inplace=True)
        self.data['fleet'] = self.data['fleet'].astype(str)
        self.data['idBike'] = self.data['idBike'].astype(str)
        self.data['station_lock'] = self.data['station_lock'].astype(str)
        self.data['station_unlock'] = self.data['station_unlock'].astype(str)

    def resume(self) -> pd.Series:
        """
        Resume los datos en una Serie con la siguiente información:
        - 'year': Año del dataset.
        - 'month': Mes del dataset.
        - 'total_uses': Total de usos en el mes.
        - 'total_time': Total de minutos usados en el mes.
        - 'most_popular_station': Estación de bloqueo más popular.
        - 'uses_from_most_popular': Cantidad de usos de la estación más popular.

        Returns:
        - pd.Series: Resumen de la información relevante.
        """
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
        """
        Representación informal del objeto, igual al método __str__ del DataFrame.
        """
        return str(self.data)
