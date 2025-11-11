import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime

def preprocess_data(df):
    """
    Clean and transform the raw supermarket data
    Returns a cleaned dataframe ready for analysis
    """
    # Create a copy to avoid modifying the original data
    df_clean = df.copy()
    
    st.info("🔄 Starting data preprocessing...")
    
    # 1. FIX DATE AND TIME COLUMNS
    with st.expander("📅 Date/Time Processing"):
        try:
            # Convert Date column (format: MM/DD/YYYY)
            df_clean['Date'] = pd.to_datetime(df_clean['Date'], format='%m/%d/%Y')
            
            # Convert Time column (format: HH:MM)
            df_clean['Time'] = pd.to_datetime(df_clean['Time'], format='%H:%M').dt.time
            
            # Create datetime combination for time series analysis
            df_clean['DateTime'] = pd.to_datetime(
                df_clean['Date'].astype(str) + ' ' + df_clean['Time'].astype(str)
            )
            
            st.write("✅ Date/Time columns converted successfully")
            
        except Exception as e:
            st.error(f"❌ Error processing date/time: {e}")
    
    # 2. EXTRACT TIME-BASED FEATURES
    with st.expander("⏰ Feature Engineering"):
        # Time features
        df_clean['Month'] = df_clean['Date'].dt.month_name()
        df_clean['MonthNumber'] = df_clean['Date'].dt.month
        df_clean['DayOfWeek'] = df_clean['Date'].dt.day_name()
        df_clean['DayNumber'] = df_clean['Date'].dt.dayofweek
        df_clean['Hour'] = pd.to_datetime(df_clean['Time'], format='%H:%M:%S').dt.hour
        
        # Time of day categories
        df_clean['TimeOfDay'] = pd.cut(
            df_clean['Hour'],
            bins=[0, 12, 17, 24],
            labels=['Morning', 'Afternoon', 'Evening'],
            include_lowest=True
        )
        
        st.write("✅ Time-based features created")
    
    # 3. CREATE REVENUE SEGMENTS
    with st.expander("💰 Revenue Segmentation"):
        # Create revenue segments
        df_clean['Revenue_Segment'] = pd.cut(
            df_clean['Total'],
            bins=[0, 100, 300, 500, float('inf')],
            labels=['Small ($0-100)', 'Medium ($100-300)', 'Large ($300-500)', 'Very Large ($500+)']
        )
        
        # Calculate transaction size
        df_clean['Transaction_Size'] = df_clean['Unit price'] * df_clean['Quantity']
        
        st.write("✅ Revenue segments created")
    
    # 4. ENHANCE CUSTOMER ANALYSIS
    with st.expander("👥 Customer Analysis Features"):
        # Create customer segments based on spending
        customer_spending = df_clean.groupby('Customer_type')['Total'].mean().to_dict()
        df_clean['Avg_CustomerType_Spending'] = df_clean['Customer_type'].map(customer_spending)
        
        st.write("✅ Customer analysis features added")
    
    # 5. DATA VALIDATION CHECKS
    with st.expander("🔍 Data Quality Check"):
        # Check for any remaining issues
        initial_rows = len(df)
        final_rows = len(df_clean)
        
        st.write(f"• Records processed: {final_rows:,} (no data loss)")
        st.write(f"• New columns created: {len(df_clean.columns) - len(df.columns)}")
        st.write(f"• Date range: {df_clean['Date'].min().strftime('%b %d, %Y')} to {df_clean['Date'].max().strftime('%b %d, %Y')}")
        st.write(f"• Cities: {', '.join(df_clean['City'].unique())}")
        st.write(f"• Product lines: {len(df_clean['Product line'].unique())} categories")
    
    st.success("🎉 Data preprocessing completed successfully!")
    return df_clean

def get_data_summary(df):
    """
    Generate a comprehensive summary of the dataset
    """
    summary = {
        'basic_info': {
            'total_records': len(df),
            'total_columns': df.shape[1],
            'date_range': f"{df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}",
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2
        },
        'revenue_metrics': {
            'total_revenue': df['Total'].sum(),
            'average_transaction': df['Total'].mean(),
            'max_transaction': df['Total'].max(),
            'min_transaction': df['Total'].min()
        },
        'customer_metrics': {
            'total_customers': df['Customer_type'].count(),
            'member_percentage': (df['Customer_type'] == 'Member').mean() * 100,
            'gender_distribution': df['Gender'].value_counts().to_dict()
        },
        'product_metrics': {
            'unique_products': df['Product line'].nunique(),
            'top_product': df['Product line'].value_counts().index[0],
            'total_quantity': df['Quantity'].sum()
        }
    }
    
    return summary