
#!/bin/bash

# Update and upgrade the system
sudo apt-get update
sudo apt-get upgrade

# Install the necessary packages
sudo apt-get install -y python3-pip
sudo apt-get install -y python3-gps
pip install flask
sudo apt-get install -y gpsd
sudo apt-get install -y gpsd-clients
sudo apt-get install -y gpsbabel
sudo apt-get update --fix-missing

# Configure gpsd
echo 'DEVICES="/dev/ttyACM0"
GPSD_OPTIONS=""
USBAUTO="true"
START_DAEMON="true"' | sudo tee /etc/default/gpsd

# Create directories and set permissions
sudo mkdir /home/pi/templates
sudo chmod 777 /home/pi/templates
sudo mkdir /home/pi/gps_logs
sudo chmod 777 /home/pi/gps_logs/
sudo mkdir /home/pi/gps_data
sudo chmod 777 /home/pi/gps_data/
sudo mkdir /home/pi/trips/
sudo chmod 777 /home/pi/trips/

# Download files from GitHub
wget -P /home/pi/templates/ https://raw.githubusercontent.com/DSCustoms/gps-logger/main/index.html
wget -P /home/pi/ https://raw.githubusercontent.com/DSCustoms/gps-logger/main/gps_translate.py
wget -P /home/pi/ https://raw.githubusercontent.com/DSCustoms/gps-logger/main/kml_to_txt.py
wget -P /home/pi/ https://raw.githubusercontent.com/DSCustoms/gps-logger/main/web_render.py

# Edit rc.local
echo '#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

# Print the IP address
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
fi

gpsd /dev/ttyACM0 -F /var/run/gpsd.sock
sleep 60
sudo gpspipe -r -d -l -o /home/pi/gps_data/data.`date +"%Y%m%d%H%M%S"`.nmea

exit 0' | sudo tee /etc/rc.local

# Create systemd services
echo '[Unit]
Description=GPSBabel Operation

[Service]
ExecStart=/usr/bin/python3 /home/pi/gps_translate.py
Restart=always
User=pi
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target' | sudo tee /etc/systemd/system/gps_translate.service

echo '[Unit]
Description=KML To TXT Filter

[Service]
ExecStart=/usr/bin/python3 /home/pi/kml_to_txt.py
Restart=on-failure
User=pi
# The configuration file in /etc/systemd/system.conf
# can be edited to change the time that units wait for
# a process to exit before killing it.
TimeoutStopSec=30

[Install]
WantedBy=multi-user.target' | sudo tee /etc/systemd/system/kml_txt.service

echo '[Unit]
Description=Web Render Engine
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi
ExecStart=/usr/bin/python3 /home/pi/web_render.py
Restart=always

[Install]
WantedBy=multi-user.target' | sudo tee /etc/systemd/system/web_render.service

# Enable and start the services
sudo systemctl enable gps_translate.service
sudo systemctl enable kml_txt.service
sudo systemctl enable web_render.service
sudo systemctl start gps_translate.service
sudo systemctl start kml_txt.service
sudo systemctl start web_render.service

# Reboot
sudo reboot
