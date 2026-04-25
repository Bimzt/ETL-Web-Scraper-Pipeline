import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load import load_to_csv, load_to_postgres, load_to_gsheets

class TestLoad(unittest.TestCase):
    
    def setUp(self):
        self.df = pd.DataFrame({
            "Title": ["Baju A"], "Price": [168000.0], 
            "Rating": [4.8], "Colors": [3], "Size": ["L"], "Gender": ["Men"]
        })
        
    @patch('pandas.DataFrame.to_csv')
    def test_load_to_csv(self, mock_to_csv):
        load_to_csv(self.df, 'test.csv')
        mock_to_csv.assert_called_once_with('test.csv', index=False)

    @patch('pandas.DataFrame.to_csv')
    def test_load_to_csv_error(self, mock_to_csv):
        mock_to_csv.side_effect = Exception("Memori penuh")
        load_to_csv(self.df, 'test.csv')

    @patch('pandas.DataFrame.to_sql')
    def test_load_to_postgres(self, mock_to_sql):
        test_url = 'postgresql://user:pass@localhost/db'
        load_to_postgres(self.df, test_url, 'test_table')
        mock_to_sql.assert_called_once_with('test_table', con=test_url, if_exists='replace', index=False)

    @patch('pandas.DataFrame.to_sql')
    def test_load_to_postgres_error(self, mock_to_sql):
        mock_to_sql.side_effect = Exception("Database mati")
        load_to_postgres(self.df, 'postgresql://user:pass@localhost/db', 'test_table')

    @patch('utils.load.build')
    @patch('utils.load.Credentials.from_service_account_file')
    def test_load_to_gsheets(self, mock_creds, mock_build):
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        load_to_gsheets(self.df, 'fake_id', 'Sheet1!A1', 'fake_creds.json')
        mock_creds.assert_called_once()
        mock_build.assert_called_once()
        mock_service.spreadsheets().values().update.assert_called_once()

if __name__ == '__main__':
    unittest.main()