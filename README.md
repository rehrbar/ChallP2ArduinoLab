# ChallP2ArduinoLab
Dieses Projekt entstand aus der Aufgabenstellung zum Modul Challenge Projekt 2 FS16.

## Aufgabenstellung
Die Aufgabenstellung ist im PDF "Challenge Projekt Raspberry-Arduino Lab.pdf" festgehalten.
Es geht um ein Miniprojekt in dem ein Sensor ausgelesen, und der Wert an verschiedene Endpunkte geschickt werden soll.
### Sensor auslesen
Ein Sensor soll an ein Arduinoboard angeschlossen werden.
Die Werte des Sensors sollen an den Arduino geschickt werden.
### Sensordaten an Raspberry übermitteln
Das Arduinoboard soll die eingelesenen Daten über eine serielle Schnittstelle an ein Raspberry PI übertragen.
### MQTT Broker
Auf dem Raspberry sollen die Daten von der seriellen Schnittstelle an einen MQTT Broker weitergeleitet werden.
Der Broker läuft auf auf dem Raspberry. Vom Raspberry aus sollen die Daten an drei verschiedene Aktoren übermittelt werden.
### Aktoren
1. LC-Display: Das Display soll den Wert anzeigen
2. LED (Schwellenwert): Wenn die Werte einen gewissen Wert überschreiten / unterschreiten soll die LED Lampe ein oder ausgeschaltet werden.
3. Websocket: Der Wert soll über eine Website angezeigt werden. Dazu können Websockets verwendet werden.

## Voraussetzungen
Für dieses Projekt setzen wir folgende Software/Hardware voraus:
* Arduino/Genuino Uno (andere Version ist auch ok, Quellcode muss aber eventuell angepasst werden)
* LC-Display 16x2 *
* Leuchtdiode & 220 Ohm Widerstand *
* Potentiometer 10 kOhm *
* Diverse Jumperkabel *
* Raspberry Pi 2
* Raspbian Jessie Lite auf SD-Karte vorinstalliert. Wir verzichten hier auf das GUI, da alle Schritte via SSH vorgenommen werden können.
* git client (ist standardmässig nicht vorinstalliert, also kurz: `sudo apt-get install git`)
* python 2.7
* python-dev 2.7 (`sudo apt-get install python-dev`)
* pip (PyPA, Package Manager für Python)
* Virtualenv (`pip install virtualenv`)

\* Inhalt des Arduino Starter Kit

## LC-Display an Raspberry Pi

| LCD Pin | an RPi GPIO          | Beschreibung                                           |
|---------|----------------------|--------------------------------------------------------|
| 1. VSS  | Pin 6 (GND)          | Versorgunsspannung (Masse)                             |
| 2. VDD  | Pin 2 (5V)           | Versorgunsspannung 5V                                  |
| 3. V0   | Pin 6 (GND)          | Kontrastspannung                                       |
| 4. RS   | Pin 22 (GPIO25)      | Registerauswahl (0: Befehlsregister, 1: Datenregister) |
| 5. RW   | Pin 6 (GND)          | Read/Write (0: Write Modus, 1: Read Modus)             |
| 6. E    | Pin 11 (GPIO17)      | Taktflanke                                             |
| 7. D0   | –                    | Datenleitung 0                                         |
| 8. D1   | –                    | Datenleitung 1                                         |
| 9. D2   | –                    | Datenleitung 2                                         |
| 10. D3  | –                    | Datenleitung 3                                         |
| 11. D4  | Pin 12 (GPIO18)      | Datenleitung 4                                         |
| 12. D5  | Pin 15 (GPIO22)      | Datenleitung 5                                         |
| 13. D6  | Pin 16 (GPIO23)      | Datenleitung 6                                         |
| 14. D7  | Pin 18 (GPIO24)      | Datenleitung 7                                         |
| 15. A   | Pin 2 (5V) (220 Ohm) | Hintergrundbeleuchtung Anode                           |
| 16. K   | Pin 6 (GND)          | Hintergrundbeleuchtung Kathode                         |

## Arduino
Der Potentiometer ist mit A0 verbunden. Der Sketch muss im Voraus auf den Arduino geladen werden.

## LED
Das zusätzliche LED befindet sich auf Pin 29 (GPIO5) und wird mit einem 220 Ohm Widerstand geschützt.

# Installation

Für das Projekt arbeiten wir in einem neuen Verzeichnis. Wenn nichts anderes vermerkt ist, so befinden wir uns in diesem. (`~/challp-arduino`)

## Virtualenv vorbereiten

Um Konflikte mit anderen Paketen und Python-Installationen vorzubeugen setzen wir auf Virtualenv (mehr Infos unter https://virtualenv.pypa.io/en/latest/).
```
virtualenv challp-env
source challp-env/bin/activate
pip install paho-mqtt pyserial RPLCD rpi.gpio
```

Für die spätere Verwendung sollte jeweils in der virtuellen Umgebung gearbeitet werden.
```
source challp-env/bin/activate
```

Verlassen der virtuellen Umgebung.
```
deactivate
```

## emqtt - Erlang MQTT Broker

Da keine Binärpakete für den Raspberry Pi bereitstehen, müssen diese selber kompiliert werden. Leider ist das Erlang-Paket und all seine Abhängigkeiten über 300 MB bross, weshalb es etwas dauern könnte.

```
git clone https://github.com/emqtt/emqttd.git
cd emqttd
git submodule update --init --recursive
make && make dist
```

Anscheinend existiert ein Bug im Erlang-Paket und es erscheint folgender Fehler:
```
==> rel (generate)
ERROR: Unable to generate spec: read file info /usr/lib/erlang/man/man3/cerfcf.3.gz failed
ERROR: Unexpected error: rebar_abort
ERROR: generate failed while processing /home/pi/challp-arduino/emqttd/rel: rebar_abort
Makefile:36: recipe for target 'rel' failed
make: *** [rel] Error 1
```
**Workaround**, welcher uns zum Ziel brachte:
```
sudo rm /usr/lib/erlang/man/man3/cerfc* -rf
make && make dist
```

Für Debian/Ubuntu/Windows können die Binärpakete heruntergeladen werden. Siehe http://emqtt.io/downloads
```
wget http://emqtt.io/downloads/debian -O emqttd-debian.zip
unzip emqttd-debian.zip
```

Der Broker verfügt über eine umfassende Dokumentation unter http://emqttd-docs.readthedocs.org.

## Projekt klonen

Wer hätte es vermutet?
```
git clone https://github.com/rehrbar/ChallP2ArduinoLab.git
```

# Ausführen

## Broker
Start des Broker in daemon-mode:
```
cd ~/challp-arduino/emqttd/rel/emqttd/bin/
./emqttd start
```
Danach ist das Webinterface unter `http://<IP des Raspberry PI>:18083` erreichbar.  
Benutzername/Passwort: admin/public

Der Broker kann nach der Verwendung wieder mit `./emqtt stop` beendet werden.

## Clients
Nun starten wir als erstes den Publish-Client, welcher die Daten von der seriellen Schnittstelle einliest und an den Broker sendet. Anschliessend noch die Subscriber, für LCD, LED und ein Webserver, welcher das Interface für den Websocket bereitstellt.
```
cd ~/challp-arduino/ChallP2ArduinoLab
python publishSerialData.py 1>/dev/null&
python subscriberLCD.py 1>/dev/null&
python subscriberLED.py 1>/dev/null&
python -m SimpleHTTPServer 8080 1>/dev/null&
```

Alternativ kann auch das Skript verwendet werden, um alle Clients gemeinsam zu starten.
```
./start-all.sh
```

Ein `Ctrl+C` stoppt die Skripts, ohne jedoch die Aufräumarbeiten auszuführen. Aus Zeitgründen wurde dies nicht mehr implementiert.
