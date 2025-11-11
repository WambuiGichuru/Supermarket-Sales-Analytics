import pandas as pd
import numpy as np
from scipy import stats
import streamlit as st

class EDAAnalysis:
    def __init__(self, df):
        self.df = df
    
    def univariate_analysis(self, column):
        """Univariate analysis for a single variable"""
        st.write(f"### 📊 Univariate Analysis: {column}")
        
        if self.df[column].dtype in ['float64', 'int64']:
            # Numerical analysis
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Mean", f"${self.df[column].mean():.2f}")
            with col2:
                st.metric("Median", f"${self.df[column].median():.2f}")
            with col3:
                st.metric("Std Dev", f"${self.df[column].std():.2f}")
            with col4:
                st.metric("Skewness", f"{self.df[column].skew():.2f}")
        else:
            # Categorical analysis
            value_counts = self.df[column].value_counts()
            st.write("Value Counts:", value_counts)
    
    def bivariate_analysis(self, col1, col2):
        """Bivariate analysis between two variables"""
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
    
    def multivariate_analysis(self):
        """Multivariate analysis for key business insights"""
        st.write("### 🎯 Multivariate Business Insights")
        
        # Insight 1: Revenue by City and Product Line
        insight1 = self.df.groupby(['City', 'Product line'])['Total'].agg(['sum', 'mean']).round(2)
        st.write("**Revenue by City and Product Line:**", insight1)
        
        # Insight 2: Customer Type behavior across cities
        insight2 = pd.crosstab(
            self.df['City'], 
            self.df['Customer_type'], 
            values=self.df['Total'], 
            aggfunc='mean'
        ).round(2)
        st.write("**Average Spending by City and Customer Type:**", insight2)