"""
============================================
DEMAND FORECASTING DASHBOARD - OLIST
============================================
8-Page Academic Dashboard for University Presentation
============================================
"""

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Demand Forecasting Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1200px;
    }
    
    .metric-card {
        background-color: #f8f9fa;
        border-left: 4px solid #1E88E5;
        padding: 15px;
        border-radius: 0 8px 8px 0;
        margin: 5px 0;
    }
    
    h1, h2, h3 {
        color: #1a1a2e;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv('demand_features_final.csv')
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

def main():
    # Sidebar
    with st.sidebar:
        st.title("📊 Demand Forecasting")
        st.markdown("**Olist E-commerce Analysis**")
        st.markdown("---")
        
        st.markdown("""
        ### 📖 Dashboard Guide
        
        **8 Pages for Complete Analysis:**
        
        1. 🏠 Data & Business Overview
        2. 👥 Customer & Seller Behavior  
        3. 📦 Price, Logistics & Delivery
        4. 🛠️ Feature Engineering
        5. 🎯 Feature Selection & SHAP
        6. 🏆 Model Comparison
        7. 📈 Time Series Focus
        8. 🌟 Final Insights
        """)
        
        st.markdown("---")
        st.markdown("""
        **🎓 Academic Project**
        
        Demand Forecasting using:
        - XGBoost
        - LightGBM
        - Prophet
        - LSTM
        """)
    
    # Main Content
    st.title("📊 Demand Forecasting Dashboard")
    st.markdown("### Olist E-commerce Platform Analysis")
    st.markdown("---")
    
    # Welcome
    st.markdown("""
    ## 🌟 Welcome to the Demand Forecasting Analysis
    
    This dashboard presents a comprehensive **demand forecasting study** for the Olist e-commerce platform.
    
    ### 🎯 Project Objective
    Build a professional, academically sound demand forecasting model that clearly communicates:
    
    > **Data Cleaning → EDA → Feature Engineering → Feature Selection → Modeling → Explainability**
    """)
    
    # Load data for metrics
    df = load_data()
    
    # Key Metrics
    st.markdown("### 📈 Dataset Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📅 Total Days", len(df))
    with col2:
        st.metric("📦 Total Orders", f"{df['daily_orders'].sum():,.0f}")
    with col3:
        st.metric("📊 Avg Daily Orders", f"{df['daily_orders'].mean():.1f}")
    with col4:
        st.metric("🔢 Total Features", len(df.columns))
    
    st.markdown("---")
    
    # Dashboard overview cards
    st.markdown("### 📊 Dashboard Structure")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
        <h4>🏠 Business Overview</h4>
        <p>Data scope, demand patterns, payment behavior</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
        <h4>🛠️ Feature Engineering</h4>
        <p>Lag features, momentum, regime indicators</p>
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
        <p>Feature importance, model interpretability</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Model Results Summary
    st.markdown("### 🏆 Model Performance Summary")
    
    metrics_df = pd.DataFrame({
        'Model': ['XGBoost', 'LightGBM', 'Prophet', 'LSTM'],
        'RMSE': [32.45, 31.62, 89.23, 45.67],
        'MAE': [27.12, 26.82, 72.45, 38.91],
        'R2': [0.845, 0.853, -0.172, 0.693]
    })
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.dataframe(
            metrics_df.style.format({
                'RMSE': '{:.2f}',
                'MAE': '{:.2f}',
                'R2': '{:.3f}'
            }).highlight_min(subset=['RMSE', 'MAE'], color='lightgreen')
            .highlight_max(subset=['R2'], color='lightgreen'),
            use_container_width=True
        )
    
    with col2:
        st.success("""
        **🏆 Champion Model**
        
        **LightGBM**
        
        - RMSE: 31.62
        - R²: 0.853
        
        *Selected based on lowest RMSE*
        """)
    
    st.markdown("---")
    
    # Navigation hint
    st.info("""
    👉 **Navigate through the pages** using the sidebar menu to explore:
    - Detailed EDA insights
    - Feature engineering rationale
    - Model comparisons
    - SHAP explainability analysis
    """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #888;'>"
        "Demand Forecasting Dashboard | Academic Project | Built with Streamlit"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
