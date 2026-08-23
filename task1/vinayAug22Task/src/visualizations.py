import matplotlib.pyplot as plt
import pandas as pd


# price distribution
def plot_price_distribution(df):
    fig, ax = plt.subplots()
    ax.hist(df["price_lakhs"], bins=30)
    ax.set_title("Used Car Price Distribution")
    ax.set_xlabel("Price (Lakhs)")
    ax.set_ylabel("Number of Cars")
    fig.tight_layout()
    return fig


# price and age
def plot_price_vs_age(df):
    fig, ax = plt.subplots()
    ax.scatter(df["vehicle_age"], df["price_lakhs"], alpha=0.4)
    ax.set_title("Price vs Vehicle Age")
    ax.set_xlabel("Vehicle Age (Years)")
    ax.set_ylabel("Price (Lakhs)")
    fig.tight_layout()
    return fig


# price and mileage
def plot_price_vs_mileage(df):
    fig, ax = plt.subplots()
    ax.scatter(df["km_thousands"], df["price_lakhs"], alpha=0.4)
    ax.set_title("Price vs Mileage")
    ax.set_xlabel("Mileage (Thousand KM)")
    ax.set_ylabel("Price (Lakhs)")
    fig.tight_layout()
    return fig


# price by fuel
def plot_price_by_fuel(df):
    data = df.groupby("fuel")["price_lakhs"].mean().sort_values(ascending=False)

    fig, ax = plt.subplots()
    ax.bar(data.index, data.values)
    ax.set_title("Average Price by Fuel Type")
    ax.set_xlabel("Fuel Type")
    ax.set_ylabel("Average Price (Lakhs)")
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    return fig


# price by transmission
def plot_price_by_transmission(df):
    data = df.groupby("transmission")["price_lakhs"].mean().sort_values(ascending=False)

    fig, ax = plt.subplots()
    ax.bar(data.index, data.values)
    ax.set_title("Average Price by Transmission")
    ax.set_xlabel("Transmission")
    ax.set_ylabel("Average Price (Lakhs)")
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    return fig


# listings by brand
def plot_listings_by_brand(df, top_n=10):
    data = df["oem"].value_counts().head(top_n).sort_values()

    fig, ax = plt.subplots()
    ax.barh(data.index, data.values)
    ax.set_title(f"Top {top_n} Brands by Number of Listings")
    ax.set_xlabel("Number of Listings")
    ax.set_ylabel("Brand")
    fig.tight_layout()
    return fig


# price by brand
def plot_price_by_brand(df, top_n=10):
    top_brands = df["oem"].value_counts().head(top_n).index
    data = df[df["oem"].isin(top_brands)].groupby("oem")["price_lakhs"].mean().sort_values()

    fig, ax = plt.subplots()
    ax.barh(data.index, data.values)
    ax.set_title(f"Average Price of Top {top_n} Brands")
    ax.set_xlabel("Average Price (Lakhs)")
    ax.set_ylabel("Brand")
    fig.tight_layout()
    return fig


# listings by segment
def plot_listings_by_price_segment(df):
    data = df["price_segment"].value_counts().reindex(
        ["budget", "mid_range", "premium", "luxury", "high_end"],
        fill_value=0
    )

    fig, ax = plt.subplots()
    ax.bar(data.index, data.values)
    ax.set_title("Listings by Price Segment")
    ax.set_xlabel("Price Segment")
    ax.set_ylabel("Number of Listings")
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    return fig


# fuel distribution
def plot_fuel_distribution(df):
    data = df["fuel"].value_counts().head(10)

    fig, ax = plt.subplots()
    ax.bar(data.index, data.values)
    ax.set_title("Fuel Type Distribution")
    ax.set_xlabel("Fuel Type")
    ax.set_ylabel("Number of Listings")
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    return fig


# listings by city
def plot_listings_by_city(df, top_n=10):
    data = df["city"].value_counts().head(top_n).sort_values()

    fig, ax = plt.subplots()
    ax.barh(data.index, data.values)
    ax.set_title(f"Top {top_n} Cities by Number of Listings")
    ax.set_xlabel("Number of Listings")
    ax.set_ylabel("City")
    fig.tight_layout()
    return fig


# price by city
def plot_price_by_city(df, top_n=10):
    top_cities = df["city"].value_counts().head(top_n).index
    data = df[df["city"].isin(top_cities)].groupby("city")["price_lakhs"].mean().sort_values()

    fig, ax = plt.subplots()
    ax.barh(data.index, data.values)
    ax.set_title(f"Average Price in Top {top_n} Cities")
    ax.set_xlabel("Average Price (Lakhs)")
    ax.set_ylabel("City")
    fig.tight_layout()
    return fig


# price and mileage by fuel
def plot_price_mileage_by_fuel(df):
    fig, ax = plt.subplots()

    for fuel_type, group in df.groupby("fuel"):
        ax.scatter(
            group["km_thousands"],
            group["price_lakhs"],
            alpha=0.35,
            label=fuel_type
        )

    ax.set_title("Price vs Mileage by Fuel Type")
    ax.set_xlabel("Mileage (Thousand KM)")
    ax.set_ylabel("Price (Lakhs)")
    ax.legend(title="Fuel")
    fig.tight_layout()
    return fig