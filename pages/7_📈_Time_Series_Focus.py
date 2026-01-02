import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Time Series Focus", page_icon="📈", layout="wide")

st.title("📈 Time Series Model Focus")
st.markdown("### Prophet vs LSTM Deep Analysis")

model_metrics = {
    'XGBoost': {'RMSE': 35.75, 'MAE': 29.56, 'R2': 0.8120, 'MAPE': 35.01, 'WMAPE': 13.74},
    'LightGBM': {'RMSE': 33.83, 'MAE': 26.33, 'R2': 0.8317, 'MAPE': 37.81, 'WMAPE': 12.24},
    'Prophet': {'RMSE': 100.84, 'MAE': 77.09, 'R2': -0.9249, 'MAPE': 76.26, 'WMAPE': 36.99},
    'LSTM': {'RMSE': 80.02, 'MAE': 68.91, 'R2': 0.0513, 'MAPE': 66.67, 'WMAPE': 30.56}
}

ts_models = ['Prophet', 'LSTM']
ml_models = ['XGBoost', 'LightGBM']

st.markdown("---")
st.subheader("⚔️ Time Series Models vs ML Models")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📊 Traditional Time Series Models")
    st.markdown("""
    **Prophet:**
    - Developed by Facebook
    - Seasonality and trend decomposition
    - Holiday effects modeling
    """)
    
    st.markdown("""
    **LSTM (Long Short-Term Memory):**
    - Deep learning based
    - Learning long-term dependencies
    - Sequence-to-sequence modeling
    """)

with col2:
    st.markdown("#### 🌳 Tree-Based ML Models")
    st.markdown("""
    **XGBoost & LightGBM:**
    - Gradient boosting algorithms
    - Strong with feature engineering
    - Optimized for tabular data
    - Lower computational cost
    """)

st.markdown("---")
st.subheader("📋 Performance Metrics Comparison")

comparison_data = []
for model in ts_models + ml_models:
    m = model_metrics[model]
    model_type = "Time Series" if model in ts_models else "ML (Tree-Based)"
    comparison_data.append({
        'Model': model,
        'Type': model_type,
        'RMSE': m['RMSE'],
        'MAE': m['MAE'],
        'R2': m['R2'],
        'MAPE': m['MAPE'],
        'WMAPE': m['WMAPE']
    })

comparison_df = pd.DataFrame(comparison_data)
st.dataframe(comparison_df, use_container_width=True, hide_index=True)

st.markdown("---")
st.subheader("📊 Visual Performance Analysis")

fig = make_subplots(rows=2, cols=3, subplot_titles=('RMSE', 'MAE', 'R2 Score', 'MAPE (%)', 'WMAPE (%)', 'Model Type Comparison'))

colors_ts = ['#e74c3c', '#9b59b6']
colors_ml = ['#3498db', '#2ecc71']

all_models = ts_models + ml_models
all_colors = colors_ts + colors_ml

fig.add_trace(go.Bar(
    x=all_models, 
    y=[model_metrics[m]['RMSE'] for m in all_models],
    marker_color=all_colors,
    text=[f"{model_metrics[m]['RMSE']:.2f}" for m in all_models],
    textposition='outside',
    showlegend=False
), row=1, col=1)

fig.add_trace(go.Bar(
    x=all_models, 
    y=[model_metrics[m]['MAE'] for m in all_models],
    marker_color=all_colors,
    text=[f"{model_metrics[m]['MAE']:.2f}" for m in all_models],
    textposition='outside',
    showlegend=False
), row=1, col=2)

fig.add_trace(go.Bar(
    x=all_models, 
    y=[model_metrics[m]['R2'] for m in all_models],
    marker_color=all_colors,
    text=[f"{model_metrics[m]['R2']:.4f}" for m in all_models],
    textposition='outside',
    showlegend=False
), row=1, col=3)

fig.add_trace(go.Bar(
    x=all_models, 
    y=[model_metrics[m]['MAPE'] for m in all_models],
    marker_color=all_colors,
    text=[f"{model_metrics[m]['MAPE']:.2f}%" for m in all_models],
    textposition='outside',
    showlegend=False
), row=2, col=1)

fig.add_trace(go.Bar(
    x=all_models, 
    y=[model_metrics[m]['WMAPE'] for m in all_models],
    marker_color=all_colors,
    text=[f"{model_metrics[m]['WMAPE']:.2f}%" for m in all_models],
    textposition='outside',
    showlegend=False
), row=2, col=2)

ts_avg_wmape = np.mean([model_metrics[m]['WMAPE'] for m in ts_models])
ml_avg_wmape = np.mean([model_metrics[m]['WMAPE'] for m in ml_models])

fig.add_trace(go.Bar(
    x=['Time Series', 'ML (Tree-Based)'], 
    y=[ts_avg_wmape, ml_avg_wmape],
    marker_color=['#e74c3c', '#2ecc71'],
    text=[f"{ts_avg_wmape:.2f}%", f"{ml_avg_wmape:.2f}%"],
    textposition='outside',
    showlegend=False
), row=2, col=3)

fig.update_layout(height=700, title_text="All Metrics Comparison")
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("🎯 MAPE vs WMAPE: Time Series Model Analysis")

col3, col4 = st.columns(2)

with col3:
    st.markdown("#### 🔮 Prophet Performance")
    
    prophet_metrics = model_metrics['Prophet']
    
    fig_prophet = go.Figure()
    fig_prophet.add_trace(go.Bar(
        x=['MAPE', 'WMAPE'],
        y=[prophet_metrics['MAPE'], prophet_metrics['WMAPE']],
        marker_color=['#f39c12', '#e74c3c'],
        text=[f"{prophet_metrics['MAPE']:.2f}%", f"{prophet_metrics['WMAPE']:.2f}%"],
        textposition='outside'
    ))
    fig_prophet.update_layout(
        title=f"Prophet: MAPE={prophet_metrics['MAPE']:.2f}%, WMAPE={prophet_metrics['WMAPE']:.2f}%",
        yaxis_title='Percentage (%)',
        height=350
    )
    st.plotly_chart(fig_prophet, use_container_width=True)
    
    st.error(f"""
    **Prophet Evaluation:**
    - R2 = {prophet_metrics['R2']:.4f} (Negative!)
    - WMAPE = {prophet_metrics['WMAPE']:.2f}%
    - Model fails to explain the data
    - Seasonality patterns insufficient
    """)

with col4:
    st.markdown("#### 🧠 LSTM Performance")
    
    lstm_metrics = model_metrics['LSTM']
    
    fig_lstm = go.Figure()
    fig_lstm.add_trace(go.Bar(
        x=['MAPE', 'WMAPE'],
        y=[lstm_metrics['MAPE'], lstm_metrics['WMAPE']],
        marker_color=['#9b59b6', '#8e44ad'],
        text=[f"{lstm_metrics['MAPE']:.2f}%", f"{lstm_metrics['WMAPE']:.2f}%"],
        textposition='outside'
    ))
    fig_lstm.update_layout(
        title=f"LSTM: MAPE={lstm_metrics['MAPE']:.2f}%, WMAPE={lstm_metrics['WMAPE']:.2f}%",
        yaxis_title='Percentage (%)',
        height=350
    )
    st.plotly_chart(fig_lstm, use_container_width=True)
    
    st.warning(f"""
    **LSTM Evaluation:**
    - R2 = {lstm_metrics['R2']:.4f} (Very low)
    - WMAPE = {lstm_metrics['WMAPE']:.2f}%
    - Better than Prophet but still insufficient
    - Needs more data and tuning
    """)

st.markdown("---")
st.subheader("❓ Why Did Time Series Models Fail?")

col5, col6 = st.columns(2)

with col5:
    st.markdown("""
    ### 🔴 Possible Reasons
    
    1. **Insufficient Data Volume**
       - LSTM deep learning model requires more data
       - Prophet expects long-term data for trend and seasonality
    
    2. **Complex Feature Relationships**
       - Demand depends on many external factors
       - Time series models only capture temporal patterns
    
    3. **Non-Stationary Data**
       - Trends and seasonality may be variable
       - Structural breaks present
    """)

with col6:
    st.markdown("""
    ### 🟢 Advantages of Tree-Based Models
    
    1. **Feature Engineering**
       - Can use manually created features
       - External factors can be included in model
    
    2. **Non-Linear Relationships**
       - Captures complex relationships
       - Learns interaction effects
    
    3. **Robustness**
       - Resistant to outliers
       - Missing value handling
    """)

st.markdown("---")
st.subheader("📌 Conclusions and Recommendations")

fig_final = go.Figure()

models_all = ['Prophet', 'LSTM', 'XGBoost', 'LightGBM']
wmape_all = [model_metrics[m]['WMAPE'] for m in models_all]

fig_final.add_trace(go.Bar(
    x=models_all,
    y=wmape_all,
    marker_color=['#e74c3c', '#9b59b6', '#3498db', '#2ecc71'],
    text=[f'{v:.2f}%' for v in wmape_all],
    textposition='outside'
))

fig_final.update_layout(
    title='Final WMAPE Comparison - All Models',
    yaxis_title='WMAPE (%)',
    height=400,
    showlegend=False
)

st.plotly_chart(fig_final, use_container_width=True)

col7, col8 = st.columns(2)

with col7:
    st.success("""
    **Recommended Model: LightGBM**
    - Lowest WMAPE: 12.24%
    - Highest R2: 0.8317
    - Fast training and prediction
    - Production-ready
    """)

with col8:
    st.info("""
    **Future Improvements:**
    - Collect more data
    - Try hybrid models (ML + TS)
    - Improve feature engineering
    - Ensemble approaches
    """)
