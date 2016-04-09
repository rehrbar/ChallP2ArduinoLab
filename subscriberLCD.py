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
    with cursor(lcd, 1, 0):
        lcd.write_string(str(msg.payload).ljust(4))

lcd = CharLCD(pin_rs=15, pin_rw=18, pin_e=16, pins_data=[21, 22, 23, 24],
              numbering_mode=GPIO.BOARD,
              cols=16, rows=2, dotsize=8,
              auto_linebreaks=True,
              pin_backlight=None, backlight_enabled=True,
              backlight_mode=BacklightMode.active_low)

with cleared(lcd):
    lcd.write_string('Messwert:')

client = mqtt.Client()
client.on_connect = on_connect

client.connect("localhost", 1883)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("^C received, shutting down subscriberLCD")
    lcd.close(clear=True)
    client.loop_stop()
