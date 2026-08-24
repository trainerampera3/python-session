import pandas as pd




CLEANED_FILE = "data/cleaned/hotel_bookings_cleaned.csv"



MONTH_ORDER = {
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




def load_data():

    df = pd.read_csv(CLEANED_FILE)

    # Make sure numeric columns are numeric
    numeric_columns = [
        "is_canceled",
        "arrival_date_year",
        "arrival_date_day_of_month",
        "stays_in_weekend_nights",
        "stays_in_week_nights",
        "adults",
        "children",
        "babies",
        "adr",
        "lead_time",
        "is_repeated_guest"
    ]

    for column in numeric_columns:

        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    # Missing values
    if "children" in df.columns:
        df["children"] = df["children"].fillna(0)

    if "adults" in df.columns:
        df["adults"] = df["adults"].fillna(0)

    if "babies" in df.columns:
        df["babies"] = df["babies"].fillna(0)

    if "adr" in df.columns:
        df["adr"] = df["adr"].fillna(0)

    if "country" in df.columns:
        df["country"] = df["country"].fillna("Unknown")

    

    df["total_nights"] = (
        df["stays_in_weekend_nights"]
        + df["stays_in_week_nights"]
    )

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

    return df



def get_overall_kpis(df):

    total_bookings = len(df)

    total_guests = int(
        df["total_guests"].sum()
    )

    total_revenue = (
        df["estimated_revenue"].sum()
    )

    average_adr = (
        df["adr"].mean()
    )

    cancellation_rate = (
        df["is_canceled"].mean() * 100
    )

    average_stay = (
        df["total_nights"].mean()
    )

    return {
        "total_bookings": total_bookings,
        "total_guests": total_guests,
        "total_revenue": total_revenue,
        "average_adr": average_adr,
        "cancellation_rate": cancellation_rate,
        "average_stay": average_stay
    }




def hotel_analysis(df):

    result = (
        df.groupby("hotel")
        .agg(
            bookings=("hotel", "size"),
            guests=("total_guests", "sum"),
            revenue=("estimated_revenue", "sum"),
            average_adr=("adr", "mean"),
            cancellation_rate=("is_canceled", "mean")
        )
        .reset_index()
    )

    result["cancellation_rate"] = (
        result["cancellation_rate"] * 100
    )

    return result




def monthly_booking_analysis(df):

    result = (
        df.groupby(
            [
                "arrival_date_year",
                "arrival_date_month"
            ]
        )
        .size()
        .reset_index(
            name="bookings"
        )
    )

    # Create month number ONLY inside this function
    result["month_number"] = (
        result["arrival_date_month"]
        .map(MONTH_ORDER)
    )

    result = result.sort_values(
        [
            "arrival_date_year",
            "month_number"
        ]
    )

    result["month_year"] = (
        result["arrival_date_month"]
        + " "
        + result["arrival_date_year"].astype(str)
    )

    return result




def country_analysis(df):

    result = (
        df.groupby("country")
        .agg(
            bookings=("country", "size"),
            guests=("total_guests", "sum"),
            revenue=("estimated_revenue", "sum")
        )
        .reset_index()
    )

    return result.sort_values(
        "bookings",
        ascending=False
    )




def customer_type_analysis(df):

    result = (
        df.groupby("customer_type")
        .agg(
            bookings=("customer_type", "size"),
            average_stay=("total_nights", "mean"),
            average_adr=("adr", "mean"),
            cancellation_rate=("is_canceled", "mean")
        )
        .reset_index()
    )

    result["cancellation_rate"] = (
        result["cancellation_rate"] * 100
    )

    return result



def market_segment_analysis(df):

    result = (
        df.groupby("market_segment")
        .agg(
            bookings=("market_segment", "size"),
            revenue=("estimated_revenue", "sum"),
            average_adr=("adr", "mean"),
            cancellation_rate=("is_canceled", "mean")
        )
        .reset_index()
    )

    result["cancellation_rate"] = (
        result["cancellation_rate"] * 100
    )

    return result.sort_values(
        "bookings",
        ascending=False
    )



def room_type_analysis(df):

    result = (
        df.groupby("reserved_room_type")
        .agg(
            bookings=("reserved_room_type", "size"),
            average_adr=("adr", "mean"),
            cancellation_rate=("is_canceled", "mean")
        )
        .reset_index()
    )

    result["cancellation_rate"] = (
        result["cancellation_rate"] * 100
    )

    return result.sort_values(
        "bookings",
        ascending=False
    )



def repeated_guest_analysis(df):

    result = (
        df.groupby("is_repeated_guest")
        .agg(
            bookings=("is_repeated_guest", "size"),
            average_stay=("total_nights", "mean"),
            average_adr=("adr", "mean")
        )
        .reset_index()
    )

    result["guest_category"] = (
        result["is_repeated_guest"]
        .map(
            {
                0: "New Guest",
                1: "Repeated Guest"
            }
        )
    )

    return result