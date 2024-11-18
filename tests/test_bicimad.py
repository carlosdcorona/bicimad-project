import unittest
import pandas as pd
from bicimad.bicimad import BiciMad

class TestBiciMad(unittest.TestCase):
    """
    Clase de prueba para la clase BiciMad.

    Esta clase contiene métodos para verificar que las funciones principales de la clase BiciMad
    funcionan como se espera, incluyendo la carga de datos, limpieza y generación de resúmenes.
    """

    def test_get_data(self):
        """
        Prueba para verificar que el método get_data carga un DataFrame válido.

        Comprueba que el atributo 'data' del objeto BiciMad sea un DataFrame no vacío.
        """
        bicimad = BiciMad(month=1, year=23)
        self.assertIsInstance(bicimad.data, pd.DataFrame, "El atributo 'data' debería ser un DataFrame.")
        self.assertFalse(bicimad.data.empty, "El DataFrame no debería estar vacío con datos reales.")

    def test_clean(self):
        """
        Prueba para verificar que el método clean realiza la limpieza correctamente.

        Comprueba que:
        - No existan filas con todos sus valores NaN después de la limpieza.
        - Las columnas 'fleet', 'idBike', 'station_lock' y 'station_unlock' sean del tipo de dato esperado.
        """
        bicimad = BiciMad(month=1, year=23)
        bicimad.clean()
        self.assertFalse(
            bicimad.data.isnull().all(axis=1).any(),
            "No debería haber filas con todos sus valores NaN después de la limpieza."
        )
        self.assertTrue(
            bicimad.data['fleet'].dtype == 'object',
            "La columna 'fleet' debería ser de tipo str después de la limpieza."
        )

    def test_resume(self):
        """
        Prueba para verificar que el método resume genera un resumen válido.

        Comprueba que el resumen generado sea una Serie con las claves esperadas,
        como 'total_uses', 'total_time', y 'most_popular_station'.
        """
        bicimad = BiciMad(month=1, year=23)
        summary = bicimad.resume()
        self.assertIn('total_uses', summary, "El resumen debería incluir 'total_uses'.")
        self.assertIn('total_time', summary, "El resumen debería incluir 'total_time'.")
        self.assertIn('most_popular_station', summary, "El resumen debería incluir 'most_popular_station'.")

if __name__ == '__main__':
    unittest.main()

