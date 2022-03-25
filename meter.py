#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import RPi.GPIO as GPIO
import config

def __measure():
  '''This function measures a distance'''
  GPIO.output(GPIO_TRIGGER, True)
  # Wait 10us
  time.sleep(0.00001)
  GPIO.output(GPIO_TRIGGER, False)
  start = time.time()
  
  while GPIO.input(GPIO_ECHO)==0:
    start = time.time()

  while GPIO.input(GPIO_ECHO)==1:
    stop = time.time()

  elapsed = stop-start
  distance = (elapsed * speedSound)/2

  return distance

def measure():
    '''Make 10 measurements'''
    for x in range(10):
        distance += __measure()
        time.sleep(0.1)
    
    # Compute average
    distance = distance / 10
    return distance

def setup
  '''setup meter'''
  # Use BCM GPIO references
  # instead of physical pin numbers
  GPIO.setmode(GPIO.BCM)
  
  # Speed of sound in cm/s at temperature celsius
  temperature = 15
  speedSound = 33100 + (0.6*temperature)
  
  # Set pins as output and input
  GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
  GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo
  
  # Set trigger to False (Low)
  GPIO.output(GPIO_TRIGGER, False)
  
  # Allow module to settle
  time.sleep(0.5)

def terminate
  GPIO.cleanup()
