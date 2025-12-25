"""
DEMAND FORECASTING DASHBOARD
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Demand Forecasting", page_icon="📊", layout="wide")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('demand_features_final.csv')
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

# Try loading
try:
    df = load_data()
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.stop()

# Sidebar
st.sidebar.title("📊 Demand Forecasting")
st.sidebar.markdown("**Olist E-commerce Analysis**")
st.sidebar.markdown("---")
st.sidebar.success(f"✅ {len(df)} days loaded")

st.sidebar.markdown("""
### 📖 Pages
1. 🏠 Home
2. 📈 EDA Overview
3. 👥 Customer & Seller
4. 📦 Logistics
5. 🛠️ Feature Engineering
6. 🎯 Feature Selection
7. 🏆 Model Comparison
8. 🌟 Final Insights
""")

# Main Page
st.title("📊 Demand Forecasting Dashboard")
st.markdown("### Olist E-commerce Platform Analysis")
st.markdown("---")

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("📅 Total Days", len(df))
col2.metric("📦 Avg Orders", f"{df['daily_orders'].mean():.0f}")
col3.metric("📈 Max Orders", f"{df['daily_orders'].max():.0f}")
col4.metric("📊 Total", f"{df['daily_orders'].sum():,.0f}")

st.markdown("---")

# Chart
st.subheader("📈 Daily Orders Trend")
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['order_date'], y=df['daily_orders'], 
                         mode='lines', name='Daily Orders',
                         line=dict(color='#1E88E5')))
if 'rolling_mean_30' in df.columns:
    fig.add_trace(go.Scatter(x=df['order_date'], y=df['rolling_mean_30'],
                             mode='lines', name='30-Day MA',
                             line=dict(color='#E53935', width=2)))
fig.update_layout(height=400, template='plotly_white', hovermode='x unified')
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.info("👈 **Navigate to other pages using the sidebar**")
