import unittest
import requests
from unittest.mock import patch
from bicimad.urlemt import UrlEMT


class TestUrlEMT(unittest.TestCase):

    @patch("requests.get")
    def test_select_valid_urls_connection_error(self, mock_get):
        mock_get.side_effect = requests.RequestException
        url_emt = UrlEMT()
        with self.assertRaises(ConnectionError):
            url_emt.select_valid_urls()

    def test_get_url_invalid_month_year(self):
        url_emt = UrlEMT()
        with self.assertRaises(ValueError):
            url_emt.get_url(13, 21)
        with self.assertRaises(ValueError):
            url_emt.get_url(6, 25)

    def test_function_documentation(self):
        url_emt = UrlEMT()
        for method_name in dir(url_emt):
            method = getattr(url_emt, method_name)
            if callable(method) and not method_name.startswith("_"):
                self.assertIsNotNone(method.__doc__, f"El método {method_name} no tiene docstring.")

    @patch("requests.get")
    def test_get_csv_valid_url(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b'Simulated ZIP content'
        url_emt = UrlEMT()
        url_emt._valid_urls = {"https://opendata.emtmadrid.es/getattachment/trips_21_06_June.csv"}

        with patch("zipfile.ZipFile") as mock_zip:
            mock_zip.return_value.namelist.return_value = ["data.csv"]
            mock_zip.return_value.read.return_value = b'idBike,fleet\n1,A\n2,B\n'

            csv_file = url_emt.get_csv(6, 21)
            self.assertEqual(csv_file.read(), 'idBike,fleet\n1,A\n2,B\n')


if __name__ == '__main__':
    unittest.main()
