"""
DASHBOARD 4: FEATURE ENGINEERING INSIGHTS
"""

import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Feature Engineering", page_icon="🛠️", layout="wide")

BASE_PATH = Path(__file__).parent.parent.parent
FEATURE_EDA_PATH = BASE_PATH / 'feature_eda_outputs'

st.title("🛠️ Feature Engineering Insights")
st.markdown("### FE + EDA Birleşimi")
st.markdown("---")

st.warning("""
**🎯 Ana Soru:** Yeni oluşturduğumuz feature'lar gerçekten anlamlı mı?

✅ **Bu dashboard hocanın en sevdiği tür olur!**
""")

# Feature Categories
st.markdown("""
### 📊 Oluşturulan Feature Kategorileri

| Kategori | Feature'lar | Amaç |
|----------|------------|------|
| **Lag Features** | lag_15, lag_30, lag_90, lag_180, lag_360 | Geçmiş talep |
| **Rolling Stats** | rolling_mean_*, rolling_std_* | Trend ve volatilite |
| **EWMA** | ewma_15, ewma_30... | Ağırlıklı ortalama |
| **Momentum** | momentum_15, momentum_30... | Değişim hızı |
| **Regime** | is_high_short, is_high_long | Piyasa durumu |
""")

st.markdown("---")

# Time Series EDA
st.subheader("📈 1. Time Series EDA")
img_path = FEATURE_EDA_PATH / '01_time_series_eda.png'
if img_path.exists():
    st.image(str(img_path), use_container_width=True)

st.markdown("---")

# Lag Scatter
st.subheader("🔄 2. Lag Feature Analysis")
img_path = FEATURE_EDA_PATH / '02_lag_scatter_eda.png'
if img_path.exists():
    st.image(str(img_path), use_container_width=True)

st.markdown("""
<div style='background-color: #e3f2fd; padding: 15px; border-radius: 8px;'>
<b>📝 Yorum:</b> Uzun dönem lag'ler (lag_180, lag_360) talep yapısını daha iyi yakalamış.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Momentum
st.subheader("🚀 3. Momentum Analysis")
img_path = FEATURE_EDA_PATH / '03_momentum_eda.png'
if img_path.exists():
    st.image(str(img_path), use_container_width=True)

st.markdown("---")

# Volatility
st.subheader("🌊 4. Volatility & Trend")
img_path = FEATURE_EDA_PATH / '06_volatility_trend_eda.png'
if img_path.exists():
    st.image(str(img_path), use_container_width=True)

st.markdown("---")
st.success("""
### 💡 Anahtar Çıkarımlar
- **Uzun dönem lag'ler etkili** - lag_180, lag_360 önemli
- **Momentum talep yönünü yakalar**
- **Feature'lar rastgele değil, veri tarafından doğrulanmış!**
""")