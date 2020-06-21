#Covid-19 Trends

""" Data from COVID-19 Data Repository by the Center for Systems Science and 
    Engineering (CSSE) at Johns Hopkins University"""

#import libaries
import streamlit as st
import pandas as pd
import numpy as np



#Get data from Data Source
confirmed_global_data = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
deaths_global_data='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
recovered_global_data='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

#Read data
confirmed_global_df = pd.read_csv(confirmed_global_data)
deaths_global_data_df = pd.read_csv(deaths_global_data)
recovered_global_data_df = pd.read_csv(recovered_global_data)

#Write to Streamlit
if st.checkbox ('Show dataframe'):
    st.write(confirmed_global_df)

option=st.selectbox(
    'Select Country',
    confirmed_global_df['Country/Region'])
    
'You Selected: ', option
