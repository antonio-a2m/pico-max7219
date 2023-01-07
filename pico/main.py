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
        
def draw_line_by_line(lines_orig):
    display.fill(0)
    lines = lines_orig[0:8]
    for i in range(len(lines)):
        for j in range(32):
            if lines[i][j] == 1:
                display.pixel(j,i,1) 
    display.show()
    

def convert_vector(orig_matrix):
    cols = 32 
    rows=max(orig_matrix)[0]+1
    mtx = [[0 for i in range(cols)] for j in range(rows)]
    for row,col in orig_matrix:
        mtx[row][col] = 1

    return mtx
    
def bitmap_vert_scroll_up(lines_orig, times=3):
    lines = lines_orig * times
    height = len(lines_orig)*times
    for i in range(height-7):
        draw_line_by_line(lines[i:])
        sleep(0.1)
        
def bitmap_vert_scroll_down(lines_orig, times=3):
    lines = lines_orig * times
    height = len(lines_orig)*times
    for i in range(height):
        draw_line_by_line(lines[-8-i:])
        sleep(0.1)



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
                bitmap_vert_scroll_up(convert_vector(msg["bitmap"]))
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
#if False:
    print("ººººººººº usb connected")
    usb_conf()
else:
    print("ººººººººº not usb")
    display_file()

    