import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="EDA Overview", page_icon="📈", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('demand_features_final.csv')
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

df = load_data()

st.sidebar.title("⚙️ EDA Settings")
n_bins = st.sidebar.slider("Histogram Bins", 10, 50, 30)
show_outliers = st.sidebar.checkbox("Show Outliers", value=True)

st.title("📈 EDA & Data Overview")
st.markdown("### What does this data tell us?")
st.markdown("---")

st.info("**🎯 Key Question:** What is the demand pattern in Olist platform?")

st.subheader("📊 Time Series Analysis")
fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    subplot_titles=['Daily Orders', 'Weekly Average'],
                    vertical_spacing=0.1)
fig.add_trace(go.Scatter(x=df['order_date'], y=df['daily_orders'],
                         mode='lines', name='Daily', line=dict(color='#1E88E5')), row=1, col=1)
weekly = df.set_index('order_date').resample('W')['daily_orders'].mean().reset_index()
fig.add_trace(go.Scatter(x=weekly['order_date'], y=weekly['daily_orders'],
                         mode='lines+markers', name='Weekly Avg', line=dict(color='#43A047')), row=2, col=1)
fig.update_layout(height=500, template='plotly_white', showlegend=True)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("📊 Distribution Analysis")
col1, col2 = st.columns(2)
with col1:
    fig = px.histogram(df, x='daily_orders', nbins=n_bins, title='Daily Orders Distribution',
                       color_discrete_sequence=['#1E88E5'])
    fig.add_vline(x=df['daily_orders'].mean(), line_dash='dash', line_color='red')
    fig.update_layout(height=350, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)
with col2:
    fig = px.box(df, y='daily_orders', title='Box Plot', color_discrete_sequence=['#43A047'],
                 points='outliers' if show_outliers else False)
    fig.update_layout(height=350, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("📅 Seasonality Patterns")
col1, col2 = st.columns(2)
with col1:
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily_avg = df.groupby('dayofweek')['daily_orders'].mean().reset_index()
    daily_avg['day_name'] = daily_avg['dayofweek'].map(lambda x: days[x])
    fig = px.bar(daily_avg, x='day_name', y='daily_orders', title='Average by Day of Week',
                 color='daily_orders', color_continuous_scale='Blues')
    fig.update_layout(height=350, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)
with col2:
    monthly_avg = df.groupby('month')['daily_orders'].mean().reset_index()
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_avg['month_name'] = monthly_avg['month'].map(lambda x: months[x-1])
    fig = px.bar(monthly_avg, x='month_name', y='daily_orders', title='Average by Month',
                 color='daily_orders', color_continuous_scale='Greens')
    fig.update_layout(height=350, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)

st.success("""
**💡 Key Insights:**
- Demand is spread over time with no sudden breaks
- Clear weekly pattern visible
- Rising trend observed
""")
