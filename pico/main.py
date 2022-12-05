from machine import Pin, SPI
import max7219
from time import sleep
import json

spi = SPI(0,sck=Pin(2),mosi=Pin(3))
cs = Pin(5, Pin.OUT)

display = max7219.Matrix8x8(spi,cs,4)

    

def verticalScroll(msg):
    for y in range(8,-8,-1):
        display.fill(0)
        display.text(msg,0,y)
        sleep(0.3)
        display.show()
    
def horizontalScroll(msg):
    length = len(msg)
    column = (length * 8)
    for x in range(32, -column, -1):     
        display.fill(0)
        display.text(msg ,x,0,1)
        display.show()
        sleep(0.1)

def blink(msg):
    for bri in range (10):
        display.fill(0)
        display.brightness(bri)
        display.text(msg,0,0)
        display.show()
        sleep(0.1)
    for bri in range (10,0,-1):
        display.fill(0)
        display.brightness(bri)
        display.text(msg,0,0)
        display.show()
        sleep(0.1)
        
def draw_bitmap(matrix):
    display.fill(0)
    for row,col in matrix:
        display.rect(col,row,1,1,1)
    display.show()
    sleep(3)


def display_file():
    with open("content.json", "r") as read_file:
        contents = json.load(read_file)

    while True:
        for msg in contents["displays"]:
            if "text" in msg:
                scrollFuncStr=msg["effect"]+"(\""+msg["text"]+"\")"
                eval(scrollFuncStr)
            elif "bitmap" in msg:
                print("it is a bmpa")
                draw_bitmap(msg["bitmap"])
        #scrollFunc(msg["text"])
        
def usb_conf():
    display.fill(0)
    display.text("usb",0,0)
    display.show()
    
    
def connected_serial_usb():
    #true if there is a serial connection (connected to a PC or device)
    SIE_STATUS=const(0x50110000+0x50)
    CONNECTED=const(1<<16)
    SUSPENDED=const(1<<4)
    return (machine.mem32[SIE_STATUS] & (CONNECTED | SUSPENDED))==CONNECTED

#### main 
if connected_serial_usb():
    print("ººººººººº usb connected")
    usb_conf()
else:
    print("ººººººººº not usb")
    display_file()

    