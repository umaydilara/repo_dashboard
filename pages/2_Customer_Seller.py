import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Customer & Seller Behavior", page_icon="👥", layout="wide")

st.title("👥 Customer & Seller Behavior Analysis")
st.markdown("---")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('demand_features_final.csv')
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🎛️ Filters")
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df['order_date'].min(), df['order_date'].max()),
    min_value=df['order_date'].min(),
    max_value=df['order_date'].max()
)

# Filter data
if len(date_range) == 2:
    mask = (df['order_date'] >= pd.to_datetime(date_range[0])) & (df['order_date'] <= pd.to_datetime(date_range[1]))
    filtered_df = df[mask]
else:
    filtered_df = df

# Key Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📅 Total Days", len(filtered_df))
with col2:
    st.metric("📦 Total Orders", f"{filtered_df['daily_orders'].sum():,.0f}")
with col3:
    st.metric("📈 Avg Daily Orders", f"{filtered_df['daily_orders'].mean():.1f}")
with col4:
    st.metric("🔝 Max Daily Orders", f"{filtered_df['daily_orders'].max():,.0f}")

st.markdown("---")

# Daily Orders Over Time
st.subheader("📈 Daily Orders Trend")
fig_trend = px.line(filtered_df, x='order_date', y='daily_orders', 
                    title='Daily Orders Over Time',
                    labels={'order_date': 'Date', 'daily_orders': 'Number of Orders'})
fig_trend.update_layout(hovermode='x unified')
st.plotly_chart(fig_trend, use_container_width=True)

# Day of Week Analysis
st.subheader("📅 Orders by Day of Week")
if 'dayofweek' in filtered_df.columns:
    dow_data = filtered_df.groupby('dayofweek')['daily_orders'].mean().reset_index()
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dow_data['day_name'] = dow_data['dayofweek'].apply(lambda x: day_names[int(x)] if x < 7 else 'Unknown')
    
    fig_dow = px.bar(dow_data, x='day_name', y='daily_orders',
                     title='Average Orders by Day of Week',
                     labels={'day_name': 'Day', 'daily_orders': 'Average Orders'},
                     color='daily_orders', color_continuous_scale='Blues')
    st.plotly_chart(fig_dow, use_container_width=True)

# Monthly Analysis
st.subheader("📆 Monthly Order Distribution")
if 'month' in filtered_df.columns:
    monthly_data = filtered_df.groupby('month')['daily_orders'].sum().reset_index()
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_data['month_name'] = monthly_data['month'].apply(lambda x: month_names[int(x)-1] if 1 <= x <= 12 else 'Unknown')
    
    fig_monthly = px.bar(monthly_data, x='month_name', y='daily_orders',
                         title='Total Orders by Month',
                         labels={'month_name': 'Month', 'daily_orders': 'Total Orders'},
                         color='daily_orders', color_continuous_scale='Viridis')
    st.plotly_chart(fig_monthly, use_container_width=True)

# Distribution Analysis
st.subheader("📊 Order Distribution")
col1, col2 = st.columns(2)
with col1:
    fig_hist = px.histogram(filtered_df, x='daily_orders', nbins=30,
                            title='Distribution of Daily Orders',
                            labels={'daily_orders': 'Daily Orders', 'count': 'Frequency'})
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    fig_box = px.box(filtered_df, y='daily_orders',
                     title='Order Volume Box Plot',
                     labels={'daily_orders': 'Daily Orders'})
    st.plotly_chart(fig_box, use_container_width=True)

st.markdown("---")
st.info("💡 **Insight:** Analyze customer ordering patterns to identify peak days and optimize resource allocation.")
