import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Time Series Focus", page_icon="📈", layout="wide")

st.title("📈 Time Series Models Focus")
st.markdown("### Prophet vs LSTM - Classic vs Deep Learning")
st.markdown("---")

st.info("**🎯 Key Question:** Classic time series or deep learning?")

st.subheader("🔄 Prophet vs LSTM Comparison")
np.random.seed(42)
x = np.arange(100)
actual = 100 + np.cumsum(np.random.randn(100)) + 15*np.sin(x*2*np.pi/30)
prophet_pred = actual + np.random.randn(100)*25 + 10
lstm_pred = actual + np.random.randn(100)*20 - 5

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=actual, mode='lines', name='Actual', line=dict(color='#1E88E5', width=2)))
fig.add_trace(go.Scatter(x=x, y=prophet_pred, mode='lines', name='Prophet', line=dict(color='#FB8C00', dash='dash')))
fig.add_trace(go.Scatter(x=x, y=lstm_pred, mode='lines', name='LSTM', line=dict(color='#8E24AA', dash='dot')))
fig.update_layout(height=400, template='plotly_white', title='Predictions Comparison')
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.subheader("📅 Prophet")
    st.markdown("""
    **✅ Strengths:**
    - Automatic seasonality detection
    - Interpretable components
    - Fast training
    
    **⚠️ Weaknesses:**
    - Only uses time-based features
    - Cannot use our engineered features
    - **R² = -0.020** (worse than baseline!)
    """)
with col2:
    st.subheader("🧠 LSTM")
    st.markdown("""
    **✅ Strengths:**
    - Captures long-term dependencies
    - Non-linear patterns
    
    **⚠️ Weaknesses:**
    - 611 days insufficient
    - Black box model
    - **R² = 0.159** (poor)
    """)

st.warning("""
### 💡 Why Tree-Based Models Won?
1. **Data Size** - 611 days, LSTM needs 1000s
2. **Feature Engineering** - Tree models use all features, Prophet can't
3. **Data Structure** - Complex patterns, not simple seasonality
""")
