#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
from dateutil.relativedelta import relativedelta
import plotly.graph_objs as go
import datetime
import pandas as pd
import numpy as np
from flask import Flask
import requests
from geopy.geocoders import Nominatim
import time

# Get data
#confirm = pd.read_csv('data/confirm.csv')
#recover = pd.read_csv('data/recover.csv')
#death = pd.read_csv('data/death.csv')

confirm = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
recover = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
death = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

# ***********************************************************************************
# Define functions

def getLatest(df):
    """
    This get the data of the last day from the dataframe and append it to the details
    """
    df_info = df.iloc[:,0:5]
    df_last = df.iloc[:,-1]
    df_info['latest'] = df_last
    
    return df_info

def display_ip():
    """
    Function To Print GeoIP Latitude & Longitude
    """
    ip_request = requests.get('https://get.geojs.io/v1/ip.json')
    my_ip = ip_request.json()['ip']
    geo_request = requests.get('https://get.geojs.io/v1/ip/geo/' +my_ip + '.json')
    geo_data = geo_request.json()
    print({'latitude': geo_data['latitude'], 'longitude': geo_data['longitude']})

def mergeData(x,recover,death):
    """
    Function that merge the confirm, recover and death to one dataframe
    """
    x = x.rename(columns = {'latest':'confirm'})
    x['recover'] = recover['latest']
    x['death'] = death['latest']

    return x


# ***********************************************************************************
# Get latest data
get_confirm = getLatest(confirm)
get_recover = getLatest(recover)
get_death = getLatest(death)

# Sending data to view


line = go.Figure()
#***************************************************************************
# Graph
confirm_line_data = confirm.iloc[:,5:].sum()
recover_line_data = recover.iloc[:,5:].sum()
death_line_data = death.iloc[:,5:].sum()




#****************************************************************************
# Merged data
get_merged = mergeData(get_confirm, get_recover, get_death)

limits = [(1,10), (10,100), (100,1000), (1000,10000), (10000,1000000000)]
size = [5, 10, 15, 20, 30]

fig = go.Figure()

for i in range(len(limits)):
    lim = limits[i]
    get_confirm_range = get_merged[get_merged['confirm']>=lim[0]]
    get_confirm_range = get_confirm_range[get_confirm_range['confirm']<lim[1]]

    customdata=np.dstack((get_confirm_range['confirm'], get_confirm_range['recover']))

    figMap = fig.add_trace(
            go.Scattergeo(
            lon = get_confirm_range['Long'],
            lat = get_confirm_range['Lat'],
            text = get_confirm_range['Country/Region'],
            mode = 'markers',
            showlegend=False,
            marker = dict(
                size = size[i],
                color = 'rgba(255, 103, 0,0.5)',
                sizemode = 'area'
            ),
            customdata=get_confirm_range['confirm'], ano = get_confirm_range['recover']
            # hovertext=[get_confirm_range['Country/Region'],get_confirm_range['confirm'],get_confirm_range['recover'],get_confirm_range['death']]
            hovertemplate = "<b>%{text}</b>,<br>Confirm:%{customdata}<extra></extra><br>",
            # # trace=off
            # hoverinfo='text'
        ),
    )
figMap.update_layout(
    autosize=True,
    margin={
        "r":0,
        "t":0,
        "l":0,
        "b":0,
    },
    height=330,
    # width=700,
    geo = go.layout.Geo(
        resolution = 50,
        showframe = False,
        showcoastlines = True,
        showcountries = True,
        landcolor = "rgb(229, 229, 229)",
        countrycolor = "white" ,
        projection = dict(scale=1.8),
        coastlinecolor = "white",
        center= dict(
            lat= 8.7832,
            lon= 20.5085,
        )
    ),
    # legend_traceorder = 'reversed'
)


# In[ ]:




