#!/usr/bin/python
# -*- coding: utf-8 -*-

MQTT_SERVER="192.168.1.108"
MQTT_SERVER_PORT=1883
MQTT_PUBLISH_PERIOD=5
MQTT_CLIENT_ID="opimonitormqtt001"

import time
import threading
import sys

try:
    import paho.mqtt.publish as publish
except ImportError:
    # This part is only required to run the example from within the examples
    # directory when the module itself is not installed.
    #
    # If you have the module installed, just use "import paho.mqtt.publish"
    import os
    import inspect
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"./lib")))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)
    import paho.mqtt.publish as publish

def get_time():
    return time.strftime("%d %b %Y %H:%M:%S", time.localtime())

def get_temperature():
    try:
        with open('/sys/devices/virtual/hwmon/hwmon1/temp1_input', 'rb') as stream:
            temp = stream.read().strip()
            return temp
    except BaseException:
        return "error"

def get_frequency():
    try:
        with open('/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq', 'rb') as stream:
            freq = int(stream.read().strip()) / 1000
            return freq
    except BaseException:
        return "error"

def main_loop():
    cur_time = get_time()
    cur_temperature = get_temperature()
    cur_freq = get_frequency()
    msg_time = ("state/opi/time", cur_time, 0, True)
    msg_temperature = ("state/opi/temperature", cur_temperature, 0, True)
    msg_freq = ("state/opi/freq", cur_freq, 0, True)
    msgs = [msg_time, msg_temperature, msg_freq]
    try:
        publish.multiple(msgs, hostname=MQTT_SERVER, port=MQTT_SERVER_PORT, client_id=MQTT_CLIENT_ID)
    except BaseException:
        pass
    threading.Timer(MQTT_PUBLISH_PERIOD, main_loop).start()

if __name__ == "__main__":
    main_loop()
