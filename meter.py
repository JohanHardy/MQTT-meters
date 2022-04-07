#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import RPi.GPIO as GPIO
import config
import statistics

def __measure():
  '''This function measures a distance'''
  # Speed of sound in cm/s at temperature celsius
  temperature = 15
  speedSound = 33100 + (0.6*temperature)

  GPIO.output(config.GPIO_TRIGGER, True)
  # Wait 10us
  time.sleep(0.00001)
  GPIO.output(config.GPIO_TRIGGER, False)
  start = time.time()
  
  while GPIO.input(config.GPIO_ECHO)==0:
    start = time.time()

  while GPIO.input(config.GPIO_ECHO)==1:
    stop = time.time()

  elapsed = stop-start
  distance = (elapsed * speedSound)/2

  return distance

def measure():
    '''Make 10 measurements'''
    distance = []
    for x in range(10):
        distance.append(__measure())
        time.sleep(0.1)
    
    # Compute average
    return statistics.mean(distance)

def setup():
  '''setup meter'''
  # Use BCM GPIO references
  # instead of physical pin numbers
  GPIO.setmode(GPIO.BCM)
  
  # Set pins as output and input
  GPIO.setup(config.GPIO_TRIGGER,GPIO.OUT)  # Trigger
  GPIO.setup(config.GPIO_ECHO,GPIO.IN)      # Echo
  
  # Set trigger to False (Low)
  GPIO.output(config.GPIO_TRIGGER, False)
  
  # Allow module to settle
  time.sleep(0.5)

def terminate():
  GPIO.cleanup()
