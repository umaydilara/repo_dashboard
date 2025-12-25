"""
DASHBOARD 1: DATA & BUSINESS OVERVIEW
"""

import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Data & Business Overview", page_icon="🏠", layout="wide")

BASE_PATH = Path(__file__).parent.parent.parent
EDA_PATH = BASE_PATH / 'eda_outputs'

st.title("🏠 Data & Business Overview")
st.markdown("### EDA - Büyük Resim")
st.markdown("---")

st.info("""
**🎯 Ana Soru:** Bu veri ne anlatıyor? Olist'te talep nasıl bir yapı gösteriyor?
""")

# Dataset Overview
st.subheader("📊 1. Dataset Overview")
img_path = EDA_PATH / '01_dataset_overview.png'
if img_path.exists():
    st.image(str(img_path), use_container_width=True)

st.markdown("""
<div style='background-color: #e8f4f8; padding: 15px; border-radius: 8px;'>
<b>📝 Yorum:</b> Dataset'in genel yapısı, veri türleri ve eksik değer oranı görülmektedir.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Time Series
st.subheader("📈 2. Time Series Analysis")
img_path = EDA_PATH / '02_time_series_analysis.png'
if img_path.exists():
    st.image(str(img_path), use_container_width=True)

st.markdown("""
<div style='background-color: #e8f4f8; padding: 15px; border-radius: 8px;'>
<b>📝 Yorum:</b> Talep zamana yayılmış, ani kopukluk yok. Yükselen trend ve mevsimsel paternler.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Product Analysis
st.subheader("📦 3. Product Analysis")
img_path = EDA_PATH / '05_product_analysis.png'
if img_path.exists():
    st.image(str(img_path), use_container_width=True)

st.markdown("---")

# Payment Analysis
st.subheader("💳 4. Payment Analysis")
img_path = EDA_PATH / '09_payment_analysis.png'
if img_path.exists():
    st.image(str(img_path), use_container_width=True)

# Key Takeaways
st.markdown("---")
st.success("""
### 💡 Anahtar Çıkarımlar
- **Talep zamana yayılmış** - ani kopukluk yok
- **Platform çok kategorili** - ürün çeşitliliği yüksek
- **Ödeme davranışı homojen** - tahmin edilebilir
""")