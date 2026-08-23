from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "processed" / "used_cars_cleaned.csv"


def load_data():
    return pd.read_csv(DATA_FILE)


def main():
    df = load_data()

    print("\ndataset")
    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])

    print("\nprice")
    print(df["listed_price"].describe())

    print("\ntop brands")
    print(df["oem"].value_counts().head(10))

    print("\nfuel")
    print(df["fuel"].value_counts())

    print("\ntransmission")
    print(df["transmission"].value_counts())

    print("\nbody type")
    print(df["body"].value_counts())

    print("\ncity")
    print(df["city"].value_counts().head(10))


if __name__ == "__main__":
    main()