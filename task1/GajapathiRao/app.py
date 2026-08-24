import pandas as pd
import streamlit as st
import plotly.express as px

from src.data_loader import load_data
from src.data_cleaning import clean_data
from src.analysis import create_master_dataframe




st.set_page_config(
    page_title="Sales Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)



st.markdown(
    """
    <style>

    

    .stApp {
        background: #f6f8fc;
    }
    header { visibility: hidden; }
    [data-testid="stDecoration"] { display: none; }

    .block-container {
        max-width: 1500px;
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }

    

    .dashboard-header {
        # background: linear-gradient(135deg, #163d8f 0%, #315fd4 55%, #5b4acb 100%);
        background: linear-gradient(135deg, #163d8f 0%, #315fd4 55%, #5b4acb 100%);
        display: flex;
        align-items: center;
        flex-direction:column;
        padding: 24px 30px;
        border-radius: 10px;
        margin-bottom: 18px;
        margin-top: 0px;
        color: white;
        box-shadow: 0 8px 24px rgba(31, 70, 150, 0.18);
    }

    .dashboard-title {
        font-size: 36px;
        font-weight: 800;
        line-height: 1.1;
        margin: 0;
        letter-spacing: -0.5px;
    }

    .dashboard-subtitle {
        font-size: 15px;
        margin-top: 8px;
        opacity: 0.92;
    }
    
    [data-testid="stMetricLabel"] p, 
    [data-testid="stMetricValue"] div {
        color: black !important;
    }

    .section-title {
        font-size: 23px;
        font-weight: 750;
        color: black;
        margin: 20px 0 10px 0;
    }
    .section-title::active {
        color: black;
    }

    .section-caption {
        color: black;
        font-size: 13px;
        margin-bottom: 12px;
    }

    

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e4e9f2;
        border-radius: 14px;
        padding: 17px 18px;
        min-height: 105px;
        box-shadow: 0 3px 12px rgba(20, 40, 80, 0.06);
    }

    div[data-testid="stMetricLabel"] {
        color: black;
        font-size: 13px;
        font-weight: 650;
    }

    div[data-testid="stMetricValue"] {
        color:black;
        font-size: 25px;
        font-weight: 800;
    }

    

    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e4e9f2;
        color: black;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #172b4d;
    }

    

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: white;
        border: 1px solid #e4e9f2;
        border-radius: 14px;
        box-shadow: 0 3px 12px rgba(20, 40, 80, 0.045);
    }

    

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }

    

    
    div[data-testid="stTabs"] {
        background: #ffffff;
        padding: 10px 16px 0px 16px;
        border-radius: 12px 12px 0 0;
        border: 1px solid #e4e9f2;
        border-bottom: none;
        margin-bottom: -1px;
    }

    
    button[data-baseweb="tab"] {
        font-weight: 700 !important;
        font-size: 15px !important;
        color: #4a5568 !important; /* Clear dark grey text */
        padding: 10px 20px !important;
        transition: all 0.2s ease;
    }

    
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #315fd4 !important; /* Matches your header blue */
        border-bottom: 3px solid #315fd4 !important;
    }

    
    div[data-testid="stTabPanel"] {
        background: white;
        border: 1px solid #e4e9f2;
        border-radius: 0 0 14px 14px;
        padding: 24px;
        box-shadow: 0 3px 12px rgba(20, 40, 80, 0.045);
    }


    

    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

    

    .insight-card {
        background: white;
        border: 1px solid #e4e9f2;
        border-radius: 14px;
        padding: 14px 16px;
        min-height: 88px;
        box-shadow: 0 3px 12px rgba(20, 40, 80, 0.045);
    }

    .insight-label {
        color: black;
        font-size: 12px;
        font-weight: 650;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }

    .insight-value {
        color: #172b4d;
        font-size: 18px;
        font-weight: 800;
        margin-top: 5px;
    }

    .insight-note {
        color: #667085;
        font-size: 12px;
        margin-top: 3px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)



def format_currency(value):
    """Format large sales values in a compact dashboard-friendly form."""
    value = float(value)

    if abs(value) >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"
    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    if abs(value) >= 1_000:
        return f"${value / 1_000:.1f}K"

    return f"${value:,.0f}"


def make_chart(fig, height=330):
    """Apply one consistent visual language to all Plotly charts."""
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=10, r=10, t=48, b=10),
        font=dict(family="Arial", color="#172b4d"),
        title=dict(
            x=0,
            xanchor="left",
            font=dict(size=16, color="#172b4d"),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.01,
            xanchor="right",
            x=1,
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    fig.update_xaxes(
        showgrid=False,
        linecolor="#e4e9f2",
    )

    fig.update_yaxes(
        gridcolor="#edf1f7",
        zeroline=False,
    )

    return fig


def ordered_month_values(series):
    """
    Keep calendar month order when the dataset contains either
    numeric months or month names.
    """
    values = series.dropna().unique().tolist()

    month_names = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December",
    ]

    short_month_names = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
    ]

    if all(isinstance(v, (int, float)) for v in values):
        return sorted(values)

    lookup = {
        name.lower(): index
        for index, name in enumerate(month_names)
    }

    lookup.update({
        name.lower(): index
        for index, name in enumerate(short_month_names)
    })

    return sorted(
        values,
        key=lambda value: lookup.get(str(value).lower(), 99),
    )


def show_table(title, dataframe, rows=10):
    """Compact table inside an expandable section."""
    with st.expander(title):
        st.dataframe(
            dataframe.head(rows),
            use_container_width=True,
            hide_index=True,
        )




payment, time, store, item, customer, fact = load_data()

payment, time, store, item, customer, fact = clean_data(
    payment,
    time,
    store,
    item,
    customer,
    fact,
)

master_df = create_master_dataframe(
    payment,
    time,
    store,
    item,
    customer,
    fact,
)


st.markdown(
    """
    <div class="dashboard-header">
        <div class="dashboard-title"> Sales Intelligence Dashboard</div>
        <div class="dashboard-subtitle">
            Interactive business analytics • Explore sales, customers,
            products, regions and transaction performance
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


st.sidebar.title("Dashboard Filters")
# st.sidebar.caption(
#     "Use the filters below to update every KPI and chart."
# )

years = sorted(master_df["year"].dropna().unique().tolist())
quarters = sorted(master_df["quarter"].dropna().unique().tolist())
months = ordered_month_values(master_df["month"])
divisions = sorted(master_df["division"].dropna().unique().tolist())
districts = sorted(master_df["district"].dropna().unique().tolist())
payment_types = sorted(master_df["trans_type"].dropna().unique().tolist())
products = sorted(master_df["item_name"].dropna().unique().tolist())

filter_keys = [
    "selected_years",
    "selected_quarters",
    "selected_months",
    "selected_divisions",
    "selected_districts",
    "selected_payment_types",
    "selected_products",
]

if st.sidebar.button("↺ Reset All Filters", use_container_width=True):
    for key in filter_keys:
        st.session_state.pop(key, None)
    st.rerun()

with st.sidebar.expander("Time Filters", expanded=True):
    selected_years = st.multiselect(
        "Year",
        years,
        default=years,
        key="selected_years",
    )

    selected_quarters = st.multiselect(
        "Quarter",
        quarters,
        default=quarters,
        key="selected_quarters",
    )

    selected_months = st.multiselect(
        "Month",
        months,
        default=months,
        key="selected_months",
    )

with st.sidebar.expander(" Geography", expanded=False):
    selected_divisions = st.multiselect(
        "Division",
        divisions,
        default=divisions,
        key="selected_divisions",
    )

    selected_districts = st.multiselect(
        "District",
        districts,
        default=districts,
        key="selected_districts",
    )

with st.sidebar.expander("Transaction & Product", expanded=False):
    selected_payment_types = st.multiselect(
        "Payment Type",
        payment_types,
        default=payment_types,
        key="selected_payment_types",
    )

    selected_products = st.multiselect(
        "Product",
        products,
        default=products,
        key="selected_products",
    )

st.sidebar.divider()
# st.sidebar.caption(
#     f"Source rows: {len(master_df):,} transactions"
# )



filtered_df = master_df[
    master_df["year"].isin(selected_years)
    & master_df["quarter"].isin(selected_quarters)
    & master_df["month"].isin(selected_months)
    & master_df["division"].isin(selected_divisions)
    & master_df["district"].isin(selected_districts)
    & master_df["trans_type"].isin(selected_payment_types)
    & master_df["item_name"].isin(selected_products)
].copy()


if filtered_df.empty:
    st.warning(
        "No transactions match the current filters. "
        "Please broaden your selection from the sidebar."
    )
    st.stop()



st.markdown(
    '<div class="section-title">Business Overview</div>',
    unsafe_allow_html=True,
)

# st.markdown(
#     f"""
#     <div class="section-caption">
#         Showing <b>{len(filtered_df):,}</b> transactions after applying
#         the selected filters.
#     </div>
#     """,
#     unsafe_allow_html=True,
# )

total_sales = filtered_df["total_price"].sum()
total_transactions = len(filtered_df)
total_quantity = filtered_df["quantity"].sum()
total_customers = filtered_df["customer_key"].nunique()
avg_transaction = (
    total_sales / total_transactions
    if total_transactions
    else 0
)

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.metric(" Total Sales", format_currency(total_sales))

with kpi2:
    st.metric("Transactions", f"{total_transactions:,}")

with kpi3:
    st.metric(" Quantity Sold", f"{total_quantity:,.0f}")

with kpi4:
    st.metric(" Unique Customers", f"{total_customers:,}")

with kpi5:
    st.metric("Avg. Transaction", format_currency(avg_transaction))



top_product_row = (
    filtered_df.groupby("item_name")["total_price"]
    .sum()
    .sort_values(ascending=False)
)

top_division_row = (
    filtered_df.groupby("division")["total_price"]
    .sum()
    .sort_values(ascending=False)
)

top_district_row = (
    filtered_df.groupby("district")["total_price"]
    .sum()
    .sort_values(ascending=False)
)

payment_mix = (
    filtered_df.groupby("trans_type")["total_price"]
    .sum()
    .sort_values(ascending=False)
)

ins1, ins2, ins3, ins4 = st.columns(4)

with ins1:
    top_product = top_product_row.index[0]
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-label">Top Product</div>
            <div class="insight-value">{top_product}</div>
            <div class="insight-note">
                {format_currency(top_product_row.iloc[0])} sales
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with ins2:
    top_division = top_division_row.index[0]
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-label">Leading Division</div>
            <div class="insight-value">{top_division}</div>
            <div class="insight-note">
                {format_currency(top_division_row.iloc[0])} sales
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with ins3:
    top_district = top_district_row.index[0]
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-label">Top District</div>
            <div class="insight-value">{top_district}</div>
            <div class="insight-note">
                {format_currency(top_district_row.iloc[0])} sales
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with ins4:
    leading_payment = payment_mix.index[0]
    payment_share = payment_mix.iloc[0] / payment_mix.sum() * 100
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-label">Leading Payment Type</div>
            <div class="insight-value">{leading_payment}</div>
            <div class="insight-note">
                {payment_share:.1f}% of filtered sales
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


overview_tab, product_tab, geography_tab, data_tab = st.tabs(
    [
        "Sales Overview",
        "Product Analytics",
        " Geography & Transactions",
        " Data Quality",
    ]
)




with overview_tab:

    st.markdown(
        '<div class="section-title">Sales Performance</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        year_sales = (
            filtered_df.groupby("year", as_index=False)["total_price"]
            .sum()
            .sort_values("year")
        )

        fig_year = px.bar(
            year_sales,
            x="year",
            y="total_price",
            title="Sales by Year",
            labels={
                "year": "Year",
                "total_price": "Sales",
            },
            text_auto=False,
        )

        fig_year.update_traces(
            hovertemplate="Year: %{x}<br>Sales: %{y:$,.2f}<extra></extra>"
        )

        st.plotly_chart(
            make_chart(fig_year),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with col2:
        monthly_sales = (
            filtered_df.groupby("month", as_index=False)["total_price"]
            .sum()
        )

        month_order = ordered_month_values(filtered_df["month"])
        monthly_sales["month"] = pd.Categorical(
            monthly_sales["month"],
            categories=month_order,
            ordered=True,
        )
        monthly_sales = monthly_sales.sort_values("month")

        fig_month = px.line(
            monthly_sales,
            x="month",
            y="total_price",
            markers=True,
            title="Monthly Sales Trend",
            labels={
                "month": "Month",
                "total_price": "Sales",
            },
        )

        fig_month.update_traces(
            hovertemplate="Month: %{x}<br>Sales: %{y:$,.2f}<extra></extra>"
        )

        st.plotly_chart(
            make_chart(fig_month),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    col3, col4 = st.columns(2)

    with col3:
        payment_sales = (
            filtered_df.groupby("trans_type", as_index=False)["total_price"]
            .sum()
            .sort_values("total_price", ascending=False)
        )

        fig_payment = px.pie(
            payment_sales,
            names="trans_type",
            values="total_price",
            hole=0.55,
            title="Sales Mix by Payment Type",
        )

        fig_payment.update_traces(
            textposition="inside",
            textinfo="percent",
            hovertemplate="%{label}<br>Sales: %{value:$,.2f}<extra></extra>",
        )

        st.plotly_chart(
            make_chart(fig_payment),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with col4:
        division_sales = (
            filtered_df.groupby("division", as_index=False)["total_price"]
            .sum()
            .sort_values("total_price", ascending=True)
        )

        fig_division = px.bar(
            division_sales,
            x="total_price",
            y="division",
            orientation="h",
            title="Sales by Division",
            labels={
                "division": "Division",
                "total_price": "Sales",
            },
        )

        fig_division.update_traces(
            hovertemplate="%{y}<br>Sales: %{x:$,.2f}<extra></extra>"
        )

        st.plotly_chart(
            make_chart(fig_division),
            use_container_width=True,
            config={"displayModeBar": False},
        )




with product_tab:

    st.markdown(
        '<div class="section-title">Product Performance</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        top_products = (
            filtered_df.groupby("item_name", as_index=False)["total_price"]
            .sum()
            .sort_values("total_price", ascending=False)
            .head(10)
            .sort_values("total_price")
        )

        fig_products = px.bar(
            top_products,
            x="total_price",
            y="item_name",
            orientation="h",
            title="Top 10 Products by Sales",
            labels={
                "item_name": "Product",
                "total_price": "Sales",
            },
        )

        fig_products.update_traces(
            hovertemplate="%{y}<br>Sales: %{x:$,.2f}<extra></extra>"
        )

        st.plotly_chart(
            make_chart(fig_products, 370),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with col2:
        product_quantity = (
            filtered_df.groupby("item_name", as_index=False)["quantity"]
            .sum()
            .sort_values("quantity", ascending=False)
            .head(10)
            .sort_values("quantity")
        )

        fig_quantity = px.bar(
            product_quantity,
            x="quantity",
            y="item_name",
            orientation="h",
            title="Top 10 Products by Quantity",
            labels={
                "item_name": "Product",
                "quantity": "Quantity",
            },
        )

        fig_quantity.update_traces(
            hovertemplate="%{y}<br>Quantity: %{x:,.0f}<extra></extra>"
        )

        st.plotly_chart(
            make_chart(fig_quantity, 370),
            use_container_width=True,
            config={"displayModeBar": False},
        )




with geography_tab:

    st.markdown(
        '<div class="section-title">Geography & Transaction Analysis</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        district_sales = (
            filtered_df.groupby("district", as_index=False)["total_price"]
            .sum()
            .sort_values("total_price", ascending=False)
            .head(10)
            .sort_values("total_price")
        )

        fig_district = px.bar(
            district_sales,
            x="total_price",
            y="district",
            orientation="h",
            title="Top 10 Districts by Sales",
            labels={
                "district": "District",
                "total_price": "Sales",
            },
        )

        fig_district.update_traces(
            hovertemplate="%{y}<br>Sales: %{x:$,.2f}<extra></extra>"
        )

        st.plotly_chart(
            make_chart(fig_district, 370),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with col2:
        district_transactions = (
            filtered_df.groupby("district", as_index=False)
            .size()
            .rename(columns={"size": "transactions"})
            .sort_values("transactions", ascending=False)
            .head(10)
            .sort_values("transactions")
        )

        fig_transactions = px.bar(
            district_transactions,
            x="transactions",
            y="district",
            orientation="h",
            title="Top 10 Districts by Transactions",
            labels={
                "district": "District",
                "transactions": "Transactions",
            },
        )

        fig_transactions.update_traces(
            hovertemplate="%{y}<br>Transactions: %{x:,}<extra></extra>"
        )

        st.plotly_chart(
            make_chart(fig_transactions, 370),
            use_container_width=True,
            config={"displayModeBar": False},
        )



with data_tab:

    st.markdown(
        '<div class="section-title">Data Quality & Dataset Health</div>',
        unsafe_allow_html=True,
    )

    datasets = {
        "Payment": payment,
        "Time": time,
        "Store": store,
        "Item": item,
        "Customer": customer,
        "Fact": fact,
    }

    quality_rows = []

    for name, dataframe in datasets.items():
        quality_rows.append(
            {
                "Dataset": name,
                "Rows": len(dataframe),
                "Columns": len(dataframe.columns),
                "Duplicate Rows": int(dataframe.duplicated().sum()),
                "Missing Cells": int(dataframe.isna().sum().sum()),
            }
        )

    quality_df = pd.DataFrame(quality_rows)

    q1, q2, q3 = st.columns(3)

    with q1:
        st.metric(
            "Dimension / Fact Tables",
            len(datasets),
        )

    with q2:
        st.metric(
            "Duplicate Rows",
            f"{quality_df['Duplicate Rows'].sum():,}",
        )

    with q3:
        st.metric(
            "Missing Cells",
            f"{quality_df['Missing Cells'].sum():,}",
        )

    st.dataframe(
        quality_df,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown(
        '<div class="section-title">Foreign Key Validation</div>',
        unsafe_allow_html=True,
    )

    def check_keys(fact_df, dimension_df, fact_key, dimension_key):
        valid_keys = set(dimension_df[dimension_key].dropna())
        return int((~fact_df[fact_key].isin(valid_keys)).sum())

    checks = {
        "Payment": ("payment_key", payment, "payment_key"),
        "Customer": ("customer_key", customer, "customer_key"),
        "Time": ("time_key", time, "time_key"),
        "Item": ("item_key", item, "item_key"),
        "Store": ("store_key", store, "store_key"),
    }

    fk_rows = []

    for name, (fact_key, dimension_df, dimension_key) in checks.items():
        invalid_count = check_keys(
            fact,
            dimension_df,
            fact_key,
            dimension_key,
        )

        fk_rows.append(
            {
                "Relationship": name,
                "Fact Key": fact_key,
                "Invalid Keys": invalid_count,
                "Status": "Valid" if invalid_count == 0 else "Issues Found",
            }
        )

    fk_df = pd.DataFrame(fk_rows)

    st.dataframe(
        fk_df,
        use_container_width=True,
        hide_index=True,
    )

    for row in fk_rows:
        if row["Invalid Keys"] == 0:
            st.success(
                f"✓ {row['Relationship']}: all fact-table keys are valid"
            )
        else:
            st.error(
                f"✕ {row['Relationship']}: "
                f"{row['Invalid Keys']:,} invalid keys found"
            )

    st.markdown(
        '<div class="section-title">Dimension Samples</div>',
        unsafe_allow_html=True,
    )

    show_table("Payment Dimension", payment)
    show_table("Time Dimension", time)
    show_table("Store Dimension", store)
    show_table("Item Dimension", item)
    show_table("Customer Dimension", customer)
    show_table("Fact Table", fact)




st.divider()

st.markdown(
    '<div class="section-title">Filtered Data</div>',
    unsafe_allow_html=True,
)

st.caption(
    "Use the export button when you need the currently filtered transaction set."
)

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered CSV",
    data=csv_data,
    file_name="filtered_sales_data.csv",
    mime="text/csv",
    use_container_width=False,
)



# st.markdown(
#     """
#     <div style="
#         text-align:center;
#         color:#667085;
#         font-size:12px;
#         padding:24px 0 5px 0;
#     ">
#         Built with Python • Pandas • Plotly • Streamlit
#     </div>
#     """,
#     unsafe_allow_html=True,
# )