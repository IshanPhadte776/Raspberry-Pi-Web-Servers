from flask import Flask,render_template, request, url_for, copy_current_request_context
import datetime
import RPi.GPIO as GPIO
from gpiozero import LED
from time import sleep
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import requests
from gpiozero import Button
from flask_socketio import SocketIO, emit
from flask_mqtt import Mqtt
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
import time
 
#Sets up the OLED Screen
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, rotate=0)
#Creates Flask and configures settings
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
 
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'localhost'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
app.config['MQTT_CLEAN_SESSION'] = True
 
#turn the flask app into a socketio app
socketio = SocketIO(app)
#Creates Button/LED
ledPinValue = 27
btnPinValue = 6
led = LED(ledPinValue)
btn = Button(btnPinValue)
 
#Creates mqtt
mqtt = Mqtt(app)
 
 
#Creates route for Home Page
@app.route('/')
def home():
    #Loads Home Page
    return render_template('homeFPT.html')
 
#Creates route to find the currentWeather in Burlington
@app.route('/currentWeatherBurlington') 
def currentWeatherBurlington():
    return render_template('currentWeatherBurlington.html')
    
@app.route('/hourlyWeatherBurlington') 
def hourlyWeatherBurlington():
    return render_template('hourlyWeatherBurlington.html')
 
    
@app.route('/dailyWeatherBurlington') 
def dailyWeatherBurlington():
    return render_template('dailyWeatherBurlington.html')
 
@app.route('/weatherSuggestionsOutput') 
def weatherSuggestionsOutput():
    return render_template('weatherSuggestionsOutput.html')
 
#When client sends a message attached to 'submit'
#When the user clicks the physical button
@socketio.on('submit')
def BurlingtonButtonPressed(data):
 
    #When the html button was clicked on the "Hourly" Temperature forecast
   if data == "Hourly":
       #Makes a request to an API 
       allData = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat=43.39&lon=-79.84&exclude=daily,current,alerts,minutely&appid=dc946d6cc73ea175d0898927dbf601f4&units=metric')
       #Turns the data into the Json format
       allDataJson = allData.json()
       
       #Removes the first line of data that we don't need
       #Looks at only the hourly data
       hourlyData = allDataJson['hourly']
       
       #Looks at only the data for the first hour (Current Temp)
       now = hourlyData[0]
       #Looks at only the temp data 
       nowTemp = now['temp']
       
       HourLater1 = hourlyData[1]
       HourLaterTemp1 = HourLater1['temp']
       
       HourLater2 = hourlyData[2]
       HourLaterTemp2 = HourLater2['temp']
       
       HourLater3 = hourlyData[3]
       HourLaterTemp3 = HourLater3['temp']
       
       HourLater4 = hourlyData[4]
       HourLaterTemp4 = HourLater4['temp']
       
       HourLater5 = hourlyData[5]
       HourLaterTemp5 = HourLater5['temp']
       
       HourLater6 = hourlyData[6]
       HourLaterTemp6 = HourLater6['temp']
       
       HourLater7 = hourlyData[7]
       HourLaterTemp7 = HourLater7['temp']
       
       HourLater8 = hourlyData[8]
       HourLaterTemp8 = HourLater8['temp']
       
       HourLater9 = hourlyData[9]
       HourLaterTemp9 = HourLater9['temp']
       
       HourLater10 = hourlyData[10]
       HourLaterTemp10 = HourLater10['temp']
       
       HourLater11 = hourlyData[11]
       HourLaterTemp11 = HourLater11['temp']
    
       #Stores all temperature values for 12 hours in an array
       hourlyBurlingtonTemp = [nowTemp,HourLaterTemp1,HourLaterTemp2,HourLaterTemp3,HourLaterTemp4,HourLaterTemp5,
                               HourLaterTemp6,HourLaterTemp7,HourLaterTemp8,HourLaterTemp9,HourLaterTemp10,
                               HourLaterTemp11]
              
       #Sends Json data back to the client on 'serverToClientHourly       
       emit('serverToClientHourly', {'words':hourlyBurlingtonTemp})
       
   if data == "Daily":
       allData = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat=43.39&lon=-79.84&exclude=hourly,current,alerts,minutely&appid=dc946d6cc73ea175d0898927dbf601f4&units=metric')
       allDataJson = allData.json()
       
       dailyData = allDataJson['daily']
       
       today = dailyData[0]  
       todayTemp = today['temp']
       todayTempDay = todayTemp['day']
       
       tomorrow = dailyData[1]
       tomorrowTemp = tomorrow['temp']
       tomorrowTempDay = tomorrowTemp['day']
       
       DaysFuture2 = dailyData[2]
       DaysFutureTemp2 = DaysFuture2['temp']
       DaysFutureTempDay2 = DaysFutureTemp2['day']
       
       DaysFuture3 = dailyData[3]
       DaysFutureTemp3 = DaysFuture3['temp']
       DaysFutureTempDay3 = DaysFutureTemp3['day']
       
       DaysFuture4 = dailyData[4]
       DaysFutureTemp4 = DaysFuture4['temp']
       DaysFutureTempDay4 = DaysFutureTemp4['day']
       
       DaysFuture5 = dailyData[5]
       DaysFutureTemp5 = DaysFuture5['temp']
       DaysFutureTempDay5 = DaysFutureTemp5['day']
       
       DaysFuture6 = dailyData[6]
       DaysFutureTemp6 = DaysFuture6['temp']
       DaysFutureTempDay6 = DaysFutureTemp6['day']
    
       
       dailyBurlingtonTemp = [todayTempDay,tomorrowTempDay,
                              DaysFutureTempDay2,DaysFutureTempDay3,
                              DaysFutureTempDay4,DaysFutureTempDay5,DaysFutureTempDay6]
              
       emit('serverToClientDaily', {'words':dailyBurlingtonTemp})
 
#To send data from MQTT Tool, you need to send it to 'weatherSuggestions/input'
@mqtt.on_connect()
def handle_connect(client,userdata,flags,rc):
    #Subscribes to 'weatherSuggestions/input'
    mqtt.subscribe('weatherSuggestions/input')
    
#When the data comes in    
@mqtt.on_message()
def handle_mqtt_message(client,userdata, message):
    data = dict (
        topic=message.topic,
        payload = message.payload.decode().strip()
        )
    #Ints the data
    weatherSuggestion = int(data['payload'])
    
    #Compares data to numbers provide advice based on the value 
    if weatherSuggestion >= 35:
        #In certain cases, led will turn to warn the user
        led.on()
        text = "Heat Warning"
        
    elif weatherSuggestion >= 20 and weatherSuggestion <= 35:
        text = "T-Shirt and Shorts"
        led.off()
        
    elif weatherSuggestion >= 5 and weatherSuggestion <= 20:
        text = "Sweater Weather"
        led.off()        
        
    elif weatherSuggestion >= -5 and weatherSuggestion <= 5:
        text = "Light Jacket"
        led.off()
        
    elif weatherSuggestion >= -20 and weatherSuggestion <= -5:
        text = "Winter Jacket"
        led.off()
        
    elif weatherSuggestion <= -20:        
        text = "Freezing"
        led.on()
 
    else:
        print("n/a")
        
    # Prints advice to the Oled Screen
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((10, 40), text, fill="white")
        
 
def updateBurlingtonCurrentWeather():
   
    allData = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat=43.39&lon=-79.84&exclude=daily,hourly,alerts,minutely&appid=dc946d6cc73ea175d0898927dbf601f4&units=metric')
    allDataJson = allData.json()
 
    currentBurlingtonJson = allDataJson['current']
    currentBurlingtonTemp = currentBurlingtonJson['temp']
           
    socketio.emit('serverToClientCurrently', {'words':str(currentBurlingtonTemp)})
   
#When the physical button is pressed    
btn.when_pressed = updateBurlingtonCurrentWeather
 
 
#URL = 0.0.0.5000
if __name__ == '__main__':
   socketio.run(app, host = '0.0.0.0', debug = 5000)
