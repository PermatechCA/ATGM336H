# ATGM336H
MicroPython Library for GPS+BD ATGM336H 
This is a simple liburary that allows access to the ATGM336H GPS unit



ATGM336H GPS Library Manual

Overview

The ATGM336H library is designed to interface with the ATGM336H GPS module using a microcontroller. It allows you to easily access GPS data such as time, location, velocity, number of satellites, and signal quality.

Setup

To use the library, you need to import it and create an instance of the ATGM336H class:

MicroPython Code 

from ATGM336H import ATGM336H

gps = ATGM336H(tx_pin=17, rx_pin=16, baudrate=9600) # Change this to your tx and rx port pins. 

Getting GPS Data

Once you have your GPS object, you can use the following methods to get GPS data:

Time: gps.gps_time() returns the current GPS time.
Velocity: gps.gps_velocity() returns the current velocity in meters per second.
Location: gps.gps_location() returns the current latitude and longitude.
Satellites: gps.gps_sats() returns the number of satellites the GPS is connected to.
Signal Quality: gps.gps_signal() returns the GPS signal quality.


MicroPython Code Example

Here’s a quick example of how to get the current location:

latitude, longitude = gps.gps_location()
print(f"Current location: Latitude {latitude}, Longitude {longitude}")
AI-generated code. Review and use carefully. More info on FAQ.



Notes
The library handles communication with the GPS module via UART.
It reads NMEA sentences from the GPS to provide the requested data.
If there’s an error or no data available, the methods will return None.
