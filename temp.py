# streamlit run app.py
# localhost:8501

import os
import pytz
import pyowm
import streamlit as st
from matplotlib import dates
from datetime import datetime
from matplotlib import pyplot as plt

# API key
owm=pyowm.OWM(os.environ['openweathermap_apikey'])
mgr=owm.weather_manager()

forecaster = mgr.forecast_at_place("pune", '3h')
cast = forecaster.forecast
mydict = cast.to_dict()
print(cast)
# print(mydict['weathers'])

st.title("5 Day Weather Forecast")
st.write("### Write the name of a City and select the Temperature Unit and Graph Type from the sidebar")

place=st.text_input("NAME OF THE CITY :", (""))

if place == None:
    st.write("Input a CITY!")

unit=st.selectbox("Select Temperature Unit", ("Celsius","Fahrenheit"))

g_type=st.selectbox("Select Graph Type", ("Line Graph","Bar Graph"))

'''
plt.bar(days, temp_min)
plt.bar(days, temp_max)
plt.plot()
''' 