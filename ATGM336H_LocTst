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

    # Public method to get the current location from the GPS
    def gps_location(self):
        gll_sentence = self._read_sentence('$GNGLL')
        return self._parse_location(gll_sentence)

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

    # Helper method to convert raw NMEA latitude and longitude to degrees
    def _convert_to_degrees(self, raw_value):
        # Convert string to float and perform the conversion
        decimal_value = float(raw_value)
        degrees = int(decimal_value / 100)
        minutes = decimal_value - (degrees * 100)
        return degrees + (minutes / 60)

# Create an instance of the ATGM336H class
gps = ATGM336H()

# Get the current location
location = gps.gps_location()
print(f"Location: {location}")
