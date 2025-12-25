"""
DASHBOARD 7: TIME SERIES MODELS FOCUS
"Klasik zaman serisi vs deep learning"
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Time Series Focus", page_icon="📈", layout="wide")

st.title("📈 Time Series Models Focus")
st.markdown("### Prophet vs LSTM - Klasik vs Deep Learning")
st.markdown("---")

# Ana soru
st.info("""
**🎯 Ana Soru:** Klasik zaman serisi modeli mi, deep learning mi?
""")

# Comparison
st.subheader("🔄 Prophet vs LSTM Karşılaştırması")

comparison_df = pd.DataFrame({
    'Metrik': ['RMSE', 'MAE', 'R²', 'Eğitim Süresi', 'Yorumlanabilirlik'],
    'Prophet': [89.23, 72.45, -0.17, 'Hızlı', 'Yüksek'],
    'LSTM': [45.67, 38.91, 0.69, 'Yavaş', 'Düşük']
})

st.dataframe(comparison_df, use_container_width=True)

st.markdown("---")

# Side by side comparison
col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Prophet")
    st.markdown("*Facebook's Additive Time Series Model*")
    
    st.markdown("""
    ### ✅ Avantajları
    - **Mevsimsellik ayrıştırması** - haftalık, yıllık
    - **Yorumlanabilir** - her bileşen açık
    - **Tatil etkileri** - özel günler modellenebilir
    - **Eksik veri toleransı** - robust
    
    ### ⚠️ Dezavantajları
    - **Sadece zaman bazlı** - dış feature alamaz
    - **Basit pattern'lar** - karmaşık ilişkilerde zayıf
    - **Bu veri için yetersiz** - R² < 0
    """)

with col2:
    st.subheader("🧠 LSTM")
    st.markdown("*Long Short-Term Memory Neural Network*")
    
    st.markdown("""
    ### ✅ Avantajları
    - **Uzun vadeli bağımlılık** - sequence learning
    - **Non-linear pattern'lar** - karmaşık ilişkiler
    - **Otomatik feature extraction** - ham veriden öğrenme
    
    ### ⚠️ Dezavantajları
    - **Çok veri gerektirir** - ~600 satır yetersiz
    - **Yorumlanması zor** - black box
    - **Overfitting riski** - regularization kritik
    - **Uzun eğitim süresi**
    """)

st.markdown("---")

# Performance Comparison Chart
st.subheader("📊 Performans Karşılaştırması")

models = ['Prophet', 'LSTM', 'XGBoost', 'LightGBM']
rmse_values = [89.23, 45.67, 32.45, 31.62]
r2_values = [-0.17, 0.69, 0.85, 0.85]

fig = go.Figure()
fig.add_trace(go.Bar(name='RMSE', x=models, y=rmse_values, marker_color='indianred'))
fig.update_layout(title='RMSE Karşılaştırması', xaxis_title='Model', yaxis_title='RMSE')
st.plotly_chart(fig, use_container_width=True)

# Key Insight
st.warning("""
### 💡 Neden Tree-Based Modeller Daha İyi Performans Gösterdi?

**1. Veri Boyutu**
- ~600 günlük veri LSTM için yetersiz
- Tree-based modeller küçük veriyle de çalışır

**2. Feature Engineering**
- Oluşturduğumuz feature'lar (lag, rolling mean) çok değerli
- Prophet bunları kullanamıyor
- Tree-based modeller hepsini kullanıyor

**3. Veri Yapısı**
- Basit mevsimsellik yok, karmaşık pattern'lar var
- Prophet basit mevsimsellik varsayıyor
- Tree-based modeller ile daha iyi yakalanıyor
""")

# Key Takeaways
st.markdown("---")
st.success("""
### 💡 Bu Sayfanın Anahtar Çıkarımları

- **LSTM karmaşık pattern'ları yakaladı** - ama veri yetersiz
- **Prophet mevsimsellikte güçlü** - ama feature kullanamıyor
- **Bu veri için tree-based optimal** - feature engineering + tree = başarı
- **Daha fazla veri olsaydı** - LSTM muhtemelen daha iyi olurdu
""")
