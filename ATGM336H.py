# ATGM336H.py

import machine
import utime

class ATGM336H:
    # Constructor for initializing the GPS module with the specified UART pins
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
        return self._parse_sats(gsa_sentence)

    # Public method to get the signal quality from the GPS
    def gps_signal(self):
        gsv_sentence = self._read_sentence('$GPGSV')
        return self._parse_signal(gsv_sentence)

    # Internal method to parse the velocity from the VTG sentence
    def _parse_velocity(self, vtg_sentence):
        try:
            parts = vtg_sentence.split(',')
            # Ensure that the velocity field is not empty and is a valid number
            if parts[7] and parts[7].replace('.', '', 1).isdigit():
                velocity_knots = float(parts[7])
                velocity_ms = velocity_knots * 0.514444
                return velocity_ms
            else:
                print('Invalid velocity data encountered.')
                return None
        except ValueError:
            print('ValueError encountered while parsing velocity.')
            return None

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
        latitude = self._convert_to_degrees(parts[1])
        longitude = self._convert_to_degrees(parts[3])
        return latitude, longitude

    # Helper method to convert raw NMEA latitude and longitude values to degrees
    def _convert_to_degrees(self, raw_value):
        decimal_point_position = raw_value.find('.')
        degrees = float(raw_value[:decimal_point_position-2])
        minutes = float(raw_value[decimal_point_position-2:])
        return degrees + (minutes/60)

    # Internal method to parse the number of satellites from the GSA sentence
    def _parse_sats(self, gsa_sentence):
        parts = gsa_sentence.split(',')
        num_satellites = int(parts[3])
        hdop = float(parts[15])
        return num_satellites, hdop

    # Internal method to parse the signal quality from the GSV sentence
    def _parse_signal(self, gsv_sentence):
        parts = gsv_sentence.split(',')
        # Assuming signal quality is in the 6th field
        signal_quality = int(parts[6])
        return signal_quality

# End of ATGM336H.py
