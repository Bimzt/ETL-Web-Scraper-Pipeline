import pandas as pd
import logging
from sqlalchemy import create_engine
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def load_to_csv(df, filename='products.csv'):
    try:
        df.to_csv(filename, index=False)
        logging.info(f"Data berhasil disimpan ke {filename}")
    except Exception as e:
        logging.error(f"Gagal menyimpan ke CSV: {e}")

def load_to_postgres(df, db_url, table_name='products'):
    try:
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        df.to_sql(table_name, con=db_url, if_exists='replace', index=False)
        
        logging.info("Data berhasil disimpan ke PostgreSQL")
    except Exception as e:
        logging.error(f"Gagal menyimpan ke PostgreSQL: {e}")

def load_to_gsheets(df, spreadsheet_id, range_name, creds_file='google-sheets-api.json'):
    try:
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        creds = Credentials.from_service_account_file(creds_file, scopes=scopes)
        service = build('sheets', 'v4', credentials=creds)
        df = df.astype(str) 
        values = [df.columns.values.tolist()] + df.values.tolist()
        body = {'values': values}
        sheet = service.spreadsheets()
        sheet.values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption='RAW', body=body
        ).execute()
        
        logging.info("Data berhasil disimpan ke Google Sheets")
    except Exception as e:
        logging.error(f"Gagal menyimpan ke Google Sheets: {e}")