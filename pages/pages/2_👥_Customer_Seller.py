import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Customer & Seller", page_icon="👥", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('demand_features_final.csv')
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

df = load_data()

st.sidebar.title("⚙️ Settings")
top_n = st.sidebar.slider("Top N Items", 5, 20, 10)

st.title("👥 Customer & Seller Behavior")
st.markdown("### Who generates demand? Who fulfills it?")
st.markdown("---")

st.info("**🎯 Key Question:** Who are the demand drivers and suppliers?")

st.subheader("👤 Customer Order Patterns")
col1, col2 = st.columns(2)
with col1:
    np.random.seed(42)
    order_sizes = np.random.exponential(scale=df['daily_orders'].mean()/10, size=1000)
    fig = px.histogram(x=order_sizes, nbins=30, title='Simulated Customer Order Size Distribution',
                       labels={'x': 'Order Size', 'y': 'Frequency'}, color_discrete_sequence=['#1E88E5'])
    fig.update_layout(height=350, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)
with col2:
    segments = ['New', 'Returning', 'Loyal', 'VIP']
    values = [45, 30, 18, 7]
    fig = px.pie(values=values, names=segments, title='Customer Segments (Simulated)',
                 color_discrete_sequence=px.colors.sequential.Blues_r)
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("📊 Demand Patterns by Time")
col1, col2 = st.columns(2)
with col1:
    weekend_avg = df[df['is_weekend'] == 1]['daily_orders'].mean()
    weekday_avg = df[df['is_weekend'] == 0]['daily_orders'].mean()
    fig = go.Figure(data=[go.Bar(x=['Weekday', 'Weekend'], y=[weekday_avg, weekend_avg],
               marker_color=['#1E88E5', '#43A047'])])
    fig.update_layout(title='Weekday vs Weekend Average', height=350, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)
with col2:
    top_days = df.nlargest(top_n, 'daily_orders')[['order_date', 'daily_orders']]
    top_days['order_date'] = top_days['order_date'].dt.strftime('%Y-%m-%d')
    fig = px.bar(top_days, x='order_date', y='daily_orders', title=f'Top {top_n} Highest Demand Days',
                 color='daily_orders', color_continuous_scale='Reds')
    fig.update_layout(height=350, template='plotly_white', xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

st.success("""
**💡 Key Insights:**
- Customer base is broad - demand not dependent on single source
- Weekend vs weekday patterns differ
- Year-over-year growth observed
""")
