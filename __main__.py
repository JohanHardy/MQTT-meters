#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MQTT meter for Water tank level.
Author: Johan Hardy
Email: hardy.johan@gmail.com
"""
import os
import time
import sys
import json
import argparse
import meter
import paho.mqtt.client as mqtt
import config

# Create a MQTT client
CLIENT = mqtt.Client()

def _execute_water_tank_activities():
    ''' Execute water tank activities '''
    payload = {}
    try:
        next_monitoring = time.time()
        while True:
            # Get water level
            payload['level'] = meter.measure()
            # Send telemetry to MQTT broker
            CLIENT.publish(config.MQTT_TOPIC_WATER_TANK, json.dumps(payload), 1)
            # Wait for next cycles
            next_monitoring += config.MQTT_INTERVAL_WATER_TANK
            sleep_time = next_monitoring - time.time()
            if sleep_time > 0:
                time.sleep(sleep_time)
    except KeyboardInterrupt:
        pass
    CLIENT.loop_stop()
    CLIENT.disconnect()

def main():
    ''' Construct the argument parser and parse the arguments '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action='version',
                        version='%(prog)s 1.0')
    parser.add_argument("--host", required=False, help="MQTT broker host",
                        default=config.MQTT_BROCKER_HOST)
    parser.add_argument("--port", required=False, help="MQTT broker port",
                        default=config.MQTT_BROCKER_PORT)
    parser.add_argument('--keep', required=False, help="MQTT broker keepalive",
                        default=config.MQTT_KEEP_ALIVE)
    args = vars(parser.parse_args())
    # Display a friendly message to the user
    print("Starting MQTT client {}:{} keepalive {}".format(args["host"],
                                                           args["port"],
                                                           args["keep"]))
    CLIENT.connect(args["host"], int(args["port"]), int(args["keep"]))
    CLIENT.loop_start()
    
    # Initialise and start meter activities
    meter.setup()
    _execute_water_tank_activities()
    meter.terminate()
    return 0

if __name__ == "__main__":
    main()
