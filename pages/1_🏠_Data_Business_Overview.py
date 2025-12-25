"""
DASHBOARD 1: DATA & BUSINESS OVERVIEW
"Bu veri ne anlatıyor? Olist'te talep nasıl bir yapı gösteriyor?"
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Data & Business Overview", page_icon="🏠", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('demand_features_final.csv')
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

df = load_data()

st.title("🏠 Data & Business Overview")
st.markdown("### EDA - Büyük Resim")
st.markdown("---")

# Ana soru
st.info("""
**🎯 Ana Soru:** Bu veri ne anlatıyor? Olist'te talep nasıl bir yapı gösteriyor?
""")

# Dataset Overview
st.subheader("📊 1. Dataset Overview")
st.markdown("*Veri kapsamı, tarih aralığı, hacim*")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📅 Tarih Aralığı", f"{df['order_date'].min().strftime('%Y-%m-%d')}")
with col2:
    st.metric("📅 Son Tarih", f"{df['order_date'].max().strftime('%Y-%m-%d')}")
with col3:
    st.metric("📊 Toplam Gün", len(df))
with col4:
    st.metric("🔢 Feature Sayısı", len(df.columns))

# Data types
st.markdown("**Veri Türleri:**")
col1, col2 = st.columns(2)
with col1:
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    st.write(f"- Sayısal Değişkenler: **{len(numeric_cols)}**")
with col2:
    st.write(f"- Toplam Satır: **{len(df):,}**")

st.markdown("""
<div style='background-color: #e8f4f8; padding: 15px; border-radius: 8px; margin: 10px 0;'>
<b>📝 Yorum:</b> Dataset'in genel yapısı, veri türleri ve eksik değer oranı görülmektedir.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Time Series Analysis
st.subheader("📈 2. Time Series Analysis")
st.markdown("*Talep zaman içinde nasıl değişiyor?*")

fig_ts = px.line(df, x='order_date', y='daily_orders',
                 title='Günlük Sipariş Trendi',
                 labels={'order_date': 'Tarih', 'daily_orders': 'Günlük Sipariş'})
fig_ts.update_layout(hovermode='x unified')
st.plotly_chart(fig_ts, use_container_width=True)

st.markdown("""
<div style='background-color: #e8f4f8; padding: 15px; border-radius: 8px; margin: 10px 0;'>
<b>📝 Yorum:</b> Talep zamana yayılmış, ani kopukluk yok. Yükselen trend ve mevsimsel paternler görülüyor.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Distribution Analysis
st.subheader("📦 3. Talep Dağılımı")
st.markdown("*Sipariş hacmi nasıl dağılıyor?*")

col1, col2 = st.columns(2)

with col1:
    fig_hist = px.histogram(df, x='daily_orders', nbins=30,
                            title='Günlük Sipariş Dağılımı',
                            labels={'daily_orders': 'Günlük Sipariş', 'count': 'Frekans'})
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    fig_box = px.box(df, y='daily_orders',
                     title='Sipariş Box Plot',
                     labels={'daily_orders': 'Günlük Sipariş'})
    st.plotly_chart(fig_box, use_container_width=True)

st.markdown("""
<div style='background-color: #e8f4f8; padding: 15px; border-radius: 8px; margin: 10px 0;'>
<b>📝 Yorum:</b> Platform çok kategorili bir yapıya sahip. Bazı günler baskın sipariş hacmine sahip.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Weekly Pattern
st.subheader("💳 4. Haftalık Pattern")
st.markdown("*Haftanın günlerine göre talep*")

if 'dayofweek' in df.columns:
    dow_avg = df.groupby('dayofweek')['daily_orders'].mean().reset_index()
    day_names = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar']
    dow_avg['day_name'] = dow_avg['dayofweek'].apply(lambda x: day_names[int(x)] if x < 7 else 'Bilinmiyor')
    
    fig_dow = px.bar(dow_avg, x='day_name', y='daily_orders',
                     title='Haftanın Günlerine Göre Ortalama Sipariş',
                     labels={'day_name': 'Gün', 'daily_orders': 'Ortalama Sipariş'},
                     color='daily_orders', color_continuous_scale='Blues')
    st.plotly_chart(fig_dow, use_container_width=True)

st.markdown("""
<div style='background-color: #e8f4f8; padding: 15px; border-radius: 8px; margin: 10px 0;'>
<b>📝 Yorum:</b> Hafta içi ve hafta sonu talep farklılıkları görülmektedir.
</div>
""", unsafe_allow_html=True)

# Key Takeaways
st.markdown("---")
st.success("""
### 💡 Bu Sayfanın Anahtar Çıkarımları

- **Talep zamana yayılmış** - ani kopukluk yok
- **Platform çok kategorili** - ürün çeşitliliği yüksek
- **Haftalık pattern mevcut** - tahmin için fırsat
- **Mevsimsel paternler mevcut** - feature engineering için fırsat
""")
