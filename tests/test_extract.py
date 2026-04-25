import unittest
from unittest.mock import patch, MagicMock
import requests
from utils.extract import scrape_data

class TestExtract(unittest.TestCase):
    
    @patch('utils.extract.requests.Session')
    def test_scrape_data_success(self, mock_session_class):
        mock_session = mock_session_class.return_value.__enter__.return_value
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"""
        <html><body>
            <div class="product-details">
                <h3 class="product-title">Baju Keren</h3>
                <span class="price">$10</span>
                <p>4.5 / 5</p>
                <p>Gender: Men</p>
                <p>3 Colors</p>
                <p>Size: M</p>
            </div>
        </body></html>
        """
        mock_session.get.return_value = mock_response
        result = scrape_data()
        
        self.assertTrue(len(result) > 0)
        self.assertEqual(result[0]['Title'], 'Baju Keren')
        self.assertEqual(result[0]['Price'], '$10')
        self.assertIn('timestamp', result[0])

    @patch('utils.extract.requests.Session')
    def test_scrape_data_request_error(self, mock_session_class):
        mock_session = mock_session_class.return_value.__enter__.return_value
        mock_session.get.side_effect = requests.exceptions.RequestException("Koneksi terputus")
        
        result = scrape_data()
        self.assertEqual(len(result), 0)

if __name__ == '__main__':
    unittest.main()