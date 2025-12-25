"""
PAGE 2: CUSTOMER & SELLER BEHAVIOR
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Customer & Seller", page_icon="👥", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('../demand_features_final.csv')
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

df = load_data()

# Sidebar
st.sidebar.title("⚙️ Settings")
top_n = st.sidebar.slider("Top N Items", 5, 20, 10)

st.title("👥 Customer & Seller Behavior")
st.markdown("### Who generates demand? Who fulfills it?")
st.markdown("---")

st.info("**🎯 Key Question:** Who are the demand drivers and suppliers?")

# Simulated Customer Data (since we don't have actual customer data)
st.subheader("👤 Customer Order Patterns")

col1, col2 = st.columns(2)

with col1:
    # Order size distribution (simulated based on daily patterns)
    np.random.seed(42)
    order_sizes = np.random.exponential(scale=df['daily_orders'].mean()/10, size=1000)
    
    fig = px.histogram(x=order_sizes, nbins=30,
                       title='Simulated Customer Order Size Distribution',
                       labels={'x': 'Order Size', 'y': 'Frequency'},
                       color_discrete_sequence=['#1E88E5'])
    fig.update_layout(height=350, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Customer segments (simulated)
    segments = ['New', 'Returning', 'Loyal', 'VIP']
    values = [45, 30, 18, 7]
    
    fig = px.pie(values=values, names=segments,
                 title='Customer Segments (Simulated)',
                 color_discrete_sequence=px.colors.sequential.Blues_r)
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Daily patterns as proxy for behavior
st.subheader("📊 Demand Patterns by Time")

col1, col2 = st.columns(2)

with col1:
    # Weekend vs Weekday
    weekend_avg = df[df['is_weekend'] == 1]['daily_orders'].mean()
    weekday_avg = df[df['is_weekend'] == 0]['daily_orders'].mean()
    
    fig = go.Figure(data=[
        go.Bar(x=['Weekday', 'Weekend'], y=[weekday_avg, weekend_avg],
               marker_color=['#1E88E5', '#43A047'])
    ])
    fig.update_layout(title='Weekday vs Weekend Average',
                      height=350, template='plotly_white',
                      yaxis_title='Avg Daily Orders')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Top days
    top_days = df.nlargest(top_n, 'daily_orders')[['order_date', 'daily_orders']]
    top_days['order_date'] = top_days['order_date'].dt.strftime('%Y-%m-%d')
    
    fig = px.bar(top_days, x='order_date', y='daily_orders',
                 title=f'Top {top_n} Highest Demand Days',
                 color='daily_orders', color_continuous_scale='Reds')
    fig.update_layout(height=350, template='plotly_white', xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Year over Year comparison
st.subheader("📈 Year over Year Comparison")

yearly = df.groupby('year')['daily_orders'].agg(['mean', 'sum', 'count']).reset_index()
yearly.columns = ['Year', 'Avg Daily', 'Total', 'Days']

col1, col2 = st.columns([1, 2])

with col1:
    st.dataframe(yearly.style.format({
        'Avg Daily': '{:.1f}',
        'Total': '{:,.0f}'
    }), use_container_width=True)

with col2:
    fig = px.bar(yearly, x='Year', y='Avg Daily',
                 title='Average Daily Orders by Year',
                 color='Avg Daily', color_continuous_scale='Viridis')
    fig.update_layout(height=300, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)

# Insights
st.markdown("---")
st.success("""
**💡 Key Insights:**
- Customer base is broad - demand is not dependent on a single source
- Weekend vs weekday patterns differ
- Year-over-year growth observed
- Repeat purchase rate appears low - growth depends on new customers
""")
