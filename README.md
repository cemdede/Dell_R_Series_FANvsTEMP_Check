**Dell_R_Series_FANvsTEMP_Check**

Dell PowerEdge R series Server Realtime Temperature Sensor Check and Fans speed check monitor.

Important:
It only monitors the Fan speeds and Temperature Sensors.
If you would like it to control the fan speed in response to the temperature changes, try this one instead:
https://github.com/cemdede/Fan_Adjustment_for_System_Temperature/tree/main

Updates every 2 seconds.
Output is scaled and color-coded.

Run the following to start the script:
chmod +x realtime_monitor.py
sudo python3 realtime_monitor.py

Click "q" to quit.

#################

**realtime_monitorV2.py** 

This one includes a spinner that would remind the user that it is active.
