"""
This is a Permatech code for setting the ESP32 Real Time Clock (RTC) and GPS location variable using the ATGM336H GPS module. 
The code initializes the GPS module and the RTC, waits for a connection to at least 4 satellites, and then retrieves the signal quality, 
location, and time from the GPS. The GPS time is used to set the RTC. The code also calculates and prints the time it took to get a lock 
on the satellites, the signal quality, the GPS location, and the RTC time.
"""

from ATGM336H import ATGM336H
import utime
from machine import RTC

# Initialize the GPS module
gps = ATGM336H(tx_pin=17, rx_pin=16, baudrate=9600)

# Initialize the RTC (Real Time Clock)
rtc = RTC()

# Function to set the RTC using the GPS time
def set_rtc(time_str):
    # Assuming time_str format is 'HH:MM:SS'
    t = time_str.split(':')
    hours = int(t[0])
    minutes = int(t[1])
    seconds = int(t[2])
    # Set the RTC time directly from the GPS time
    rtc.datetime((2024, 1, 1, 0, hours, minutes, seconds, 0))

# Function to print the RTC time in HH:MM:SS format
def print_rtc_time():
    year, month, day, weekday, hours, minutes, seconds, subseconds = rtc.datetime()
    print('RTC Time: {:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds))

# Variable to store the start time
start_time = utime.time()

# Variable to store the number of satellites
num_sats = gps.gps_sats()

# Wait for at least 4 satellites to be connected
while num_sats < 4:
    num_sats = gps.gps_sats()
    print(f"Connected satellites: {num_sats}")
    utime.sleep(10)

# Calculate the time it took to get a lock on 4 satellites
time_to_lock = utime.time() - start_time

# Get the signal quality, location, and time from the GPS
signal_quality = gps.gps_signal()
location = gps.gps_location()
gps_time = gps.gps_time()

# Print the results
print(f"Time to get a lock on to satellites: {time_to_lock} seconds")
print(f"Signal Quality: {signal_quality}")
print(f"Location: {location}")
print(f"GPS Time: {gps_time}")


# Set the RTC with the GPS time
set_rtc(gps_time)

# Print the RTC time in the desired format
print_rtc_time()

