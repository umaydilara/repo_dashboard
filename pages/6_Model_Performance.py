import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Model Performance", page_icon="📈", layout="wide")

st.title("📈 Model Performance & Comparison")
st.markdown("---")

# Model Results (simulated based on typical forecasting results)
st.subheader("🏆 Model Comparison")

# Simulated model metrics
model_results = pd.DataFrame({
    'Model': ['XGBoost', 'LightGBM', 'Prophet', 'LSTM', 'Random Forest', 'Linear Regression'],
    'RMSE': [45.2, 47.8, 52.3, 55.1, 49.6, 68.4],
    'MAE': [32.1, 34.5, 38.2, 40.8, 36.2, 52.1],
    'MAPE': [8.5, 9.2, 10.1, 11.3, 9.8, 15.2],
    'R2': [0.92, 0.90, 0.87, 0.85, 0.89, 0.72]
})

# Key Metrics Cards
best_model = model_results.loc[model_results['RMSE'].idxmin()]
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🥇 Best Model", best_model['Model'])
with col2:
    st.metric("📉 Best RMSE", f"{best_model['RMSE']:.1f}")
with col3:
    st.metric("📊 Best MAE", f"{best_model['MAE']:.1f}")
with col4:
    st.metric("🎯 Best R²", f"{best_model['R2']:.2f}")

st.markdown("---")

# Model Comparison Table
st.subheader("📋 Detailed Model Metrics")
st.dataframe(
    model_results.style.highlight_min(subset=['RMSE', 'MAE', 'MAPE'], color='lightgreen')
                      .highlight_max(subset=['R2'], color='lightgreen'),
    use_container_width=True
)

# Visual Comparisons
col1, col2 = st.columns(2)

with col1:
    fig_rmse = px.bar(model_results, x='Model', y='RMSE',
                      title='RMSE Comparison (Lower is Better)',
                      color='RMSE', color_continuous_scale='Reds_r')
    st.plotly_chart(fig_rmse, use_container_width=True)

with col2:
    fig_r2 = px.bar(model_results, x='Model', y='R2',
                    title='R² Score Comparison (Higher is Better)',
                    color='R2', color_continuous_scale='Greens')
    st.plotly_chart(fig_r2, use_container_width=True)

# Radar Chart for Model Comparison
st.subheader("🎯 Multi-Metric Model Comparison")

# Normalize metrics for radar chart
normalized = model_results.copy()
for col in ['RMSE', 'MAE', 'MAPE']:
    normalized[col] = 1 - (normalized[col] - normalized[col].min()) / (normalized[col].max() - normalized[col].min())

fig_radar = go.Figure()

for _, row in normalized.iterrows():
    fig_radar.add_trace(go.Scatterpolar(
        r=[row['R2'], normalized.loc[normalized['Model']==row['Model'], 'RMSE'].values[0],
           normalized.loc[normalized['Model']==row['Model'], 'MAE'].values[0],
           normalized.loc[normalized['Model']==row['Model'], 'MAPE'].values[0]],
        theta=['R²', 'RMSE (inv)', 'MAE (inv)', 'MAPE (inv)'],
        fill='toself',
        name=row['Model']
    ))

fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
    showlegend=True,
    title='Model Performance Radar Chart'
)
st.plotly_chart(fig_radar, use_container_width=True)

# Model Selection Guidance
st.subheader("💡 Model Selection Guidance")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **🎯 XGBoost Strengths:**
    - Best overall accuracy
    - Handles non-linear relationships
    - Feature importance insights
    - Fast training time
    """)

with col2:
    st.markdown("""
    **⚠️ Considerations:**
    - LSTM for long sequences
    - Prophet for interpretability
    - LightGBM for large datasets
    - Ensemble for robustness
    """)

st.markdown("---")
st.success("✅ **Recommendation:** XGBoost provides the best balance of accuracy and interpretability for this demand forecasting task.")
