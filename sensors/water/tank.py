#!/usr/bin/env python
import RPi.GPIO as GPIO

# Table mapping the water gauge and GPIOs (10 levels for 100%)
gauges = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Water gauge health (Healthy = True, Unhealthy = False)
gauges_health = [True, True, True, True, True, True, True, True, True]

# Water gauge state (GPIO.HIGH = water, GPIO.LOW = no water)
gauges_state = [GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW]


def set_gauge_unheahlthy(level):
    gauges_health[level] = False


def set_gauge_heahlthy(level):
    gauges_health[level] = True


def get_gauge_health(level):
    return gauges_health[level]


def is_gauge_health(level):
    return bool(gauges_health[level] is True)


def sample(level):
    # returns GPIO.LOW or GPIO.HIGH at the gauge level.
    return GPIO.input(gauges[level])


def setup():
    # Setup GPIO port and clean up
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)

    # Sel all GPIO gauges as input ports.
    for level in gauges:
        GPIO.setup(gauges[level], GPIO.IN)


def get_level():
    # Acquire all gauge levels and compute level in percentage
    percentage = 0
    for level in range(0, gauges_state.__len__-1):
        gauges_state[level] = sample(level)
        if (gauges_state[level] is GPIO.High) and (is_gauge_health(level)):
            percentage = max(percentage, ((level*gauges_state.__len__)/100)

    return percentage


def monitor_gauges():
    pass
