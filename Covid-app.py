#Covid-19 Trends.py

""" A simple streamlit app
    Data Source: from COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University
    run the app by installing streamlit with pip and typing
    >streamlit run Covid-app.py
"""

#import libraries
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

import plotly as py
import plotly.express as px
import plotly.graph_objs as go 
from plotly.subplots import make_subplots
from plotly.offline import download_plotlyjs,init_notebook_mode,plot, iplot
init_notebook_mode(connected=True)



#Collect data 
confirmed_global_data = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
deaths_global_data='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
recovered_global_data='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

#Read data
confirmed_global_df = pd.read_csv(confirmed_global_data)
deaths_global_df = pd.read_csv(deaths_global_data)
recovered_global_df = pd.read_csv(recovered_global_data)

#--------------------------------------------------------------------------- Confirmed global data  --------------------------------------------------------------------"""
#prepare confirmed cases data
confirmed_cases_df=pd.melt(confirmed_global_df,id_vars=['Province/State','Country/Region','Lat','Long'], var_name='Date',value_name='Cases')
#format date
confirmed_cases_df['Date'] = pd.to_datetime(confirmed_cases_df['Date'], format='%m/%d/%y')
#filter data to today's date
recent_date = confirmed_cases_df['Date'].max()
confirmed_cases_df=confirmed_cases_df[confirmed_cases_df['Date'].isin([recent_date])]

#Total number of cases
total_confirmed=confirmed_cases_df['Cases'].sum()
total_confirmed='{:,}'.format(total_confirmed)
#Total by country
confirmed_Country=confirmed_cases_df.groupby(['Country/Region']).sum().reset_index()
confirmed_Country=confirmed_Country.sort_values(by=['Cases'], ascending=False)
confirmed_Country['Cases '] = confirmed_Country['Cases'].map('{:,}'.format)
confirmed_Country.drop(columns=['Lat', 'Long','Cases'], inplace=True)

#--------------------------------------------------------------------------- Deaths global data  --------------------------------------------------------------------"""

#--------------------------------------------------------------------------- Recovered global data  --------------------------------------------------------------------"""

#--------------------------------------------------------------------------- Create a Streamlit App  --------------------------------------------------------------------"""
#Create A title for the App
st.sidebar.title('Covid-19 Dashboard')
st.title('Covid-19 Dashboard')

#Summary data ( side bar)
st.sidebar.header("Total Confirmed Cases :")
st.sidebar.markdown(total_confirmed)

st.sidebar.header("Confirmed Cases by Country :")
st.sidebar.dataframe(confirmed_Country.head())

#Select whole list of hotels
if st.sidebar.checkbox ('Click to Show Full list of countries'):
    st.subheader("Confirmed Cases by Country ")
    st.write(confirmed_Country)
    #st.dataframe(map_data.style.highlight_max(axis=0))  , i need to look at this
    st.subheader("Top 15 - Confirmed Cases by Country ")
    st.line_chart(confirmed_Country.head(15))

#Select Country to check the cases
option=st.sidebar.selectbox(
    'Select Country :',
    confirmed_global_df['Country/Region'])

'Selected Country : ',option

line_df=pd.melt(confirmed_global_df,id_vars=['Province/State','Country/Region','Lat','Long'], var_name='Date',value_name='Cases')
line_df=line_df[line_df['Country/Region'].isin([option])]
line_df.drop(columns=['Province/State','Date','Lat','Long','Country/Region'], inplace=True)
st.line_chart(line_df)

#Draw a map
st.header("Map Overview")
map_data=confirmed_global_df.copy()
map_data=map_data.rename(columns={"Lat": "lat", "Long": "lon"})
st.map(map_data)

#Draw a map2 doesnt work
global_map_data=confirmed_cases_df.copy()
global_map_data=global_map_data.groupby(['Country/Region']).sum().reset_index()
global_map_data=global_map_data.query("Cases >=1000")
global_map_data=global_map_data.rename(columns={"Lat": "lat", "Long": "lon"})
st.map(global_map_data)

#plotly graph
#Manipulating the data
static_Chor_map_data=confirmed_global_df.copy()
static_Chor_map_data=pd.melt(static_Chor_map_data,id_vars=['Province/State','Country/Region','Lat','Long'], var_name='Date',value_name='Cases')
static_Chor_map_data['Date'] = pd.to_datetime(static_Chor_map_data['Date'], format='%m/%d/%y')
recent_date = static_Chor_map_data['Date'].max()
static_Chor_map_data=static_Chor_map_data[static_Chor_map_data['Date'].isin([recent_date])]
static_Chor_map_data=static_Chor_map_data.groupby(['Country/Region','Date']).sum().reset_index()
static_Chor_map_data=static_Chor_map_data.query("Cases >0")

#Create the Choropleth
fig=go.Figure(data=go.Choropleth(
                                  locations=static_Chor_map_data['Country/Region'],
                                  locationmode='country names',
                                  z=static_Chor_map_data['Cases'],
                                  colorscale='Reds',
                                  marker_line_color='black',
                                  marker_line_width=0.5,
                                ))

fig.update_layout(
                  title_text='Confirmed Cases as of May 15,2020',
                  title_x=0.5,
                  geo=dict(
                           showframe=False,
                           projection_type='equirectangular'
                          )
                 )

st.plotly_chart(fig,use_container_width=True)



#Animated Choropleth Map
#Manipulating the original data
Chor_map_data=confirmed_global_df.copy()
Chor_map_data=pd.melt(Chor_map_data,id_vars=['Province/State','Country/Region','Lat','Long'], var_name='Date',value_name='Cases')
Chor_map_data['Date'] = pd.to_datetime(Chor_map_data['Date'], format='%m/%d/%y')
Chor_map_data=Chor_map_data.query("Cases >0")
Chor_map_data=Chor_map_data.groupby(['Country/Region','Date']).sum().reset_index()
Chor_map_data['Date'] = Chor_map_data.Date.apply(lambda x: x.date()).apply(str)

#Creating the visualisation
fig=px.choropleth(Chor_map_data,
                  locations="Country/Region",
                  locationmode="country names",
                  color='Cases',
                  hover_name="Country/Region",
                  animation_frame='Date'
                 )

fig.update_layout(
                  title_text='Global Spread of Coronavirus',
                  title_x=0.5,
                  geo=dict(
                          showframe=False,
                          showcoastlines=False
                          )
                )

fig.show()        

st.plotly_chart(fig)


#Pie Chart-Proportion of Confirmed Cases by Country
fig=px.pie(static_Chor_map_data, values='Cases', names='Country/Region', height=600)
fig.update_traces(textposition='inside', textinfo='percent + label')

fig.update_layout(
                   title_x=0.5,
                   geo=dict(
                             showframe=False,
                             showcoastlines=False,
                           )
                 )
fig.show()
st.plotly_chart(fig)


#Bar Chart-Total number of confirmed cases over time
bar_data=Chor_map_data.copy()
fig=px.bar(bar_data,x="Date",y="Cases",color='Country/Region',text='Cases',orientation='v',height=600,title='Confirmed Cases')

fig.show()
st.plotly_chart(fig)

#Number of Countries
num_countries=confirmed_Country['Country/Region'].nunique()
st.sidebar.subheader("Number of Countries/ Regions :")
st.sidebar.markdown(num_countries)

#Update time
now=datetime.now()
dt_string=now.strftime(("%d/%m/%Y %H:%M:%S"))
st.sidebar.subheader("Last updated at(M/D/YYYY)")
st.sidebar.markdown(dt_string)
