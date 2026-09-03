from pathlib import Path

import pandas as pd
import numpy as np


BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA = BASE_DIR / "data" / "rawData"
PROCESSED_DATA = BASE_DIR / "data" / "processed"

INPUT_FILE = RAW_DATA / "cars_data_clean.csv"
OUTPUT_FILE = PROCESSED_DATA / "used_cars_cleaned.csv"
QUALITY_FILE = PROCESSED_DATA / "data_quality_report.csv"


def load_data():
    df = pd.read_csv(INPUT_FILE, low_memory=False)

    
    print("\nRAW DATA")
    print("Rows    :", df.shape[0])
    print("Columns :", df.shape[1])

    return df


def select_useful_columns(df):
    useful_columns = [
        # vehicle details
        "usedCarSkuId",
        "oem",
        "model",
        "variant",
        "myear",
        "body",
        "fuel",
        "transmission",
        "km",
        "owner_type",

        # location
        "City",
        "state",

        # seller
        "utype",
        "listed_price",

        # appearance
        "Color",

        # engine
        "Engine Type",
        "No of Cylinder",
        "Turbo Charger",
        "Super Charger",

        # dimensions
        "Length",
        "Width",
        "Height",
        "Wheel Base",
        "Seats",

        # drivetrain
        "Gear Box",
        "Drive Type",

        # performance
        "Max Power Delivered",
        "Max Torque Delivered",
    ]

    useful_columns = [column for column in useful_columns if column in df.columns]
    df = df[useful_columns].copy()

    
    print("\nCOLUMN REDUCTION")
    print("Columns before:", 66)
    print("Columns after :", len(df.columns))

    return df


def clean_column_names(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_", regex=False)

    return df


def remove_duplicates(df):
    before = len(df)

    if "usedcarskuid" in df.columns:
        df = df.drop_duplicates(subset="usedcarskuid", keep="first")
    else:
        df = df.drop_duplicates()

    after = len(df)
    print("\nDUPLICATES")
    print("Duplicates removed:", before - after)

    return df


def clean_categorical_columns(df):
    categorical_columns = [
        "oem",
        "model",
        "variant",
        "body",
        "fuel",
        "transmission",
        "owner_type",
        "city",
        "state",
        "utype",
        "color",
        "engine_type",
        "gear_box",
        "drive_type"
    ]

    for column in categorical_columns:
        if column in df.columns:
            df[column] = df[column].astype("string").str.strip().str.lower()
            df[column] = df[column].replace(["", "nan", "none", "null", "na", "n/a"], pd.NA)

    return df


def clean_numeric_columns(df):
    numeric_columns = [
        "myear",
        "km",
        "listed_price",
        "no_of_cylinder",
        "length",
        "width",
        "height",
        "wheel_base",
        "seats",
        "max_power_delivered",
        "max_torque_delivered"
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


def remove_invalid_values(df):
    # price
    if "listed_price" in df.columns:
        df = df[df["listed_price"] > 0]

    # year
    if "myear" in df.columns:
        current_year = pd.Timestamp.now().year
        df = df[df["myear"].between(1990, current_year)]

    # kilometres
    if "km" in df.columns:
        df = df[df["km"] >= 0]

    # seats
    if "seats" in df.columns:
        df.loc[~df["seats"].between(1, 20), "seats"] = np.nan

    # cylinders
    if "no_of_cylinder" in df.columns:
        df.loc[~df["no_of_cylinder"].between(1, 16), "no_of_cylinder"] = np.nan

    non_negative_columns = [
        "length",
        "width",
        "height",
        "wheel_base",
        "max_power_delivered",
        "max_torque_delivered"
    ]

    for column in non_negative_columns:
        if column in df.columns:
            df.loc[df[column] < 0, column] = np.nan

    return df


def handle_missing_values(df):
    
    print("\nMISSING VALUES")

    numeric_columns = df.select_dtypes(include=np.number).columns

    for column in numeric_columns:
        missing = df[column].isna().sum()

        if missing > 0:
            median_value = df[column].median()
            df[column] = df[column].fillna(median_value)
            print(f"{column}: {missing} missing → median {median_value}")

    categorical_columns = df.select_dtypes(include=["object", "string"]).columns

    for column in categorical_columns:
        missing = df[column].isna().sum()

        if missing > 0:
            df[column] = df[column].fillna("unknown")
            print(f"{column}: {missing} missing → unknown")

    return df


def create_derived_columns(df):
    current_year = pd.Timestamp.now().year

    # vehicle age
    df["vehicle_age"] = current_year - df["myear"]

    # km in thousands
    df["km_thousands"] = df["km"] / 1000

    # price in lakhs
    df["price_lakhs"] = df["listed_price"] / 100000

    # price segment
    df["price_segment"] = pd.cut(
        df["listed_price"],
        bins=[0, 300000, 600000, 1000000, 2000000, np.inf],
        labels=["budget", "mid_range", "premium", "luxury", "high_end"],
        include_lowest=True
    )

    return df


def validate_data(df):
    
    print(" \nFINAL VALIDATION")
    print("Rows    :", df.shape[0])
    print("Columns :", df.shape[1])

    total_missing = df.isna().sum().sum()
    print("\nTotal missing values:", total_missing)

    if total_missing == 0:
        print("✓ Dataset has no missing values")
    else:
        print("✗ Missing values still exist")
        print(df.isna().sum().sort_values(ascending=False).head(20))

    duplicates = df.duplicated().sum()
    print("\nDuplicate rows:", duplicates)

    print("\nData types:")
    print(df.dtypes)


def create_quality_report(df):
    report = pd.DataFrame({
        "column": df.columns,
        "data_type": df.dtypes.astype(str).values,
        "missing_count": df.isna().sum().values,
        "missing_percentage": df.isna().mean().values * 100,
        "unique_values": df.nunique(dropna=True).values
    })

    return report


def save_data(df, report):
    PROCESSED_DATA.mkdir(parents=True, exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False)
    report.to_csv(QUALITY_FILE, index=False)

    
    print(" \nFILES CREATED")
    print("Clean dataset:", OUTPUT_FILE)
    print("Quality report:", QUALITY_FILE)


def main():
    # load data
    df = load_data()

    # select columns
    df = select_useful_columns(df)

    # clean names
    df = clean_column_names(df)

    # remove duplicates
    df = remove_duplicates(df)

    # clean categories
    df = clean_categorical_columns(df)

    # clean numbers
    df = clean_numeric_columns(df)

    # remove invalid values
    df = remove_invalid_values(df)

    # fill missing values
    df = handle_missing_values(df)

    # add useful columns
    df = create_derived_columns(df)

    # validate data
    validate_data(df)

    report = create_quality_report(df)
    save_data(df, report)

    
    print("\n ====DATA CLEANING COMPLETE ✓")


if __name__ == "__main__":
    main()