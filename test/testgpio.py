import os
import socket
import paho.mqtt.client as mqtt
import yaml
import time
import threading
import traceback
import logging
from logging.handlers import RotatingFileHandler
import sys

def get_device_type():
    uname = str(os.uname())
    if "v8+" in uname:
        return 'rpi'
    elif "tegra" in uname:
        return "jetson"
    elif "x86_64" in uname:
        return "x86"
    elif "Darwin" in uname:
        return "darwin"
    else:
        return None
    
device_type = get_device_type()
print(f"Device type: {device_type}")

# GPIO 설정
try:
    if device_type == "rpi":
        import RPi.GPIO as GPIO
    elif device_type == "jetson":
        import Jetson.GPIO as GPIO
    else:
        raise RuntimeError("Unsupported device type")
except Exception as e:
    print(f"Error occurred in importing GPIO Library: {str(e)}. Ensure you have the necessary privileges (use 'sudo' to run the script).")
    sys.exit(1)


# turn on and off the all GPIO pins periodically

def turn_on_off_gpio_pins():
    while True:
        for pin in range(2, 28):
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(0.5)

if __name__ == '__main__':
    # GPIO 설정
    if device_type == "rpi":
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        for pin in range(2, 28):
            GPIO.setup(pin, GPIO.OUT)
    elif device_type == "jetson":
        GPIO.setmode(GPIO.BOARD)
        for pin in range(2, 28):
            GPIO.setup(pin, GPIO.OUT)
    else:
        print("Unsupported device type")
        sys.exit(1)

    turn_on_off_gpio_pins()
    GPIO.cleanup()

