# ETL-Web-Scraper-Pipeline

# Simple ETL Pipeline - Fashion Catalog Scraper

Repositori ini berisi proyek data pipeline **ETL (Extract, Transform, Load)** sederhana dan modular yang dibangun menggunakan Python. Proyek ini berfungsi untuk mengekstrak data produk secara otomatis dari sebuah website katalog pakaian, membersihkan dan mentransformasikan data tersebut, serta memuatnya ke dalam tiga tempat penyimpanan berbeda: file CSV, database PostgreSQL, dan Google Sheets.

## Fitur Utama

* **Extract**: Melakukan *web scraping* secara otomatis pada website `https://fashion-studio.dicoding.dev/` menggunakan `BeautifulSoup` dan `requests`. Script ini mendukung navigasi multi-halaman untuk mengambil informasi produk seperti Nama, Harga, Rating, Warna, Ukuran, dan Gender.
* **Transform**: Menggunakan `pandas` untuk pembersihan data secara mendalam. Proses transformasi meliputi:
  * Menghapus baris kosong (Missing Values) dan data duplikat.
  * Memfilter produk yang tidak valid ("Unknown Product", "Invalid Rating", "Price Unavailable").
  * Membersihkan format teks (menghapus simbol `$`, kata "Size:", "Gender:").
  * Mengonversi tipe data dan mata uang (Mengubah harga USD ke IDR dengan asumsi kurs 1 USD = Rp16.000).
* **Load**: Memuat hasil data yang sudah bersih ke dalam tiga repositori target:
  1. File CSV lokal (`products.csv`).
  2. Database PostgreSQL lokal.
  3. Cloud via Google Sheets menggunakan Google Sheets API.
* **Automated Testing**: Kode dilengkapi dengan pengujian unit (*Unit Tests*) menggunakan `pytest` dan fungsi *mocking* untuk menguji setiap tahapan ETL secara terisolasi.

## Struktur Repositori

```text
├── main.py                     # Skrip utama untuk menjalankan keseluruhan ETL pipeline
├── requirements.txt            # Daftar library Python yang dibutuhkan (dependencies)
├── google-sheets-api.json      # File kredensial API Google Sheets (Service Account)
├── utils/                      # Folder berisi modul-modul utama ETL
│   ├── extract.py              # Logik web scraping
│   ├── transform.py            # Logik pembersihan & transformasi data (Pandas)
│   └── load.py                 # Logik penyimpanan ke CSV, PostgreSQL, dan GSheets
└── tests/                      # Folder berisi skrip unit testing
    ├── test_extract.py         
    ├── test_transform.py       
    └── test_load.py
```

## Persyaratan Sistem
Sebelum menjalankan proyek ini, pastikan sistem kamu sudah terinstal:
- Python 3.12 atau versi lebih baru.
- Database PostgreSQL yang sedang berjalan.
- Google Cloud Service Account dengan file JSON kredensial (google-sheets-api.json) untuk mengakses Google Sheets API.

## Setup & Instalasi

**1. Clone Repositori**
```bash
git clone [https://github.com/Bimzt/ETL-Web-Scraper-Pipeline.git](https://github.com/Bimzt/ETL-Web-Scraper-Pipeline.git)
cd ETL-Web-Scraper-Pipeline
```

**2. Install Dependencies**
Install semua library yang dibutuhkan melalui file requirements.txt:
```bash
pip install -r requirements.txt
```

**3. Konfigurasi Database & Google Sheets**
Buka file main.py dan sesuaikan kredensial di bagian Load dengan pengaturan milikmu:
```bash
# Sesuaikan dengan URL PostgreSQL kamu
DB_URL = "postgresql://username:password@localhost:5432/ETL Sederhana" 

# Sesuaikan dengan ID Spreadsheet Google kamu
SPREADSHEET_ID = "10oKpAbNGXqtW8TAetZRkd367QLQuI7Cgeg0F6M90Fg8"
```
(Catatan: Jangan lupa untuk meletakkan file kredensial google-sheets-api.json di dalam folder utama proyek ini).

## Cara Menjalankan Pipeline
Untuk mengeksekusi pipeline ETL dari awal hingga akhir, cukup jalankan skrip utama:
```bash
python main.py
```
Kamu akan melihat log proses di terminal yang menampilkan status Ekstrak, Transform, dan Load, beserta metrik jumlah data yang berhasil diproses.

## Testing
Proyek ini menggunakan pytest untuk memastikan setiap modul berjalan dengan baik. Jalankan semua Unit Test:
```bash
python -m pytest tests
```
Jalankan test beserta laporan persentase cakupan kode (Coverage Report):
```bash
coverage run -m pytest tests
coverage report -m
```
