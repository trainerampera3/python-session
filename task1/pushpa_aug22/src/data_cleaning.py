import pandas as pd
import os




input_file = "/home/siyyadripushpa/python-session/task1/pushpa_aug22/data/raw/hotel_bookings.csv"

df = pd.read_csv(input_file)

print("Raw data loaded successfully.")
print("Original shape:", df.shape)




duplicate_count = df.duplicated().sum()

print("Duplicate rows:", duplicate_count)

df = df.drop_duplicates()

print("Shape after removing duplicates:", df.shape)




# Children has only a few missing values.
df["children"] = df["children"].fillna(0)


# Country has a small number of missing values.
# We use "Unknown" instead of deleting those bookings.
df["country"] = df["country"].fillna("Unknown")


# Agent and company have many missing values.
# Missing agent/company means no agent/company was associated
# with the booking.
df["agent"] = df["agent"].fillna("No Agent")
df["company"] = df["company"].fillna("No Company")



numeric_columns = [
    "children",
    "adults",
    "babies",
    "lead_time",
    "stays_in_weekend_nights",
    "stays_in_week_nights",
    "adr",
    "booking_changes",
    "days_in_waiting_list",
    "required_car_parking_spaces",
    "total_of_special_requests"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )




month_mapping = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}

df["arrival_month_number"] = (
    df["arrival_date_month"]
    .map(month_mapping)
)

df["arrival_date"] = pd.to_datetime(
    dict(
        year=df["arrival_date_year"],
        month=df["arrival_month_number"],
        day=df["arrival_date_day_of_month"]
    ),
    errors="coerce"
)



df["total_nights"] = (
    df["stays_in_weekend_nights"]
    + df["stays_in_week_nights"]
)


#
df["total_guests"] = (
    df["adults"]
    + df["children"]
    + df["babies"]
)



df["estimated_revenue"] = (
    df["adr"]
    * df["total_nights"]
)




df["booking_status"] = df["is_canceled"].map(
    {
        0: "Confirmed/Completed",
        1: "Canceled"
    }
)


#
df["guest_type"] = "Adults Only"

df.loc[
    df["children"] > 0,
    "guest_type"
] = "Family"

df.loc[
    df["babies"] > 0,
    "guest_type"
] = "Family with Baby"




os.makedirs(
    "data/cleaned",
    exist_ok=True
)




cleaned_file = (
    "data/cleaned/"
    "hotel_bookings_cleaned.csv"
)

df.to_csv(
    cleaned_file,
    index=False
)



hotel_summary = (
    df.groupby("hotel")
    .agg(
        total_bookings=("hotel", "size"),
        total_guests=("total_guests", "sum"),
        average_adr=("adr", "mean"),
        total_revenue=("estimated_revenue", "sum"),
        cancellation_rate=("is_canceled", "mean"),
        average_lead_time=("lead_time", "mean"),
        average_stay_nights=("total_nights", "mean")
    )
    .reset_index()
)


# Convert cancellation rate to percentage
hotel_summary["cancellation_rate"] = (
    hotel_summary["cancellation_rate"] * 100
)


# Round numerical columns
hotel_summary["average_adr"] = (
    hotel_summary["average_adr"].round(2)
)

hotel_summary["total_revenue"] = (
    hotel_summary["total_revenue"].round(2)
)

hotel_summary["cancellation_rate"] = (
    hotel_summary["cancellation_rate"].round(2)
)

hotel_summary["average_lead_time"] = (
    hotel_summary["average_lead_time"].round(2)
)

hotel_summary["average_stay_nights"] = (
    hotel_summary["average_stay_nights"].round(2)
)


# Save hotel summary
summary_file = (
    "data/cleaned/"
    "hotel_summary.csv"
)

hotel_summary.to_csv(
    summary_file,
    index=False
)



print("\nCleaning completed successfully!")

print(
    "\nCleaned dataset shape:",
    df.shape
)

print(
    "\nCleaned file saved at:",
    cleaned_file
)

print(
    "Hotel summary saved at:",
    summary_file
)

print(
    "\nRemaining missing values:"
)

print(
    df.isnull().sum()
    .sort_values(ascending=False)
    .head(10)
)