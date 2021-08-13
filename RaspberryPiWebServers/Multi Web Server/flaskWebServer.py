#imports
from flask import Flask,render_template, request
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
 
# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(board.D4)
 
# Change these
# to the right size for your display!
WIDTH = 128
HEIGHT = 32  # Change to 64 if needed
BORDER = 5
 
# Use for I2C.
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)
# Clear display.
oled.fill(0)
oled.show()
 
# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new("1", (oled.width, oled.height))
 
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
 
# Draw a white background
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
 
# Draw a smaller inner rectangle
draw.rectangle(
    (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
    outline=0,
    fill=0,
)
 
# Load default font.
font = ImageFont.load_default()
 
app = Flask(__name__) #create the Flask app'
 
#Sets up GPIO pins
GPIO.setmode(GPIO.BCM)
 
#Creates Buttons/Leds
led1 = LED(4)
led2 = LED(26)
button = Button(27)
 
#Creates route for Home Page
@app.route('/')
def home():
    #Loads Home Page
    return render_template('home.html') 
 
#Part 1
#Requires a pin, finds status of that pin
@app.route("/pinStatus/<pin>")
def pinStatus(pin):
   try:
      GPIO.setup(int(pin), GPIO.IN)
      #If the status of pin isn't used(Button not pressed,High)
      if GPIO.input(int(pin)) == True:
         response = "Pin number " + pin + " is high!"
      else: #Else low
         response = "Pin number " + pin + " is low!"
   except: #If user gives weird pin number (100,7472,etc)
      response = "There was an error reading pin " + pin + "."
 
   templateData = { #creates data for the html page
      'title' : 'Status of Pin' + pin,
      'response' : response
      }
    #Sends Data to the html page
   return render_template('pinStatus.html', **templateData)
 
#Part 2
#Accepts a Post request, turn leds on/off accordingly
@app.route('/json', methods=['POST']) #GET requests will be blocked
def json():
    req_data = request.get_json() #When json data arrives
 
    #Finds json data for pin4 / 26
    pin4 = req_data['pin4']
    pin26 = req_data['pin26']
 
    #If the message said to turn Pins On/Off, turn the leds on accordingly
    if pin4 == "ON":
        led1.on()
        LED1 = "on"
            
    if pin26 == "ON":
        led2.on()
        LED2 = "on"
        
    if pin4 == "OFF":
        led1.off()
        LED1 = "off"
        
    if pin26 == "OFF":
        led2.off()
        LED2 = "off"
 
        
    templateData = {
        'title': 'Turning LED 1/2 On/Off',
        'led1State': 'LED1 is '+ LED1,
        'led2State': 'LED2 is '+ LED2
        }
        
    return render_template('json.html', **templateData)
 
#Part 3
#Send data through a form, data is then displayed on an OLED Screen
@app.route('/form', methods=['GET','POST']) 
def form():
    if request.method == 'POST': #this block is only entered when the form is submitted
                
                # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        image = Image.new("1", (oled.width, oled.height))
         
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
         
        # Draw a white background
        draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
         
        # Draw a smaller inner rectangle
        draw.rectangle(
            (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
            outline=0,
            fill=0,
        )
                # Clear display.
        oled.fill(0)
        oled.show()        
        
        #Text coms from the form
        text = request.form.get('text')
        
        
        (font_width, font_height) = font.getsize(text)
        draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),                text,
        font=font,
        fill=255,
        )
             
        # Display image
        oled.image(image)
        oled.show()
        
        #Displays data from the form second
        return render_template('formData.html')
 
    #Renders the form first
    return render_template('form.html')
 
#Part 4
#If a button is pressed, gets info from an API
@app.route('/api')
def api():
    #request data from API
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?zip='+str(90051)+',us&appid=dc946d6cc73ea175d0898927dbf601f4')
    #Creates a JSOn object so we use the data
    json_object = r.json()
    #Converts data to float so we use it easier.
    tempK = float(json_object['main']['temp'])
    #Convert to F
    tempF = (tempK - 273.15) * 1.8 + 32
    
    #If button is pressed, do nothing
    if button.is_pressed:
        tempDisplayed = tempF
    
    #Else, display wrong data
    else:
        tempDisplayed = 9999
    
    templateData = {
        'message': 'The Temperature is ' + str(tempDisplayed)
        }
    
    return render_template('api.html',**templateData)
#Use debug mode, host is 0.0.0.0, Place of Server, port= 80
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
