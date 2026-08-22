import streamlit as st

from src.data_loader import load_data


st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
)


st.title("📊 Sales Analytics Dashboard")


payment, time, store, item, customer, fact = load_data()

st.write("Dashboard loaded successfully")