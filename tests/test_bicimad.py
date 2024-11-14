import unittest
import pandas as pd
from bicimad.bicimad import BiciMad

class TestBiciMad(unittest.TestCase):
    def test_get_data(self):
        bicimad = BiciMad(month=2, year=23, test_mode=True)
        self.assertIsInstance(bicimad.data, pd.DataFrame)
        self.assertFalse(bicimad.data.empty)

    def test_clean(self):
        bicimad = BiciMad(month=2, year=23, test_mode=True)
        bicimad.clean()
        self.assertFalse(bicimad.data.isnull().all(axis=1).any())
        self.assertTrue(bicimad.data['fleet'].dtype == 'object')

    def test_resume(self):
        bicimad = BiciMad(month=2, year=23, test_mode=True)
        summary = bicimad.resume()
        self.assertIn('total_uses', summary)
        self.assertIn('total_time', summary)
        self.assertIn('most_popular_station', summary)
        self.assertIn('uses_from_most_popular', summary)

if __name__ == '__main__':
    unittest.main()

