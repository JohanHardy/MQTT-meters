#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generic MQTT meter for Water, gaz and electricity.
Author: Johan Hardy
Email: hardy.johan@gmail.com
"""
import sys
import paho.mqtt.client as mqtt


def main():
    """Entry point of the MQTT meters."""
    for arg in sys.argv[1:]:
        print(arg)

    return 0


if __name__ == "__main__":
    main()
