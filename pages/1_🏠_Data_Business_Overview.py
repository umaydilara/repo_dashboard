"""
DASHBOARD 1: DATA & BUSINESS OVERVIEW
"What does this data tell us? What kind of demand pattern does Olist show?"
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Data & Business Overview", page_icon="🏠", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('demand_features_final.csv')
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

df = load_data()

st.title("🏠 Data & Business Overview")
st.markdown("### EDA - The Big Picture")
st.markdown("---")

# Main question
st.info("""
**🎯 Main Question:** What does this data tell us? What kind of demand pattern does Olist show?
""")

# Dataset Overview
st.subheader("📊 1. Dataset Overview")
st.markdown("*Data scope, date range, volume*")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📅 Start Date", f"{df['order_date'].min().strftime('%Y-%m-%d')}")
with col2:
    st.metric("📅 End Date", f"{df['order_date'].max().strftime('%Y-%m-%d')}")
with col3:
    st.metric("📊 Total Days", len(df))
with col4:
    st.metric("🔢 Feature Count", len(df.columns))

# Data types
st.markdown("**Data Types:**")
col1, col2 = st.columns(2)
with col1:
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    st.write(f"- Numeric Variables: **{len(numeric_cols)}**")
with col2:
    st.write(f"- Total Rows: **{len(df):,}**")

st.markdown("""
<div style='background-color: #ef9a9a; padding: 15px; border-radius: 8px; margin: 10px 0;'>
<b>📝 Comment:</b> The general structure of the dataset, data types, and missing value ratio are displayed.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Time Series Analysis
st.subheader("📈 2. Time Series Analysis")
st.markdown("*How does demand change over time?*")

fig_ts = px.line(df, x='order_date', y='daily_orders',
                 title='Daily Order Trend',
                 labels={'order_date': 'Date', 'daily_orders': 'Daily Orders'})
fig_ts.update_layout(hovermode='x unified')
st.plotly_chart(fig_ts, use_container_width=True)

st.markdown("""
<div style='background-color: #ef9a9a; padding: 15px; border-radius: 8px; margin: 10px 0;'>
<b>📝 Comment:</b> Demand is spread over time with no sudden breaks. Rising trend and seasonal patterns are visible.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Distribution Analysis
st.subheader("📦 3. Demand Distribution")
st.markdown("*How is order volume distributed?*")

col1, col2 = st.columns(2)

with col1:
    fig_hist = px.histogram(df, x='daily_orders', nbins=30,
                            title='Daily Orders Distribution',
                            labels={'daily_orders': 'Daily Orders', 'count': 'Frequency'})
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    fig_box = px.box(df, y='daily_orders',
                     title='Orders Box Plot',
                     labels={'daily_orders': 'Daily Orders'})
    st.plotly_chart(fig_box, use_container_width=True)

st.markdown("""
<div style='background-color: #ef9a9a; padding: 15px; border-radius: 8px; margin: 10px 0;'>
<b>📝 Comment:</b> The platform has a multi-category structure. Some days have dominant order volumes.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Weekly Pattern
st.subheader("💳 4. Weekly Pattern")
st.markdown("*Demand by day of week*")

if 'dayofweek' in df.columns:
    dow_avg = df.groupby('dayofweek')['daily_orders'].mean().reset_index()
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dow_avg['day_name'] = dow_avg['dayofweek'].apply(lambda x: day_names[int(x)] if x < 7 else 'Unknown')
    
    fig_dow = px.bar(dow_avg, x='day_name', y='daily_orders',
                     title='Average Orders by Day of Week',
                     labels={'day_name': 'Day', 'daily_orders': 'Average Orders'},
                     color='daily_orders', color_continuous_scale='Blues')
    st.plotly_chart(fig_dow, use_container_width=True)

st.markdown("""
<div style='background-color: #ef9a9a; padding: 15px; border-radius: 8px; margin: 10px 0;'>
<b>📝 Comment:</b> Weekday and weekend demand differences are observed.
</div>
""", unsafe_allow_html=True)

# Key Takeaways
st.markdown("---")
st.success("""
### 💡 Key Takeaways from This Page

- **Demand is spread over time** - no sudden breaks
- **Multi-category platform** - high product diversity
- **Weekly pattern exists** - opportunity for forecasting
- **Seasonal patterns present** - opportunity for feature engineering
""")
