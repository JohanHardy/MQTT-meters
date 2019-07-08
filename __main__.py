#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generic MQTT meter for Water, tank level, gaz and electricity.
Author: Johan Hardy
Email: hardy.johan@gmail.com
"""
import os
import time
import sys
import json
import argparse
import water.meter
import water.tank
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
            # Monitor all gauges in the tank
            water.tank.monitor_gauges()
            # Get water level
            payload['level'] = water.tank.get_level()
            # Get gauge healthes
            gauge_health = water.tank.get_gauges_health()

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
    parser.add_argument('--meter', required=True, help="Kind of meter",
                        choices=['tank', 'water'])
    args = vars(parser.parse_args())
    # Display a friendly message to the user
    print("Starting MQTT client {}:{} keepalive {}".format(args["host"],
                                                           args["port"],
                                                           args["keep"]))
    CLIENT.connect(args["host"], int(args["port"]), int(args["keep"]))
    CLIENT.loop_start()
    # Initialise and start meter activities
    if args["meter"] == 'tank':
        water.tank.setup()
        _execute_water_tank_activities()
    elif args["meter"] == 'water':
        water.meter.setup()
    else:
        print("Should never happen!")
    return 0


if __name__ == "__main__":
    main()
