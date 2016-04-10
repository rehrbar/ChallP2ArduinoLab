import sys, signal
import re
import serial
import paho.mqtt.client as mqtt

def cleanup():
    client.loop_stop()

def signal_term_handler(signal, frame):
    cleanup()

signal.signal(signal.SIGTERM, signal_term_handler)

# callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected to broker with result code " + str(rc))

# initialize
regexPattern = re.compile("^pot0:(\d+)\r$")
ser = serial.Serial("/dev/ttyACM0", 9600)
client = mqtt.Client()
client.on_connect = on_connect

client.connect("localhost", 1883)
client.loop_start()

try:
    # publish loop
    while True:
        groups = regexPattern.search(ser.readline())
        if groups is not None:
            pot0 = groups.group(1)
            print("Sensor value: " + pot0)
            client.publish("arduino/pot0", pot0)
        else:
            print("Error reading value!")
except KeyboardInterrupt:
    print("^C received, shutting down client")
    cleanup()
