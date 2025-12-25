"""
DASHBOARD 3: PRICE, LOGISTICS & DELIVERY
"Fiyat, kargo ve teslimat talebi nasıl etkiliyor?"
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Price, Logistics & Delivery", page_icon="📦", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('demand_features_final.csv')
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

df = load_data()

st.title("📦 Price, Logistics & Delivery")
st.markdown("### EDA - Operasyonel Perspektif")
st.markdown("---")

# Ana soru
st.info("""
**🎯 Ana Soru:** Fiyat, kargo ve teslimat talebi nasıl etkiliyor?
""")

# Volatility Analysis
st.subheader("💰 1. Talep Volatilitesi")
st.markdown("*Talep değişkenliği analizi*")

# Calculate volatility
df_sorted = df.sort_values('order_date').copy()
df_sorted['rolling_std'] = df_sorted['daily_orders'].rolling(window=14).std()
df_sorted['rolling_mean'] = df_sorted['daily_orders'].rolling(window=14).mean()
df_sorted['cv'] = df_sorted['rolling_std'] / df_sorted['rolling_mean'] * 100

col1, col2 = st.columns(2)

with col1:
    fig_vol = px.line(df_sorted, x='order_date', y='rolling_std',
                      title='14 Günlük Rolling Volatilite',
                      labels={'order_date': 'Tarih', 'rolling_std': 'Std Sapma'})
    st.plotly_chart(fig_vol, use_container_width=True)

with col2:
    fig_cv = px.line(df_sorted, x='order_date', y='cv',
                     title='Değişim Katsayısı (%)',
                     labels={'order_date': 'Tarih', 'cv': 'CV %'})
    st.plotly_chart(fig_cv, use_container_width=True)

st.markdown("""
<div style='background-color: #e8f5e9; padding: 15px; border-radius: 8px; margin: 10px 0;'>
<b>📝 Yorum:</b> Volatilite zaman içinde değişiyor. Yüksek volatilite dönemleri 
stok ve lojistik planlamada risk oluşturuyor.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Delivery/Operations Metrics
st.subheader("🚚 2. Operasyonel Metrikler")
st.markdown("*Kapasite planlama için istatistikler*")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📊 Ortalama Sipariş", f"{df['daily_orders'].mean():.1f}")
with col2:
    st.metric("📈 Maksimum", f"{df['daily_orders'].max():.0f}")
with col3:
    st.metric("📉 Minimum", f"{df['daily_orders'].min():.0f}")
with col4:
    st.metric("🎯 Std Sapma", f"{df['daily_orders'].std():.1f}")

# Percentile analysis
st.markdown("**Kapasite Planlama için Yüzdelikler:**")
percentiles = [50, 75, 90, 95, 99]
perc_values = [np.percentile(df['daily_orders'], p) for p in percentiles]

fig_perc = px.bar(x=[f'{p}. Yüzdelik' for p in percentiles], y=perc_values,
                  title='Sipariş Hacmi Yüzdelikleri',
                  labels={'x': 'Yüzdelik', 'y': 'Sipariş Sayısı'},
                  color=perc_values, color_continuous_scale='Oranges')
st.plotly_chart(fig_perc, use_container_width=True)

st.markdown("""
<div style='background-color: #e8f5e9; padding: 15px; border-radius: 8px; margin: 10px 0;'>
<b>📝 Yorum:</b> 95. yüzdelik değeri günlük kapasite planlaması için kritik.
Bu değerin üzerindeki günler için ekstra kaynak gerekiyor.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Peak Analysis
st.subheader("📏 3. Peak Günler Analizi")
st.markdown("*Yüksek talep dönemleri*")

threshold_90 = np.percentile(df['daily_orders'], 90)
df_peaks = df[df['daily_orders'] >= threshold_90].copy()

st.write(f"**90. yüzdelik üzeri gün sayısı:** {len(df_peaks)} ({len(df_peaks)/len(df)*100:.1f}%)")

if 'dayofweek' in df_peaks.columns:
    peak_dow = df_peaks['dayofweek'].value_counts().sort_index()
    day_names = ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz']
    
    fig_peak = px.bar(x=[day_names[int(i)] for i in peak_dow.index],
                      y=peak_dow.values,
                      title='Peak Günlerin Hafta İçi Dağılımı',
                      labels={'x': 'Gün', 'y': 'Peak Gün Sayısı'})
    st.plotly_chart(fig_peak, use_container_width=True)

st.markdown("""
<div style='background-color: #e8f5e9; padding: 15px; border-radius: 8px; margin: 10px 0;'>
<b>📝 Yorum:</b> Peak günler belirli hafta günlerinde yoğunlaşıyor.
Lojistik kapasite bu günlere göre planlanmalı.
</div>
""", unsafe_allow_html=True)

# Key Takeaways
st.markdown("---")
st.success("""
### 💡 Bu Sayfanın Anahtar Çıkarımları

- **Volatilite değişken** - bazı dönemler daha riskli
- **95. yüzdelik kritik** - kapasite planlaması için temel
- **Peak günler tahmin edilebilir** - haftalık pattern mevcut
- **Operasyonel metrikler** - talep tahmininde dışsal değişken olarak kullanılabilir
""")
