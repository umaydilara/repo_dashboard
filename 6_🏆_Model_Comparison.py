"""
DASHBOARD 6: MODEL COMPARISON
"""

import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Model Comparison", page_icon="🏆", layout="wide")

BASE_PATH = Path(__file__).parent.parent.parent
XGB_PATH = BASE_PATH / 'xgboost_outputs'
LGB_PATH = BASE_PATH / 'lightgbm_outputs'
PROPHET_PATH = BASE_PATH / 'prophet_outputs'
LSTM_PATH = BASE_PATH / 'lstm_outputs'
COMPARISON_PATH = BASE_PATH / 'model_comparison_outputs'

st.title("🏆 Model Comparison")
st.markdown("### Hangi Model Neden Daha İyi?")
st.markdown("---")

st.info("""**🎯 Ana Soru:** Hangi model neden daha iyi?""")

# Metrics
st.subheader("📊 Model Performance Metrics")

metrics_file = COMPARISON_PATH / 'model_metrics.csv'
if metrics_file.exists():
    metrics_df = pd.read_csv(metrics_file)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.dataframe(metrics_df, use_container_width=True, height=200)
    
    with col2:
        best_model = metrics_df.loc[metrics_df['RMSE'].idxmin(), 'Model']
        best_rmse = metrics_df['RMSE'].min()
        
        st.success(f"""
        ### 🏆 Şampiyon Model
        **{best_model}**
        - RMSE: {best_rmse:.2f}
        """)

# Comparison Chart
img_path = COMPARISON_PATH / 'model_comparison_metrics.png'
if img_path.exists():
    st.image(str(img_path), use_container_width=True)

st.markdown("---")

# Model Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🌳 XGBoost", "🌲 LightGBM", "📈 Prophet", "🧠 LSTM"])

with tab1:
    st.subheader("🌳 XGBoost Results")
    img_path = XGB_PATH / 'xgboost_results.png'
    if img_path.exists():
        st.image(str(img_path), use_container_width=True)

with tab2:
    st.subheader("🌲 LightGBM Results")
    img_path = LGB_PATH / 'lightgbm_results.png'
    if img_path.exists():
        st.image(str(img_path), use_container_width=True)

with tab3:
    st.subheader("📈 Prophet Results")
    col1, col2 = st.columns(2)
    with col1:
        img_path = PROPHET_PATH / 'prophet_results.png'
        if img_path.exists():
            st.image(str(img_path), use_container_width=True)
    with col2:
        img_path = PROPHET_PATH / 'prophet_components.png'
        if img_path.exists():
            st.image(str(img_path), use_container_width=True)

with tab4:
    st.subheader("🧠 LSTM Results")
    img_path = LSTM_PATH / 'lstm_results.png'
    if img_path.exists():
        st.image(str(img_path), use_container_width=True)

st.markdown("---")
st.success("""
### 💡 Anahtar Çıkarımlar
- **Tree-based modeller üstün** - feature'ları daha iyi kullandı
- **LightGBM en iyi RMSE** - şampiyon model
- **Prophet mevsimsellikte güçlü** - ama bu veri için yetersiz
""")