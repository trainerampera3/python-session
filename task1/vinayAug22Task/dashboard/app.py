import sys
from pathlib import Path

import pandas as pd
import streamlit as st


# project path
BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
sys.path.append(str(SRC_DIR))


# visualizations
from visualizations import (
    plot_price_distribution,
    plot_price_vs_age,
    plot_price_vs_mileage,
    plot_price_by_fuel,
    plot_price_by_transmission,
    plot_listings_by_brand,
    plot_price_by_brand,
    plot_listings_by_price_segment,
    plot_fuel_distribution,
    plot_listings_by_city,
    plot_price_by_city,
    plot_price_mileage_by_fuel,
)


DATA_FILE = BASE_DIR / "data" / "processed" / "used_cars_cleaned.csv"


st.set_page_config(page_title="Used Car Market Dashboard", page_icon="🚗", layout="wide")


# load data
@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)


df = load_data()


st.title("🚗 Used Car Market Dashboard")
st.write("Explore used-car prices, vehicle characteristics, inventory and market patterns.")


# sidebar controls
st.sidebar.header("Dashboard Controls")

perspective = st.sidebar.selectbox(
    "Select Perspective",
    ["Overview", "Customer", "Seller / Dealer", "Market Analysis"]
)

st.sidebar.subheader("Filters")


brands = sorted(df["oem"].dropna().unique().tolist())
selected_brands = st.sidebar.multiselect("Brand", brands)

fuels = sorted(df["fuel"].dropna().unique().tolist())
selected_fuels = st.sidebar.multiselect("Fuel Type", fuels)

transmissions = sorted(df["transmission"].dropna().unique().tolist())
selected_transmissions = st.sidebar.multiselect("Transmission", transmissions)

cities = sorted(df["city"].dropna().unique().tolist())
selected_cities = st.sidebar.multiselect("City", cities)


min_price = float(df["price_lakhs"].min())
max_price = float(df["price_lakhs"].max())

price_range = st.sidebar.slider(
    "Price Range (Lakhs)",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price)
)


# apply filters
filtered_df = df.copy()

if selected_brands:
    filtered_df = filtered_df[filtered_df["oem"].isin(selected_brands)]

if selected_fuels:
    filtered_df = filtered_df[filtered_df["fuel"].isin(selected_fuels)]

if selected_transmissions:
    filtered_df = filtered_df[filtered_df["transmission"].isin(selected_transmissions)]

if selected_cities:
    filtered_df = filtered_df[filtered_df["city"].isin(selected_cities)]

filtered_df = filtered_df[filtered_df["price_lakhs"].between(price_range[0], price_range[1])]


if filtered_df.empty:
    st.warning("No cars match the selected filters.")
    st.stop()


# market overview
st.subheader("Market Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Cars", f"{len(filtered_df):,}")

with col2:
    st.metric("Average Price", f"₹{filtered_df['price_lakhs'].mean():.2f} L")

with col3:
    st.metric("Average Mileage", f"{filtered_df['km'].mean():,.0f} km")

with col4:
    top_brand = filtered_df["oem"].value_counts().index[0]
    st.metric("Top Brand", top_brand.title())


# overview
if perspective == "Overview":
    st.header("Used Car Market Overview")
    st.write("A high-level view of prices, vehicle age, mileage and market composition.")

    col1, col2 = st.columns(2)

    with col1:
        st.pyplot(plot_price_distribution(filtered_df))

    with col2:
        st.pyplot(plot_listings_by_brand(filtered_df))

    col1, col2 = st.columns(2)

    with col1:
        st.pyplot(plot_listings_by_price_segment(filtered_df))

    with col2:
        st.pyplot(plot_fuel_distribution(filtered_df))


# customer
elif perspective == "Customer":
    st.header("👤 Customer Perspective")
    st.write("Understand used-car prices and how vehicle characteristics relate to price.")

    # price distribution
    st.subheader("1. Price Distribution")
    st.pyplot(plot_price_distribution(filtered_df))

    # price and age
    st.subheader("2. Price vs Vehicle Age")
    st.pyplot(plot_price_vs_age(filtered_df))

    # price and mileage
    st.subheader("3. Price vs Mileage")
    st.pyplot(plot_price_vs_mileage(filtered_df))

    # fuel prices
    st.subheader("4. Average Price by Fuel Type")
    st.pyplot(plot_price_by_fuel(filtered_df))

    # transmission prices
    st.subheader("5. Average Price by Transmission")
    st.pyplot(plot_price_by_transmission(filtered_df))


# seller / dealer
elif perspective == "Seller / Dealer":
    st.header("🏪 Seller / Dealer Perspective")
    st.write("Understand inventory composition, brand presence and price segments.")

    # brand listings
    st.subheader("1. Listings by Brand")
    st.pyplot(plot_listings_by_brand(filtered_df))

    # brand prices
    st.subheader("2. Average Price by Brand")
    st.pyplot(plot_price_by_brand(filtered_df))

    # price segments
    st.subheader("3. Listings by Price Segment")
    st.pyplot(plot_listings_by_price_segment(filtered_df))

    # fuel distribution
    st.subheader("4. Fuel Type Distribution")
    st.pyplot(plot_fuel_distribution(filtered_df))


# market analysis
elif perspective == "Market Analysis":
    st.header("🌍 Market Analysis")
    st.write("Understand geographic patterns and relationships within the used-car market.")

    # city listings
    st.subheader("1. Listings by City")
    st.pyplot(plot_listings_by_city(filtered_df))

    # city prices
    st.subheader("2. Average Price by City")
    st.pyplot(plot_price_by_city(filtered_df))

    # price and mileage by fuel
    st.subheader("3. Price vs Mileage by Fuel Type")
    st.pyplot(plot_price_mileage_by_fuel(filtered_df))


st.divider()
st.caption("Used Car Market Analysis | Pandas + NumPy + Matplotlib + Streamlit")