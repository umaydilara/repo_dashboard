import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="EDA", page_icon="📈", layout="wide")

df = pd.read_csv('demand_features_final.csv')
df['order_date'] = pd.to_datetime(df['order_date'])

st.title("📈 EDA Overview")

fig = px.line(df, x='order_date', y='daily_orders')
st.plotly_chart(fig)

st.dataframe(df.head(10))
