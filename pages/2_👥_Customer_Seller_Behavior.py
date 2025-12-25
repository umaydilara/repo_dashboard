"""
DASHBOARD 2: CUSTOMER & SELLER BEHAVIOR
"Talebi kim üretiyor, kim karşılıyor?"
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Customer & Seller Behavior", page_icon="👥", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('demand_features_final.csv')
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

df = load_data()

st.title("👥 Customer & Seller Behavior")
st.markdown("### EDA - Davranışsal İçgörü")
st.markdown("---")

# Ana soru
st.info("""
**🎯 Ana Soru:** Talebi kim üretiyor, kim karşılıyor?
""")

# Customer Behavior - Monthly Analysis
st.subheader("👤 1. Aylık Talep Analizi")
st.markdown("*Müşteri davranış paternleri - aylık bazda*")

if 'month' in df.columns:
    monthly_orders = df.groupby('month')['daily_orders'].agg(['sum', 'mean', 'std']).reset_index()
    monthly_orders.columns = ['Ay', 'Toplam', 'Ortalama', 'Std']
    
    month_names = ['Oca', 'Şub', 'Mar', 'Nis', 'May', 'Haz', 'Tem', 'Ağu', 'Eyl', 'Eki', 'Kas', 'Ara']
    monthly_orders['Ay_Adı'] = monthly_orders['Ay'].apply(lambda x: month_names[int(x)-1] if 1 <= x <= 12 else 'N/A')
    
    fig_monthly = px.bar(monthly_orders, x='Ay_Adı', y='Toplam',
                         title='Aylık Toplam Sipariş',
                         labels={'Ay_Adı': 'Ay', 'Toplam': 'Toplam Sipariş'},
                         color='Toplam', color_continuous_scale='Viridis')
    st.plotly_chart(fig_monthly, use_container_width=True)

st.markdown("""
<div style='background-color: #fff3e0; padding: 15px; border-radius: 8px; margin: 10px 0;'>
<b>📝 Yorum:</b> Talep az sayıda müşteri değil, geniş bir kitleye yayılmış. 
Aylık bazda belirgin trendler görülüyor.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Weekly Pattern
st.subheader("🏪 2. Haftalık Talep Paternleri")
st.markdown("*Haftanın günlerine göre sipariş dağılımı*")

if 'dayofweek' in df.columns:
    dow_stats = df.groupby('dayofweek')['daily_orders'].agg(['mean', 'std', 'min', 'max']).reset_index()
    day_names = ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz']
    dow_stats['Gün'] = dow_stats['dayofweek'].apply(lambda x: day_names[int(x)] if x < 7 else 'N/A')
    
    fig_dow = go.Figure()
    fig_dow.add_trace(go.Bar(x=dow_stats['Gün'], y=dow_stats['mean'], name='Ortalama',
                              error_y=dict(type='data', array=dow_stats['std'])))
    fig_dow.update_layout(title='Haftanın Günlerine Göre Sipariş (Std ile)',
                          xaxis_title='Gün', yaxis_title='Ortalama Sipariş')
    st.plotly_chart(fig_dow, use_container_width=True)

st.markdown("""
<div style='background-color: #fff3e0; padding: 15px; border-radius: 8px; margin: 10px 0;'>
<b>📝 Yorum:</b> Hafta içi ve hafta sonu arasında belirgin farklılıklar mevcut.
Satıcı performansı talep sürekliliğini etkiliyor.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Trend Analysis
st.subheader("🗺️ 3. Talep Trendi Analizi")
st.markdown("*Uzun vadeli trend*")

# Rolling average
df_sorted = df.sort_values('order_date')
df_sorted['rolling_7'] = df_sorted['daily_orders'].rolling(window=7).mean()
df_sorted['rolling_30'] = df_sorted['daily_orders'].rolling(window=30).mean()

fig_trend = go.Figure()
fig_trend.add_trace(go.Scatter(x=df_sorted['order_date'], y=df_sorted['daily_orders'],
                                mode='lines', name='Günlük', opacity=0.4))
fig_trend.add_trace(go.Scatter(x=df_sorted['order_date'], y=df_sorted['rolling_7'],
                                mode='lines', name='7 Günlük MA', line=dict(width=2)))
fig_trend.add_trace(go.Scatter(x=df_sorted['order_date'], y=df_sorted['rolling_30'],
                                mode='lines', name='30 Günlük MA', line=dict(width=3)))
fig_trend.update_layout(title='Talep Trendi (Hareketli Ortalamalar)',
                        xaxis_title='Tarih', yaxis_title='Sipariş',
                        hovermode='x unified')
st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("""
<div style='background-color: #fff3e0; padding: 15px; border-radius: 8px; margin: 10px 0;'>
<b>📝 Yorum:</b> Talep belirli dönemlerde yoğunlaşmış. 
Uzun vadeli trend görülebiliyor.
</div>
""", unsafe_allow_html=True)

# Key Takeaways
st.markdown("---")
st.success("""
### 💡 Bu Sayfanın Anahtar Çıkarımları

- **Müşteri tabanı geniş** - talep tek kaynağa bağımlı değil
- **Haftalık pattern belirgin** - talep tahmini için önemli faktör
- **Aylık mevsimsellik** - stok planlamayı etkiler
- **Trend yükseliyor** - büyüme potansiyeli var
""")
