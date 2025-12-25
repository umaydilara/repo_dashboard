"""
PAGE 6: MODEL COMPARISON
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Model Comparison", page_icon="🏆", layout="wide")

# Sidebar
st.sidebar.title("⚙️ Settings")
metric_choice = st.sidebar.selectbox("Primary Metric", ["RMSE", "MAE", "R2"])
show_details = st.sidebar.checkbox("Show Model Details", value=True)

st.title("🏆 Model Comparison")
st.markdown("### Which model performs best and why?")
st.markdown("---")

st.info("**🎯 Key Question:** Which model should we deploy?")

# Model Metrics
metrics_data = {
    'Model': ['LightGBM', 'XGBoost', 'LSTM', 'Prophet'],
    'RMSE': [31.62, 36.34, 75.36, 83.30],
    'MAE': [26.82, 28.83, 63.45, 69.79],
    'R2': [0.853, 0.806, 0.159, -0.020],
    'Training Time': ['Fast', 'Medium', 'Slow', 'Fast'],
    'Interpretability': ['High', 'High', 'Low', 'High']
}
metrics_df = pd.DataFrame(metrics_data)

# Champion Model
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Model Performance Metrics")
    
    styled_df = metrics_df.style.format({
        'RMSE': '{:.2f}',
        'MAE': '{:.2f}',
        'R2': '{:.3f}'
    }).background_gradient(subset=['RMSE', 'MAE'], cmap='Reds_r')\
      .background_gradient(subset=['R2'], cmap='Greens')
    
    st.dataframe(styled_df, use_container_width=True, height=200)

with col2:
    best_idx = metrics_df['RMSE'].idxmin()
    best_model = metrics_df.loc[best_idx, 'Model']
    best_rmse = metrics_df.loc[best_idx, 'RMSE']
    best_r2 = metrics_df.loc[best_idx, 'R2']
    
    st.success(f"""
    ### 🏆 Champion Model
    
    ## {best_model}
    
    - **RMSE:** {best_rmse:.2f}
    - **R²:** {best_r2:.3f}
    
    *Explains {best_r2*100:.1f}% of variance*
    """)

st.markdown("---")

# Metric Comparison Charts
st.subheader("📈 Visual Comparison")

col1, col2 = st.columns(2)

with col1:
    colors = ['#43A047', '#1E88E5', '#FB8C00', '#E53935']
    fig = go.Figure(data=[
        go.Bar(x=metrics_df['Model'], y=metrics_df['RMSE'],
               marker_color=colors, text=metrics_df['RMSE'].round(1),
               textposition='outside')
    ])
    fig.update_layout(title='RMSE Comparison (Lower is Better ↓)',
                      height=400, template='plotly_white',
                      yaxis_title='RMSE')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = go.Figure(data=[
        go.Bar(x=metrics_df['Model'], y=metrics_df['R2'],
               marker_color=colors, text=metrics_df['R2'].round(3),
               textposition='outside')
    ])
    fig.add_hline(y=0, line_dash='dash', line_color='red')
    fig.update_layout(title='R² Comparison (Higher is Better ↑)',
                      height=400, template='plotly_white',
                      yaxis_title='R²')
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Model Details
if show_details:
    st.subheader("📋 Model Details")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🌲 LightGBM", "🌳 XGBoost", "🧠 LSTM", "📈 Prophet"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### LightGBM
            **Type:** Gradient Boosting (Tree-based)
            
            **✅ Strengths:**
            - Fastest training time
            - Handles large datasets well
            - Leaf-wise growth strategy
            - Uses all engineered features
            
            **Hyperparameters:**
            - n_estimators: 100
            - max_depth: 6
            - learning_rate: 0.1
            """)
        with col2:
            # Simulated predictions
            np.random.seed(42)
            actual = 100 + np.cumsum(np.random.randn(50))
            pred = actual + np.random.randn(50) * 10
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=actual, mode='lines', name='Actual'))
            fig.add_trace(go.Scatter(y=pred, mode='lines', name='Predicted', line=dict(dash='dash')))
            fig.update_layout(height=250, template='plotly_white', title='Predictions Sample')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### XGBoost
            **Type:** Gradient Boosting (Tree-based)
            
            **✅ Strengths:**
            - Strong regularization
            - Good for structured data
            - Feature importance built-in
            
            **⚠️ Compared to LightGBM:**
            - Slightly slower
            - Higher RMSE in this case
            """)
        with col2:
            pred = actual + np.random.randn(50) * 15
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=actual, mode='lines', name='Actual'))
            fig.add_trace(go.Scatter(y=pred, mode='lines', name='Predicted', line=dict(dash='dash')))
            fig.update_layout(height=250, template='plotly_white', title='Predictions Sample')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### LSTM
            **Type:** Deep Learning (RNN)
            
            **✅ Strengths:**
            - Captures long-term dependencies
            - Non-linear pattern recognition
            
            **⚠️ Weaknesses (for this data):**
            - 611 days is insufficient
            - Requires more data
            - Black box model
            - Longer training time
            """)
        with col2:
            pred = actual + np.random.randn(50) * 30 + 10
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=actual, mode='lines', name='Actual'))
            fig.add_trace(go.Scatter(y=pred, mode='lines', name='Predicted', line=dict(dash='dash')))
            fig.update_layout(height=250, template='plotly_white', title='Predictions Sample')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### Prophet
            **Type:** Additive Time Series Model
            
            **✅ Strengths:**
            - Automatic seasonality detection
            - Handles holidays
            - Interpretable components
            
            **⚠️ Weaknesses (for this data):**
            - Cannot use external features
            - Simple seasonality assumption
            - R² < 0 (worse than baseline)
            """)
        with col2:
            pred = actual + np.random.randn(50) * 35 + 15
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=actual, mode='lines', name='Actual'))
            fig.add_trace(go.Scatter(y=pred, mode='lines', name='Predicted', line=dict(dash='dash')))
            fig.update_layout(height=250, template='plotly_white', title='Predictions Sample')
            st.plotly_chart(fig, use_container_width=True)

# Insights
st.markdown("---")
st.success("""
**💡 Key Insights:**
- **Tree-based models win** - they leverage engineered features effectively
- **LightGBM is champion** - best RMSE (31.62) and R² (0.853)
- **Deep learning needs more data** - 611 days insufficient for LSTM
- **Prophet too simple** - cannot use our valuable features
""")
