import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Final Insights", page_icon="🌟", layout="wide")

st.title("🌟 Final Insights & Conclusions")
st.markdown("### Demand Forecasting Project Summary")

model_metrics = {
    'XGBoost': {'RMSE': 35.75, 'MAE': 29.56, 'R2': 0.8120, 'MAPE': 35.01, 'WMAPE': 13.74},
    'LightGBM': {'RMSE': 33.83, 'MAE': 26.33, 'R2': 0.8317, 'MAPE': 37.81, 'WMAPE': 12.24},
    'Prophet': {'RMSE': 100.84, 'MAE': 77.09, 'R2': -0.9249, 'MAPE': 76.26, 'WMAPE': 36.99},
    'LSTM': {'RMSE': 80.02, 'MAE': 68.91, 'R2': 0.0513, 'MAPE': 66.67, 'WMAPE': 30.56}
}

st.markdown("---")

st.markdown("""
<div style="background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%); padding: 30px; border-radius: 15px; text-align: center; margin: 20px 0;">
    <h1 style="color: white; margin: 0;">🏆 CHAMPION MODEL</h1>
    <h2 style="color: white; margin: 10px 0;">LightGBM</h2>
    <p style="color: white; font-size: 18px; margin: 0;">R2 = 0.8317 | WMAPE = 12.24% | RMSE = 33.83</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.subheader("📊 Champion Model Metrics")

col1, col2, col3, col4, col5 = st.columns(5)

lgbm = model_metrics['LightGBM']

with col1:
    st.metric("RMSE", f"{lgbm['RMSE']:.2f}", delta="Best")
with col2:
    st.metric("MAE", f"{lgbm['MAE']:.2f}", delta="Best")
with col3:
    st.metric("R2 Score", f"{lgbm['R2']:.4f}", delta="Best")
with col4:
    st.metric("MAPE", f"{lgbm['MAPE']:.2f}%")
with col5:
    st.metric("WMAPE", f"{lgbm['WMAPE']:.2f}%", delta="Best")

st.markdown("---")
st.subheader("🏅 Final Model Rankings")

def calculate_overall_score(metrics):
    all_rmse = [m['RMSE'] for m in model_metrics.values()]
    all_mae = [m['MAE'] for m in model_metrics.values()]
    all_r2 = [m['R2'] for m in model_metrics.values()]
    all_mape = [m['MAPE'] for m in model_metrics.values()]
    all_wmape = [m['WMAPE'] for m in model_metrics.values()]
    
    rmse_score = 1 - (metrics['RMSE'] - min(all_rmse)) / (max(all_rmse) - min(all_rmse) + 1e-8)
    mae_score = 1 - (metrics['MAE'] - min(all_mae)) / (max(all_mae) - min(all_mae) + 1e-8)
    r2_score = (metrics['R2'] - min(all_r2)) / (max(all_r2) - min(all_r2) + 1e-8)
    mape_score = 1 - (metrics['MAPE'] - min(all_mape)) / (max(all_mape) - min(all_mape) + 1e-8)
    wmape_score = 1 - (metrics['WMAPE'] - min(all_wmape)) / (max(all_wmape) - min(all_wmape) + 1e-8)
    
    return np.mean([rmse_score, mae_score, r2_score, mape_score, wmape_score])

ranking_data = []
for model, metrics in model_metrics.items():
    score = calculate_overall_score(metrics)
    ranking_data.append({
        'Model': model,
        'RMSE': metrics['RMSE'],
        'MAE': metrics['MAE'],
        'R2': metrics['R2'],
        'MAPE': metrics['MAPE'],
        'WMAPE': metrics['WMAPE'],
        'Overall Score': score
    })

ranking_df = pd.DataFrame(ranking_data)
ranking_df = ranking_df.sort_values('Overall Score', ascending=False)
ranking_df['Rank'] = ['🥇', '🥈', '🥉', '4']
ranking_df = ranking_df[['Rank', 'Model', 'RMSE', 'MAE', 'R2', 'MAPE', 'WMAPE', 'Overall Score']]

st.dataframe(ranking_df, use_container_width=True, hide_index=True)

st.markdown("---")
st.subheader("📈 Final Performance Visualization")

col_viz1, col_viz2 = st.columns(2)

with col_viz1:
    fig_scores = go.Figure()
    
    sorted_df = ranking_df.sort_values('Overall Score', ascending=True)
    colors = ['#e74c3c', '#f39c12', '#3498db', '#2ecc71']
    
    fig_scores.add_trace(go.Bar(
        y=sorted_df['Model'],
        x=sorted_df['Overall Score'],
        orientation='h',
        marker_color=colors,
        text=[f"{s:.3f}" for s in sorted_df['Overall Score']],
        textposition='outside'
    ))
    
    fig_scores.update_layout(title='Overall Score Ranking', xaxis_title='Score (Higher = Better)', height=400)
    st.plotly_chart(fig_scores, use_container_width=True)

with col_viz2:
    fig_wmape = go.Figure()
    
    models = list(model_metrics.keys())
    wmape_vals = [model_metrics[m]['WMAPE'] for m in models]
    
    fig_wmape.add_trace(go.Bar(
        x=models,
        y=wmape_vals,
        marker_color=['#3498db', '#2ecc71', '#f39c12', '#9b59b6'],
        text=[f"{v:.2f}%" for v in wmape_vals],
        textposition='outside'
    ))
    
    fig_wmape.update_layout(title='WMAPE Comparison (Lower = Better)', yaxis_title='WMAPE (%)', height=400)
    fig_wmape.add_hline(y=20, line_dash="dash", line_color="red", annotation_text="20% Threshold")
    
    st.plotly_chart(fig_wmape, use_container_width=True)

st.markdown("---")
st.subheader("🔍 MAPE vs WMAPE Deep Dive")

st.info("""
**Why is WMAPE More Reliable than MAPE?**

- **MAPE** evaluates each prediction with equal weight
- **WMAPE** gives more weight to larger values
- In demand forecasting, high-volume days are more critical
- Therefore, WMAPE is the preferred metric
""")

fig_scatter = go.Figure()

for model, metrics in model_metrics.items():
    color = {'XGBoost': '#3498db', 'LightGBM': '#2ecc71', 'Prophet': '#f39c12', 'LSTM': '#9b59b6'}[model]
    
    fig_scatter.add_trace(go.Scatter(
        x=[metrics['MAPE']],
        y=[metrics['WMAPE']],
        mode='markers+text',
        marker=dict(size=30, color=color),
        text=[model],
        textposition='top center',
        name=model
    ))

fig_scatter.add_trace(go.Scatter(
    x=[0, 80], y=[0, 80],
    mode='lines',
    line=dict(dash='dash', color='gray'),
    name='MAPE = WMAPE'
))

fig_scatter.update_layout(title='MAPE vs WMAPE Comparison', xaxis_title='MAPE (%)', yaxis_title='WMAPE (%)', height=500)
st.plotly_chart(fig_scatter, use_container_width=True)

col_mape1, col_mape2 = st.columns(2)

with col_mape1:
    st.markdown("""
    #### 📊 MAPE Ranking
    1. **XGBoost**: 35.01%
    2. **LightGBM**: 37.81%
    3. **LSTM**: 66.67%
    4. **Prophet**: 76.26%
    """)

with col_mape2:
    st.markdown("""
    #### 📊 WMAPE Ranking
    1. **LightGBM**: 12.24%
    2. **XGBoost**: 13.74%
    3. **LSTM**: 30.56%
    4. **Prophet**: 36.99%
    """)

st.success("""
**🎯 Key Finding:** 
- While XGBoost looks better in MAPE, LightGBM is the clear winner in WMAPE!
- This difference shows that LightGBM makes better predictions on high-demand days.
""")

st.markdown("---")
st.subheader("📝 Project Conclusions")

col_conc1, col_conc2 = st.columns(2)

with col_conc1:
    st.markdown("""
    ### Achievements
    
    1. **Effective Model Selection**
       - 12.24% WMAPE with LightGBM
       - R2 = 0.8317 explanatory power
    
    2. **Comprehensive Model Comparison**
       - 4 different models tested
       - ML vs Time Series analysis
    
    3. **Reliable Metric Usage**
       - Realistic evaluation with WMAPE
       - Comparison of 5 different metrics
    """)

with col_conc2:
    st.markdown("""
    ### Future Recommendations
    
    1. **Model Improvement**
       - Hyperparameter tuning
       - Ensemble methods
    
    2. **Data Enrichment**
       - More external features
       - Long-term data collection
    
    3. **Production Deployment**
       - Model monitoring
       - Automated retraining
    """)

st.markdown("---")

st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px; margin: 20px 0;">
    <h2 style="color: white; text-align: center;">📊 Executive Summary</h2>
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap; margin-top: 20px;">
        <div style="text-align: center; padding: 15px;">
            <h3 style="color: #a8e6cf; margin: 0;">🏆 Champion</h3>
            <p style="color: white; font-size: 24px; margin: 5px 0;">LightGBM</p>
        </div>
        <div style="text-align: center; padding: 15px;">
            <h3 style="color: #a8e6cf; margin: 0;">📈 R2 Score</h3>
            <p style="color: white; font-size: 24px; margin: 5px 0;">0.8317</p>
        </div>
        <div style="text-align: center; padding: 15px;">
            <h3 style="color: #a8e6cf; margin: 0;">🎯 WMAPE</h3>
            <p style="color: white; font-size: 24px; margin: 5px 0;">12.24%</p>
        </div>
        <div style="text-align: center; padding: 15px;">
            <h3 style="color: #a8e6cf; margin: 0;">📉 RMSE</h3>
            <p style="color: white; font-size: 24px; margin: 5px 0;">33.83</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; padding: 20px;">
    <p>📊 Demand Forecasting Dashboard | University Project</p>
    <p>Built with Streamlit & Plotly</p>
</div>
""", unsafe_allow_html=True)
