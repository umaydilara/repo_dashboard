"""
PAGE 7: TIME SERIES MODELS FOCUS
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Time Series Focus", page_icon="📈", layout="wide")

st.title("📈 Time Series Models Focus")
st.markdown("### Prophet vs LSTM - Classic vs Deep Learning")
st.markdown("---")

st.info("**🎯 Key Question:** Classic time series or deep learning?")

# Comparison Chart
st.subheader("🔄 Prophet vs LSTM Comparison")

np.random.seed(42)
x = np.arange(100)
actual = 100 + np.cumsum(np.random.randn(100)) + 15*np.sin(x*2*np.pi/30)
prophet_pred = actual + np.random.randn(100)*25 + 10
lstm_pred = actual + np.random.randn(100)*20 - 5

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=actual, mode='lines', name='Actual',
                         line=dict(color='#1E88E5', width=2)))
fig.add_trace(go.Scatter(x=x, y=prophet_pred, mode='lines', name='Prophet',
                         line=dict(color='#FB8C00', width=2, dash='dash')))
fig.add_trace(go.Scatter(x=x, y=lstm_pred, mode='lines', name='LSTM',
                         line=dict(color='#8E24AA', width=2, dash='dot')))

fig.update_layout(height=400, template='plotly_white',
                  title='Predictions Comparison',
                  xaxis_title='Test Sample',
                  yaxis_title='Daily Orders',
                  legend=dict(orientation='h', yanchor='bottom', y=1.02))
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Side by side comparison
col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Prophet")
    
    st.markdown("""
    **Type:** Additive Decomposition Model
    
    ### ✅ Strengths
    - Automatic seasonality detection
    - Handles missing data well
    - Interpretable components
    - Fast training
    - Holiday effects modeling
    
    ### ⚠️ Weaknesses
    - Only uses time-based features
    - Cannot incorporate external features
    - Assumes simple seasonality
    - **R² = -0.020** (worse than baseline!)
    """)
    
    st.error("""
    **Why it failed here:**
    - Cannot use our engineered features
    - Demand pattern is more complex than simple seasonality
    """)

with col2:
    st.subheader("🧠 LSTM")
    
    st.markdown("""
    **Type:** Recurrent Neural Network
    
    ### ✅ Strengths
    - Captures long-term dependencies
    - Non-linear pattern recognition
    - Sequence learning capability
    - Can handle complex patterns
    
    ### ⚠️ Weaknesses
    - Requires large datasets
    - Black box model
    - Long training time
    - **R² = 0.159** (poor performance)
    """)
    
    st.warning("""
    **Why it underperformed:**
    - 611 days is insufficient training data
    - Neural networks need thousands of samples
    - Overfitting risk with small data
    """)

st.markdown("---")

# Why Tree-Based Won
st.subheader("💡 Why Tree-Based Models Outperformed?")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    ### 📊 Data Size
    
    - 611 days of data
    - LSTM needs 1000s of samples
    - Tree models work with small data
    """)

with col2:
    st.info("""
    ### 🛠️ Feature Engineering
    
    - We created valuable features
    - Prophet can't use them
    - Tree models leverage them all
    """)

with col3:
    st.info("""
    ### 📈 Data Structure
    
    - Complex demand patterns
    - Not simple seasonality
    - Regime changes present
    """)

# Metrics comparison
st.subheader("📊 Direct Comparison")

comparison_df = pd.DataFrame({
    'Metric': ['RMSE', 'MAE', 'R²', 'Training Time', 'Interpretability', 'Uses Features'],
    'Prophet': ['83.30', '69.79', '-0.020', 'Fast', 'High', '❌ No'],
    'LSTM': ['75.36', '63.45', '0.159', 'Slow', 'Low', '⚠️ Limited'],
    'LightGBM': ['31.62', '26.82', '0.853', 'Fast', 'High', '✅ Yes']
})

st.dataframe(comparison_df, use_container_width=True, hide_index=True)

# Insights
st.markdown("---")
st.success("""
**💡 Key Insights:**
- **LSTM captured some patterns** - but insufficient data
- **Prophet is too simplistic** - can't use engineered features
- **For this dataset, tree-based is optimal** - feature engineering + tree = success
- **With more data, LSTM could improve** - but we have what we have
""")
