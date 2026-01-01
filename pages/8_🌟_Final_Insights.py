"""
DASHBOARD 8: FINAL INSIGHTS
"What did we learn from this study?"
"""

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Final Insights", page_icon="🌟", layout="wide")

st.title("🌟 Final Insights")
st.markdown("### Presentation Closing - What Did We Learn from This Study?")
st.markdown("---")

# Journey Summary
st.markdown("""
## 📊 Our Analysis Journey

Data Cleaning → EDA → Feature Engineering → Feature Selection → Modeling → Explainability

""")

# Model Result
st.subheader("🏆 1. Best Model")

col1, col2 = st.columns([1, 2])

with col1:
    st.success("""
    ### 🥇 LightGBM
    
    | Metric | Value |
    |--------|-------|
    | **RMSE** | 31.62 |
    | **MAE** | 26.82 |
    | **R²** | 0.853 |
    
    *Explains 85%+ of variance*
    """)

with col2:
    metrics_df = pd.DataFrame({
        'Model': ['XGBoost', 'LightGBM', 'Prophet', 'LSTM'],
        'RMSE': [32.45, 31.62, 89.23, 45.67],
        'R2': [0.845, 0.853, -0.172, 0.693]
    })
    
    fig = px.bar(metrics_df, x='Model', y='RMSE', color='RMSE',
                 title='Model RMSE Comparison',
                 color_continuous_scale='RdYlGn_r')
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Top Features
st.subheader("🎯 2. Top 5 Most Important Features")

st.markdown("""
| Rank | Feature | Description | Importance |
|------|---------|-------------|------------|
| 1 | **rolling_mean_30** | 30-day average | ⭐⭐⭐⭐⭐ |
| 2 | **lag_7** | Demand 7 days ago | ⭐⭐⭐⭐ |
| 3 | **rolling_mean_7** | 7-day average | ⭐⭐⭐⭐ |
| 4 | **lag_14** | Demand 14 days ago | ⭐⭐⭐ |
| 5 | **dayofweek** | Day of week | ⭐⭐⭐ |
""")

col1, col2 = st.columns(2)

with col1:
    features = ['rolling_mean_30', 'lag_7', 'rolling_mean_7', 'lag_14', 'dayofweek']
    importance = [0.85, 0.72, 0.68, 0.55, 0.48]
    
    fig = px.bar(x=importance, y=features, orientation='h',
                 title='Feature Importance',
                 labels={'x': 'Importance', 'y': 'Feature'},
                 color=importance, color_continuous_scale='Viridis')
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("""
    ### 📝 Feature Importance Interpretation
    
    **Rolling Mean is Dominant:**
    - Trend is the most important factor
    - Captures short and medium-term trends
    
    **Lag Features are Important:**
    - Past demand affects future demand
    - 7 and 14-day lags are critical
    
    **Weekly Pattern:**
    - Day of week affects demand
    """)

st.markdown("---")

# Business Insights
st.subheader("💼 3. Business Insights")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    ### 📦 Inventory Planning
    
    **Recommendation:** Adjust inventory levels 
    based on rolling mean values
    
    - Rising trend → Increase stock
    - Falling trend → Reduce stock
    """)

with col2:
    st.info("""
    ### 📅 Campaign Timing
    
    **Recommendation:** Launch campaigns
    during high demand periods
    
    - Predict peak periods in advance
    - Optimize marketing budget
    """)

with col3:
    st.info("""
    ### 🚚 Logistics Planning
    
    **Recommendation:** Adjust capacity
    based on demand fluctuations
    
    - High volatility = Extra capacity
    - Stable period = Optimized capacity
    """)

st.markdown("---")

# Academic Value
st.subheader("🎓 4. Academic Value")

st.markdown("""
### Academic Contribution of This Study

| Area | Contribution |
|------|--------------|
| **Methodology** | Robust evaluation with multiple feature selection methods |
| **Comparison** | Comprehensive comparison of Tree-based vs Time Series vs Deep Learning |
| **Explainability** | Non-black-box model explanation with SHAP |
| **Reproducibility** | All code and visualizations shared |
""")

st.markdown("---")

# Conclusion
st.success("""
## 🌟 Conclusion

> "We understood the data → Created meaningful features → Selected carefully → 
Compared models fairly → Explained the winner."

### Main Message:
**Rolling mean and lag features are the most critical factors in demand forecasting.**

This structure:
- ✅ Can be used in inventory planning
- ✅ Can be used in campaign timing  
- ✅ Can be used in logistics optimization
""")

# Celebration
st.balloons()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px;'>
<h3>🎓 Demand Forecasting Project</h3>
<p>Data Cleaning → EDA → Feature Engineering → Modeling → Explainability</p>
<p><strong>Thank You!</strong></p>
</div>
""", unsafe_allow_html=True)
