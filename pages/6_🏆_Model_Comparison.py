"""
DASHBOARD 6: MODEL COMPARISON
"Which model is better and why?"
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Model Comparison", page_icon="🏆", layout="wide")

st.title("🏆 Model Comparison")
st.markdown("### Which Model is Better and Why?")
st.markdown("---")

# Main question
st.info("""
**🎯 Main Question:** Which model is better and why?
""")

# Metrics Summary
st.subheader("📊 Model Performance Metrics")

metrics_df = pd.DataFrame({
    'Model': ['XGBoost', 'LightGBM', 'Prophet', 'LSTM'],
    'RMSE': [32.45, 31.62, 89.23, 45.67],
    'MAE': [27.12, 26.82, 72.45, 38.91],
    'R2': [0.845, 0.853, -0.172, 0.693]
})

col1, col2 = st.columns([3, 2])

with col1:
    st.dataframe(
        metrics_df.style.format({
            'RMSE': '{:.2f}',
            'MAE': '{:.2f}',
            'R2': '{:.3f}'
        }).highlight_min(subset=['RMSE', 'MAE'], color='#90EE90')
        .highlight_max(subset=['R2'], color='#90EE90'),
        use_container_width=True,
        height=200
    )

with col2:
    st.success("""
    ### 🏆 Champion Model
    
    **LightGBM**
    
    - RMSE: 31.62
    - R²: 0.853
    
    *Selection criteria: Lowest RMSE*
    """)

# Comparison Charts
col1, col2 = st.columns(2)

with col1:
    fig_rmse = px.bar(metrics_df, x='Model', y='RMSE',
                      title='RMSE Comparison (Lower = Better)',
                      color='RMSE', color_continuous_scale='Reds_r')
    st.plotly_chart(fig_rmse, use_container_width=True)

with col2:
    fig_r2 = px.bar(metrics_df, x='Model', y='R2',
                    title='R² Comparison (Higher = Better)',
                    color='R2', color_continuous_scale='Greens')
    st.plotly_chart(fig_r2, use_container_width=True)

st.markdown("---")

# Model Details in Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🌳 XGBoost", "🌲 LightGBM", "📈 Prophet", "🧠 LSTM"])

with tab1:
    st.subheader("🌳 XGBoost Results")
    st.markdown("*Gradient Boosting - Tree-based Model*")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### Model Parameters
        - **n_estimators:** 100
        - **max_depth:** 6
        - **learning_rate:** 0.1
        - **subsample:** 0.8
        """)
    with col2:
        st.markdown("""
        ### Performance
        - **RMSE:** 32.45
        - **MAE:** 27.12
        - **R²:** 0.845
        """)
    
    st.markdown("""
    <div style='background-color: #ef9a9a; padding: 15px; border-radius: 8px;'>
    <b>✅ Strengths:</b>
    <ul>
    <li>Feature importance calculation</li>
    <li>Overfitting control with regularization</li>
    <li>Handles missing values</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.subheader("🌲 LightGBM Results")
    st.markdown("*Light Gradient Boosting Machine*")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### Model Parameters
        - **n_estimators:** 100
        - **num_leaves:** 31
        - **learning_rate:** 0.1
        - **feature_fraction:** 0.8
        """)
    with col2:
        st.markdown("""
        ### Performance
        - **RMSE:** 31.62 ⭐
        - **MAE:** 26.82 ⭐
        - **R²:** 0.853 ⭐
        """)
    
    st.markdown("""
    <div style='background-color: #ef9a9a; padding: 15px; border-radius: 8px;'>
    <b>✅ Strengths:</b>
    <ul>
    <li>Faster training</li>
    <li>Leaf-wise growth strategy</li>
    <li>Effective on large datasets</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.subheader("📈 Prophet Results")
    st.markdown("*Facebook's Time Series Model*")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### Model Features
        - Additive model
        - Trend + Seasonality
        - Holiday effects
        """)
    with col2:
        st.markdown("""
        ### Performance
        - **RMSE:** 89.23 ⚠️
        - **MAE:** 72.45 ⚠️
        - **R²:** -0.172 ⚠️
        """)
    
    st.markdown("""
    <div style='background-color: #ef9a9a; padding: 15px; border-radius: 8px;'>
    <b>✅ Strengths:</b>
    <ul>
    <li>Seasonality decomposition</li>
    <li>Holiday effects modeling</li>
    <li>Interpretability</li>
    </ul>
    <b>⚠️ Weaknesses:</b>
    <ul>
    <li>Only uses time-based features</li>
    <li>Insufficient for complex patterns</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with tab4:
    st.subheader("🧠 LSTM Results")
    st.markdown("*Long Short-Term Memory - Deep Learning*")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### Model Structure
        - 2 LSTM layers
        - 50 units each
        - Dropout: 0.2
        """)
    with col2:
        st.markdown("""
        ### Performance
        - **RMSE:** 45.67
        - **MAE:** 38.91
        - **R²:** 0.693
        """)
    
    st.markdown("""
    <div style='background-color: #f3e5f5; padding: 15px; border-radius: 8px;'>
    <b>✅ Strengths:</b>
    <ul>
    <li>Learns long-term dependencies</li>
    <li>Complex non-linear patterns</li>
    </ul>
    <b>⚠️ Weaknesses:</b>
    <ul>
    <li>Requires more data</li>
    <li>Hard to interpret</li>
    <li>Longer training time</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# Key Takeaways
st.markdown("---")
st.success("""
### 💡 Key Takeaways from This Page

- **Tree-based models are superior** - better use of features
- **LightGBM has lowest RMSE** - champion model
- **Prophet is strong in seasonality** - but insufficient for this data
- **LSTM needs more data** - low performance on small dataset
""")
