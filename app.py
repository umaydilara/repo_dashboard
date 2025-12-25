"""
DEMAND FORECASTING DASHBOARD - OLIST
8-Page Academic Dashboard
"""

import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Demand Forecasting Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paths
BASE_PATH = Path(__file__).parent.parent
COMPARISON_PATH = BASE_PATH / 'model_comparison_outputs'

# Custom CSS
st.markdown("""
<style>
    .main .block-container {
        padding-top: 1rem;
        max-width: 1200px;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-left: 4px solid #1E88E5;
        padding: 15px;
        border-radius: 0 8px 8px 0;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)


def main():
    # Sidebar
    with st.sidebar:
        st.title("📊 Demand Forecasting")
        st.markdown("**Olist E-commerce Analysis**")
        st.markdown("---")
        
        st.markdown("""
        ### 📖 Dashboard Guide
        
        **8 Pages:**
        1. 🏠 Data & Business Overview
        2. 👥 Customer & Seller Behavior  
        3. 📦 Price, Logistics & Delivery
        4. 🛠️ Feature Engineering
        5. 🎯 Feature Selection & SHAP
        6. 🏆 Model Comparison
        7. 📈 Time Series Focus
        8. 🌟 Final Insights
        """)
    
    # Main Content
    st.title("📊 Demand Forecasting Dashboard")
    st.markdown("### Olist E-commerce Platform Analysis")
    st.markdown("---")
    
    st.markdown("""
    ## 🌟 Welcome
    
    This dashboard presents a comprehensive **demand forecasting study**.
    
    ### 🎯 Project Flow
    > **Data Cleaning → EDA → Feature Engineering → Feature Selection → Modeling → Explainability**
    """)
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
        <h4>🏠 Business Overview</h4>
        <p>Data scope, demand patterns</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
        <h4>🛠️ Feature Engineering</h4>
        <p>Lag, momentum, regime</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
        <h4>🏆 Model Comparison</h4>
        <p>XGBoost, LightGBM, Prophet, LSTM</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
        <h4>🎯 SHAP Analysis</h4>
        <p>Feature importance</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Model Results
    st.markdown("### 🏆 Model Performance Summary")
    
    metrics_file = COMPARISON_PATH / 'model_metrics.csv'
    if metrics_file.exists():
        metrics_df = pd.read_csv(metrics_file)
        best_model = metrics_df.loc[metrics_df['RMSE'].idxmin(), 'Model']
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.dataframe(metrics_df, use_container_width=True)
        
        with col2:
            st.success(f"""
            **🏆 Champion Model**
            
            **{best_model}**
            
            Selected based on lowest RMSE
            """)
    else:
        st.info("Model metrics not found. Run models first.")
    
    st.markdown("---")
    st.info("👉 **Navigate through the pages** using the sidebar menu")


if __name__ == "__main__":
    main()