"""
DASHBOARD 6: MODEL COMPARISON
"Hangi model neden daha iyi?"
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Model Comparison", page_icon="🏆", layout="wide")

st.title("🏆 Model Comparison")
st.markdown("### Hangi Model Neden Daha İyi?")
st.markdown("---")

# Ana soru
st.info("""
**🎯 Ana Soru:** Hangi model neden daha iyi?
""")

# Metrics Summary
st.subheader("📊 Model Performance Metrics")

metrics_df = pd.DataFrame({
    'Model': ['XGBoost', 'LightGBM', 'Prophet', 'LSTM'],
    'RMSE': [32.45, 31.62, 89.23, 45.67],
    'MAE': [27.12, 26.82, 72.45, 38.91],
    'R2': [0.845, 0.853, -0.172, 0.693]
})

col1, col2 = st.columns([3, 2])

with col1:
    st.dataframe(
        metrics_df.style.format({
            'RMSE': '{:.2f}',
            'MAE': '{:.2f}',
            'R2': '{:.3f}'
        }).highlight_min(subset=['RMSE', 'MAE'], color='#90EE90')
        .highlight_max(subset=['R2'], color='#90EE90'),
        use_container_width=True,
        height=200
    )

with col2:
    st.success("""
    ### 🏆 Şampiyon Model
    
    **LightGBM**
    
    - RMSE: 31.62
    - R²: 0.853
    
    *Seçim kriteri: En düşük RMSE*
    """)

# Comparison Charts
col1, col2 = st.columns(2)

with col1:
    fig_rmse = px.bar(metrics_df, x='Model', y='RMSE',
                      title='RMSE Karşılaştırması (Düşük = İyi)',
                      color='RMSE', color_continuous_scale='Reds_r')
    st.plotly_chart(fig_rmse, use_container_width=True)

with col2:
    fig_r2 = px.bar(metrics_df, x='Model', y='R2',
                    title='R² Karşılaştırması (Yüksek = İyi)',
                    color='R2', color_continuous_scale='Greens')
    st.plotly_chart(fig_r2, use_container_width=True)

st.markdown("---")

# Model Details in Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🌳 XGBoost", "🌲 LightGBM", "📈 Prophet", "🧠 LSTM"])

with tab1:
    st.subheader("🌳 XGBoost Results")
    st.markdown("*Gradient Boosting - Tree-based Model*")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### Model Parametreleri
        - **n_estimators:** 100
        - **max_depth:** 6
        - **learning_rate:** 0.1
        - **subsample:** 0.8
        """)
    with col2:
        st.markdown("""
        ### Performans
        - **RMSE:** 32.45
        - **MAE:** 27.12
        - **R²:** 0.845
        """)
    
    st.markdown("""
    <div style='background-color: #e3f2fd; padding: 15px; border-radius: 8px;'>
    <b>✅ Güçlü Yönleri:</b>
    <ul>
    <li>Feature importance hesaplama</li>
    <li>Regularization ile overfitting kontrolü</li>
    <li>Eksik değerlerle baş edebilme</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.subheader("🌲 LightGBM Results")
    st.markdown("*Light Gradient Boosting Machine*")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### Model Parametreleri
        - **n_estimators:** 100
        - **num_leaves:** 31
        - **learning_rate:** 0.1
        - **feature_fraction:** 0.8
        """)
    with col2:
        st.markdown("""
        ### Performans
        - **RMSE:** 31.62 ⭐
        - **MAE:** 26.82 ⭐
        - **R²:** 0.853 ⭐
        """)
    
    st.markdown("""
    <div style='background-color: #e8f5e9; padding: 15px; border-radius: 8px;'>
    <b>✅ Güçlü Yönleri:</b>
    <ul>
    <li>Daha hızlı eğitim</li>
    <li>Leaf-wise growth stratejisi</li>
    <li>Büyük veri setlerinde etkili</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.subheader("📈 Prophet Results")
    st.markdown("*Facebook's Time Series Model*")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### Model Özellikleri
        - Additive model
        - Trend + Seasonality
        - Holiday effects
        """)
    with col2:
        st.markdown("""
        ### Performans
        - **RMSE:** 89.23 ⚠️
        - **MAE:** 72.45 ⚠️
        - **R²:** -0.172 ⚠️
        """)
    
    st.markdown("""
    <div style='background-color: #fff3e0; padding: 15px; border-radius: 8px;'>
    <b>✅ Güçlü Yönleri:</b>
    <ul>
    <li>Mevsimsellik ayrıştırması</li>
    <li>Tatil etkileri modelleme</li>
    <li>Yorumlanabilirlik</li>
    </ul>
    <b>⚠️ Zayıf Yönleri:</b>
    <ul>
    <li>Sadece zaman bazlı feature kullanır</li>
    <li>Karmaşık pattern'larda yetersiz</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with tab4:
    st.subheader("🧠 LSTM Results")
    st.markdown("*Long Short-Term Memory - Deep Learning*")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### Model Yapısı
        - 2 LSTM layer
        - 50 units each
        - Dropout: 0.2
        """)
    with col2:
        st.markdown("""
        ### Performans
        - **RMSE:** 45.67
        - **MAE:** 38.91
        - **R²:** 0.693
        """)
    
    st.markdown("""
    <div style='background-color: #f3e5f5; padding: 15px; border-radius: 8px;'>
    <b>✅ Güçlü Yönleri:</b>
    <ul>
    <li>Uzun vadeli bağımlılıkları öğrenme</li>
    <li>Karmaşık non-linear pattern'lar</li>
    </ul>
    <b>⚠️ Zayıf Yönleri:</b>
    <ul>
    <li>Daha fazla veri gerektirir</li>
    <li>Yorumlanması zor</li>
    <li>Daha uzun eğitim süresi</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# Key Takeaways
st.markdown("---")
st.success("""
### 💡 Bu Sayfanın Anahtar Çıkarımları

- **Tree-based modeller üstün** - feature'ları daha iyi kullandı
- **LightGBM en iyi RMSE** - şampiyon model
- **Prophet mevsimsellikte güçlü** - ama bu veri için yetersiz
- **LSTM daha fazla veriye ihtiyaç duyar** - küçük dataset'te düşük performans
""")
