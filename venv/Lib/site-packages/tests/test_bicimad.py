import unittest
import pandas as pd
from bicimad.bicimad import BiciMad

class TestBiciMad(unittest.TestCase):
    def test_get_data(self):
        bicimad = BiciMad(month=1, year=23)
        self.assertIsInstance(bicimad.data, pd.DataFrame)
        self.assertFalse(bicimad.data.empty, "El DataFrame no debería estar vacío con datos reales")

    def test_clean(self):
        bicimad = BiciMad(month=1, year=23)
        bicimad.clean()
        self.assertFalse(bicimad.data.isnull().all(axis=1).any())
        self.assertTrue(bicimad.data['fleet'].dtype == 'object')

    def test_resume(self):
        bicimad = BiciMad(month=1, year=23)
        summary = bicimad.resume()
        self.assertIn('total_uses', summary)
        self.assertIn('total_time', summary)
        self.assertIn('most_popular_station', summary)

if __name__ == '__main__':
    unittest.main()
