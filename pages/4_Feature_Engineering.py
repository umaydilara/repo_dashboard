import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Feature Engineering", page_icon="⚙️", layout="wide")

st.title("⚙️ Feature Engineering Insights")
st.markdown("---")

@st.cache_data
def load_data():
    df = pd.read_csv('demand_features_final.csv')
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

df = load_data()

# Show all features
st.subheader("📋 Dataset Features Overview")
st.write(f"**Total Features:** {len(df.columns)}")
st.write(f"**Total Records:** {len(df):,}")

# Feature Categories
st.subheader("🏷️ Feature Categories")

# Categorize features
time_features = [col for col in df.columns if any(x in col.lower() for x in ['date', 'day', 'week', 'month', 'year', 'quarter'])]
lag_features = [col for col in df.columns if 'lag' in col.lower()]
rolling_features = [col for col in df.columns if 'rolling' in col.lower() or 'ma' in col.lower()]
other_features = [col for col in df.columns if col not in time_features + lag_features + rolling_features]

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("⏰ Time Features", len(time_features))
with col2:
    st.metric("📊 Lag Features", len(lag_features))
with col3:
    st.metric("📈 Rolling Features", len(rolling_features))
with col4:
    st.metric("📁 Other Features", len(other_features))

# Feature Details in Expanders
with st.expander("⏰ Time-based Features", expanded=True):
    if time_features:
        st.write(", ".join(time_features))
    else:
        st.write("No time features found")

with st.expander("📊 Lag Features"):
    if lag_features:
        st.write(", ".join(lag_features))
    else:
        st.write("No lag features found")

with st.expander("📈 Rolling/Moving Average Features"):
    if rolling_features:
        st.write(", ".join(rolling_features))
    else:
        st.write("No rolling features found")

st.markdown("---")

# Correlation Analysis
st.subheader("🔗 Feature Correlations with Target")
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

if 'daily_orders' in numeric_cols and len(numeric_cols) > 1:
    correlations = df[numeric_cols].corr()['daily_orders'].drop('daily_orders').sort_values(ascending=False)
    
    # Top correlations
    top_n = min(15, len(correlations))
    top_corr = correlations.head(top_n)
    bottom_corr = correlations.tail(top_n)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🔝 Top Positive Correlations**")
        fig_pos = px.bar(x=top_corr.values, y=top_corr.index, orientation='h',
                         title='Top Positive Correlations',
                         labels={'x': 'Correlation', 'y': 'Feature'},
                         color=top_corr.values, color_continuous_scale='Greens')
        fig_pos.update_layout(height=400)
        st.plotly_chart(fig_pos, use_container_width=True)
    
    with col2:
        st.markdown("**🔻 Top Negative Correlations**")
        fig_neg = px.bar(x=bottom_corr.values, y=bottom_corr.index, orientation='h',
                         title='Top Negative Correlations',
                         labels={'x': 'Correlation', 'y': 'Feature'},
                         color=bottom_corr.values, color_continuous_scale='Reds_r')
        fig_neg.update_layout(height=400)
        st.plotly_chart(fig_neg, use_container_width=True)

# Feature Statistics
st.subheader("📊 Feature Statistics")
stats_df = df[numeric_cols].describe().T
stats_df = stats_df.round(2)
st.dataframe(stats_df, use_container_width=True)

# Sample Data
st.subheader("🔍 Sample Data Preview")
st.dataframe(df.head(10), use_container_width=True)

st.markdown("---")
st.info("💡 **Feature Engineering Impact:** Well-crafted features capture temporal patterns, seasonality, and trends that improve model accuracy.")
