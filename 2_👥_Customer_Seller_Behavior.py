"""
DASHBOARD 2: CUSTOMER & SELLER BEHAVIOR
"""

import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Customer & Seller Behavior", page_icon="👥", layout="wide")

BASE_PATH = Path(__file__).parent.parent.parent
EDA_PATH = BASE_PATH / 'eda_outputs'

st.title("👥 Customer & Seller Behavior")
st.markdown("### EDA - Davranışsal İçgörü")
st.markdown("---")

st.info("""
**🎯 Ana Soru:** Talebi kim üretiyor, kim karşılıyor?
""")

# Customer Behavior
st.subheader("👤 1. Customer Behavior Analysis")
img_path = EDA_PATH / '04_customer_behavior_analysis.png'
if img_path.exists():
    st.image(str(img_path), use_container_width=True)

st.markdown("""
<div style='background-color: #fff3e0; padding: 15px; border-radius: 8px;'>
<b>📝 Yorum:</b> Talep geniş bir kitleye yayılmış. Tekrar satın alma oranı düşük.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Seller Performance
st.subheader("🏪 2. Seller Performance")
img_path = EDA_PATH / '11_seller_performance.png'
if img_path.exists():
    st.image(str(img_path), use_container_width=True)

st.markdown("---")

# Geographic
st.subheader("🗺️ 3. Geographic Analysis")
img_path = EDA_PATH / '03_geographic_analysis.png'
if img_path.exists():
    st.image(str(img_path), use_container_width=True)

st.markdown("---")
st.success("""
### 💡 Anahtar Çıkarımlar
- **Müşteri tabanı geniş** - talep tek kaynağa bağımlı değil
- **Satıcı performansı değişken**
- **Bölgesel yoğunluk** - Sao Paulo baskın
""")