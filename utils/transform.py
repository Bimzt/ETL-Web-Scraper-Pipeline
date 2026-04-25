import pandas as pd
import logging

def transform_data(raw_data):
    try:
        df = pd.DataFrame(raw_data)
        df = df.dropna()
        df = df.drop_duplicates()
        df = df[~df['Title'].str.contains('Unknown Product', na=False, case=False)]
        df = df[~df['Rating'].str.contains('Invalid Rating', na=False, case=False)]
        df = df[~df['Price'].str.contains('Price Unavailable', na=False, case=False)]
        df['Price'] = df['Price'].str.replace('$', '', regex=False).str.strip()
        df['Price'] = (df['Price'].astype('float64') * 16000.0)
        df['Rating'] = df['Rating'].str.extract(r'([0-9.]+)')[0].astype('float64')
        df['Colors'] = df['Colors'].str.extract(r'(\d+)')[0].astype('int64')
        df['Size'] = df['Size'].str.replace('Size: ', '', regex=False).str.strip()
        df['Gender'] = df['Gender'].str.replace('Gender: ', '', regex=False).str.strip()
        df['Title'] = df['Title'].astype('object')
        df['Size'] = df['Size'].astype('object')
        df['Gender'] = df['Gender'].astype('object')
        
        logging.info(f"Transformasi selesai. Sisa baris data: {len(df)}")
        return df
        
    except KeyError as e:
        logging.error(f"Kolom tidak ditemukan saat transformasi: {e}")
        raise e
    except Exception as e:
        logging.error(f"Error umum saat transformasi: {e}")
        raise e