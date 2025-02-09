'''This file runs as the systems is started.'''

try:  # TRY to import 'usocket' but if there is ERROR then jump to 'except'
    import usocket as socket
except:  # If TRY fails then 'socket' module will be imported.
    import socket

# Other 'Module' import that are necessary for code to run.
from machine import Pin
import network
import esp

esp.osdebug(None)  # Turn Off vendor OperatingSystem debugging messages
import gc  # Gabage Collector. Will ensure that the processor is not overloaded with unused variables. #

gc.collect()

ssid = "Namith's"  # Replace with actual 'SSID' of your WiFi Network (Mobile Hotspot) #
password = "namith123"  # Replace with actual 'Password' of afore given 'SSID' #

station = network.WLAN(
    network.STA_IF
)  # Telling the ESP module to work in 'Station' mode.

station.active(True)
station.ifconfig(
    ("192.168.157.220", "255.255.255.0", "192.168.157.210", "8.8.8.8")
)  # Creating a static IP for nodemcu.
station.connect(ssid, password)

while station.isconnected() == False:
    pass

print("Connection successful")
print(station.ifconfig())

'''Assisging the pins as an output pins and assigining the values as 1 as there is positive reference taken for the relays so the maximum voltage i.e. 1 in binnary
will be off and minimum voltage i.e. 0 in binary will be on.'''
# ESP8266 GPIO 4 (D2)
Rly1 = Pin(4, Pin.OUT)
Rly1.value(1)

# ESP8266 GPIO 0 (D3)
Rly2 = Pin(0, Pin.OUT)
Rly2.value(1)

# ESP8266 GPIO 2 (D4)
Rly3 = Pin(2, Pin.OUT)
Rly3.value(1)

# ESP8266 GPIO 14 (D5)
Rly4 = Pin(14, Pin.OUT)
Rly4.value(1)
