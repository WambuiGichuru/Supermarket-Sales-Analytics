import pandas as pd
import streamlit as st
from datetime import datetime

@st.cache_data
def load_raw_data():
    ''' Loading and caching the supermarket sales data'''
    try:
        df= pd.read_csv('data/raw/supermarkets_sales.csv')
        return df
    except FileNotFoundError:
        st.error(" !! Data File not found. Please check the filepath")
        return None
