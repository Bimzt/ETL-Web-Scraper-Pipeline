import logging
from utils.extract import scrape_data
from utils.transform import transform_data
from utils.load import load_to_csv, load_to_postgres, load_to_gsheets

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main():
    logging.info("=== ETL Pipeline Sederhana ===")

    logging.info("Memulai proses Extract...")
    raw_data = scrape_data()
    if not raw_data:
        logging.error("EKSTRAK GAGAL: Data mentah kosong.")
        return
    logging.info(f"Sukses mendapatkan {len(raw_data)} data mentah.")

    logging.info("Memulai proses Transform...")
    try:
        clean_data = transform_data(raw_data)
        logging.info(f"Sukses mentransformasi data. Sisa data bersih: {len(clean_data)} baris.")
        print("\n=== TIPE DATA HASIL TRANSFORMASI ===")
        clean_data.info()
        
    except Exception as e:
        logging.error(f"TRANSFORM GAGAL: {e}")
        return

    logging.info("Memulai proses Load ke Repositori...")
    load_to_csv(clean_data, filename='products.csv')

    DB_URL = "postgresql://postgres:******/@localhost:5432/ETL Sederhana" 
    load_to_postgres(clean_data, DB_URL, table_name='products')
    SPREADSHEET_ID = "yourspreadsheetsid"
    RANGE_NAME = "Sheet1!A1"
    CREDS_FILE = "google-sheets-api.json" 
    load_to_gsheets(clean_data, SPREADSHEET_ID, RANGE_NAME, CREDS_FILE)

    logging.info("=== Proses ETL Pipeline Selesai dengan Sukses! ===")

if __name__ == "__main__":
    main()
