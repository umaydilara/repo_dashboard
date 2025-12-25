import streamlit as st
import pandas as pd

st.set_page_config(page_title="Final Insights", page_icon="🌟", layout="wide")

st.title("🌟 Final Insights")
st.markdown("### What did we learn from this analysis?")
st.markdown("---")

st.subheader("📊 Analysis Journey")
st.info("**Data Cleaning → EDA → Feature Engineering → Feature Selection → Modeling → Explainability**")

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.success("""
    ## 🏆 Best Model: LightGBM
    
    | Metric | Value |
    |--------|-------|
    | **RMSE** | 31.62 |
    | **MAE** | 26.82 |
    | **R²** | 0.853 |
    
    **Explains 85%+ of variance**
    """)
with col2:
    st.subheader("🎯 Top 5 Features")
    features = [("is_high_long", "Long-term high demand"), ("momentum_360", "Yearly momentum"),
                ("momentum_180", "6-month momentum"), ("rolling_mean_180", "6-month average"),
                ("is_high_short", "Short-term high demand")]
    for i, (feat, desc) in enumerate(features, 1):
        st.markdown(f"**{i}. `{feat}`** - {desc}")

st.markdown("---")
st.subheader("💼 Business Recommendations")
col1, col2, col3 = st.columns(3)
with col1:
    st.info("### 📦 Inventory\nAdjust stock based on regime indicators\n\n`is_high_long=1` → Increase stock")
with col2:
    st.info("### 📅 Campaigns\nTime promotions with demand peaks\n\nPredict peaks in advance")
with col3:
    st.info("### 🚚 Logistics\nScale capacity with volatility\n\nHigh volatility → Extra buffer")

st.markdown("---")
st.success("""
## 🌟 Conclusion

> "We understood the data → Created meaningful features → Selected them rigorously → 
> Compared models fairly → Explained the winner."

**Key Message:** Long-term regime indicators and momentum are the most critical factors in demand forecasting.
""")

st.balloons()
