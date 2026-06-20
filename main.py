from utils.extract import scrape_all_pages
from utils.transform import transform
from utils.load import load_to_csv, load_to_google_sheets, load_to_postgresql
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")


def main():
    raw_data = scrape_all_pages()
    df = transform(raw_data)
    load_to_csv(df)
    load_to_google_sheets(df, spreadsheets_id=SPREADSHEET_ID)
    load_to_postgresql(df, db_url=DATABASE_URL)


if __name__ == "__main__":
    main()
