import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Model Comparison", page_icon="🏆", layout="wide")

st.sidebar.title("⚙️ Settings")
metric_choice = st.sidebar.selectbox("Primary Metric", ["RMSE", "MAE", "R2"])
show_details = st.sidebar.checkbox("Show Model Details", value=True)

st.title("🏆 Model Comparison")
st.markdown("### Which model performs best and why?")
st.markdown("---")

st.info("**🎯 Key Question:** Which model should we deploy?")

metrics_data = {
    'Model': ['LightGBM', 'XGBoost', 'LSTM', 'Prophet'],
    'RMSE': [31.62, 36.34, 75.36, 83.30],
    'MAE': [26.82, 28.83, 63.45, 69.79],
    'R2': [0.853, 0.806, 0.159, -0.020]
}
metrics_df = pd.DataFrame(metrics_data)

col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("📊 Model Performance Metrics")
    st.dataframe(metrics_df, use_container_width=True, height=200)
with col2:
    st.success("""
    ### 🏆 Champion Model
    ## LightGBM
    - **RMSE:** 31.62
    - **R²:** 0.853
    
    *Explains 85%+ of variance*
    """ )

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    colors = ['#43A047', '#1E88E5', '#FB8C00', '#E53935']
    fig = go.Figure(data=[go.Bar(x=metrics_df['Model'], y=metrics_df['RMSE'], marker_color=colors,
               text=metrics_df['RMSE'].round(1), textposition='outside')])
    fig.update_layout(title='RMSE Comparison (Lower is Better ↓)', height=400, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)
with col2:
    fig = go.Figure(data=[go.Bar(x=metrics_df['Model'], y=metrics_df['R2'], marker_color=colors,
               text=metrics_df['R2'].round(3), textposition='outside')])
    fig.add_hline(y=0, line_dash='dash', line_color='red')
    fig.update_layout(title='R² Comparison (Higher is Better ↑)', height=400, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)

if show_details:
    st.markdown("---")
    st.subheader("📋 Model Details")
    tab1, tab2, tab3, tab4 = st.tabs(["🌲 LightGBM", "🌳 XGBoost", "🧠 LSTM", "📈 Prophet"])
    with tab1:
        st.markdown("""
        **✅ Strengths:** Fastest training, handles large data, uses all features
        
        **Hyperparameters:** n_estimators=100, max_depth=6, learning_rate=0.1
        """ )
    with tab2:
        st.markdown("**✅ Strengths:** Strong regularization, good for structured data")
    with tab3:
        st.markdown("**⚠️ Weakness:** 611 days insufficient, needs more data")
    with tab4:
        st.markdown("**⚠️ Weakness:** Cannot use external features, R² < 0")

st.success("""
**💡 Key Insights:**
- Tree-based models win - they leverage engineered features
- LightGBM is champion - best RMSE and R²
- Deep learning needs more data
""")
