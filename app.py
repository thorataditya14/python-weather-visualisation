# streamlit run app.py
# localhost:8501


import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib
import tkinter
import numpy


import os
api_key = os.environ['openweathermap_apikey']


import streamlit as st
# api_key = st.secrets["API_KEY"]


# from dotenv import load_dotenv
# load_dotenv()
# api_key = os.getenv('API_KEY')


# from boto.s3.connection import S3Connection
# api_key = S3Connection(os.environ['API_KEY'])


matplotlib.use('TkAgg')


def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]


def getcurrloc():
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    return response.get("region")


def getapidata(place):
    api_link = "https://api.openweathermap.org/data/2.5/forecast?q=" + place + "&appid=" + api_key
    api_data = requests.get(api_link)
    data = api_data.json()
    return data


def getfivedays():
    days = []
    a = datetime.today()
    for x in range (0, 5):
        days.append(str((a + timedelta(days = x)).strftime("%d %b %Y")))
    return days


def linegraph(place, days, temp_min, temp_max):
    plt.plot(days, temp_min, linewidth=2)
    plt.plot(days, temp_max, linewidth=2)
    plt.title(place)
    plt.show()


def bargraph(dayst, place, days, temp_min, temp_max):
    width = 0.3
    plt.bar(dayst, temp_min, width, label='Min Temp')
    plt.bar(dayst + width, temp_max, width, label='Max Temp')
    plt.xticks(dayst + width / 2, days)
    plt.legend(loc='best')
    plt.title(place)
    plt.show()


def main():
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
            dayst.append(int(i/8))

        days = getfivedays()

        dayst = numpy.array(dayst)

        if(g_type == "Line Graph"):
            linegraph(place, days, temp_min, temp_max)
        elif(g_type == "Bar Graph"):
            bargraph(dayst, place, days, temp_min, temp_max)
        
    else:
        print(data['message'])

if __name__ == "__main__":
    main()