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

#################

**realtime_monitorV3.py** 

Added the ability to monitor Nvidia Card Temperatures as well.

<img width="1068" alt="Screenshot 2023-09-06 at 9 36 47 AM" src="https://github.com/cemdede/Dell_R_Series_FANvsTEMP_Check/assets/14031604/c2f9ed6b-73b4-424c-83d6-ca2741a7f467">

Cheers !!!!
