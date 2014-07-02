from django.http import HttpResponse
from django.shortcuts import render
import smtplib, os
import time
import re
import urllib2
import json
from datetime import *

day_hours = [7,8,9,18,19,20]
evening_hours = [18,19,20]
comfortable_temp = 14
comfortable_rain = 0.25

def get_json(url):
    json_text = urllib2.urlopen(url).read()
    return json_text

def get_weather_forecast(json_text,current_date):
    # print current_date
    # fill in default weather forecast
    day_forecast = []
    for h in range(0,24):
        day_forecast.append({"temp":0,"rain":0})
    
    # load weather from json 
    weather_json = json.loads(json_text)

    # fill in actual weather forecast
    for i in range(len(weather_json['list'])):
        date_value = datetime.strptime(weather_json['list'][i]['dt_txt'], "%Y-%m-%d %H:%M:%S")
        if date_value.date() == current_date:
            hour = date_value.hour
            try:
                rain = weather_json['list'][i]['rain']
            except:
                rain = 0
            temp = weather_json['list'][i]['main']['temp']
            day_forecast[hour] = {"temp":temp,"rain":rain}
            if hour < 23:
                day_forecast[hour+1] = day_forecast[hour]
                day_forecast[hour+2] = day_forecast[hour]
    return day_forecast

def is_good_to_ride(weather_forecast,ride_hours,allowed_temp,allowed_rain):
    good_to_ride = 0
    average_temp = 0.
    average_rain = 0.
    for i in ride_hours:
        try:
            average_temp = average_temp + weather_forecast[i]["temp"]
            average_rain = average_rain + weather_forecast[i]["rain"]["3h"]
        except:
            average_rain = average_rain
        # debug
        # print weather_forecast[i]["temp"]
    average_temp = average_temp / len(ride_hours)
    #print average_rain
    #print average_temp
    if (average_temp >=allowed_temp) and (average_rain <= allowed_rain):
        good_to_ride = 1
    return good_to_ride


def index(request):
    url = "http://api.openweathermap.org/data/2.5/forecast?q=Minsk&units=metric"
    forecast = get_weather_forecast(get_json(url),date.today() + timedelta(days = 1))
    good_to_ride = is_good_to_ride(forecast,day_hours,comfortable_temp,comfortable_rain)
    context = {"is_good_to_ride" : good_to_ride}
    return render(request, 'index.html',context)
    #return HttpResponse(forecast)

def today(request):
    url = "http://api.openweathermap.org/data/2.5/forecast?q=Minsk&units=metric"
    forecast = get_weather_forecast(get_json(url),date.today())
    good_to_ride = is_good_to_ride(forecast,evening_hours,comfortable_temp,comfortable_rain)
    context = {"is_good_to_ride" : good_to_ride}
    return render(request, 'index.html',context)

def tomorrow(request):
    url = "http://api.openweathermap.org/data/2.5/forecast?q=Minsk&units=metric"
    forecast = get_weather_forecast(get_json(url),date.today() + timedelta(days = 1))
    good_to_ride = is_good_to_ride(forecast,day_hours,comfortable_temp,comfortable_rain)
    context = {"is_good_to_ride" : good_to_ride}
    return render(request, 'index.html',context)
