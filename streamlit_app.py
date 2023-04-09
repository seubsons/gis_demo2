import streamlit as st
import leafmap.foliumap as leafmap
from folium import Icon

import pandas as pd
import requests
import numpy as np
import datetime

api_key = st.secrets["pass"]

# city = 'bangkok'
# url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
# response = requests.get(url.format(city, api_key))
# data = response.json()
#st.write(data)


df2 = pd.read_csv('th.csv')
df3 = df2[0:50]

map_center = (13.25, 101.0)

url2 = "http://api.openweathermap.org/data/2.5/air_pollution?lat={}&lon={}&appid={}"
def getdata(lat, lon):
    response = requests.get(url2.format(lat, lon, api_key))
    if response:
        data = response.json()
        pm2_5 = data['list'][0]['components']['pm2_5']
        
    else:
        pm2_5 = 0.0
        data = 0.0
    return pm2_5, data

df3 = df3.assign(pm2_5=[0] * len(df3))
# c = 0
# pm2_5, data = getdata(df3.loc[c, 'lat'], df3.loc[c, 'lng'])
# df3.loc[c, 'pm2_5'] = pm2_5
for c in np.arange(len(df3)):
    pm2_5, data = getdata(df3.loc[c, 'lat'], df3.loc[c, 'lng'])
    df3.loc[c, 'pm2_5'] = pm2_5
#df3.to_csv('owm_pm2_5.csv', index=False)

timestamp = data['list'][0]['dt']
dt_object = datetime.datetime.fromtimestamp(timestamp)
Date = dt_object.date()
Time = dt_object.time()
Last_Update = f"Last Updated: {Date}, {Time} UTC"
##################################################################
st.set_page_config(layout="wide")

# Customize page title
st.title("GPT OpenWeather leafmap")
#st.write(df3)

# //////////////////////////////////////
st.header("PM2.5")
st.write(Last_Update)

col1, col2 = st.columns(2)
with col1:
    m = leafmap.Map(center=map_center, zoom=6,
                draw_control=False,
                measure_control=False,
               )
    # m.add_heatmap(
    #             df3,
    #             latitude="lat",
    #             longitude="lng",
    #             value="population",
    #             name="Heatmap",
    #             radius=25)
    for i, row in df3.iterrows():
        mag = row['pm2_5']
        lat = row['lat']
        lon = row['lng']
        color = 'purple' if mag > 75 else 'red' if mag > 50 else 'blue' if mag > 25 else 'orange' if mag > 10 else 'green'
        m.add_marker(location=[lat, lon], tooltip=str(mag), icon=Icon(color=color))

    m.to_streamlit(height=700)

# with col2:
#     m = leafmap.Map(center=map_center, zoom=6,
#                 draw_control=False,
#                 measure_control=False,
#                )
#     lat = df3.loc[0, 'lat']
#     lon = df3.loc[0, 'lng']
#     mag = df3.loc[0, 'population']
#     m.add_marker(location=[lat, lon], tooltip=str(mag), icon=Icon(color='red'))
#     # m.add_heatmap(
#     #             df3,
#     #             latitude="lat",
#     #             longitude="lng",
#     #             value="pm2_5",
#     #             name="Heatmap",
#     #             radius=25)
#     m.to_streamlit(height=700)

with col2:
    show_temp = st.beta_expander(label='PM2.5')
    df4 = df3.copy()
    df4['population'] = df4['population'].apply('{:,.0f}'.format)
    df4['pm2_5'] = df4['pm2_5'].apply('{:.2f}'.format)

    with show_temp:
        st.table(df4[['city', 'population', 'pm2_5']])

# //////////////////////////////////////
st.header("Weather")

m = leafmap.Map(center=map_center, zoom=8,
                draw_control=False,
                measure_control=False,
               )

m.add_basemap("HYBRID", show=False)
m.add_basemap("Esri.WorldStreetMap", show=True)

layer = "precipitation_new"
m.add_tile_layer(url=f"http://tile.openweathermap.org/map/{layer}/{{z}}/{{x}}/{{y}}.png?appid={api_key}",
        attribution="OWM",
        name="Precipitation",
                )
layer = "clouds_new"
m.add_tile_layer(url=f"http://tile.openweathermap.org/map/{layer}/{{z}}/{{x}}/{{y}}.png?appid={api_key}",
        attribution="OWM",
        name="Clouds",
        shown=False,
                )
layer = "pressure_new"
m.add_tile_layer(url=f"http://tile.openweathermap.org/map/{layer}/{{z}}/{{x}}/{{y}}.png?appid={api_key}",
        attribution="OWM",
        name="Pressure",
        shown=False,
        opacity=1.0,
                )
layer = "wind_new"
m.add_tile_layer(url=f"http://tile.openweathermap.org/map/{layer}/{{z}}/{{x}}/{{y}}.png?appid={api_key}",
        attribution="OWM",
        name="Wind",
        shown=False,
        opacity=1.0,
                )
layer = "temp_new"
m.add_tile_layer(url=f"http://tile.openweathermap.org/map/{layer}/{{z}}/{{x}}/{{y}}.png?appid={api_key}",
        attribution="OWM",
        name="Tempurature",
        shown=False,
        opacity=1.0,
                )

m.to_streamlit(height=700)


