"""
PAGE 8: FINAL INSIGHTS
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Final Insights", page_icon="🌟", layout="wide")

st.title("🌟 Final Insights")
st.markdown("### What did we learn from this analysis?")
st.markdown("---")

# Journey
st.subheader("📊 Analysis Journey")

st.info("""
Data Cleaning → EDA → Feature Engineering → Feature Selection → Modeling → Explainability

""")

st.markdown("---")

# Key Results
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Best Model")
    
    st.success("""
    ## LightGBM
    
    | Metric | Value |
    |--------|-------|
    | **RMSE** | 31.62 |
    | **MAE** | 26.82 |
    | **R²** | 0.853 |
    
    **Explains 85%+ of demand variance**
    
    *Selected based on lowest RMSE with tie-breaker: MAE → R²*
    """)

with col2:
    st.subheader("🎯 Top 5 Features")
    
    features = [
        ("is_high_long", "Long-term high demand regime"),
        ("momentum_360", "Yearly momentum"),
        ("momentum_180", "6-month momentum"),
        ("rolling_mean_180", "6-month rolling average"),
        ("is_high_short", "Short-term high demand")
    ]
    
    for i, (feat, desc) in enumerate(features, 1):
        st.markdown(f"**{i}. `{feat}`** - {desc}")

st.markdown("---")

# Business Recommendations
st.subheader("💼 Business Recommendations")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    ### 📦 Inventory Planning
    
    **Recommendation:**
    Adjust stock levels based on long-term regime indicators
    
    **Actions:**
    - `is_high_long = 1` → Increase stock
    - `momentum_360 > 0` → Growth expected
    - `momentum_360 < 0` → Reduce inventory
    """)

with col2:
    st.info("""
    ### 📅 Campaign Timing
    
    **Recommendation:**
    Launch campaigns during predicted high-demand periods
    
    **Actions:**
    - Predict peak periods in advance
    - Optimize marketing budget allocation
    - Avoid campaigns in low-demand regimes
    """)

with col3:
    st.info("""
    ### 🚚 Logistics Planning
    
    **Recommendation:**
    Adjust capacity based on demand volatility
    
    **Actions:**
    - High volatility → Extra capacity buffer
    - Stable period → Optimize costs
    - Pre-position inventory for peaks
    """)

st.markdown("---")

# Academic Value
st.subheader("🎓 Academic Contribution")

st.markdown("""
| Area | Contribution |
|------|--------------|
| **Methodology** | Multi-method feature selection (Correlation + MI + RF) |
| **Comparison** | Comprehensive Tree-based vs Time Series vs Deep Learning |
| **Explainability** | SHAP analysis - not a black box |
| **Reproducibility** | All code and visualizations shared |
| **Practical Value** | Actionable business recommendations |
""")

st.markdown("---")

# Final Conclusion
st.success("""
## 🌟 Conclusion

> "We understood the data → Created meaningful features → Selected them rigorously → 
> Compared models fairly → Explained the winner."

### Key Message:
**Long-term regime indicators and momentum are the most critical factors in demand forecasting.**

### This framework can be used for:
- ✅ Inventory optimization
- ✅ Campaign planning
- ✅ Logistics capacity management
- ✅ Revenue forecasting
""")

st.markdown("---")

# Thank you
st.markdown("""
<div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; border-radius: 15px; margin: 20px 0;'>
    <h2>🎓 Demand Forecasting Project</h2>
    <p style='font-size: 18px;'>Data → Features → Models → Insights</p>
    <h3>Thank You!</h3>
</div>
""", unsafe_allow_html=True)

st.balloons()
