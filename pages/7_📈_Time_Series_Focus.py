"""
DASHBOARD 7: TIME SERIES MODELS FOCUS
"Classical time series vs deep learning"
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Time Series Focus", page_icon="📈", layout="wide")

st.title("📈 Time Series Models Focus")
st.markdown("### Prophet vs LSTM - Classical vs Deep Learning")
st.markdown("---")

# Main question
st.info("""
**🎯 Main Question:** Classical time series model or deep learning?
""")

# Comparison
st.subheader("🔄 Prophet vs LSTM Comparison")

comparison_df = pd.DataFrame({
    'Metric': ['RMSE', 'MAE', 'R²', 'Training Time', 'Interpretability'],
    'Prophet': [89.23, 72.45, -0.17, 'Fast', 'High'],
    'LSTM': [45.67, 38.91, 0.69, 'Slow', 'Low']
})

st.dataframe(comparison_df, use_container_width=True)

st.markdown("---")

# Side by side comparison
col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Prophet")
    st.markdown("*Facebook's Additive Time Series Model*")
    
    st.markdown("""
    ### ✅ Advantages
    - **Seasonality decomposition** - weekly, yearly
    - **Interpretable** - each component is clear
    - **Holiday effects** - special days can be modeled
    - **Missing data tolerance** - robust
    
    ### ⚠️ Disadvantages
    - **Time-based only** - cannot take external features
    - **Simple patterns** - weak in complex relationships
    - **Insufficient for this data** - R² < 0
    """)

with col2:
    st.subheader("🧠 LSTM")
    st.markdown("*Long Short-Term Memory Neural Network*")
    
    st.markdown("""
    ### ✅ Advantages
    - **Long-term dependency** - sequence learning
    - **Non-linear patterns** - complex relationships
    - **Automatic feature extraction** - learns from raw data
    
    ### ⚠️ Disadvantages
    - **Requires lots of data** - ~600 rows insufficient
    - **Hard to interpret** - black box
    - **Overfitting risk** - regularization critical
    - **Long training time**
    """)

st.markdown("---")

# Performance Comparison Chart
st.subheader("📊 Performance Comparison")

models = ['Prophet', 'LSTM', 'XGBoost', 'LightGBM']
rmse_values = [89.23, 45.67, 32.45, 31.62]
r2_values = [-0.17, 0.69, 0.85, 0.85]

fig = go.Figure()
fig.add_trace(go.Bar(name='RMSE', x=models, y=rmse_values, marker_color='indianred'))
fig.update_layout(title='RMSE Comparison', xaxis_title='Model', yaxis_title='RMSE')
st.plotly_chart(fig, use_container_width=True)

# Key Insight
st.warning("""
### 💡 Why Did Tree-Based Models Perform Better?

**1. Data Size**
- ~600 days of data is insufficient for LSTM
- Tree-based models work well with small data

**2. Feature Engineering**
- Our created features (lag, rolling mean) are very valuable
- Prophet cannot use them
- Tree-based models use all of them

**3. Data Structure**
- No simple seasonality, complex patterns exist
- Prophet assumes simple seasonality
- Better captured with tree-based models
""")

# Key Takeaways
st.markdown("---")
st.success("""
### 💡 Key Takeaways from This Page

- **LSTM captured complex patterns** - but data is insufficient
- **Prophet strong in seasonality** - but cannot use features
- **Tree-based optimal for this data** - feature engineering + tree = success
- **If more data was available** - LSTM would probably perform better
""")
