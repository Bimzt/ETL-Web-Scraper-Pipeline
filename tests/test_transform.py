import unittest
import pandas as pd
from utils.transform import transform_data

class TestTransform(unittest.TestCase):
    
    def setUp(self):
        self.raw_data = [
            {"Title": "Baju A", "Price": "$10.5", "Rating": "4.8 / 5", "Colors": "3 Colors", "Size": "Size: L", "Gender": "Gender: Men"}
        ]
        
    def test_transform_data_cleaning(self):
        df_result = transform_data(self.raw_data)
        row = df_result.iloc[0]
        self.assertEqual(row['Price'], 168000.0)
        self.assertEqual(row['Rating'], 4.8)
        self.assertEqual(row['Colors'], 3)
        self.assertEqual(row['Size'], "L")
        self.assertEqual(row['Gender'], "Men")

    def test_transform_data_key_error(self):
        bad_data = [{"Nama_Baju": "Baju A", "Harga": "100"}]
        with self.assertRaises(KeyError):
            transform_data(bad_data)

if __name__ == '__main__':
    unittest.main()