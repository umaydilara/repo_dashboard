"""
DASHBOARD 3: PRICE, LOGISTICS & DELIVERY
"""

import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Price, Logistics & Delivery", page_icon="📦", layout="wide")

BASE_PATH = Path(__file__).parent.parent.parent
EDA_PATH = BASE_PATH / 'eda_outputs'

st.title("📦 Price, Logistics & Delivery")
st.markdown("### EDA - Operasyonel Perspektif")
st.markdown("---")

st.info("""
**🎯 Ana Soru:** Fiyat, kargo ve teslimat talebi nasıl etkiliyor?
""")

# Price & Freight
st.subheader("💰 1. Price & Freight Analysis")
img_path = EDA_PATH / '08_price_freight_analysis.png'
if img_path.exists():
    st.image(str(img_path), use_container_width=True)

st.markdown("---")

# Delivery Performance
st.subheader("🚚 2. Delivery Performance")
img_path = EDA_PATH / '07_delivery_performance.png'
if img_path.exists():
    st.image(str(img_path), use_container_width=True)

st.markdown("---")

# Product Dimensions
st.subheader("📏 3. Product Dimensions")
img_path = EDA_PATH / '06_product_dimensions.png'
if img_path.exists():
    st.image(str(img_path), use_container_width=True)

st.markdown("---")
st.success("""
### 💡 Anahtar Çıkarımlar
- **Kargo maliyeti talep üzerinde etkili**
- **Teslimat gecikmeleri** - müşteri kaybına yol açabilir
- **Ürün boyutu lojistiği etkiler**
""")