import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def create_visualizations(df):
    """Create interactive visualizations with error handling"""
    
    # Validate input data
    if df is None or len(df) == 0:
        st.error("📊 No data available for visualization")
        return
    
    st.subheader("📊 Data Visualizations")
    
    # Check required columns for visualizations
    required_cols = ['City', 'Total', 'Product line', 'Quantity', 'Date']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        st.error(f"❌ Missing columns for visualizations: {missing_cols}")
        return
    
    try:
        # Revenue by City
        with st.expander("🏙️ Revenue by City", expanded=True):
            try:
                city_revenue = df.groupby('City')['Total'].sum().reset_index()
                if len(city_revenue) > 0:
                    fig1 = px.bar(
                        city_revenue,
                        x='City',
                        y='Total',
                        title='Total Revenue by City',
                        color='City',
                        labels={'Total': 'Revenue ($)', 'City': 'City'}
                    )
                    st.plotly_chart(fig1, use_container_width=True)
                else:
                    st.info("No city revenue data to display")
            except Exception as e:
                st.error(f"❌ Error creating city revenue chart: {e}")
        
        # Product Line Performance
        with st.expander("📦 Product Line Performance", expanded=True):
            try:
                product_sales = df.groupby('Product line').agg({
                    'Total': 'sum',
                    'Quantity': 'sum',
                    'Rating': 'mean' if 'Rating' in df.columns else None
                }).reset_index()
                
                # Remove Rating if not available
                if 'Rating' not in df.columns:
                    product_sales['Rating'] = 1  # Default size
                
                if len(product_sales) > 0:
                    fig2 = px.scatter(
                        product_sales,
                        x='Quantity',
                        y='Total',
                        size='Rating',
                        color='Product line',
                        title='Product Line Performance: Quantity vs Revenue',
                        hover_data=['Product line'],
                        labels={'Total': 'Total Revenue ($)', 'Quantity': 'Quantity Sold'}
                    )
                    st.plotly_chart(fig2, use_container_width=True)
                else:
                    st.info("No product line data to display")
            except Exception as e:
                st.error(f"❌ Error creating product performance chart: {e}")
        
        # Time-based analysis
        with st.expander("📅 Temporal Analysis", expanded=True):
            try:
                # Daily revenue trend
                daily_revenue = df.groupby('Date')['Total'].sum().reset_index()
                if len(daily_revenue) > 0:
                    fig3 = px.line(
                        daily_revenue,
                        x='Date',
                        y='Total',
                        title='Daily Revenue Trend',
                        labels={'Total': 'Revenue ($)', 'Date': 'Date'}
                    )
                    st.plotly_chart(fig3, use_container_width=True)
                else:
                    st.info("No daily revenue data to display")
            except Exception as e:
                st.error(f"❌ Error creating daily revenue chart: {e}")
        
        # Additional visualizations if we have the data
        if 'Gender' in df.columns and 'Customer_type' in df.columns:
            with st.expander("👥 Customer Demographics", expanded=False):
                try:
                    # Customer type distribution
                    customer_dist = df['Customer_type'].value_counts().reset_index()
                    customer_dist.columns = ['Customer Type', 'Count']
                    
                    fig4 = px.pie(
                        customer_dist,
                        values='Count',
                        names='Customer Type',
                        title='Customer Type Distribution'
                    )
                    st.plotly_chart(fig4, use_container_width=True)
                except Exception as e:
                    st.error(f"❌ Error creating customer demographics chart: {e}")
    
    except Exception as e:
        st.error(f"❌ Unexpected error in visualization module: {e}")

def create_simple_visualization(df, chart_type, x_col, y_col, title):
    """Create a simple visualization with error handling"""
    try:
        if chart_type == 'bar':
            fig = px.bar(df, x=x_col, y=y_col, title=title)
        elif chart_type == 'line':
            fig = px.line(df, x=x_col, y=y_col, title=title)
        elif chart_type == 'scatter':
            fig = px.scatter(df, x=x_col, y=y_col, title=title)
        else:
            st.error(f"Unsupported chart type: {chart_type}")
            return None
        
        return fig
    except Exception as e:
        st.error(f"Error creating {chart_type} chart: {e}")
        return None