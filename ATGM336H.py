# ATGM336H.py

"""
This is a MicroPython library for the ATGM336H GPS module developed by Permatech. 
It provides functionality to:
- Initialize the GPS module with specified UART pins and baud rate.
- Read specific types of NMEA sentences from the GPS module.
- Get the current GPS time, velocity, location (latitude and longitude), number of connected satellites, and signal quality.
- Parse raw NMEA sentences into usable data.
"""

import machine
import utime

class ATGM336H:
    def __init__(self, tx_pin=17, rx_pin=16, baudrate=9600):
        # Set up UART communication on the specified pins and baud rate
        self.uart = machine.UART(1, tx=tx_pin, rx=rx_pin, baudrate=baudrate)

    # Private method to read a specific type of NMEA sentence from the GPS
    def _read_sentence(self, sentence_type):
        # Continuously read from UART until a sentence of the desired type is found
        while True:
            if self.uart.any():
                try:
                    line = self.uart.readline().decode('utf-8').strip()
                    if line.startswith(sentence_type):
                        return line
                except UnicodeError:
                    # If a UnicodeError is encountered, skip the line and continue
                    print('Unicode decoding error encountered. Skipping line.')
                utime.sleep(0.5)

    # Public method to get the current GPS time
    def gps_time(self):
        zda_sentence = self._read_sentence('$GNZDA')
        return self._parse_time(zda_sentence)

    # Public method to get the current velocity from the GPS
    def gps_velocity(self):
        vtg_sentence = self._read_sentence('$GNVTG')
        return self._parse_velocity(vtg_sentence)

    # Public method to get the current location from the GPS
    def gps_location(self):
        gll_sentence = self._read_sentence('$GNGLL')
        return self._parse_location(gll_sentence)

    # Public method to get the number of connected satellites
    def gps_sats(self):
        gsa_sentence = self._read_sentence('$GNGSA')
        parts = gsa_sentence.split(',')
        sats = int(parts[7])  # Assuming the number of satellites is in the 8th field
        return sats

    # Public method to get the signal quality from the GPS
    def gps_signal(self):
        gsv_sentence = self._read_sentence('$GPGSV')
        return self._parse_signal(gsv_sentence)

    # Internal method to parse the velocity from the VTG sentence
    def _parse_velocity(self, vtg_sentence):
        parts = vtg_sentence.split(',')
        velocity_knots = float(parts[7])
        velocity_ms = velocity_knots * 0.514444
        return velocity_ms

    # Internal method to parse the time from the ZDA sentence
    def _parse_time(self, zda_sentence):
        parts = zda_sentence.split(',')
        utc_time = parts[1]
        hours = int(utc_time[:2]) - 3  # Adjust for Atlantic Time Zone
        minutes = int(utc_time[2:4])
        seconds = int(utc_time[4:6])
        if hours < 0:
            hours += 24
        return '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)

    # Internal method to parse the location from the GLL sentence
    def _parse_location(self, gll_sentence):
        parts = gll_sentence.split(',')
        latitude_raw = parts[1]
        latitude_direction = parts[2]
        longitude_raw = parts[3]
        longitude_direction = parts[4]

        # Convert raw values to degrees
        latitude = self._convert_to_degrees(latitude_raw)
        longitude = self._convert_to_degrees(longitude_raw)

        # Apply negative sign for south latitude or west longitude
        if latitude_direction == 'S':
            latitude = -latitude
        if longitude_direction == 'W':
            longitude = -longitude

        return latitude, longitude

    # Internal method to parse the number of satellites from the GSA sentence
    def _parse_sats(self, gsa_sentence):
        parts = gsa_sentence.split(',')
        sats = int(parts[7])
        hdop = float(parts[8]) if len(parts) > 8 else None  # Replace 8 with the correct index if needed
        return sats, hdop

    # Internal method to parse the signal quality from the GSV sentence
    def _parse_signal(self, gsv_sentence):
        parts = gsv_sentence.split(',')
        # Assuming signal quality is in the 6th field
        signal_quality = int(parts[6])
        return signal_quality

    # Helper method to convert raw NMEA latitude and longitude to degrees
    def _convert_to_degrees(self, raw_value):
        # Convert string to float and perform the conversion
        decimal_value = float(raw_value)
        degrees = int(decimal_value / 100)
        minutes = decimal_value - (degrees * 100)
        return degrees + (minutes / 60)


# End of ATGM336H.py
