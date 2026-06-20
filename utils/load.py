import gspread
from google.oauth2.service_account import Credentials
from sqlalchemy import create_engine
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_to_csv(df, filepatch="products.csv"):
    try:
        df.to_csv(filepatch, index=False)
        logger.info("CSV berhasil dibuat !")
    except Exception as e:
        logger.error(f"Error load_to_csv: {e}")
        raise


def load_to_google_sheets(df, spreadsheets_id,
                          credentials_path="google-sheets-api.json"):
    try:

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        creds = Credentials.from_service_account_file(
            credentials_path, scopes=scopes)
        client = gspread.authorize(creds)

        spreadsheet = client.open_by_key(spreadsheets_id)
        worksheet = spreadsheet.sheet1

        worksheet.clear()
        data = [df.columns.tolist()] + df.values.tolist()
        worksheet.update(data)
        logger.info("Berhasil simpan di google sheet !")
    except Exception as e:
        logger.error(f"load_to_google_sheets error: {e}")
        raise


def load_to_postgresql(df, db_url):

    try:
        engine = create_engine(db_url)
        df.to_sql("products", con=engine, if_exists="replace", index=False)
        logger.info("Berhasil simpan ke PostgreSQL !")
    except Exception as e:
        logger.error(f"load_to_postgresql error: {e}")
        raise


if __name__ == "__main__":
    import sys
    sys.path.insert(0, '.')
    from utils.extract import scrape_all_pages
    from utils.transform import transform

    raw = scrape_all_pages()
    df = transform(raw)
    load_to_csv(df)
    logger.info("CSV berhasil dibuat")

    load_to_google_sheets(
        df, spreadsheets_id="1bY7wXNPfnqYhu4rDpOhQZ1bJmd945XWSFnb8CqbJFOg")
    load_to_postgresql(
        df, db_url="postgresql://postgres:riosatrio58@localhost:5432/fashion_db")
