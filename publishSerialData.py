#!/usr/bin/python
import serial
import paho.mqtt.client as mqtt

# callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected to broker with result code " + str(rc))

# initialize
ser = serial.Serial('/dev/ttyACM0', 9600)
client = mqtt.Client()
client.on_connect = on_connect

client.connect("localhost", 1883)
client.loop_start()

try:
    # publish loop
    while True:
        sensor_value = int(ser.readline())
        print("Sensor value: " + sensor_value)
        client.publish("arduino/poti", sensor_value)
except KeyboardInterrupt:
    print('^C received, shutting down client')
    client.loop_stop()
