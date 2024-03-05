# gps-logger
This project is a simple GPS logger / tracking device running on a Raspberry Pi. It logs GPS locations to a file and provides a web interface to view the logged data on a map. Once installed, you just need to power up the raspberry pi with the gps puck plugged in and it will always be logging the location. Then just get on the same network as the pi and open the map to see all the location history. The map will have a menu in the top left that shows all the "trips" it took, it creates a new one with each reboot. 

Borrowed the gpspipe idea from https://www.instructables.com/Raspberry-Pi-3-GPS-Data-Logger/ then turned it into a complete solution. 

## Prerequisites

- A Raspberry Pi with a fresh install of Raspberry Pi OS. This runs fine on the cheapest RPI zero w.  [Visit RPILocator](https://rpilocator.com/)
- A USB GPS device [Amazon Link, no affiliate](https://www.amazon.com/gp/product/B0BV7JC4G4)
- SSH access to the Raspberry Pi, which means it needs to be connected to your network
- A Google Maps API key. You can get one from the Google Cloud Console.


Installation
1. Download the install.sh script from the GPS LoggerX GitHub repository:

   ```
   wget https://github.com/DSCustoms/gps-logger/blob/main/install.sh
   ```

2. Make the script executable by running:

   ```
   chmod +x install.sh
   ```

3. Run the script with:

   ```
   ./install.sh
   ```

   This will install all necessary dependencies, download the scripts from the GitHub repository, configure gpsd, create the necessary directories, set up the rc.local file, create the systemd services, and finally reboot the system.

Configuration
After installation, you need to add your Google Maps API key to the index.html file:

1. Open the index.html file located in /home/pi/templates/ with a text editor. You can use nano by running:
   ```
   nano /home/pi/templates/index.html
   ```
3. Find the line:
   <script src='https://maps.googleapis.com/maps/api/js?key=YOUR_GOOGLE_MAPS_API_KEY&callback=initMap'></script>

4. Replace YOUR_GOOGLE_MAPS_API_KEY with your actual Google Maps API key.

   If you don’t have a Google Maps API key, you can get one by following these steps:
   - Go to the Google Cloud Console.
   - Create a new project.
   - Enable the Maps JavaScript API for your project.
   - Create credentials for the API.
   - Copy the API key.

Usage
After installation and configuration, you can access the web service at http://YOUR-PI-IP:5000/.

Verification and Testing
You can verify the installation of the packages by running:
   dpkg -l | grep <package-name>

   Replace <package-name> with the name of the package you want to check.

You can view the output and input files to make sure they are working. The output files are located in /home/pi/gps_logs/ and the input files are in /home/pi/trips/.

You can start, stop, and check the status of the systemd services with the following commands:

- Start a service:
  ```
  sudo systemctl start <service-name>
  ```
- Stop a service:
  ```
  sudo systemctl stop <service-name>
  ```
- Check the status of a service:
  ```
  sudo systemctl status <service-name>
  ```
  Replace <service-name> with the name of the service (gps_translate, kml_txt, or web_render).

You can view the live GPS data to see if you have a fix by running:
   ```
   cgps -s
   ```
If you have any questions or encounter any issues, feel free to open an issue on the GitHub repository. Happy logging!



## Manual Installation
If you want to manually install it, install all the dependencies and use the code found in 'app.py', 'gps_logger.py' and 'index.html'


GPS_TPV_test.py is a script that will test the gps output of your device once everything is set up

GPS_Heart.py is a script that will draw a giant heart on the map output. Run this once and go view the web page. Fully customizable. 

I know this is simple, but it should also be simple for people to set up and use. Hope this helps someone!

If this isn't finding your gps module, you need to find it yourself. 

## Configuring GPSD

GPSD needs to be configured to use the correct device. Here's how you can do it:

1. **Locate the GPS device**

    The GPS device is usually connected via a USB or serial port. You can list all connected devices with the following command:

    ```bash
    ls /dev
    ```

    Look for a device that starts with `tty`. This is usually the GPS device.

2. **Identify the device type**

    The device type is usually `ttyACM0` for GPS devices connected via USB. If you're not sure, check the documentation of your GPS device. This is a safe starting point.
    However, the exact name can vary depending on the GPS device and how it’s connected to your Raspberry Pi.
    You can confirm this by disconnecting your GPS device, running ls /dev, and then comparing the output to the output when the GPS device is connected. The device that appears when the GPS device 
    is connected and disappears when it’s disconnected is likely to be your GPS device.
    Once you’ve identified your GPS device, you can test it by running a GPS client such as gpsmon or cgps with your device as the argument, like so:
    ```bash
    gpsmon /dev/ttyACM0
    ```
    
    Replace ttyACM0 with the name of your device. If your GPS device is working correctly, you should see GPS data being output in the terminal.

4. **Update the gpsd configuration file**

    Open the gpsd configuration file with the following command:

    ```bash
    sudo nano /etc/default/gpsd
    ```

    Find the line that starts with `DEVICES=""` and replace it with `DEVICES="/dev/ttyACM0"` (replace `ttyACM0` with your actual device type). Then save and close the file.

