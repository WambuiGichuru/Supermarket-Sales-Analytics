import streamlit as st
import pandas as pd
from src.data_loader import load_raw_data, preprocess_data
from src.eda_analysis import EDAAnalysis
from src.visualization import create_visualizations

# Page configuration
st.set_page_config(
    page_title="Supermarket Sales Analytics",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🏪 Supermarket Sales Analytics Dashboard")
    st.markdown("Interactive analysis of supermarket sales data")
    
    # Load data
    with st.spinner('Loading data...'):
        raw_df = load_raw_data()
        if raw_df is not None:
            df = preprocess_data(raw_df)
            st.success(f'✅ Loaded {len(df)} records')
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # City filter
    cities = ['All'] + list(df['City'].unique())
    selected_city = st.sidebar.selectbox('Select City', cities)
    
    # Product line filter
    product_lines = ['All'] + list(df['Product line'].unique())
    selected_product = st.sidebar.selectbox('Select Product Line', product_lines)
    
    # Date range filter
    min_date = df['Date'].min()
    max_date = df['Date'].max()
    date_range = st.sidebar.date_input(
        "Select Date Range",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    
    # Apply filters
    filtered_df = apply_filters(df, selected_city, selected_product, date_range)
    
    # Main dashboard
    display_dashboard(filtered_df)

def apply_filters(df, city, product, date_range):
    """Apply user filters to dataframe"""
    filtered_df = df.copy()
    
    if city != 'All':
        filtered_df = filtered_df[filtered_df['City'] == city]
    
    if product != 'All':
        filtered_df = filtered_df[filtered_df['Product line'] == product]
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df['Date'] >= pd.to_datetime(start_date)) & 
            (filtered_df['Date'] <= pd.to_datetime(end_date))
        ]
    
    return filtered_df

def display_dashboard(df):
    """Display the main dashboard"""
    
    # KPI Cards
    st.subheader("📈 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = df['Total'].sum()
        st.metric("Total Revenue", f"${total_revenue:,.2f}")
    
    with col2:
        avg_transaction = df['Total'].mean()
        st.metric("Avg Transaction", f"${avg_transaction:.2f}")
    
    with col3:
        total_customers = df['Customer_type'].count()
        st.metric("Total Transactions", f"{total_customers:,}")
    
    with col4:
        avg_rating = df['Rating'].mean()
        st.metric("Avg Rating", f"{avg_rating:.2f}/10")
    
    # Visualizations
    create_visualizations(df)
    
    # EDA Section
    st.subheader("🔍 Exploratory Data Analysis")
    eda = EDAAnalysis(df)
    
    # Variate Analysis Selection
    analysis_type = st.selectbox(
        "Select Analysis Type",
        ["Univariate", "Bivariate", "Multivariate"]
    )
    
    if analysis_type == "Univariate":
        column = st.selectbox("Select Variable", df.select_dtypes(include=[np.number]).columns)
        eda.univariate_analysis(column)
    
    elif analysis_type == "Bivariate":
        col1, col2 = st.columns(2)
        with col1:
            var1 = st.selectbox("Variable 1", df.select_dtypes(include=[np.number]).columns)
        with col2:
            var2 = st.selectbox("Variable 2", df.select_dtypes(include=[np.number]).columns)
        eda.bivariate_analysis(var1, var2)
    
    else:
        eda.multivariate_analysis()

if __name__ == "__main__":
    main()