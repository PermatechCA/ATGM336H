from ATGM336H import ATGM336H

# Initialize the GPS module
gps = ATGM336H()

# Get GPS data
current_time = gps.gps_time()
current_velocity = gps.gps_velocity()
current_location = gps.gps_location()
connected_satellites = gps.gps_sats()
signal_quality = gps.gps_signal()

# Print GPS data
print("Current Time:", current_time)
print("Current Velocity:", current_velocity)
print("Current Location:", current_location)
print("Connected Satellites:", connected_satellites)
print("Signal Quality:", signal_quality)
