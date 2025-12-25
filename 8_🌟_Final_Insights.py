"""
DASHBOARD 8: FINAL INSIGHTS
"""

import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Final Insights", page_icon="🌟", layout="wide")

BASE_PATH = Path(__file__).parent.parent.parent
COMPARISON_PATH = BASE_PATH / 'model_comparison_outputs'
SHAP_PATH = BASE_PATH / 'shap_outputs'

st.title("🌟 Final Insights")
st.markdown("### Bu Çalışmadan Ne Öğrendik?")
st.markdown("---")

st.markdown("""
## 📊 Analiz Yolculuğumuz""")

# Best Model
st.subheader("🏆 1. En İyi Model")

col1, col2 = st.columns([1, 2])

with col1:
    st.success("""
    ### 🥇 LightGBM
    
    | Metrik | Değer |
    |--------|-------|
    | **RMSE** | 31.62 |
    | **MAE** | 26.82 |
    | **R²** | 0.853 |
    
    *85%+ varyansı açıklama*
    """)

with col2:
    img_path = COMPARISON_PATH / 'model_comparison_metrics.png'
    if img_path.exists():
        st.image(str(img_path), use_container_width=True)

st.markdown("---")

# Top Features
st.subheader("🎯 2. En Önemli 5 Feature")

st.markdown("""
| Sıra | Feature | Açıklama |
|------|---------|---------|
| 1 | **is_high_long** | Uzun vadeli yüksek talep rejimi |
| 2 | **momentum_360** | Yıllık değişim hızı |
| 3 | **momentum_180** | 6 aylık değişim hızı |
| 4 | **is_high_short** | Kısa vadeli yüksek talep |
| 5 | **rolling_mean_180** | 6 aylık ortalama |
""")

col1, col2 = st.columns(2)
with col1:
    img_path = SHAP_PATH / '01_shap_summary_bar.png'
    if img_path.exists():
        st.image(str(img_path), use_container_width=True)

st.markdown("---")

# Business Insights
st.subheader("💼 3. İşsel Çıkarımlar")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    ### 📦 Stok Planlama
    Uzun vadeli rejim göstergelerine göre stok seviyelerini ayarla
    """)

with col2:
    st.info("""
    ### 📅 Kampanya Zamanlaması
    Yüksek talep dönemlerinde kampanya başlat
    """)

with col3:
    st.info("""
    ### 🚚 Lojistik Planlama
    Talep dalgalanmalarına göre kapasite ayarla
    """)

st.markdown("---")

# Conclusion
st.success("""
## 🌟 Sonuç

> "Veriyi anladık → Anlamlı feature'lar oluşturduk → Titizlikle seçtik → 
Modelleri adil karşılaştırdık → Kazananı açıkladık."

### Ana Mesaj:
**Uzun vadeli rejim göstergeleri ve momentum, talep tahmininde en kritik faktörler.**
""")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px;'>
<h3>🎓 Talep Tahmini Projesi</h3>
<p><strong>Teşekkürler!</strong></p>
</div>
""", unsafe_allow_html=True)