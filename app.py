# streamlit run app.py
# localhost:8501

import os
import requests
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import matplotlib
import tkinter
import numpy


matplotlib.use('TkAgg')


def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]


def getcurrloc():
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    return response.get("region")


def getapidata(place):
    api_link = "https://api.openweathermap.org/data/2.5/forecast?q=" + place + "&appid=" + os.getenv('api_key')
    api_data = requests.get(api_link)
    data = api_data.json()
    return data


def getfivedays():
    days = {}
    a = datetime.today()
    for x in range (0, 5):
        days[x] =  str((a + timedelta(days = x)).strftime("%d %b %Y"))
    return days


def linegraph(place, days, temp_min, temp_max):
    plt.plot(days.values(), temp_min, linewidth=2)
    plt.plot(days.values(), temp_max, linewidth=2)
    plt.title(place)
    plt.show()


def bargraph(place, days, temp_min, temp_max):
    width = 2
    dayst = days.keys()
    plt.bar(dayst, temp_min, width, label='Min Temp')
    plt.bar(dayst + width, temp_max, width, label='Max Temp')
    plt.xticks(dayst + width / 2, days.values())
    plt.legend(loc='best')
    plt.title(place)
    plt.show()


def main():
    load_dotenv()

    st.title("5 Day Weather Forecast")
    st.write("### Enter Location name and select Graph type from dropdown")
    place=st.text_input("Type city name here:", getcurrloc())
    g_type = st.selectbox("Choose graph type", ("Line Graph", "Bar Graph"))

    data = getapidata(place)

    if(data['cod'] == '200'):
        temp_min = []
        temp_max = []
        dayst = []

        for i in range(0, data['cnt'], 8):
            temp_min.append(data['list'][i+5]['main']['temp_min'] - 273.17)
            temp_max.append(data['list'][i+1]['main']['temp_max'] - 273.17)
            dayst.append(i)

        days = getfivedays()

        if(g_type == "Line Graph"):
            linegraph(place, days, temp_min, temp_max)
        elif(g_type == "Bar Graph"):
            bargraph(place, days, temp_min, temp_max)
        
    else:
        print(data['message'])

if __name__ == "__main__":
    main()