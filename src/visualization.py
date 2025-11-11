import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def create_visualizations(df):
    """Create interactive visualizations"""
    
    # Revenue by City
    fig1 = px.bar(
        df.groupby('City')['Total'].sum().reset_index(),
        x='City',
        y='Total',
        title='Total Revenue by City',
        color='City'
    )
    
    # Product Line Performance
    product_sales = df.groupby('Product line').agg({
        'Total': 'sum',
        'Quantity': 'sum',
        'Rating': 'mean'
    }).reset_index()
    
    fig2 = px.scatter(
        product_sales,
        x='Quantity',
        y='Total',
        size='Rating',
        color='Product line',
        title='Product Line Performance: Quantity vs Revenue vs Rating',
        hover_data=['Product line']
    )
    
    # Display charts
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.plotly_chart(fig2, use_container_width=True)
    
    # Time-based analysis
    st.subheader("📅 Temporal Analysis")
    
    # Daily revenue trend
    daily_revenue = df.groupby('Date')['Total'].sum().reset_index()
    fig3 = px.line(
        daily_revenue,
        x='Date',
        y='Total',
        title='Daily Revenue Trend'
    )
    st.plotly_chart(fig3, use_container_width=True)