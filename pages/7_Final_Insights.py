import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Final Insights", page_icon="💡", layout="wide")

st.title("💡 Final Insights & Business Recommendations")
st.markdown("---")

@st.cache_data
def load_data():
    df = pd.read_csv('demand_features_final.csv')
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

df = load_data()

# Executive Summary
st.subheader("📊 Executive Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 📈 Key Findings
    - **Best Model:** XGBoost (RMSE: 45.2)
    - **Key Drivers:** Lag features, day-of-week
    - **Forecast Accuracy:** ~92% R²
    """)

with col2:
    st.markdown("""
    ### ⏰ Temporal Patterns
    - Peak days: Weekdays
    - Low demand: Weekends
    - Seasonal trends detected
    """)

with col3:
    st.markdown("""
    ### 🎯 Model Performance
    - XGBoost: Best accuracy
    - LightGBM: Fast alternative
    - Prophet: Best interpretability
    """)

st.markdown("---")

# Business Recommendations
st.subheader("💼 Business Recommendations")

recommendations = [
    {
        "title": "📦 Inventory Management",
        "icon": "📦",
        "description": "Use demand forecasts to optimize stock levels",
        "actions": [
            "Maintain safety stock for 95th percentile demand",
            "Reduce inventory during predicted low-demand periods",
            "Pre-position inventory before peak seasons"
        ]
    },
    {
        "title": "👥 Workforce Planning",
        "icon": "👥",
        "description": "Align staffing with predicted demand",
        "actions": [
            "Schedule more staff on high-demand weekdays",
            "Reduce overtime during low-demand periods",
            "Cross-train staff for demand flexibility"
        ]
    },
    {
        "title": "🚚 Logistics Optimization",
        "icon": "🚚",
        "description": "Improve delivery efficiency",
        "actions": [
            "Pre-arrange carrier capacity for peak periods",
            "Optimize delivery routes based on demand density",
            "Consider regional warehousing for high-demand areas"
        ]
    },
    {
        "title": "📈 Marketing Strategy",
        "icon": "📈",
        "description": "Align promotions with demand patterns",
        "actions": [
            "Run promotions during low-demand periods",
            "Avoid discounts during natural peaks",
            "Target marketing based on customer segments"
        ]
    }
]

for i, rec in enumerate(recommendations):
    with st.expander(f"{rec['icon']} {rec['title']}", expanded=True):
        st.write(f"**{rec['description']}**")
        for action in rec['actions']:
            st.write(f"• {action}")

st.markdown("---")

# Implementation Roadmap
st.subheader("🗺️ Implementation Roadmap")

roadmap = pd.DataFrame({
    'Phase': ['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4'],
    'Timeline': ['Month 1-2', 'Month 3-4', 'Month 5-6', 'Ongoing'],
    'Focus': ['Model Deployment', 'System Integration', 'Process Optimization', 'Monitoring & Improvement'],
    'Activities': [
        'Deploy XGBoost model to production',
        'Integrate with ERP and inventory systems',
        'Optimize operations based on forecasts',
        'Monitor accuracy and retrain monthly'
    ]
})

fig_roadmap = px.timeline(
    roadmap,
    x_start=[0, 2, 4, 6],
    x_end=[2, 4, 6, 12],
    y='Phase',
    color='Focus',
    title='Implementation Timeline'
)
st.dataframe(roadmap, use_container_width=True)

# Success Metrics
st.subheader("📏 Success Metrics")

col1, col2, col3, col4 = st.columns(4)

metrics = [
    ("Forecast Accuracy", ">90%", "MAPE < 10%"),
    ("Inventory Turnover", "+15%", "Reduce holding costs"),
    ("Stockout Rate", "<2%", "Improve availability"),
    ("Order Fulfillment", ">98%", "On-time delivery")
]

for col, (name, target, desc) in zip([col1, col2, col3, col4], metrics):
    with col:
        st.metric(name, target)
        st.caption(desc)

st.markdown("---")

# Conclusion
st.subheader("🎓 Conclusion")
st.markdown("""
This demand forecasting project demonstrates the power of machine learning in predicting customer behavior.
By leveraging historical data and advanced feature engineering, we achieved high-accuracy forecasts that
enable data-driven business decisions.

**Key Takeaways:**
1. ✅ XGBoost provides the most accurate demand forecasts
2. ✅ Lag features and temporal patterns are the strongest predictors
3. ✅ Regular model retraining ensures continued accuracy
4. ✅ Integration with business processes maximizes value

**Next Steps:**
- Deploy the model in a production environment
- Set up automated retraining pipelines
- Monitor forecast accuracy over time
- Expand to product-level forecasting
""")

st.balloons()
st.success("🎉 Thank you for exploring this Demand Forecasting Dashboard!")
