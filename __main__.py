#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generic MQTT meter for Water, gaz and electricity.
Author: Johan Hardy
Email: hardy.johan@gmail.com
"""
import sys
import argparse
#import water.meter
#import water.tank
#import paho.mqtt.client as mqtt
import config


def main():
    ''' Construct the argument parse and parse the arguments '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action='version',
                        version='%(prog)s 1.0')
    parser.add_argument("--host", required=False, help="MQTT broker host",
                        default=config.MQTT_BROCKER_HOST)
    parser.add_argument("--port", required=False, help="MQTT broker port",
                        default=config.MQTT_BROCKER_PORT)
    parser.add_argument('--keep', required=False, help="MQTT broker keepalive",
                        default=config.MQTT_KEEP_ALIVE)
    parser.add_argument('--meter', required=True, help="Kind of meter", choices=['tank', 'water'])
    args = vars(parser.parse_args())
    # Display a friendly message to the user
    print("Starting MQTT client {}:{} keepalive {}".format(args["host"],
                                                           args["port"],
                                                           args["keep"]))
    print("Setting up {} meter".format(args["meter"]))
    return 0


if __name__ == "__main__":
    main()
