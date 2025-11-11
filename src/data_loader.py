import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    """Load and cache the supermarket sales data"""
    df = pd.read_csv('data/supermarket_sales.csv')
    return df

def get_basic_info(df):
    """Get basic dataset information"""
    st.write("### 📈 Dataset Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Records", len(df))
    with col2:
        st.metric("Columns", df.shape[1])
    with col3:
        st.metric("Date Range", f"{df['Date'].min()} to {df['Date'].max()}")