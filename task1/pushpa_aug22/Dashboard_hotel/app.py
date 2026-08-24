import sys
from pathlib import Path

import streamlit as st



PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)




from src.analysis import (
    load_data,
    get_overall_kpis,
    hotel_analysis,
    monthly_booking_analysis,
    country_analysis,
    customer_type_analysis,
    market_segment_analysis,
    room_type_analysis,
    repeated_guest_analysis
)




from src.visualization import (
    monthly_booking_chart,
    hotel_booking_chart,
    hotel_cancellation_chart,
    top_country_chart,
    customer_type_chart,
    market_segment_chart,
    room_type_chart,
    repeated_guest_chart,
    lead_time_chart
)





st.set_page_config(
    page_title="Hotel Booking Analytics",
    page_icon="🏨",
    layout="wide"
)



@st.cache_data
def load_dashboard_data():

    return load_data()


df = load_dashboard_data()




st.sidebar.title(" Hotel Analytics")

st.sidebar.write(
    "Use the filters below to explore the booking data."
)

st.sidebar.divider()



hotel_list = sorted(
    df["hotel"]
    .dropna()
    .unique()
    .tolist()
)

selected_hotel = st.sidebar.selectbox(
    "Select Hotel",
    ["All Hotels"] + hotel_list
)




year_list = sorted(
    df["arrival_date_year"]
    .dropna()
    .unique()
    .tolist()
)

selected_year = st.sidebar.selectbox(
    "Select Arrival Year",
    ["All Years"] + year_list
)




month_list = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

selected_month = st.sidebar.selectbox(
    "Select Arrival Month",
    ["All Months"] + month_list
)




customer_list = sorted(
    df["customer_type"]
    .dropna()
    .unique()
    .tolist()
)

selected_customer = st.sidebar.selectbox(
    "Select Customer Type",
    ["All Customer Types"] + customer_list
)



segment_list = sorted(
    df["market_segment"]
    .dropna()
    .unique()
    .tolist()
)

selected_segment = st.sidebar.selectbox(
    "Select Market Segment",
    ["All Market Segments"] + segment_list
)




status_list = sorted(
    df["booking_status"]
    .dropna()
    .unique()
    .tolist()
)

selected_status = st.sidebar.selectbox(
    "Select Booking Status",
    ["All Booking Status"] + status_list
)



filtered_df = df.copy()


if selected_hotel != "All Hotels":

    filtered_df = filtered_df[
        filtered_df["hotel"] == selected_hotel
    ]


if selected_year != "All Years":

    filtered_df = filtered_df[
        filtered_df["arrival_date_year"]
        == selected_year
    ]


if selected_month != "All Months":

    filtered_df = filtered_df[
        filtered_df["arrival_date_month"]
        == selected_month
    ]


if selected_customer != "All Customer Types":

    filtered_df = filtered_df[
        filtered_df["customer_type"]
        == selected_customer
    ]


if selected_segment != "All Market Segments":

    filtered_df = filtered_df[
        filtered_df["market_segment"]
        == selected_segment
    ]


if selected_status != "All Booking Status":

    filtered_df = filtered_df[
        filtered_df["booking_status"]
        == selected_status
    ]



st.title(
    " Hotel Booking Analytics Dashboard"
)

st.write(
    "Analyze hotel performance, customer behavior and booking trends."
)



if filtered_df.empty:

    st.warning(
        "No bookings found for the selected filters."
    )

    st.stop()




kpis = get_overall_kpis(
    filtered_df
)




col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "Total Bookings",
        f"{kpis['total_bookings']:,}"
    )


with col2:

    st.metric(
        "Total Guests",
        f"{kpis['total_guests']:,}"
    )


with col3:

    st.metric(
        "Estimated Revenue",
        f"${kpis['total_revenue']:,.0f}"
    )


with col4:

    st.metric(
        "Average ADR",
        f"${kpis['average_adr']:.2f}"
    )


with col5:

    st.metric(
        "Cancellation Rate",
        f"{kpis['cancellation_rate']:.1f}%"
    )


st.divider()




overview_tab, hotel_tab, customer_tab, booking_tab = st.tabs(
    [
        "📊 Overview",
        "🏨 Hotels",
        "👤 Customers",
        "📅 Bookings"
    ]
)



with overview_tab:

    st.header(
        "Overall Performance"
    )

    monthly_data = monthly_booking_analysis(
        filtered_df
    )

    hotel_data = hotel_analysis(
        filtered_df
    )

    col1, col2 = st.columns(2)

    with col1:

        if not monthly_data.empty:

            fig = monthly_booking_chart(
                monthly_data
            )

            st.pyplot(
                fig,
                use_container_width=True
            )

    with col2:

        if not hotel_data.empty:

            fig = hotel_booking_chart(
                hotel_data
            )

            st.pyplot(
                fig,
                use_container_width=True
            )

    st.subheader(
        "Hotel Summary"
    )

    st.dataframe(
        hotel_data.round(2),
        use_container_width=True,
        hide_index=True
    )




with hotel_tab:

    st.header(
        "🏨 Hotel Performance"
    )

    hotel_data = hotel_analysis(
        filtered_df
    )

    col1, col2 = st.columns(2)

    with col1:

        fig = hotel_booking_chart(
            hotel_data
        )

        st.pyplot(
            fig,
            use_container_width=True
        )

    with col2:

        fig = hotel_cancellation_chart(
            hotel_data
        )

        st.pyplot(
            fig,
            use_container_width=True
        )

    st.subheader(
        "Hotel Performance Data"
    )

    st.dataframe(
        hotel_data.round(2),
        use_container_width=True,
        hide_index=True
    )




with customer_tab:

    st.header(
        "👤 Customer Analysis"
    )

    customer_data = customer_type_analysis(
        filtered_df
    )

    country_data = country_analysis(
        filtered_df
    )

    repeated_data = repeated_guest_analysis(
        filtered_df
    )

    col1, col2 = st.columns(2)

    with col1:

        fig = customer_type_chart(
            customer_data
        )

        st.pyplot(
            fig,
            use_container_width=True
        )

    with col2:

        fig = repeated_guest_chart(
            repeated_data
        )

        st.pyplot(
            fig,
            use_container_width=True
        )

    st.subheader(
        "Top 10 Countries"
    )

    fig = top_country_chart(
        country_data
    )

    st.pyplot(
        fig,
        use_container_width=True
    )

    st.subheader(
        "Customer Type Data"
    )

    st.dataframe(
        customer_data.round(2),
        use_container_width=True,
        hide_index=True
    )

    st.subheader(
        "Country Data"
    )

    st.dataframe(
        country_data.head(20),
        use_container_width=True,
        hide_index=True
    )



with booking_tab:

    st.header(
        "📅 Booking Analysis"
    )

    segment_data = market_segment_analysis(
        filtered_df
    )

    room_data = room_type_analysis(
        filtered_df
    )

    col1, col2 = st.columns(2)

    with col1:

        fig = market_segment_chart(
            segment_data
        )

        st.pyplot(
            fig,
            use_container_width=True
        )

    with col2:

        fig = room_type_chart(
            room_data
        )

        st.pyplot(
            fig,
            use_container_width=True
        )

    st.subheader(
        "Booking Lead Time"
    )

    fig = lead_time_chart(
        filtered_df
    )

    st.pyplot(
        fig,
        use_container_width=True
    )

    st.subheader(
        "Market Segment Data"
    )

    st.dataframe(
        segment_data.round(2),
        use_container_width=True,
        hide_index=True
    )

    st.subheader(
        "Room Type Data"
    )

    st.dataframe(
        room_data.round(2),
        use_container_width=True,
        hide_index=True
    )




st.sidebar.divider()

st.sidebar.write(
    f"Showing {len(filtered_df):,} bookings"
)

st.sidebar.write(
    "Hotel Booking Analytics"
)