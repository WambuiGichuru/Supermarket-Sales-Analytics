import pandas as pd
import numpy as np
from scipy import stats
import streamlit as st

class EDAAnalysis:
    def __init__(self, df):
        self.df = df
    
    def univariate_analysis(self, column):
        """Univariate analysis for a single variable"""
        if self.df is None or len(self.df) == 0:
            st.error("No data available for analysis")
            return
            
        if column not in self.df.columns:
            st.error(f"Column '{column}' not found in dataset")
            return
            
        st.write(f"### 📊 Univariate Analysis: {column}")
        
        if self.df[column].dtype in ['float64', 'int64']:
            # Numerical analysis
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                # FIXED: Only show $ for likely currency columns
                if column in ['Total', 'Unit price', 'Tax 5%', 'cogs', 'gross income']:
                    st.metric("Mean", f"${self.df[column].mean():.2f}")
                else:
                    st.metric("Mean", f"{self.df[column].mean():.2f}")
            with col2:
                if column in ['Total', 'Unit price', 'Tax 5%', 'cogs', 'gross income']:
                    st.metric("Median", f"${self.df[column].median():.2f}")
                else:
                    st.metric("Median", f"{self.df[column].median():.2f}")
            with col3:
                st.metric("Std Dev", f"{self.df[column].std():.2f}")
            with col4:
                st.metric("Skewness", f"{self.df[column].skew():.2f}")
        else:
            # Categorical analysis
            value_counts = self.df[column].value_counts()
            st.write("Value Counts:", value_counts)
    
    def bivariate_analysis(self, col1, col2):
        """Bivariate analysis between two variables"""
        if self.df is None or len(self.df) == 0:
            st.error("No data available for analysis")
            return
            
        # Check if columns exist
        missing_cols = [col for col in [col1, col2] if col not in self.df.columns]
        if missing_cols:
            st.error(f"Columns not found: {missing_cols}")
            return
            
        st.write(f"### 🔗 Bivariate Analysis: {col1} vs {col2}")
        
        # Check if both are numerical
        if (self.df[col1].dtype in ['float64', 'int64'] and 
            self.df[col2].dtype in ['float64', 'int64']):
            
            correlation = self.df[col1].corr(self.df[col2])
            st.metric("Correlation Coefficient", f"{correlation:.3f}")
            
            # Interpretation
            if abs(correlation) > 0.7:
                st.info("💡 **Strong correlation** between variables")
            elif abs(correlation) > 0.3:
                st.info("💡 **Moderate correlation** between variables")
            else:
                st.info("💡 **Weak correlation** between variables")
        else:
            st.info("🔍 At least one variable is categorical - try numerical columns for correlation analysis")
    
    def multivariate_analysis(self):
        """Multivariate analysis for key business insights"""
        if self.df is None or len(self.df) == 0:
            st.error("No data available for analysis")
            return
            
        st.write("### 🎯 Multivariate Business Insights")
        
        # Check if required columns exist
        required_cols = ['City', 'Product line', 'Total', 'Customer_type']
        missing_cols = [col for col in required_cols if col not in self.df.columns]
        
        if missing_cols:
            st.error(f"Missing columns for multivariate analysis: {missing_cols}")
            return
        
        # Insight 1: Revenue by City and Product Line
        try:
            insight1 = self.df.groupby(['City', 'Product line'])['Total'].agg(['sum', 'mean']).round(2)
            st.write("**Revenue by City and Product Line:**")
            st.dataframe(insight1)
        except Exception as e:
            st.error(f"Error in revenue analysis: {e}")
        
        # Insight 2: Customer Type behavior across cities
        try:
            insight2 = pd.crosstab(
                self.df['City'], 
                self.df['Customer_type'], 
                values=self.df['Total'], 
                aggfunc='mean'
            ).round(2)
            st.write("**Average Spending by City and Customer Type:**")
            st.dataframe(insight2)
        except Exception as e:
            st.error(f"Error in customer analysis: {e}")