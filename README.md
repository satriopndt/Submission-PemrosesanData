# ETL Pipeline - Fashion Studio Data

Submission Dicoding: Belajar Fundamental Pemrosesan Data

## Deskripsi

Project ini melakukan web scraping data produk fashion dari [Fashion Studio](https://fashion-studio.dicoding.dev), membersihkan datanya, lalu menyimpannya ke 3 repositori: CSV, Google Sheets, dan PostgreSQL.


## Struktur Foldeer
```
submission-pemda/
├── tests/
│   ├── test_extract.py
│   ├── test_transform.py
│   └── test_load.py
├── utils/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── main.py
├── requirements.txt
├── README.md
└── products.csv
```

## Cara Install & Jalankan
1. Clone atau download project ini

2. Buat virtual environment
```bash
py -m venv venv
venv\Scripts\Activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Buat file `.env` berisi:
```
DATABASE_URL=postgresql://user:password@localhost:5432/fashion_db
SPREADSHEET_ID=your-spreadsheet-id
```

5. Jalankan ETL pipeline
```bash
py main.py
```

6. Jalankan unit test
```bash
py -m pytest tests
```

7. Cek test coverage
```bash
py -m pytest tests --cov=utils --cov-report=term-missing
```