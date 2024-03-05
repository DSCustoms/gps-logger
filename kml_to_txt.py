import os
import time
import xml.etree.ElementTree as ET
import re
import logging
import logging.handlers

def log_gps_data():
    # Set up logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.handlers.SysLogHandler(address='/dev/log')
    logger.addHandler(handler)

    # Get the list of .kml files
    files = [f for f in os.listdir('/home/pi/trips/') if f.endswith('.kml')]
    
    logger.info(f"Found {len(files)} .kml files")

    # If there are any .kml files, sort them by modification time and get the latest one
    if files:
        latest_file = max(files, key=lambda x: os.path.getmtime(os.path.join('/home/pi/trips/', x)))
        
        logger.info(f"Processing file {latest_file}")

        # Parse the KML file
        tree = ET.parse(os.path.join('/home/pi/trips/', latest_file))
        root = tree.getroot()

        # Create a new log file for each boot
        boot_time = time.strftime('%Y%m%d%H%M%S')
        log_file = f'/home/pi/gps_logs/{boot_time}.txt'

        logger.info(f"Created log file {log_file}")

        # Find all description elements in the KML file
        descriptions = root.findall('.//{http://www.opengis.net/kml/2.2}description')

        # Regular expression pattern to match the data
        pattern = r"Longitude: (.*?) .*?Latitude: (.*?) .*?Time: (.*?) .*?</table>"

        for description in descriptions:
            try:
                # Search for the pattern in the description text
                match = re.search(pattern, description.text, re.DOTALL)
                if match:
                    longitude, latitude, when = match.groups()

                    try:
                        # Write the data to the log file
                        with open(log_file, 'a') as f:
                            f.write(f"{when},{latitude},{longitude}\n")
                    except Exception as e:
                        logger.error(f"An error occurred while writing to the log file: {e}")

            except Exception as e:
                logger.error(f"An error occurred while processing a description element: {e}")

        time.sleep(15)

if __name__ == "__main__":
    log_gps_data()
