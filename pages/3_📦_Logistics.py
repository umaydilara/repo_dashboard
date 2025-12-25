"""
PAGE 3: PRICE, LOGISTICS & DELIVERY
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Logistics", page_icon="📦", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('../demand_features_final.csv')
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

df = load_data()

# Sidebar
st.sidebar.title("⚙️ Settings")
volatility_threshold = st.sidebar.slider("Volatility Threshold", 10, 50, 30)

st.title("📦 Price, Logistics & Delivery")
st.markdown("### How do operations affect demand?")
st.markdown("---")

st.info("**🎯 Key Question:** How do price, freight, and delivery impact demand?")

# Volatility Analysis
st.subheader("🌊 Demand Volatility Analysis")

col1, col2 = st.columns(2)

with col1:
    if 'volatility_30' in df.columns:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['order_date'], y=df['volatility_30'],
                                 mode='lines', fill='tozeroy',
                                 line=dict(color='#FB8C00')))
        fig.add_hline(y=volatility_threshold, line_dash='dash', line_color='red',
                      annotation_text=f'Threshold: {volatility_threshold}')
        fig.update_layout(title='30-Day Volatility Over Time',
                          height=350, template='plotly_white',
                          yaxis_title='Volatility')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Volatility data not available")

with col2:
    if 'rolling_std_30' in df.columns:
        fig = px.histogram(df, x='rolling_std_30', nbins=30,
                           title='Rolling Std Distribution (30-day)',
                           color_discrete_sequence=['#E53935'])
        fig.update_layout(height=350, template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Trend Analysis
st.subheader("📈 Trend Indicators")

trend_cols = ['trend_15_30', 'trend_30_90', 'trend_90_180', 'trend_180_360']
available_trends = [c for c in trend_cols if c in df.columns]

if available_trends:
    col1, col2 = st.columns(2)
    
    with col1:
        # Trend distribution
        trend_means = {col: df[col].mean() for col in available_trends}
        
        fig = go.Figure(data=[
            go.Bar(x=list(trend_means.keys()), y=list(trend_means.values()),
                   marker_color=['#1E88E5', '#43A047', '#FB8C00', '#E53935'])
        ])
        fig.add_hline(y=1, line_dash='dash', line_color='gray',
                      annotation_text='No trend (1.0)')
        fig.update_layout(title='Average Trend Ratios',
                          height=350, template='plotly_white',
                          yaxis_title='Trend Ratio')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Trend over time (first available)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['order_date'], y=df[available_trends[0]],
                                 mode='lines', name=available_trends[0],
                                 line=dict(color='#1E88E5')))
        fig.add_hline(y=1, line_dash='dash', line_color='red')
        fig.update_layout(title=f'{available_trends[0]} Over Time',
                          height=350, template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Regime Analysis
st.subheader("🎯 Demand Regime Analysis")

regime_cols = ['is_high_short', 'is_high_long', 'is_peak_long']
available_regimes = [c for c in regime_cols if c in df.columns]

if available_regimes:
    col1, col2 = st.columns(2)
    
    with col1:
        # Regime distribution
        regime_counts = {col: df[col].sum() for col in available_regimes}
        
        fig = go.Figure(data=[
            go.Bar(x=list(regime_counts.keys()), y=list(regime_counts.values()),
                   marker_color=['#43A047', '#1E88E5', '#FB8C00'])
        ])
        fig.update_layout(title='Days in Each Regime',
                          height=350, template='plotly_white',
                          yaxis_title='Number of Days')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # High regime demand comparison
        if 'is_high_long' in df.columns:
            high_demand = df[df['is_high_long'] == 1]['daily_orders'].mean()
            low_demand = df[df['is_high_long'] == 0]['daily_orders'].mean()
            
            fig = go.Figure(data=[
                go.Bar(x=['Normal Period', 'High Regime'],
                       y=[low_demand, high_demand],
                       marker_color=['#90CAF9', '#1E88E5'])
            ])
            fig.update_layout(title='Avg Orders: Normal vs High Regime',
                              height=350, template='plotly_white',
                              yaxis_title='Avg Daily Orders')
            st.plotly_chart(fig, use_container_width=True)

# Insights
st.markdown("---")
st.success("""
**💡 Key Insights:**
- Volatility indicates demand uncertainty - important for inventory planning
- Trend ratios show direction of demand changes
- Regime indicators help identify high/low demand periods
- Operational metrics can be used as external variables in forecasting
""")
