# ChallP2ArduinoLab
Dieses Projekt entstand aus der Aufgabenstellung zum Modul Challenge Projekt 2 FS16.

**TODO** Aufgabenstellung näher beschreiben.

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
* pip (PyPA, Package Manager für Python)
* Virtualenv (`pip install virtualenv`)

\* Inhalt des Arduino Starter Kit

# Installation

Für das Projekt arbeiten wir in einem neuen Verzeichnis. Wenn nichts anderes vermerkt ist, so befinden wir uns in diesem. (`~/challp-arduino`)

## Virtualenv vorbereiten

Um Konflikte mit anderen Paketen und Python-Installationen vorzubeugen setzen wir auf Virtualenv (mehr Infos unter https://virtualenv.pypa.io/en/latest/).
```
virtualenv challp-env
source challp-env/bin/activate
pip install paho-mqtt
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

Start des Broker in daemon-mode:
```
cd ~/challp-arduino/emqttd/rel/emqttd/bin/
./emqttd start
```
Danach ist das Webinterface unter `http://<IP des Raspberry PI>:18083` erreichbar.  
Benutzername/Passwort: admin/public

**TODO** Eigentliche ausführung des Projektes erwähnen.
