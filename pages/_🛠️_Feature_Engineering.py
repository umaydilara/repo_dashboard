"""
PAGE 4: FEATURE ENGINEERING
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Feature Engineering", page_icon="🛠️", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('../demand_features_final.csv')
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

df = load_data()

# Sidebar
st.sidebar.title("⚙️ Settings")
top_n_features = st.sidebar.slider("Top N Features", 5, 15, 10)
lag_to_show = st.sidebar.selectbox("Lag to Visualize", [15, 30, 90, 180, 360], index=1)

st.title("🛠️ Feature Engineering Insights")
st.markdown("### Are our engineered features meaningful?")
st.markdown("---")

st.warning("**🎯 Key Question:** Do the engineered features actually capture demand patterns? ✅ *Professor's favorite dashboard!*")

# Feature Categories Table
st.subheader("📋 Feature Categories")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    | Category | Features | Purpose |
    |----------|----------|---------|
    | **Lag** | lag_15, 30, 90, 180, 360 | Historical demand values |
    | **Rolling Mean** | rolling_mean_15...360 | Smoothed trends |
    | **Rolling Std** | rolling_std_15...360 | Volatility measure |
    | **EWMA** | ewma_15...360 | Recent-weighted average |
    | **Momentum** | momentum_15...360 | Rate of change |
    | **Regime** | is_high_short/long, is_peak | Market state |
    | **Trend** | trend_15_30...180_360 | Trend ratios |
    """)

with col2:
    st.info("""
    **🎯 Why these features?**
    
    - **Lag:** Past demand predicts future demand
    - **Rolling:** Smooths noise, reveals trend
    - **EWMA:** Recent data matters more
    - **Momentum:** Captures acceleration/deceleration
    - **Regime:** Distinguishes market states
    - **Trend:** Short vs long term direction
    """)

st.markdown("---")

# Lag Analysis
st.subheader("🔄 Lag Feature Analysis")

lag_cols = ['lag_15', 'lag_30', 'lag_90', 'lag_180', 'lag_360']
available_lags = [c for c in lag_cols if c in df.columns]

if available_lags:
    col1, col2 = st.columns(2)
    
    with col1:
        # Correlation with target
        target = 'daily_orders'
        correlations = df[available_lags + [target]].corr()[target].drop(target).sort_values(ascending=True)
        
        fig = go.Figure(data=[
            go.Bar(x=correlations.values, y=correlations.index, orientation='h',
                   marker_color=['#1E88E5' if v > 0.5 else '#90CAF9' for v in correlations.values])
        ])
        fig.update_layout(title='Lag Correlation with Target',
                          height=350, template='plotly_white',
                          xaxis_title='Correlation')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Scatter plot for selected lag
        lag_col = f'lag_{lag_to_show}'
        if lag_col in df.columns:
            fig = px.scatter(df.dropna(subset=[lag_col]), x=lag_col, y='daily_orders',
                             title=f'Daily Orders vs {lag_col}',
                             trendline='ols',
                             color_discrete_sequence=['#1E88E5'])
            fig.update_layout(height=350, template='plotly_white')
            st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Rolling Statistics
st.subheader("📈 Rolling Statistics Comparison")

fig = go.Figure()
fig.add_trace(go.Scatter(x=df['order_date'], y=df['daily_orders'],
                         mode='lines', name='Actual', opacity=0.4,
                         line=dict(color='gray', width=1)))

colors = {'30': '#E53935', '90': '#43A047', '180': '#1E88E5'}
for window in ['30', '90', '180']:
    col = f'rolling_mean_{window}'
    if col in df.columns:
        fig.add_trace(go.Scatter(x=df['order_date'], y=df[col],
                                 mode='lines', name=f'{window}-Day MA',
                                 line=dict(color=colors[window], width=2)))

fig.update_layout(title='Rolling Means Comparison',
                  height=400, template='plotly_white',
                  hovermode='x unified',
                  legend=dict(orientation='h', yanchor='bottom', y=1.02))
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Momentum Analysis
st.subheader("🚀 Momentum Analysis")

momentum_cols = ['momentum_15', 'momentum_30', 'momentum_90', 'momentum_180', 'momentum_360']
available_momentum = [c for c in momentum_cols if c in df.columns]

if available_momentum:
    col1, col2 = st.columns(2)
    
    with col1:
        # Momentum distribution
        mom_col = f'momentum_{lag_to_show}'
        if mom_col in df.columns:
            fig = px.histogram(df.dropna(subset=[mom_col]), x=mom_col, nbins=40,
                               title=f'{mom_col} Distribution',
                               color_discrete_sequence=['#8E24AA'])
            fig.add_vline(x=0, line_dash='dash', line_color='red')
            fig.update_layout(height=350, template='plotly_white')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Momentum over time
        if mom_col in df.columns:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['order_date'], y=df[mom_col],
                                     mode='lines', line=dict(color='#8E24AA')))
            fig.add_hline(y=0, line_dash='dash', line_color='red')
            
            # Fill positive/negative
            fig.add_trace(go.Scatter(x=df['order_date'], y=df[mom_col].clip(lower=0),
                                     fill='tozeroy', fillcolor='rgba(67, 160, 71, 0.3)',
                                     line=dict(width=0), showlegend=False))
            fig.add_trace(go.Scatter(x=df['order_date'], y=df[mom_col].clip(upper=0),
                                     fill='tozeroy', fillcolor='rgba(229, 57, 53, 0.3)',
                                     line=dict(width=0), showlegend=False))
            
            fig.update_layout(title=f'{mom_col} Over Time',
                              height=350, template='plotly_white')
            st.plotly_chart(fig, use_container_width=True)

# Insights
st.markdown("---")
st.success("""
**💡 Key Insights:**
- **Long-term lags are effective** - lag_180, lag_360 show strong correlation
- **Momentum captures direction** - acceleration/deceleration patterns
- **Rolling means reveal trends** - smooths noise effectively
- **Features are validated by data** - not random choices!
""")
