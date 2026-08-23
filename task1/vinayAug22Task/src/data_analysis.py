from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "processed" / "used_cars_cleaned.csv"


def load_data():
    return pd.read_csv(DATA_FILE)


def main():
    df = load_data()

    print("\nDataset :\n ")
    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])

    print("\nPrice : \n")
    print(df["listed_price"].describe())

    print("\nTop brands : \n")
    print(df["oem"].value_counts().head(10))

    print("\nFuel : \n")
    print(df["fuel"].value_counts())

    print("\nTransmission : \n")
    print(df["transmission"].value_counts())

    print("\nBody type : \n")
    print(df["body"].value_counts())

    print("\nCity : \n")
    print(df["city"].value_counts().head(10).reset_index(name = "Count"))


if __name__ == "__main__":
    main()