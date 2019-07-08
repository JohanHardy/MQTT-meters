#!/usr/bin/env python
"""
Water tank level meter implementing fault detection algorithm.
The script reads 10 Raspberry Pi GPIOs corresponding each to 10% level of the
tank. Each gauge has a health status and a fault counter. In case the algoritm
detects WATER_TANK_GAUGE_FAULT_TOLERANCE faults for a gauge, the gauge is
considered unhealthy. The function monitor_gauges() must be called before
get_level().
Author: Johan Hardy
Email: hardy.johan@gmail.com
"""
import RPi.GPIO as GPIO

# Table mapping the water gauges (10 GPIOS = 10 levels = 100%)
GAUGE = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  # GPIO IDs are TBD
# Water gauge health status (healthy or unhealthy)
GAUGE_HEALTH = ['healthy']*10
# Water gauge state (GPIO.HIGH = water presence, GPIO.LOW = no water presence)
GAUGE_STATE = [GPIO.LOW]*10
# Water gauge fault counter
GAUGE_FAULT = [0]*10
# Fault dectection filter
WATER_TANK_GAUGE_FAULT_TOLERANCE = 3


def set_gauge_unhealthy(level):
    ''' Set a gauge unhealthy '''
    GAUGE_HEALTH[level] = 'unhealthy'


def set_gauge_healthy(level):
    ''' Set a gauge healthy '''
    GAUGE_HEALTH[level] = 'healthy'


def is_gauge_healthy(level):
    ''' Check whether a gauge is healthy or not '''
    return bool(GAUGE_HEALTH[level] == 'healthy')


def get_gauges_health():
    ''' Get all gauge healthes '''
    return GAUGE_HEALTH


def sample(level):
    ''' Read GPIO (i.e. whether the water reached level of gauge). GPIO.LOW or
    GPIO.HIGH at the gauge level '''
    return GPIO.input(GAUGE[level])


def setup():
    ''' Setup Raspberry Pi and its GPIOs for each gauge '''
    print("Setting up tank meter")
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    # Sel all GPIO gauges as input ports.
    for gpio in GAUGE:
        GPIO.setup(gpio, GPIO.IN)


def get_level():
    ''' Computes and returns level of water tank in percentage '''
    level_percent = 0
    # For each healthy gauge, try to compute level in percent
    for level in range(0, len(GAUGE)):
        if is_gauge_healthy(level):
            if GAUGE_STATE[level] is GPIO.HIGH:
                level_percent = max(level_percent, ((level+1)*(len(GAUGE)/100)*100))
    return level_percent


def monitor_gauges():
    ''' Checks each gauge against faulty floater '''
    for level in range(0, len(GAUGE)):
        # Acquire the level of each gauge
        GAUGE_STATE[level] = sample(level)
        # For each gauge, check gauge against other gauges (upper/lower)
        if (GAUGE_STATE[level] is GPIO.LOW) and (level+1 < len(GAUGE)):
            if (GAUGE_STATE[level+1] is GPIO.HIGH) and (is_gauge_healthy(level+1)):
                GAUGE_FAULT[level] += 1
            else:
                GAUGE_FAULT[level] = 0
        elif (GAUGE_STATE[level] is GPIO.HIGH) and (level-1 >= 0):
            if (GAUGE_STATE[level-1] is GPIO.LOW) and (is_gauge_healthy(level-1)):
                GAUGE_FAULT[level] += 1
            else:
                GAUGE_FAULT[level] = 0
        # Update health of gauges
        if GAUGE_FAULT[level] >= WATER_TANK_GAUGE_FAULT_TOLERANCE:
            set_gauge_unhealthy(level)
        else:
            set_gauge_healthy(level)
