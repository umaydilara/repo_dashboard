import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="EDA Overview", page_icon="📈", layout="wide")

df = pd.read_csv('demand_features_final.csv')
df['order_date'] = pd.to_datetime(df['order_date'])

st.title("📈 EDA & Data Overview")
st.markdown("---")

# Time Series
st.subheader("📊 Time Series")
fig = px.line(df, x='order_date', y='daily_orders', title='Daily Orders')
st.plotly_chart(fig, use_container_width=True)

# Distribution
col1, col2 = st.columns(2)
with col1:
    fig = px.histogram(df, x='daily_orders', title='Distribution')
    st.plotly_chart(fig, use_container_width=True)
with col2:
    fig = px.box(df, y='daily_orders', title='Box Plot')
    st.plotly_chart(fig, use_container_width=True)
