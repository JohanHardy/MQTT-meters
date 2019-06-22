#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generic MQTT meters
Author: Johan Hardy
Email: hardy.johan@gmail.com
"""
import sys
import mqtt.client


def main():
    """Entry point of the MQTT meters."""
    for arg in sys.argv[1:]:
        print(arg)

    return 0


if __name__ == "__main__":
    main()
