import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Feature Selection & SHAP", page_icon="🎯", layout="wide")

st.title("🎯 Feature Selection & SHAP Analysis")
st.markdown("---")

@st.cache_data
def load_data():
    df = pd.read_csv('demand_features_final.csv')
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

df = load_data()

# Introduction
st.markdown("""
SHAP (SHapley Additive exPlanations) values help us understand how each feature contributes to model predictions.
This analysis reveals which features are most important for demand forecasting.
""")

# Simulated Feature Importance (based on correlation as proxy)
st.subheader("📊 Feature Importance Analysis")

numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
if 'daily_orders' in numeric_cols:
    numeric_cols.remove('daily_orders')

if numeric_cols:
    # Calculate importance proxy using absolute correlation
    importance = df[numeric_cols].corrwith(df['daily_orders']).abs().sort_values(ascending=False)
    importance = importance.dropna()
    
    top_features = importance.head(15)
    
    # Feature Importance Bar Chart
    fig_importance = px.bar(
        x=top_features.values,
        y=top_features.index,
        orientation='h',
        title='Top 15 Most Important Features (Correlation-based)',
        labels={'x': 'Importance Score', 'y': 'Feature'},
        color=top_features.values,
        color_continuous_scale='Viridis'
    )
    fig_importance.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_importance, use_container_width=True)
    
    # Feature Categories Impact
    st.subheader("🏷️ Feature Category Impact")
    
    # Categorize and calculate average importance
    categories = {
        'Time Features': [col for col in top_features.index if any(x in col.lower() for x in ['day', 'week', 'month', 'year'])],
        'Lag Features': [col for col in top_features.index if 'lag' in col.lower()],
        'Rolling Features': [col for col in top_features.index if 'rolling' in col.lower() or 'ma' in col.lower()],
        'Other': []
    }
    
    category_importance = {}
    for cat, features in categories.items():
        if features:
            category_importance[cat] = importance[features].mean()
    
    if category_importance:
        fig_cat = px.pie(
            values=list(category_importance.values()),
            names=list(category_importance.keys()),
            title='Average Importance by Feature Category'
        )
        st.plotly_chart(fig_cat, use_container_width=True)

# SHAP Interpretation Guide
st.subheader("📖 Understanding SHAP Values")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **What SHAP Values Tell Us:**
    - **Positive SHAP:** Feature increases prediction
    - **Negative SHAP:** Feature decreases prediction
    - **Magnitude:** Importance of contribution
    """)

with col2:
    st.markdown("""
    **Key Insights:**
    - Lag features capture recent trends
    - Day-of-week affects ordering patterns
    - Rolling averages smooth noise
    """)

# Feature Selection Summary
st.subheader("✅ Recommended Features for Modeling")

if len(importance) > 0:
    threshold = importance.median()
    selected_features = importance[importance >= threshold].index.tolist()
    
    st.success(f"**{len(selected_features)} features selected** with importance above median threshold ({threshold:.3f})")
    
    with st.expander("View Selected Features"):
        for i, feat in enumerate(selected_features, 1):
            st.write(f"{i}. {feat} (Score: {importance[feat]:.3f})")

st.markdown("---")
st.info("💡 **Tip:** Feature selection reduces model complexity and prevents overfitting while maintaining predictive power.")
