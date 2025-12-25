import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Logistics & Operations", page_icon="🚚", layout="wide")

st.title("🚚 Logistics & Operations Analysis")
st.markdown("---")

@st.cache_data
def load_data():
    df = pd.read_csv('demand_features_final.csv')
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

df = load_data()

# Sidebar
st.sidebar.header("🎛️ Filters")
rolling_window = st.sidebar.slider("Rolling Average Window (days)", 3, 30, 7)

# Calculate rolling statistics
df['rolling_mean'] = df['daily_orders'].rolling(window=rolling_window).mean()
df['rolling_std'] = df['daily_orders'].rolling(window=rolling_window).std()

# Key Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📊 Order Volatility", f"{df['daily_orders'].std():.1f}")
with col2:
    st.metric("📈 Trend Direction", "↗️ Upward" if df['daily_orders'].iloc[-30:].mean() > df['daily_orders'].iloc[:30].mean() else "↘️ Downward")
with col3:
    st.metric("🎯 Coefficient of Variation", f"{(df['daily_orders'].std() / df['daily_orders'].mean() * 100):.1f}%")
with col4:
    peak_day = df.loc[df['daily_orders'].idxmax(), 'order_date'].strftime('%Y-%m-%d')
    st.metric("🔝 Peak Day", peak_day)

st.markdown("---")

# Rolling Average Chart
st.subheader(f"📈 {rolling_window}-Day Rolling Average")
fig_rolling = go.Figure()
fig_rolling.add_trace(go.Scatter(x=df['order_date'], y=df['daily_orders'], 
                                  mode='lines', name='Daily Orders', opacity=0.5))
fig_rolling.add_trace(go.Scatter(x=df['order_date'], y=df['rolling_mean'], 
                                  mode='lines', name=f'{rolling_window}-Day Average', line=dict(width=3)))
fig_rolling.update_layout(title=f'Daily Orders with {rolling_window}-Day Moving Average',
                          xaxis_title='Date', yaxis_title='Orders',
                          hovermode='x unified')
st.plotly_chart(fig_rolling, use_container_width=True)

# Volatility Analysis
st.subheader("📊 Demand Volatility Over Time")
fig_vol = go.Figure()
fig_vol.add_trace(go.Scatter(x=df['order_date'], y=df['rolling_std'],
                              mode='lines', name='Rolling Std Dev', fill='tozeroy'))
fig_vol.update_layout(title='Order Volatility (Rolling Standard Deviation)',
                      xaxis_title='Date', yaxis_title='Standard Deviation')
st.plotly_chart(fig_vol, use_container_width=True)

# Weekly Pattern
st.subheader("📅 Weekly Operational Pattern")
if 'dayofweek' in df.columns:
    weekly_stats = df.groupby('dayofweek').agg({
        'daily_orders': ['mean', 'std', 'min', 'max']
    }).round(1)
    weekly_stats.columns = ['Average', 'Std Dev', 'Minimum', 'Maximum']
    weekly_stats.index = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][:len(weekly_stats)]
    
    st.dataframe(weekly_stats, use_container_width=True)

# Capacity Planning
st.subheader("🎯 Capacity Planning Insights")
col1, col2 = st.columns(2)

with col1:
    percentiles = [50, 75, 90, 95, 99]
    perc_values = [np.percentile(df['daily_orders'], p) for p in percentiles]
    
    fig_perc = px.bar(x=[f'{p}th' for p in percentiles], y=perc_values,
                      title='Order Volume Percentiles',
                      labels={'x': 'Percentile', 'y': 'Orders'})
    st.plotly_chart(fig_perc, use_container_width=True)

with col2:
    st.markdown("""
    **📋 Capacity Recommendations:**
    - **Base Capacity:** Handle average daily volume
    - **Standard Capacity:** Cover 75th percentile
    - **Peak Capacity:** Prepare for 95th percentile
    - **Emergency Buffer:** Account for 99th percentile
    """)

st.markdown("---")
st.success("✅ **Recommendation:** Use rolling averages to smooth out daily fluctuations and plan logistics capacity accordingly.")
