"""
DASHBOARD 5: FEATURE SELECTION & SHAP
"""

import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Feature Selection & SHAP", page_icon="🎯", layout="wide")

BASE_PATH = Path(__file__).parent.parent.parent
FS_PATH = BASE_PATH / 'feature_selection_outputs'
SHAP_PATH = BASE_PATH / 'shap_outputs'

st.title("🎯 Feature Selection & SHAP")
st.markdown("### Neden Bu Feature'lar?")
st.markdown("---")

st.info("""
**🎯 Ana Soru:** Feature'ları rastgele değil, kanıtla seçtik.
""")

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Feature Selection", "🔍 SHAP Analysis", "🔗 Korelasyon"])

with tab1:
    st.subheader("📊 Feature Selection Results")
    st.markdown("""
    ### Kullanılan Yöntemler:
    1. **Correlation Analysis** - Hedef ile korelasyon
    2. **Mutual Information** - Non-linear bağımlılık
    3. **Random Forest Importance** - Tree-based önem
    """)
    
    img_path = FS_PATH / 'feature_selection_results.png'
    if img_path.exists():
        st.image(str(img_path), use_container_width=True)

with tab2:
    st.subheader("🔍 SHAP Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**SHAP Summary Bar**")
        img_path = SHAP_PATH / '01_shap_summary_bar.png'
        if img_path.exists():
            st.image(str(img_path), use_container_width=True)
    
    with col2:
        st.markdown("**SHAP Beeswarm**")
        img_path = SHAP_PATH / '02_shap_beeswarm.png'
        if img_path.exists():
            st.image(str(img_path), use_container_width=True)
    
    st.markdown("---")
    st.markdown("**SHAP Dependence Plots**")
    img_path = SHAP_PATH / '03_shap_dependence.png'
    if img_path.exists():
        st.image(str(img_path), use_container_width=True)

with tab3:
    st.subheader("🔗 Selected Features Correlation")
    img_path = FS_PATH / 'selected_features_correlation.png'
    if img_path.exists():
        st.image(str(img_path), use_container_width=True)

st.markdown("---")
st.success("""
### 💡 Anahtar Çıkarımlar
- **Çoklu yöntem** - tek yönteme bağımlı değiliz
- **SHAP doğrulaması** - feature önemi açıklanabilir
- **Uzun dönem feature'lar baskın** - is_high_long, momentum_360
""")