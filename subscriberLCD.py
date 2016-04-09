import RPi.GPIO as GPIO
from RPLCD import CharLCD, cleared, cursor
import paho.mqtt.client as mqtt

# callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected to broker with result code " + str(rc))
    client.subscribe("arduino/pot0")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    lcd.cursor_pos = (1,0)
    # fill up the whole line with spaces to clear previous values.
    lcd.write_string(str(msg.payload).ljust(16))

lcd = CharLCD(pin_rs=25, pin_rw=None, pin_e=17, pins_data=[18, 22, 23, 24],
              numbering_mode=GPIO.BCM,
              cols=16, rows=2)

lcd.clear()
lcd.write_string('Messwert:')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("^C received, shutting down subscriberLCD")
    lcd.close(clear=True)
    client.loop_stop()
