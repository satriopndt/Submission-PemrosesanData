import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from unittest.mock import patch, MagicMock
from utils.load import load_to_csv, load_to_google_sheets, load_to_postgresql


def make_sample_df():
    return pd.DataFrame({
        "Title": ["T-shirt 1"],
        "Price": [160000.0],
        "Rating": [4.0],
        "Size": ["M"],
        "Gender": ["Men"],
        "timestamp": ["2025-01-01"]
    })

def test_load_to_csv_creates_file(tmp_path):
    df = make_sample_df()
    filepath = str(tmp_path / "test.csv")
    load_to_csv(df, filepath)
    assert os.path.exists(filepath)

def test_load_csv_content_correct(tmp_path):
    df = make_sample_df()
    filepath = str(tmp_path / "test.csv")
    load_to_csv(df, filepath)
    loaded = pd.read_csv(filepath)
    assert len(loaded) == 1
    assert loaded["Title"][0] == "T-shirt 1"

def test_load_csv_empty_dataframe(tmp_path):
    df = pd.DataFrame()
    filepath = str(tmp_path / "test.csv")
    load_to_csv(df, filepath)
    assert os.path.exists(filepath)

def test_load_google_sheets_success(tmp_path):
    df = make_sample_df()
    mock_worksheet = MagicMock()
    mock_spreadsheet = MagicMock()
    mock_spreadsheet.sheet1 = mock_worksheet
    mock_client = MagicMock()
    mock_client.open_by_key.return_value = mock_spreadsheet

    with patch("utils.load.gspread.authorize", return_value=mock_client), \
        patch("utils.load.Credentials.from_service_account_file", return_value=MagicMock()), \
        patch("os.path.exists", return_value=True):
        load_to_google_sheets(df, "fake-id", "fake-creds.json")

    mock_worksheet.clear.assert_called_once()

def test_load_postgresql_success():
    df = make_sample_df()

    with patch("utils.load.create_engine", return_value=MagicMock()), \
        patch.object(df.__class__, "to_sql", return_value=None):
        load_to_postgresql(df, "postgresql://user:riosatrio58@localhost/db  ")

