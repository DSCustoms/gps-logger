import time
import os
import subprocess

def run_gpsbabel():
    # Wait for 5 minutes
    time.sleep(300)

    # Get the boot time
    boot_time = time.strftime('%Y%m%d%H%M%S')

    while True:
        # Get the list of .nmea files
        files = [f for f in os.listdir('/home/pi/gps_data/') if f.endswith('.nmea')]
        
        # If there are any .nmea files, sort them by modification time and get the latest one
        if files:
            latest_file = max(files, key=lambda x: os.path.getmtime(os.path.join('/home/pi/gps_data/', x)))
            output_file = f'{boot_time}_{latest_file.replace(".nmea", ".kml")}'
            
            # Run gpsbabel on the latest file
            subprocess.run(['gpsbabel', '-i', 'nmea', '-f', os.path.join('/home/pi/gps_data/', latest_file), '-o', 'kml', '-F', os.path.join('/home/pi/trips/', output_file)])
        
        # Wait for 30 seconds before the next run
        time.sleep(30)

if __name__ == "__main__":
    run_gpsbabel()
