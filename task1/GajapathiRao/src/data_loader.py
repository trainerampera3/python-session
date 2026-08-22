import pandas as pd
from pathlib import Path


DATA_DIR = Path("data")


def load_data():
    payment = pd.read_csv(DATA_DIR / "payment_dim.csv")
    time = pd.read_csv(DATA_DIR / "time_dim.csv")
    store = pd.read_csv(DATA_DIR / "store_dim.csv")
    item = pd.read_csv(DATA_DIR / "item_dim.csv")
    customer = pd.read_csv(DATA_DIR / "customer_dim.csv")
    fact = pd.read_csv(DATA_DIR / "fact_table.csv")

    return payment, time, store, item, customer, fact