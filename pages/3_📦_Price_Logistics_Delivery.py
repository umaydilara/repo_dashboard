"""
DASHBOARD 3: PRICE, LOGISTICS & DELIVERY
"How do price, shipping, and delivery affect demand?"
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Price, Logistics & Delivery", page_icon="📦", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('demand_features_final.csv')
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

df = load_data()

st.title("📦 Price, Logistics & Delivery")
st.markdown("### EDA - Operational Perspective")
st.markdown("---")

# Main question
st.info("""
**🎯 Main Question:** How do price, shipping, and delivery affect demand?
""")

# Volatility Analysis
st.subheader("💰 1. Demand Volatility")
st.markdown("*Demand variability analysis*")

df_sorted = df.sort_values('order_date').copy()
df_sorted['rolling_std'] = df_sorted['daily_orders'].rolling(window=14).std()
df_sorted['rolling_mean'] = df_sorted['daily_orders'].rolling(window=14).mean()
df_sorted['cv'] = df_sorted['rolling_std'] / df_sorted['rolling_mean'] * 100

col1, col2 = st.columns(2)

with col1:
    fig_vol = px.line(df_sorted, x='order_date', y='rolling_std',
                      title='14-Day Rolling Volatility',
                      labels={'order_date': 'Date', 'rolling_std': 'Std Deviation'})
    st.plotly_chart(fig_vol, use_container_width=True)

with col2:
    fig_cv = px.line(df_sorted, x='order_date', y='cv',
                     title='Coefficient of Variation (%)',
                     labels={'order_date': 'Date', 'cv': 'CV %'})
    st.plotly_chart(fig_cv, use_container_width=True)

st.markdown("""
<div style='background-color: #e8f5e9; padding: 15px; border-radius: 8px; margin: 10px 0;'>
<b>📝 Comment:</b> Volatility changes over time. High volatility periods 
pose risks for inventory and logistics planning.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Operational Metrics
st.subheader("🚚 2. Operational Metrics")
st.markdown("*Statistics for capacity planning*")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📊 Average Orders", f"{df['daily_orders'].mean():.1f}")
with col2:
    st.metric("📈 Maximum", f"{df['daily_orders'].max():.0f}")
with col3:
    st.metric("📉 Minimum", f"{df['daily_orders'].min():.0f}")
with col4:
    st.metric("🎯 Std Deviation", f"{df['daily_orders'].std():.1f}")

# Percentile analysis
st.markdown("**Percentiles for Capacity Planning:**")
percentiles = [50, 75, 90, 95, 99]
perc_values = [np.percentile(df['daily_orders'], p) for p in percentiles]

fig_perc = px.bar(x=[f'{p}th Percentile' for p in percentiles], y=perc_values,
                  title='Order Volume Percentiles',
                  labels={'x': 'Percentile', 'y': 'Order Count'},
                  color=perc_values, color_continuous_scale='Oranges')
st.plotly_chart(fig_perc, use_container_width=True)

st.markdown("""
<div style='background-color: #e8f5e9; padding: 15px; border-radius: 8px; margin: 10px 0;'>
<b>📝 Comment:</b> The 95th percentile is critical for daily capacity planning.
Extra resources are needed for days above this value.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Peak Analysis
st.subheader("📏 3. Peak Days Analysis")
st.markdown("*High demand periods*")

threshold_90 = np.percentile(df['daily_orders'], 90)
df_peaks = df[df['daily_orders'] >= threshold_90].copy()

st.write(f"**Days above 90th percentile:** {len(df_peaks)} ({len(df_peaks)/len(df)*100:.1f}%)")

if 'dayofweek' in df_peaks.columns:
    peak_dow = df_peaks['dayofweek'].value_counts().sort_index()
    day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    fig_peak = px.bar(x=[day_names[int(i)] for i in peak_dow.index],
                      y=peak_dow.values,
                      title='Peak Days Distribution by Day of Week',
                      labels={'x': 'Day', 'y': 'Peak Day Count'})
    st.plotly_chart(fig_peak, use_container_width=True)

st.markdown("""
<div style='background-color: #e8f5e9; padding: 15px; border-radius: 8px; margin: 10px 0;'>
<b>📝 Comment:</b> Peak days are concentrated on certain days of the week.
Logistics capacity should be planned according to these days.
</div>
""", unsafe_allow_html=True)

# Key Takeaways
st.markdown("---")
st.success("""
### 💡 Key Takeaways from This Page

- **Variable volatility** - some periods are riskier
- **95th percentile is critical** - basis for capacity planning
- **Peak days are predictable** - weekly pattern exists
- **Operational metrics** - can be used as external variables in forecasting
""")
