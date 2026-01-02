
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title=\"Model Comparison\", page_icon=\"🏆\", layout=\"wide\")

st.title(\"🏆 Model Comparison\")
st.markdown(\"### XGBoost vs LightGBM vs Prophet vs LSTM\")

# =============================================================================
# ACTUAL MODEL METRICS (TEST SET)
# =============================================================================
model_metrics = {
    'XGBoost': {'RMSE': 35.75, 'MAE': 29.56, 'R2': 0.8120, 'MAPE': 35.01, 'WMAPE': 13.74},
    'LightGBM': {'RMSE': 33.83, 'MAE': 26.33, 'R2': 0.8317, 'MAPE': 37.81, 'WMAPE': 12.24},
    'Prophet': {'RMSE': 100.84, 'MAE': 77.09, 'R2': -0.9249, 'MAPE': 76.26, 'WMAPE': 36.99},
    'LSTM': {'RMSE': 80.02, 'MAE': 68.91, 'R2': 0.0513, 'MAPE': 66.67, 'WMAPE': 30.56}
}

model_colors = {
    'XGBoost': '#3498db',
    'LightGBM': '#2ecc71', 
    'Prophet': '#f39c12',
    'LSTM': '#9b59b6'
}

# =============================================================================
# METRICS TABLE
# =============================================================================
st.markdown(\"---\")
st.subheader(\"📊 Test Set Metrics Summary\")

# Create DataFrame for display
metrics_df = pd.DataFrame(model_metrics).T
metrics_df = metrics_df.reset_index()
metrics_df.columns = ['Model', 'RMSE', 'MAE', 'R²', 'MAPE (%)', 'WMAPE (%)']

# Add ranking column
def calculate_score(row):
    # Normalize each metric (lower is better except R2)
    all_rmse = [model_metrics[m]['RMSE'] for m in model_metrics]
    all_mae = [model_metrics[m]['MAE'] for m in model_metrics]
    all_r2 = [model_metrics[m]['R2'] for m in model_metrics]
    all_mape = [model_metrics[m]['MAPE'] for m in model_metrics]
    all_wmape = [model_metrics[m]['WMAPE'] for m in model_metrics]
    
    rmse_score = 1 - (row['RMSE'] - min(all_rmse)) / (max(all_rmse) - min(all_rmse) + 1e-8)
    mae_score = 1 - (row['MAE'] - min(all_mae)) / (max(all_mae) - min(all_mae) + 1e-8)
    r2_score = (row['R²'] - min(all_r2)) / (max(all_r2) - min(all_r2) + 1e-8)
    mape_score = 1 - (row['MAPE (%)'] - min(all_mape)) / (max(all_mape) - min(all_mape) + 1e-8)
    wmape_score = 1 - (row['WMAPE (%)'] - min(all_wmape)) / (max(all_wmape) - min(all_wmape) + 1e-8)
    
    return np.mean([rmse_score, mae_score, r2_score, mape_score, wmape_score])

metrics_df['Overall Score'] = metrics_df.apply(calculate_score, axis=1)
metrics_df = metrics_df.sort_values('Overall Score', ascending=False)
metrics_df['Rank'] = range(1, len(metrics_df) + 1)

# Reorder columns
metrics_df = metrics_df[['Rank', 'Model', 'RMSE', 'MAE', 'R²', 'MAPE (%)', 'WMAPE (%)', 'Overall Score']]

# Style the dataframe
def highlight_winner(row):
    if row['Rank'] == 1:
        return ['background-color: #a8e6cf'] * len(row)
    return [''] * len(row)

st.dataframe(
    metrics_df.style.apply(highlight_winner, axis=1).format({
        'RMSE': '{:.2f}',
        'MAE': '{:.2f}',
        'R²': '{:.4f}',
        'MAPE (%)': '{:.2f}%',
        'WMAPE (%)': '{:.2f}%',
        'Overall Score': '{:.3f}'
    }),
    use_container_width=True,
    hide_index=True
)

# Winner announcement
winner = metrics_df[metrics_df['Rank'] == 1]['Model'].values[0]
st.success(f\"🏆 **Champion Model: {winner}** - En yüksek Overall Score ile birinci!\")

# =============================================================================
# METRIC COMPARISON CHARTS
# =============================================================================
st.markdown(\"---\")
st.subheader(\"📈 Detailed Metric Comparison\")

col1, col2 = st.columns(2)

with col1:
    # RMSE Comparison
    fig_rmse = go.Figure()
    models = list(model_metrics.keys())
    rmse_vals = [model_metrics[m]['RMSE'] for m in models]
    
    fig_rmse.add_trace(go.Bar(
        x=models, y=rmse_vals,
        marker_color=[model_colors[m] for m in models],
        text=[f'{v:.2f}' for v in rmse_vals],
        textposition='outside'
    ))
    fig_rmse.update_layout(
        title='RMSE (Lower = Better)',
        yaxis_title='RMSE',
        showlegend=False,
        height=400
    )
    st.plotly_chart(fig_rmse, use_container_width=True)

with col2:
    # MAE Comparison
    fig_mae = go.Figure()
    mae_vals = [model_metrics[m]['MAE'] for m in models]
    
    fig_mae.add_trace(go.Bar(
        x=models, y=mae_vals,
        marker_color=[model_colors[m] for m in models],
        text=[f'{v:.2f}' for v in mae_vals],
        textposition='outside'
    ))
    fig_mae.update_layout(
        title='MAE (Lower = Better)',
        yaxis_title='MAE',
        showlegend=False,
        height=400
    )
    st.plotly_chart(fig_mae, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    # R² Comparison
    fig_r2 = go.Figure()
    r2_vals = [model_metrics[m]['R2'] for m in models]
    
    fig_r2.add_trace(go.Bar(
        x=models, y=r2_vals,
        marker_color=[model_colors[m] for m in models],
        text=[f'{v:.4f}' for v in r2_vals],
        textposition='outside'
    ))
    fig_r2.update_layout(
        title='R² Score (Higher = Better)',
        yaxis_title='R²',
        showlegend=False,
        height=400
    )
    st.plotly_chart(fig_r2, use_container_width=True)

with col4:
    # Overall Score Comparison
    fig_score = go.Figure()
    score_df = metrics_df.sort_values('Overall Score', ascending=True)
    
    fig_score.add_trace(go.Bar(
        y=score_df['Model'], x=score_df['Overall Score'],
        orientation='h',
        marker_color=[model_colors[m] for m in score_df['Model']],
        text=[f'{v:.3f}' for v in score_df['Overall Score']],
        textposition='outside'
    ))
    fig_score.update_layout(
        title='Overall Score (Higher = Better)',
        xaxis_title='Score',
        showlegend=False,
        height=400
    )
    st.plotly_chart(fig_score, use_container_width=True)

# =============================================================================
# MAPE vs WMAPE COMPARISON (NEW SECTION)
# =============================================================================
st.markdown(\"---\")
st.subheader(\"📊 MAPE vs WMAPE Analysis\")

st.info(\"\"\"
**MAPE (Mean Absolute Percentage Error):** Ortalama mutlak yüzde hata. Her bir tahmin hatasının yüzdesel ortalaması.

**WMAPE (Weighted Mean Absolute Percentage Error):** Ağırlıklı ortalama mutlak yüzde hata. 
Büyük değerlere daha fazla ağırlık verir, bu nedenle talep tahmininde daha güvenilir bir metriktir.
\"\"\")

col5, col6 = st.columns(2)

with col5:
    # MAPE Comparison
    fig_mape = go.Figure()
    mape_vals = [model_metrics[m]['MAPE'] for m in models]
    
    fig_mape.add_trace(go.Bar(
        x=models, y=mape_vals,
        marker_color='#27ae60',
        text=[f'{v:.2f}%' for v in mape_vals],
        textposition='outside',
        name='MAPE'
    ))
    fig_mape.update_layout(
        title='MAPE % (Lower = Better)',
        yaxis_title='MAPE (%)',
        showlegend=False,
        height=400
    )
    st.plotly_chart(fig_mape, use_container_width=True)

with col6:
    # WMAPE Comparison
    fig_wmape = go.Figure()
    wmape_vals = [model_metrics[m]['WMAPE'] for m in models]
    
    fig_wmape.add_trace(go.Bar(
        x=models, y=wmape_vals,
        marker_color='#e74c3c',
        text=[f'{v:.2f}%' for v in wmape_vals],
        textposition='outside',
        name='WMAPE'
    ))
    fig_wmape.update_layout(
        title='WMAPE % (Lower = Better)',
        yaxis_title='WMAPE (%)',
        showlegend=False,
        height=400
    )
    st.plotly_chart(fig_wmape, use_container_width=True)

# MAPE vs WMAPE Side by Side
st.markdown(\"#### MAPE vs WMAPE Direct Comparison\")

fig_compare = go.Figure()

x = np.arange(len(models))
width = 0.35

fig_compare.add_trace(go.Bar(
    name='MAPE (%)',
    x=[m + ' ' for m in models],  # Slight offset for grouping
    y=mape_vals,
    marker_color='#27ae60',
    text=[f'{v:.2f}%' for v in mape_vals],
    textposition='outside',
    offsetgroup=0
))

fig_compare.add_trace(go.Bar(
    name='WMAPE (%)',
    x=[m + ' ' for m in models],
    y=wmape_vals,
    marker_color='#e74c3c',
    text=[f'{v:.2f}%' for v in wmape_vals],
    textposition='outside',
    offsetgroup=1
))

fig_compare.update_layout(
    title='MAPE vs WMAPE Comparison by Model',
    yaxis_title='Percentage (%)',
    barmode='group',
    height=500,
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
)

st.plotly_chart(fig_compare, use_container_width=True)

# =============================================================================
# RADAR CHART
# =============================================================================
st.markdown(\"---\")
st.subheader(\"🎯 Radar Chart - Multi-Metric Comparison\")

# Normalize metrics for radar chart (all should be 0-1 where 1 is best)
def normalize_metrics(model_name):
    m = model_metrics[model_name]
    all_rmse = [model_metrics[n]['RMSE'] for n in models]
    all_mae = [model_metrics[n]['MAE'] for n in models]
    all_r2 = [model_metrics[n]['R2'] for n in models]
    all_mape = [model_metrics[n]['MAPE'] for n in models]
    all_wmape = [model_metrics[n]['WMAPE'] for n in models]
    
    return [
        1 - (m['RMSE'] - min(all_rmse)) / (max(all_rmse) - min(all_rmse) + 1e-8),
        1 - (m['MAE'] - min(all_mae)) / (max(all_mae) - min(all_mae) + 1e-8),
        (m['R2'] - min(all_r2)) / (max(all_r2) - min(all_r2) + 1e-8),
        1 - (m['MAPE'] - min(all_mape)) / (max(all_mape) - min(all_mape) + 1e-8),
        1 - (m['WMAPE'] - min(all_wmape)) / (max(all_wmape) - min(all_wmape) + 1e-8)
    ]

categories = ['RMSE', 'MAE', 'R²', 'MAPE', 'WMAPE']

fig_radar = go.Figure()

for model in models:
    values = normalize_metrics(model)
    values.append(values[0])  # Close the radar
    
    fig_radar.add_trace(go.Scatterpolar(
        r=values,
        theta=categories + [categories[0]],
        fill='toself',
        name=model,
        line_color=model_colors[model],
        opacity=0.7
    ))

fig_radar.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 1])
    ),
    showlegend=True,
    title='Normalized Performance Comparison (Closer to edge = Better)',
    height=600
)

st.plotly_chart(fig_radar, use_container_width=True)

# =============================================================================
# KEY INSIGHTS
# =============================================================================
st.markdown(\"---\")
st.subheader(\"💡 Key Insights\")

col_ins1, col_ins2 = st.columns(2)

with col_ins1:
    st.markdown(\"\"\"
    **🥇 LightGBM Performansı:**
    - En düşük RMSE (33.83) ve MAE (26.33)
    - En yüksek R² (0.8317)
    - En düşük WMAPE (%12.24)
    - Gradient boosting ailesinden güçlü performans
    \"\"\")

with col_ins2:
    st.markdown(\"\"\"
    **📉 Prophet & LSTM Sonuçları:**
    - Prophet negatif R² (-0.9249) ile zayıf performans
    - LSTM düşük R² (0.0513) gösteriyor
    - Her iki model de bu veri seti için uygun değil
    - Tree-based modeller zaman serisi için daha etkili
    \"\"\")

st.warning(\"\"\"
**⚠️ MAPE vs WMAPE Farkı:**
- MAPE'de LightGBM (%37.81) > XGBoost (%35.01)
- WMAPE'de LightGBM (%12.24) < XGBoost (%13.74)
- WMAPE büyük değerlere daha fazla ağırlık verir, bu nedenle talep tahmininde daha güvenilir bir metriktir.
- **Sonuç:** WMAPE'ye göre LightGBM açık ara kazanan!
\"\"\")
"
Observation: Create successful: /app/advanced_case/streamlit_dashboard/pages/6_🏆_Model_Comparison.py
