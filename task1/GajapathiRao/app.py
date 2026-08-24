import streamlit as st

import plotly.express as px

from src.data_loader import load_data
from src.data_cleaning import clean_data
from src.analysis import create_master_dataframe

# --------------------------------------------------
# Dashboard Styling
# --------------------------------------------------

# --------------------------------------------------
# Dashboard Styling
# --------------------------------------------------

st.markdown(
    """
    <style>
    
    # *{
    #     background-color: grey;
    #     # color: #333;
    # }

    /* ----------------------------------------------
       Main Page
    ---------------------------------------------- */

    .main-title {
        font-size: 40px;
        font-weight: 700;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 30px;
    }


    /* ----------------------------------------------
       KPI Cards
    ---------------------------------------------- */

    div[data-testid="stMetric"] {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        background-color: white;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 15px;
        font-weight: 600;
    }

    div[data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 700;
    }


    /* ----------------------------------------------
       Section Headers
    ---------------------------------------------- */

    h1 {
        font-weight: 700;
    }

    h2 {
        font-weight: 650;
        margin-top: 25px;
    }

    h3 {
        font-weight: 600;
    }


    /* ----------------------------------------------
       Sidebar
    ---------------------------------------------- */

    section[data-testid="stSidebar"] {
        border-right: 1px solid #e5e5e5;
    }

    section[data-testid="stSidebar"] h2 {
        font-size: 22px;
    }


    /* ----------------------------------------------
       Dataframes
    ---------------------------------------------- */

    div[data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
    }


    /* ----------------------------------------------
       Success Message
    ---------------------------------------------- */

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }


    /* ----------------------------------------------
       Charts / Containers
    ---------------------------------------------- */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
)


st.markdown(
    '<div class="main-title">Sales Analytics Dashboard</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">Interactive Sales Intelligence Dashboard</div>',
    unsafe_allow_html=True,
)

payment, time, store, item, customer, fact = load_data()

payment, time, store, item, customer, fact = clean_data(
    payment,
    time,
    store,
    item,
    customer,
    fact
)

master_df = create_master_dataframe(
    payment,
    time,
    store,
    item,
    customer,
    fact,
)
st.header("Master DataFrame")

st.write("Rows:", len(master_df))
st.write("Columns:", len(master_df.columns))

st.dataframe(master_df.head())

st.success("Dashboard loaded successfully")

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------

st.sidebar.header(" Dashboard Filters")


# --------------------------------------------------
# Year Filter
# --------------------------------------------------

years = sorted(
    master_df["year"].dropna().unique()
)

selected_year = st.sidebar.selectbox(
    "Year",
    years,
)


# --------------------------------------------------
# Quarter Filter
# --------------------------------------------------

quarters = sorted(
    master_df["quarter"].dropna().unique()
)

selected_quarter = st.sidebar.multiselect(
    "Quarter",
    quarters,
    default=quarters,
)


# --------------------------------------------------
# Month Filter
# --------------------------------------------------

months = sorted(
    master_df["month"].dropna().unique()
)

selected_month = st.sidebar.multiselect(
    "Month",
    months,
    default=months,
)


# --------------------------------------------------
# Division Filter
# --------------------------------------------------

divisions = sorted(
    master_df["division"].dropna().unique()
)

selected_divisions = st.sidebar.multiselect(
    "Division",
    divisions,
    default=divisions,
)


# --------------------------------------------------
# District Filter
# --------------------------------------------------

districts = sorted(
    master_df["district"].dropna().unique()
)

selected_districts = st.sidebar.multiselect(
    "District",
    districts,
    default=districts,
)


# --------------------------------------------------
# Payment Type Filter
# --------------------------------------------------

payment_types = sorted(
    master_df["trans_type"].dropna().unique()
)

selected_payment_types = st.sidebar.multiselect(
    "Payment Type",
    payment_types,
    default=payment_types,
)


# --------------------------------------------------
# Product Filter
# --------------------------------------------------

products = sorted(
    master_df["item_name"].dropna().unique()
)

selected_products = st.sidebar.multiselect(
    "Product",
    products,
    default=products,
)


# --------------------------------------------------
# Apply Filters
# --------------------------------------------------

filtered_df = master_df[
    (master_df["year"] == selected_year)
    & (master_df["quarter"].isin(selected_quarter))
    & (master_df["month"].isin(selected_month))
    & (master_df["division"].isin(selected_divisions))
    & (master_df["district"].isin(selected_districts))
    & (master_df["trans_type"].isin(selected_payment_types))
    & (master_df["item_name"].isin(selected_products))
].copy()

## --------------------------------------------------
# KPI Calculations
# --------------------------------------------------

total_sales = filtered_df["total_price"].sum()

total_transactions = len(filtered_df)

total_quantity = filtered_df["quantity"].sum()

total_customers = filtered_df["customer_key"].nunique()


# --------------------------------------------------
# KPI Cards
# --------------------------------------------------

st.header("Business Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Total Sales",
        f"${total_sales:,.2f}",
    )

with col2:
    st.metric(
        "🛒 Total Transactions",
        f"{total_transactions:,}",
    )

with col3:
    st.metric(
        "📦 Total Quantity",
        f"{total_quantity:,.0f}",
    )

with col4:
    st.metric(
        "👥 Unique Customers",
        f"{total_customers:,}",
    )


# --------------------------------------------------
# Sales Analytics Charts
# --------------------------------------------------

st.header("Sales Analytics")


# --------------------------------------------------
# 1. Sales by Year
# --------------------------------------------------

year_sales = (
    filtered_df
    .groupby("year", as_index=False)["total_price"]
    .sum()
)

fig_year = px.bar(
    year_sales,
    x="year",
    y="total_price",
    title="Sales by Year",
    labels={
        "year": "Year",
        "total_price": "Total Sales",
    },
)

fig_year.update_layout(
    xaxis_title="Year",
    yaxis_title="Sales",
)

st.plotly_chart(
    fig_year,
    use_container_width=True,
)

# --------------------------------------------------
# 2. Monthly Sales Trend
# --------------------------------------------------

monthly_sales = (
    filtered_df
    .groupby("month", as_index=False)["total_price"]
    .sum()
)

monthly_sales["month"] = monthly_sales["month"].astype(str)

fig_month = px.line(
    monthly_sales,
    x="month",
    y="total_price",
    markers=True,
    title="Monthly Sales Trend",
    labels={
        "month": "Month",
        "total_price": "Total Sales",
    },
)

st.plotly_chart(
    fig_month,
    use_container_width=True,
)


# --------------------------------------------------
# 3. Sales by Payment Type
# --------------------------------------------------

payment_sales = (
    filtered_df
    .groupby("trans_type", as_index=False)["total_price"]
    .sum()
)

fig_payment = px.pie(
    payment_sales,
    names="trans_type",
    values="total_price",
    title="Sales by Payment Type",
    hole=0.4,
)

st.plotly_chart(
    fig_payment,
    use_container_width=True,
)


# --------------------------------------------------
# 4. Sales by Division
# --------------------------------------------------

division_sales = (
    filtered_df
    .groupby("division", as_index=False)["total_price"]
    .sum()
    .sort_values("total_price", ascending=False)
)

fig_division = px.bar(
    division_sales,
    x="division",
    y="total_price",
    title="Sales by Division",
    labels={
        "division": "Division",
        "total_price": "Total Sales",
    },
)

st.plotly_chart(
    fig_division,
    use_container_width=True,
)


# --------------------------------------------------
# 5. Top 10 Products
# --------------------------------------------------

top_products = (
    filtered_df
    .groupby("item_name", as_index=False)["total_price"]
    .sum()
    .sort_values(
        "total_price",
        ascending=False,
    )
    .head(10)
)

fig_products = px.bar(
    top_products.sort_values("total_price"),
    x="total_price",
    y="item_name",
    orientation="h",
    title="Top 10 Products by Sales",
    labels={
        "item_name": "Product",
        "total_price": "Total Sales",
    },
)

st.plotly_chart(
    fig_products,
    use_container_width=True,
)



district_sales = (
    filtered_df
    .groupby("district", as_index=False)["total_price"]
    .sum()
    .sort_values(
        "total_price",
        ascending=False,
    )
    .head(10)
)

fig_district = px.bar(
    district_sales.sort_values("total_price"),
    x="total_price",
    y="district",
    orientation="h",
    title="Top 10 Districts by Sales",
    labels={
        "district": "District",
        "total_price": "Total Sales",
    },
)

st.plotly_chart(
    fig_district,
    use_container_width=True,
)
# --------------------------------------------------
# Dataset overview
# --------------------------------------------------

st.header("Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Payment Rows", len(payment))
    st.metric("Time Rows", len(time))

with col2:
    st.metric("Store Rows", len(store))
    st.metric("Item Rows", len(item))

with col3:
    st.metric("Customer Rows", len(customer))
    st.metric("Fact Rows", len(fact))



st.header("Payment Dimension")
st.dataframe(payment.head())

st.header("Time Dimension")
st.dataframe(time.head())

st.header("Store Dimension")
st.dataframe(store.head())

st.header("Item Dimension")
st.dataframe(item.head())

st.header("Customer Dimension")
st.dataframe(customer.head())

st.header("Fact Table")
st.dataframe(fact.head())

# --------------------------------------------------
# Data Quality Checks
# --------------------------------------------------

st.header("Data Quality Checks")


datasets = {
    "Payment": payment,
    "Time": time,
    "Store": store,
    "Item": item,
    "Customer": customer,
    "Fact": fact,
}


for name, dataframe in datasets.items():

    st.subheader(name)

    col1, col2 = st.columns(2)

    with col1:
        st.write("Columns")
        st.write(list(dataframe.columns))

    with col2:
        st.write("Duplicate Rows")
        st.write(dataframe.duplicated().sum())

    st.write("Missing Values")

    missing = dataframe.isna().sum()

    missing = missing[missing > 0]

    if missing.empty:
        st.success("No missing values")
    else:
        st.dataframe(missing)
        
        
# --------------------------------------------------
# Foreign Key Validation
# --------------------------------------------------

st.header("Foreign Key Validation")


def check_keys(fact_df, dimension_df, fact_key, dimension_key):

    valid_keys = set(dimension_df[dimension_key].dropna())

    invalid_count = (~fact_df[fact_key].isin(valid_keys)).sum()

    return invalid_count


checks = {
    "Payment": (
        "payment_key",
        payment,
        "payment_key",
    ),
    "Customer": (
    "customer_key",
    customer,
    "customer_key",
),
    "Time": (
        "time_key",
        time,
        "time_key",
    ),
    "Item": (
        "item_key",
        item,
        "item_key",
    ),
    "Store": (
        "store_key",
        store,
        "store_key",
    ),
}


for name, (fact_key, dimension_df, dimension_key) in checks.items():

    invalid_count = check_keys(
        fact,
        dimension_df,
        fact_key,
        dimension_key,
    )

    if invalid_count == 0:
        st.success(
            f"{name}: All fact-table keys are valid"
        )
    else:
        st.error(
            f"{name}: {invalid_count:,} invalid keys found"
        )