from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_data():
    payment = pd.read_csv(DATA_DIR / "Trans_dim.csv" , encoding="cp1252")
    time = pd.read_csv(DATA_DIR / "time_dim.csv", encoding="cp1252")
    store = pd.read_csv(DATA_DIR / "store_dim.csv", encoding="cp1252")
    item = pd.read_csv(DATA_DIR / "item_dim.csv", encoding="cp1252")
    customer = pd.read_csv(DATA_DIR / "customer_dim.csv", encoding="cp1252")
    fact = pd.read_csv(DATA_DIR / "fact_table.csv", encoding="cp1252")

    return payment, time, store, item, customer, fact