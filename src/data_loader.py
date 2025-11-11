import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    """Load and cache the supermarket sales data"""
    try:
        
        df = pd.read_csv('data/raw/supermarket_sales.csv')
        st.success("✅ Data loaded successfully!")
        return df
    except FileNotFoundError:
        st.error("❌ File not found: data/raw/supermarket_sales.csv")
        st.info("💡 Please make sure your CSV file is in the 'data/raw/' folder")
        return None
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return None

def get_basic_info(df):
    """Get basic dataset information"""
    if df is None:
        st.error("No data available")
        return
    
    st.write("### 📈 Dataset Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Records", len(df))
    with col2:
        st.metric("Columns", df.shape[1])
    with col3:
        
        if 'Date' in df.columns:
            # For now, just show the column exists - we'll format dates in preprocessing
            st.metric("Date Column", "Available")
        else:
            st.metric("Date Column", "Missing")