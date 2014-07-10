#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
import csv
import smtplib, os
import time
import re
import urllib2
import json
from datetime import *
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

def send_mail(send_from, send_to, subject, text, files=[], server="localhost"):
	assert type(send_to)==list
	assert type(files)==list
	msg = MIMEMultipart('alternative')
	msg['From'] = send_from
	msg['To'] = COMMASPACE.join(send_to)
	msg['Date'] = formatdate(localtime=True)
	msg['Subject'] = subject
	msg['Content-Type'] = "text/html; charset=utf-8"
	
	msg.attach(MIMEText(text.encode('utf-8'),'plain','utf-8')
	
	for f in files:
		part = MIMEBase('application', "octet-stream")
		part.set_payload( open(f,"rb").read() )
		Encoders.encode_base64(part)
		part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
		msg.attach(part)
		
	smtp = smtplib.SMTP(server)
	smtp.sendmail(send_from, send_to, msg.as_string())
	smtp.close()
	print "Email sent\n"

def get_json(url):
	json_text = urllib2.urlopen(url).read()
	return json_text
	
def get_weather_forecast(json_text,current_date):
	
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

if __name__ == "__main__":
	url = "http://api.openweathermap.org/data/2.5/forecast?q=Minsk&units=metric"	
	forecast = get_weather_forecast(get_json(url),date.today() + timedelta(days = 1))
	if is_good_to_ride(forecast,[7,8,9,18,19,20],14,0.25):
		is_good_to_ride_text = 'Да, езжай, пацан! БВК!!'
	else:
		is_good_to_ride_text = 'Не суйся, дружище. Сиди дома, попивай горячий шоколад с маффинами'
	
	
	send_mail("root@goridethebike.com",["ypiskunovich@gmail.com","adolgushin@gmail.com"],"Weather",is_good_to_ride_text,[])
	
