import pandas as pd
import re
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

EXCHANGE_RATE = 16000


def convert_price(price_str):
    """
    Mengkonversi harga dari USD ke Rupiah
    Args:
        price_str itu string harga dalam format dollar "$xx.xx" 
        lalu akan dikonversi yang dimana mengembalikan float harga
    Returns:
        float harga dalam rupiah atau none jika tidak valid
    """

    if price_str is None:
        return None
    cleaned = re.sub(r'[^\d.]', '', str(price_str))
    if not cleaned:
        return None
    return float(cleaned) * EXCHANGE_RATE


def convert_rating(rating_str):

    try:
        match = re.search(r'\d+\.\d+', rating_str)
        if match:
            return float(match.group())
        return None
    except Exception as e:
        logger.error(f"Error convert_rating: {e}")
        return None


def convert_colors(colors_str):
    try:
        color = re.search(r'\d+', colors_str)
        if color:
            return int(color.group())
        return None
    except Exception as e:
        logger.error(f"Error convert_colors: {e}")
        return None


def clean_size(size_str):
    try:
        return size_str.replace("Size: ", "")
    except Exception as e:
        logger.error(f"Error clean_size: {e}")
        return None


def clean_gender(gender_str):
    try:
        return gender_str.replace("Gender: ", "")
    except Exception as e:
        logger.error(f"Error clean_gender: {e}")
        return None


def transform(data):
    try:
        logger.info(f'Memulai tranformasi: {len(data)} data mentah')
        df = pd.DataFrame(data)

        df["Price"] = df["Price"].apply(convert_price)
        df["Rating"] = df["Rating"].apply(convert_rating)
        df["Colors"] = df["Colors"].apply(convert_colors)
        df["Size"] = df["Size"].apply(clean_size)
        df["Gender"] = df["Gender"].apply(clean_gender)

        df = df[df["Title"] != "Unknown Product"]
        df = df.dropna()
        df = df.drop_duplicates()

        logger.info(f"Transformasi selesai: {len(df)} data bersih")
        return df
    except Exception as e:
        logger.error(f"Error saat transformasi: {e}")
        raise


if __name__ == "__main__":
    from extract import scrape_all_pages
    raw_data = scrape_all_pages()
    df = transform(raw_data)
    print(df)
    print(df.dtypes)
