import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

THRESHOLD = 500
HOSTNAME = "localhost"
PORT = 1883

# callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected to broker with result code " + str(rc))
    client.subscribe("arduino/pot0")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    try:
        GPIO.output(int(msg.payload) > THRESHOLD)
    except ValueError:
        print("Message was not an integer.")

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(HOSTNAME, PORT)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("^C received, shutting down subscriberLCD")
    client.loop_stop()
