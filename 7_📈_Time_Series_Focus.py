"""
DASHBOARD 7: TIME SERIES MODELS FOCUS
"""

import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Time Series Focus", page_icon="📈", layout="wide")

BASE_PATH = Path(__file__).parent.parent.parent
PROPHET_PATH = BASE_PATH / 'prophet_outputs'
LSTM_PATH = BASE_PATH / 'lstm_outputs'
COMPARISON_PATH = BASE_PATH / 'model_comparison_outputs'

st.title("📈 Time Series Models Focus")
st.markdown("### Prophet vs LSTM")
st.markdown("---")

st.info("""**🎯 Ana Soru:** Klasik zaman serisi mi, deep learning mi?""")

# Comparison
st.subheader("🔄 Prophet vs LSTM Karşılaştırması")
img_path = COMPARISON_PATH / 'prophet_vs_lstm_comparison.png'
if img_path.exists():
    st.image(str(img_path), use_container_width=True)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Prophet")
    img_path = PROPHET_PATH / 'prophet_components.png'
    if img_path.exists():
        st.image(str(img_path), use_container_width=True)
    
    st.markdown("""
    ### ✅ Avantajları
    - Mevsimsellik ayrıştırması
    - Yorumlanabilir
    - Tatil etkileri
    
    ### ⚠️ Dezavantajları
    - Sadece zaman bazlı
    - Dış feature alamaz
    """)

with col2:
    st.subheader("🧠 LSTM")
    img_path = LSTM_PATH / 'lstm_results.png'
    if img_path.exists():
        st.image(str(img_path), use_container_width=True)
    
    st.markdown("""
    ### ✅ Avantajları
    - Uzun vadeli bağımlılık
    - Non-linear pattern'lar
    
    ### ⚠️ Dezavantajları
    - Çok veri gerektirir
    - Black box
    """)

st.markdown("---")
st.warning("""
### 💡 Neden Tree-Based Modeller Daha İyi?

1. **Veri Boyutu** - 611 gün LSTM için yetersiz
2. **Feature Engineering** - Tree-based modeller hepsini kullanıyor
3. **Veri Yapısı** - Basit mevsimsellik yok, karmaşık pattern'lar var
""")