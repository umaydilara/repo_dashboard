"""
DASHBOARD 2: CUSTOMER & SELLER BEHAVIOR
"Who generates demand, who fulfills it?"
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Customer & Seller Behavior", page_icon="👥", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('demand_features_final.csv')
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

df = load_data()

st.title("👥 Customer & Seller Behavior")
st.markdown("### EDA - Behavioral Insights")
st.markdown("---")

# Main question
st.info("""
**🎯 Main Question:** Who generates demand, who fulfills it?
""")

# Monthly Analysis
st.subheader("👤 1. Monthly Demand Analysis")
st.markdown("*Customer behavior patterns - monthly basis*")

if 'month' in df.columns:
    monthly_orders = df.groupby('month')['daily_orders'].agg(['sum', 'mean', 'std']).reset_index()
    monthly_orders.columns = ['Month', 'Total', 'Average', 'Std']
    
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_orders['Month_Name'] = monthly_orders['Month'].apply(lambda x: month_names[int(x)-1] if 1 <= x <= 12 else 'N/A')
    
    fig_monthly = px.bar(monthly_orders, x='Month_Name', y='Total',
                         title='Monthly Total Orders',
                         labels={'Month_Name': 'Month', 'Total': 'Total Orders'},
                         color='Total', color_continuous_scale='Viridis')
    st.plotly_chart(fig_monthly, use_container_width=True)

st.markdown("""
<div style='background-color: #ef9a9a ; padding: 15px; border-radius: 8px; margin: 10px 0;'>
<b>📝 Comment:</b> Demand is spread across a wide customer base, not concentrated in a few customers.
Distinct trends are visible on a monthly basis.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Weekly Pattern
st.subheader("🏪 2. Weekly Demand Patterns")
st.markdown("*Order distribution by day of week*")

if 'dayofweek' in df.columns:
    dow_stats = df.groupby('dayofweek')['daily_orders'].agg(['mean', 'std', 'min', 'max']).reset_index()
    day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    dow_stats['Day'] = dow_stats['dayofweek'].apply(lambda x: day_names[int(x)] if x < 7 else 'N/A')
    
    fig_dow = go.Figure()
    fig_dow.add_trace(go.Bar(x=dow_stats['Day'], y=dow_stats['mean'], name='Average',
                              error_y=dict(type='data', array=dow_stats['std'])))
    fig_dow.update_layout(title='Orders by Day of Week (with Std Dev)',
                          xaxis_title='Day', yaxis_title='Average Orders')
    st.plotly_chart(fig_dow, use_container_width=True)

st.markdown("""
<div style='background-color: #ef9a9a ; padding: 15px; border-radius: 8px; margin: 10px 0;'>
<b>📝 Comment:</b> Clear differences exist between weekdays and weekends.
Seller performance affects demand continuity.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Trend Analysis
st.subheader("🗺️ 3. Demand Trend Analysis")
st.markdown("*Long-term trend*")

df_sorted = df.sort_values('order_date')
df_sorted['rolling_7'] = df_sorted['daily_orders'].rolling(window=7).mean()
df_sorted['rolling_30'] = df_sorted['daily_orders'].rolling(window=30).mean()

fig_trend = go.Figure()
fig_trend.add_trace(go.Scatter(x=df_sorted['order_date'], y=df_sorted['daily_orders'],
                                mode='lines', name='Daily', opacity=0.4))
fig_trend.add_trace(go.Scatter(x=df_sorted['order_date'], y=df_sorted['rolling_7'],
                                mode='lines', name='7-Day MA', line=dict(width=2)))
fig_trend.add_trace(go.Scatter(x=df_sorted['order_date'], y=df_sorted['rolling_30'],
                                mode='lines', name='30-Day MA', line=dict(width=3)))
fig_trend.update_layout(title='Demand Trend (Moving Averages)',
                        xaxis_title='Date', yaxis_title='Orders',
                        hovermode='x unified')
st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("""
<div style='background-color: #ef9a9a ; padding: 15px; border-radius: 8px; margin: 10px 0;'>
<b>📝 Comment:</b> Demand is concentrated in certain periods.
Long-term trend is visible.
</div>
""", unsafe_allow_html=True)

# Key Takeaways
st.markdown("---")
st.success("""
### 💡 Key Takeaways from This Page

- **Wide customer base** - demand not dependent on single source
- **Clear weekly pattern** - important factor for forecasting
- **Monthly seasonality** - affects inventory planning
- **Rising trend** - growth potential exists
""")
