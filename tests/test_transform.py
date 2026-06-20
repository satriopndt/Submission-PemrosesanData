import sys 
import os
import pandas as pd
from utils.transform import transform

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from utils.transform import convert_price, convert_rating, convert_colors, clean_size, clean_gender

def test_transform_returns_dataframe():
    raw=[
        {"Title": "T-shirt 1", "Price": "$10.00", "Rating": "Rating: ⭐ 4.0 / 5", 
         "Colors": "3 Colors", "Size": "Size: M", "Gender": "Gender: Men", 
         "timestamp": "2025-01-01"}
    ]
    result = transform(raw)
    assert isinstance(result, pd.DataFrame)

def test_transform_removes_unknown_product():
    raw = [
        {"Title": "Unknown Product", "Price": "$10.00", "Rating": "Rating: ⭐ 4.0 / 5",
         "Colors": "3 Colors", "Size": "Size: M", "Gender": "Gender: Men",
         "timestamp": "2024-01-01"}
    ]
    result = transform(raw)
    assert "Unknown Product" not in result["Title"].values

def test_convert_price_normal():
    assert convert_price("$10.00") == 160000.0

def test_convert_price_none():
    assert convert_price("None") is None

def test_convert_invalid():
    assert convert_price("Price Unvailable") is None

def test_convert_rating_normal():
    assert convert_rating("Rating: ⭐ 4.5 / 5") == 4.5

def test_convert_rating_none():
    assert convert_rating("None") is None

def test_convert_rating_invalid():
    assert convert_rating("Rating Unvailable") is None

def test_convert_colors_normal():
    assert convert_colors("3 Colors") == 3

def test_convert_colors_none():
    assert convert_colors("None") is None

def test_clean_size_normal():
    assert clean_size("Size: M") == "M"

def test_clean_gender():
    assert clean_gender("Gender: Men") == "Men"

