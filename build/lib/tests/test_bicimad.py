import unittest
import pandas as pd
from bicimad.bicimad import BiciMad


class TestBiciMad(unittest.TestCase):

    def setUp(self):
        """
        Configuración inicial para los tests.
        Crea una instancia de BiciMad en modo de prueba para evitar dependencias de datos externos.
        """
        self.bicimad = BiciMad(month=2, year=23, test_mode=True)

    def test_get_data(self):
        """
        Verifica que el método get_data en modo de prueba devuelve un DataFrame válido y no vacío.
        """
        self.assertIsInstance(self.bicimad.data, pd.DataFrame, "El atributo data debe ser un DataFrame.")
        self.assertFalse(self.bicimad.data.empty, "El DataFrame de datos no debe estar vacío en modo de prueba.")

    def test_clean(self):
        """
        Verifica que el método clean elimina correctamente las filas con todos los valores NaN
        y convierte las columnas especificadas a tipo str.
        """
        # Insertar una fila con valores NaN para probar su eliminación
        nan_row = pd.DataFrame([[None] * len(self.bicimad.data.columns)], columns=self.bicimad.data.columns)
        if not nan_row.dropna(how='all').empty:
            self.bicimad.data = pd.concat([self.bicimad.data, nan_row], ignore_index=True)

        # Aplicar limpieza
        self.bicimad.clean()

        # Verificar que no hay filas completamente NaN y que las columnas especificadas son de tipo str
        self.assertFalse(self.bicimad.data.isnull().all(axis=1).any(),
                         "No deben quedar filas con todos sus valores NaN.")
        self.assertEqual(self.bicimad.data['fleet'].dtype, 'object', "La columna 'fleet' debe ser de tipo str.")
        self.assertEqual(self.bicimad.data['idBike'].dtype, 'object', "La columna 'idBike' debe ser de tipo str.")
        self.assertEqual(self.bicimad.data['station_lock'].dtype, 'object',
                         "La columna 'station_lock' debe ser de tipo str.")
        self.assertEqual(self.bicimad.data['station_unlock'].dtype, 'object',
                         "La columna 'station_unlock' debe ser de tipo str.")

    def test_resume(self):
        """
        Verifica que el método resume devuelva un resumen en formato Series con las etiquetas adecuadas
        y valores válidos en modo de prueba.
        """
        summary = self.bicimad.resume()

        # Verificar las etiquetas y que las claves están en el resumen
        expected_keys = ['year', 'month', 'total_uses', 'total_time', 'most_popular_station', 'uses_from_most_popular']
        for key in expected_keys:
            self.assertIn(key, summary, f"El resumen debe contener la clave '{key}'.")

        # Verificar que el resumen contiene datos válidos
        self.assertEqual(summary['year'], self.bicimad.year,
                         "El año en el resumen debe coincidir con el año del objeto.")
        self.assertEqual(summary['month'], self.bicimad.month,
                         "El mes en el resumen debe coincidir con el mes del objeto.")
        self.assertGreaterEqual(summary['total_uses'], 0, "El total de usos debe ser un número no negativo.")
        self.assertGreaterEqual(summary['total_time'], 0, "El total de tiempo debe ser un número no negativo.")

    def test_function_documentation(self):
        """
        Verifica que cada método público en la clase BiciMad tenga un docstring.
        """
        for method_name in dir(self.bicimad):
            method = getattr(self.bicimad, method_name)
            if callable(method) and not method_name.startswith("_"):
                self.assertIsNotNone(method.__doc__, f"El método {method_name} no tiene docstring.")


if __name__ == '__main__':
    unittest.main()

