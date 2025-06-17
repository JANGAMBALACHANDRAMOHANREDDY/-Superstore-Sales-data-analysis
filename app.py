import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Superstore Sales Dashboard")

uploaded_file = st.file_uploader("Upload your train.csv file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
    df = df.dropna(subset=['Order Date'])

    total_sales = df['Sales'].sum()
    total_orders = df['Order ID'].nunique()
    total_customers = df['Customer ID'].nunique()

    st.metric("💰 Total Sales", f"${total_sales:,.2f}")
    st.metric("📦 Total Orders", total_orders)
    st.metric("👥 Unique Customers", total_customers)

    region = st.selectbox("Select Region", options=['All'] + sorted(df['Region'].unique().tolist()))
    category = st.multiselect("Filter by Category", options=df['Category'].unique())

    filtered_df = df.copy()
    if region != 'All':
        filtered_df = filtered_df[filtered_df['Region'] == region]
    if category:
        filtered_df = filtered_df[filtered_df['Category'].isin(category)]

    filtered_df.set_index('Order Date', inplace=True)
    monthly_sales = filtered_df['Sales'].resample('M').sum()

    st.subheader("📅 Monthly Sales Trend")
    fig, ax = plt.subplots()
    monthly_sales.plot(ax=ax, color='teal')
    plt.xlabel("Month")
    plt.ylabel("Sales ($)")
    st.pyplot(fig)

    st.subheader("📦 Sales by Category")
    cat_sales = filtered_df.groupby("Category")["Sales"].sum()
    st.bar_chart(cat_sales)

    st.subheader("🌍 Sales by Region")
    reg_sales = filtered_df.groupby("Region")["Sales"].sum()
    st.bar_chart(reg_sales)
