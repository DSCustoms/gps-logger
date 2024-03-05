import datetime
import numpy as np

# Settings
num_points = 1000  # Number of individual plot points
time_interval_seconds = 60  # Amount of time between locations in seconds
heart_height = 45  # Height of the heart
heart_width = 33  # Width of the heart

# Heart parameters
h = -80.604117  # Longitude of the heart's center
k = 28.608116  # Latitude of the heart's center
t = np.linspace(0, 2*np.pi, num_points)

# Generate the x and y coordinates for the heart shape
x = h + heart_height*np.sin(t)**3
y = k + heart_width*(np.cos(t) - 0.5*np.cos(2*t) - 0.2*np.cos(3*t) - 0.1*np.cos(4*t))

# Time parameters
start_time = datetime.datetime(2024, 1, 1, 12, 1, 1)
time_interval = datetime.timedelta(seconds=time_interval_seconds)

# Generate timestamps for each point
timestamps = [start_time + i*time_interval for i in range(num_points)]

# Combine timestamps and coordinates into a list
gps_log = list(zip(timestamps, y, x))

# Open a text file in write mode
with open('gps_logs/20240101120101.txt', 'w') as f:
    # Write the GPS log to the file
    for timestamp, lat, lon in gps_log:
        f.write(f'{timestamp},{lat},{lon}\n')
