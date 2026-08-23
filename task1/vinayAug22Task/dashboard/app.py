import sys
from pathlib import Path

import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"

sys.path.append(str(SRC_DIR))

from analysis_visualization import (
    plot_price_distribution,
    plot_price_by_model,
    plot_price_vs_mileage,
    plot_car_comparison,
    plot_brand_listings,
    plot_model_listings,
    plot_brand_price,
    plot_price_segments,
    plot_city_listings,
    plot_city_price,
    plot_fuel_distribution
)

DATA_FILE = BASE_DIR / "data" / "processed" / "used_cars_cleaned.csv"

st.set_page_config(
    page_title="Used Car Analytics",
    page_icon="🚗",
    layout="wide"
)


@st.cache_data
def load_data():
    # Load the processed dataset
    return pd.read_csv(DATA_FILE)


df = load_data()

st.title("🚗 Used Car Market Analytics")
st.caption("Interactive dashboard for customers, dealers and market analysis")


# Select the type of user
perspective = st.sidebar.selectbox(
    "Select Perspective",
    [
        "Customer",
        "Seller / Dealer",
        "Market Analyst"
    ]
)

st.sidebar.header("Filters")


# Common filters
brand_options = sorted(df["oem"].dropna().unique())
fuel_options = sorted(df["fuel"].dropna().unique())
transmission_options = sorted(df["transmission"].dropna().unique())
city_options = sorted(df["city"].dropna().unique())


selected_brand = st.sidebar.selectbox(
    "Brand",
    ["All"] + list(brand_options)
)

selected_fuel = st.sidebar.selectbox(
    "Fuel",
    ["All"] + list(fuel_options)
)

selected_transmission = st.sidebar.selectbox(
    "Transmission",
    ["All"] + list(transmission_options)
)

selected_city = st.sidebar.selectbox(
    "City",
    ["All"] + list(city_options)
)


# Apply common filters
filtered_df = df.copy()

if selected_brand != "All":
    filtered_df = filtered_df[
        filtered_df["oem"] == selected_brand
    ]

if selected_fuel != "All":
    filtered_df = filtered_df[
        filtered_df["fuel"] == selected_fuel
    ]

if selected_transmission != "All":
    filtered_df = filtered_df[
        filtered_df["transmission"] == selected_transmission
    ]

if selected_city != "All":
    filtered_df = filtered_df[
        filtered_df["city"] == selected_city
    ]


if filtered_df.empty:
    st.warning("No cars match the selected filters.")
    st.stop()


# Customer dashboard
if perspective == "Customer":

    st.header("Customer Dashboard")
    st.write("Find and compare used cars based on price and vehicle characteristics.")

    model_options = sorted(
        filtered_df["model"].dropna().unique()
    )

    selected_model = st.sidebar.selectbox(
        "Select Model",
        ["All"] + list(model_options)
    )

    if selected_model != "All":
        customer_df = filtered_df[
            filtered_df["model"] == selected_model
        ]
    else:
        customer_df = filtered_df

    if customer_df.empty:
        st.warning("No cars found for the selected model.")
        st.stop()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Cars Found",
        f"{len(customer_df):,}"
    )

    col2.metric(
        "Average Price",
        f"₹{customer_df['price_lakhs'].mean():.2f} L"
    )

    col3.metric(
        "Lowest Price",
        f"₹{customer_df['price_lakhs'].min():.2f} L"
    )

    col4.metric(
        "Average Mileage",
        f"{customer_df['km'].mean():,.0f} km"
    )

    st.subheader("Price Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.pyplot(
            plot_price_distribution(customer_df)
        )

    with col2:
        st.pyplot(
            plot_price_by_model(filtered_df)
        )

    st.subheader("Vehicle Comparison")

    compare_models = st.multiselect(
        "Select models to compare",
        model_options,
        max_selections=4
    )

    if len(compare_models) >= 2:
        st.pyplot(
            plot_car_comparison(
                filtered_df,
                compare_models
            )
        )
    else:
        st.info("Select at least two models to compare.")

    st.subheader("Price and Usage")

    st.pyplot(
        plot_price_vs_mileage(customer_df)
    )


# Seller dashboard
elif perspective == "Seller / Dealer":

    st.header("Seller / Dealer Dashboard")
    st.write("Understand inventory, brands, models and price segments.")

    col1, col2, col3, col4 = st.columns(4)

    top_model = (
        filtered_df["model"]
        .value_counts()
        .index[0]
    )

    col1.metric(
        "Total Listings",
        f"{len(filtered_df):,}"
    )

    col2.metric(
        "Average Price",
        f"₹{filtered_df['price_lakhs'].mean():.2f} L"
    )

    col3.metric(
        "Average Mileage",
        f"{filtered_df['km'].mean():,.0f} km"
    )

    col4.metric(
        "Top Model",
        top_model.title()
    )

    col1, col2 = st.columns(2)

    with col1:
        st.pyplot(
            plot_brand_listings(filtered_df)
        )

    with col2:
        st.pyplot(
            plot_model_listings(filtered_df)
        )

    col1, col2 = st.columns(2)

    with col1:
        st.pyplot(
            plot_brand_price(filtered_df)
        )

    with col2:
        st.pyplot(
            plot_price_segments(filtered_df)
        )


# Market analyst dashboard
else:

    st.header("Market Analysis Dashboard")
    st.write("Understand overall market patterns, pricing and locations.")

    col1, col2, col3, col4 = st.columns(4)

    top_brand = (
        filtered_df["oem"]
        .value_counts()
        .index[0]
    )

    top_city = (
        filtered_df["city"]
        .value_counts()
        .index[0]
    )

    col1.metric(
        "Total Listings",
        f"{len(filtered_df):,}"
    )

    col2.metric(
        "Average Market Price",
        f"₹{filtered_df['price_lakhs'].mean():.2f} L"
    )

    col3.metric(
        "Top Brand",
        top_brand.title()
    )

    col4.metric(
        "Top City",
        top_city.title()
    )

    col1, col2 = st.columns(2)

    with col1:
        st.pyplot(
            plot_brand_listings(filtered_df)
        )

    with col2:
        st.pyplot(
            plot_brand_price(filtered_df)
        )

    col1, col2 = st.columns(2)

    with col1:
        st.pyplot(
            plot_city_listings(filtered_df)
        )

    with col2:
        st.pyplot(
            plot_city_price(filtered_df)
        )

    st.subheader("Fuel Market")

    st.pyplot(
        plot_fuel_distribution(filtered_df)
    )

    st.subheader("Price and Mileage")

    st.pyplot(
        plot_price_vs_mileage(filtered_df)
    )

st.divider()

st.caption(
    "Used Car Market Analytics | Pandas | NumPy | Matplotlib | Streamlit"
)