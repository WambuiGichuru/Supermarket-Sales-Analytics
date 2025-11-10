
def preprocess_data(): 
    """ Cleaning anf Preprocessing the dataset"""
    # creating a copy to avoid modifying cached data
    df_clean = df.copy()

    #conversion of date and time
    df_clean['Date']= pd.to_datetime(df_clean['Date'], format='%m%d%Y')
    df_clean['Time']=pd.to_datetime(df_clean['Time'], format='%H:%M').dt.time

    df_clean['DateTime']=pd.to_datetime(df_clean['Date'].astype(str)+''+ df_clean['Time'].astype(str))

    # extracting time based features
    df_clean['Month']=df_clean['Date'].dt.month_name()
    df_clean['DayOfWeek']=df_clean['Date'].dt.day_name()
    df_clean['Hour']= pd.to_datetime(df_clean['Time'], format='%H:%M:%S').dt.hour

    #create revenue segments
    df_clean['Revenue_Segment']= pd.cut(
                df_clean['Total'],
                bins=[0,200,500,1000, float('inf')],
                labels=['Low','Medium','High','Very High']
                                        )
    return df_clean