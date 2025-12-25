"""
DASHBOARD 8: FINAL INSIGHTS
"Bu çalışmadan ne öğrendik?"
"""

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Final Insights", page_icon="🌟", layout="wide")

st.title("🌟 Final Insights")
st.markdown("### Sunum Kapanışı - Bu Çalışmadan Ne Öğrendik?")
st.markdown("---")

# Journey Summary
st.markdown("""
## 📊 Analiz Yolculuğumuz

Data Cleaning → EDA → Feature Engineering → Feature Selection → Modeling → Explainability

""")

# Model Result
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
    metrics_df = pd.DataFrame({
        'Model': ['XGBoost', 'LightGBM', 'Prophet', 'LSTM'],
        'RMSE': [32.45, 31.62, 89.23, 45.67],
        'R2': [0.845, 0.853, -0.172, 0.693]
    })
    
    fig = px.bar(metrics_df, x='Model', y='RMSE', color='RMSE',
                 title='Model RMSE Karşılaştırması',
                 color_continuous_scale='RdYlGn_r')
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Top Features
st.subheader("🎯 2. En Önemli 5 Feature")

st.markdown("""
| Sıra | Feature | Açıklama | Önem |
|------|---------|---------|------|
| 1 | **rolling_mean_30** | 30 günlük ortalama | ⭐⭐⭐⭐⭐ |
| 2 | **lag_7** | 7 gün önceki talep | ⭐⭐⭐⭐ |
| 3 | **rolling_mean_7** | 7 günlük ortalama | ⭐⭐⭐⭐ |
| 4 | **lag_14** | 14 gün önceki talep | ⭐⭐⭐ |
| 5 | **dayofweek** | Haftanın günü | ⭐⭐⭐ |
""")

col1, col2 = st.columns(2)

with col1:
    features = ['rolling_mean_30', 'lag_7', 'rolling_mean_7', 'lag_14', 'dayofweek']
    importance = [0.85, 0.72, 0.68, 0.55, 0.48]
    
    fig = px.bar(x=importance, y=features, orientation='h',
                 title='Feature Importance',
                 labels={'x': 'Importance', 'y': 'Feature'},
                 color=importance, color_continuous_scale='Viridis')
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("""
    ### 📝 Feature Önemleri Yorumu
    
    **Rolling Mean Baskın:**
    - Trend en önemli faktör
    - Kısa ve orta vade trendi yakalar
    
    **Lag Feature'lar Önemli:**
    - Geçmiş talep gelecek talebi etkiler
    - 7 ve 14 günlük lag'ler kritik
    
    **Haftalık Pattern:**
    - Haftanın günü talebi etkiliyor
    """)

st.markdown("---")

# Business Insights
st.subheader("💼 3. İşsel Çıkarımlar")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    ### 📦 Stok Planlama
    
    **Öneri:** Rolling mean değerlerine 
    göre stok seviyelerini ayarla
    
    - Yükselen trend → Stok artır
    - Düşen trend → Stok azalt
    """)

with col2:
    st.info("""
    ### 📅 Kampanya Zamanlaması
    
    **Öneri:** Yüksek talep dönemlerinde
    kampanya başlatma
    
    - Peak dönemleri önceden tahmin et
    - Pazarlama bütçesini optimize et
    """)

with col3:
    st.info("""
    ### 🚚 Lojistik Planlama
    
    **Öneri:** Talep dalgalanmalarına
    göre kapasite ayarla
    
    - Yüksek volatilite = Ekstra kapasite
    - Stabil dönem = Optimize kapasite
    """)

st.markdown("---")

# Academic Value
st.subheader("🎓 4. Akademik Değer")

st.markdown("""
### Bu Çalışmanın Akademik Katkısı

| Alan | Katkı |
|------|------|
| **Metodoloji** | Çoklu feature selection yöntemi ile robust değerlendirme |
| **Karşılaştırma** | Tree-based vs Time Series vs Deep Learning kapsamlı karşılaştırma |
| **Açıklanabilirlik** | SHAP ile black-box olmayan model açıklaması |
| **Tekrarlanabilirlik** | Tüm kod ve görseller paylaşıldı |
""")

st.markdown("---")

# Conclusion
st.success("""
## 🌟 Sonuç

> "Veriyi anladık → Anlamlı feature'lar oluşturduk → Titizlikle seçtik → 
Modelleri adil karşılaştırdık → Kazananı açıkladık."

### Ana Mesaj:
**Rolling mean ve lag feature'ları, talep tahmininde en kritik faktörler.**

Bu yapı:
- ✅ Stok planlamada kullanılabilir
- ✅ Kampanya zamanlamada kullanılabilir  
- ✅ Lojistik optimizasyonda kullanılabilir
""")

# Celebration
st.balloons()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px;'>
<h3>🎓 Talep Tahmini Projesi</h3>
<p>Data Cleaning → EDA → Feature Engineering → Modeling → Explainability</p>
<p><strong>Teşekkürler!</strong></p>
</div>
""", unsafe_allow_html=True)
