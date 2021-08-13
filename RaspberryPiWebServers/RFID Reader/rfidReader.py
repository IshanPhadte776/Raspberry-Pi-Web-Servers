#Imports
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
from time import sleep
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from gpiozero import DistanceSensor, LED



# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(board.D4)
 
#Size of display
WIDTH = 128
HEIGHT = 32  
BORDER = 5
 
# Use for I2C.
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)
 
#Creates reader and sensor object
reader = SimpleMFRC522()
sensor = DistanceSensor(23,24)
#Creates Led and sets port
led = LED(17)

#Reset screen
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
     
# Draw Some Text
text = "Scan your Card"
(font_width, font_height) = font.getsize(text)
draw.text(
    (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
    text,
    font=font,
    fill=255,
)
     
# Display image
oled.image(image)
oled.show()
 
#Forever loop 
while True:
    
    #Checks for card swipe (Will wait for card)
    RFIDcard = reader.read()

    #If data was scanned..
    if RFIDcard != "":
        #Checks sensor distance.    
        distance = sensor.distance    
    #If the user is distanced correctly,    
    if distance >= 1.0:
        #turns off led and changes text
        led.off()
        text = "You may enter"
        
    
    else: #Besides that, turns on led and tells user to distance correctly
        led.on()
        text = "Back away"
    
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
    
    oled.image(image)
    oled.show()
    
        # Draw Some Text
    (font_width, font_height) = font.getsize(text)
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
        text,
        font=font,
        fill=255,
    )
         
    # Display image
    oled.image(image)
    oled.show()
    
    #Pause every 2 seconds
    sleep(2)
    