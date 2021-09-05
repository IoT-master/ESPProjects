from machine import Pin
from time import sleep
p2 = Pin(2, Pin.OUT)
while True:
    p2.on()
    sleep(2)
    p2.off()
    sleep(2)
