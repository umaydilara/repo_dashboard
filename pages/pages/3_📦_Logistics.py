import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Logistics", page_icon="📦", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('demand_features_final.csv')
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

df = load_data()

st.sidebar.title("⚙️ Settings")
volatility_threshold = st.sidebar.slider("Volatility Threshold", 10, 50, 30)

st.title("📦 Price, Logistics & Delivery")
st.markdown("### How do operations affect demand?")
st.markdown("---")

st.info("**🎯 Key Question:** How do price, freight, and delivery impact demand?")

st.subheader("🌊 Demand Volatility Analysis")
col1, col2 = st.columns(2)
with col1:
    if 'volatility_30' in df.columns:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['order_date'], y=df['volatility_30'],
                                 mode='lines', fill='tozeroy', line=dict(color='#FB8C00')))
        fig.add_hline(y=volatility_threshold, line_dash='dash', line_color='red')
        fig.update_layout(title='30-Day Volatility Over Time', height=350, template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)
with col2:
    if 'rolling_std_30' in df.columns:
        fig = px.histogram(df, x='rolling_std_30', nbins=30, title='Rolling Std Distribution (30-day)',
                           color_discrete_sequence=['#E53935'])
        fig.update_layout(height=350, template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("🎯 Demand Regime Analysis")
regime_cols = ['is_high_short', 'is_high_long', 'is_peak_long']
available_regimes = [c for c in regime_cols if c in df.columns]
if available_regimes:
    col1, col2 = st.columns(2)
    with col1:
        regime_counts = {col: df[col].sum() for col in available_regimes}
        fig = go.Figure(data=[go.Bar(x=list(regime_counts.keys()), y=list(regime_counts.values()),
                   marker_color=['#43A047', '#1E88E5', '#FB8C00'])])
        fig.update_layout(title='Days in Each Regime', height=350, template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        if 'is_high_long' in df.columns:
            high_demand = df[df['is_high_long'] == 1]['daily_orders'].mean()
            low_demand = df[df['is_high_long'] == 0]['daily_orders'].mean()
            fig = go.Figure(data=[go.Bar(x=['Normal Period', 'High Regime'], y=[low_demand, high_demand],
                       marker_color=['#90CAF9', '#1E88E5'])])
            fig.update_layout(title='Avg Orders: Normal vs High Regime', height=350, template='plotly_white')
            st.plotly_chart(fig, use_container_width=True)

st.success("""
**💡 Key Insights:**
- Volatility indicates demand uncertainty
- Regime indicators help identify high/low demand periods
- Operational metrics useful for forecasting
""")
