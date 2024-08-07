import paho.mqtt.client as mqtt

# Define callback functions for MQTT events
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        # Subscribe to the desired topic(s) here
        client.subscribe("ioss-1/#")
    else:
        print("Failed to connect, return code: ", rc)

def on_message(client, userdata, msg):
    # Process the received message here
    
    print(f"{client=} {userdata=} {msg=}")
    print("Received message: ", msg.payload.decode())

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker")

# Create an MQTT client instance
client = mqtt.Client()

# Set the callback functions
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

# Set the MQTT broker address and port
broker_address = "127.0.0.1"
broker_port = 1883

# Connect to the MQTT broker
client.connect(broker_address, broker_port)

# Start the MQTT client loop
client.loop_forever()