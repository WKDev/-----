import os
import socket
import paho.mqtt.client as mqtt
import yaml
import time
import threading
import traceback
import logging
from logging.handlers import RotatingFileHandler

def get_device_type():
    uname = str(os.uname())
    if "rpi" in uname:
        return 'rpi'
    elif "tegra" in uname:
        return "jetson"
    elif "x86_64" in uname:
        return "x86"
    elif "Darwin" in uname:
        return "darwin"
    else:
        return None

# 기본 설정
default_config = {
    'mqtt': {
        'broker': {
            'ip': '192.168.11.38',
            'port': 1883
        },
        'device_type': 'dss',
        'mode': 1,
    },
    'gpio': {
        'release_time': 3,
        'rpi_pins': [16,20,21],
        'jetson_pins': [12, 13, 18],
        'default_pins': [1, 2, 3]
    },
    'logging': {
        'level': 'INFO',
        'file': '/Users/chson/gpio_driver_log.log'
    }
}

def create_default_config(config_path):
    with open(config_path, 'w') as file:
        yaml.safe_dump(default_config, file)
    print(f"Default configuration file created at {config_path}")



# 설정 파일 로드
config_path = os.path.expanduser('~/configuration.yml')
if not os.path.exists(config_path):
    create_default_config(config_path)

with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

hostname = socket.gethostname()
hostname = hostname.replace('.local', '')

print(f"Hostname: {hostname}, loaing Config from {config_path}")


# Logging 설정
log_level = getattr(logging, config['logging']['level'].upper(), logging.INFO)
log_file = config['logging']['file']

# 로그 핸들러 설정
try:
    if not os.path.exists(os.path.dirname(log_file)):
        os.makedirs(os.path.dirname(log_file))
    handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
except (PermissionError, FileNotFoundError):
    log_file = os.path.expanduser('~/mqtt_controller.log')
    handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)

logging.basicConfig(level=log_level, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        handler,
                        logging.StreamHandler()
                    ])
logger = logging.getLogger('MQTT_GPIO_Controller')


gpio_pins = config['gpio']['default_pins']
device_type = get_device_type()
if device_type == "rpi":
    gpio_pins = config['gpio']['rpi_pins']
elif device_type == "jetson":
    gpio_pins = config['gpio']['jetson_pins']

# GPIO 설정
try:
    if device_type == "rpi":
        import RPi.GPIO as GPIO
    elif device_type == "jetson":
        import Jetson.GPIO as GPIO
    else:
        raise RuntimeError("Unsupported device type")
except Exception as e:
    logger.error(f"Error occurred in importing GPIO Library: {str(e)}. Ensure you have the necessary privileges (use 'sudo' to run the script).")
    GPIO = None

class GPIOController:
    def __init__(self, pins, release_time=3):
        self.GPIO_INTERVAL = release_time
        self.pins = pins

        if GPIO:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            for pin in self.pins:
                GPIO.setup(pin, GPIO.OUT)

    def set_release_time(self, release_time):
        self.GPIO_INTERVAL = release_time

    def activate_pin(self, pin_index):
        if GPIO and pin_index < len(self.pins):
            pin = self.pins[pin_index]
            threading.Thread(target=self._activate_pin_thread, args=(pin,)).start()

    def _activate_pin_thread(self, pin):
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(self.GPIO_INTERVAL)
        GPIO.output(pin, GPIO.LOW)

gpio_controller = GPIOController(gpio_pins, config['gpio']['release_time'])

# Callback for connection
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to MQTT broker")
        client.subscribe(f"{hostname}/time")
        client.subscribe(f"{hostname}/mode")
        client.subscribe(f"{hostname}/release_time")

        print(f"Subscribed to {hostname}/time")
        print(f"Subscribed to {hostname}/mode")
        print(f"Subscribed to {hostname}/release_time")
    else:
        logger.error(f"Failed to connect to MQTT broker, return code {rc}")

# Callback for received message
def on_message(client, userdata, msg):
    logger.info(f"Topic: {msg.topic}, Message: {msg.payload.decode()}")
    topic = msg.topic.split('/')[-1]
    
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    if topic in ['mode', 'release_time', 'time']:
        config['mqtt'][topic] = msg.payload.decode()
        
        with open(config_path, 'w') as file:
            yaml.safe_dump(config, file)
        
        # If the topic is 'release_time', update GPIO release time
        if topic == 'release_time':
            gpio_controller.set_release_time(int(msg.payload.decode()))
        
        # If the topic is 'time', handle GPIO logic
        elif topic == 'time':
            
            new_timestamp = int(msg.payload.decode())
            current_timestamp = int(time.time())
            if abs(current_timestamp - new_timestamp) <= 5:
                gpio_controller.activate_pin(0)  # Example: Activate first pin
                gpio_controller.activate_pin(1)  # Example: Activate first pin
                gpio_controller.activate_pin(2)  # Example: Activate first pin

# Initialize MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Read MQTT broker address and connect
mqtt_broker = config['mqtt']['broker']['ip']
mqtt_port = config['mqtt']['broker']['port']
client.connect(mqtt_broker, mqtt_port, 60)

# Loop forever, handling reconnects and messages
client.loop_forever()
