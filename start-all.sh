#!/bin/bash
python publishSerialData.py 1>/dev/null&
client1=$!
python subscriberLCD.py 1>/dev/null&
client2=$!
python subscriberLED.py 1>/dev/null&
client3=$!
python -m SimpleHTTPServer 8080 1>/dev/null&
client4=$!

function ctrl_c() {
	kill $client1
	kill $client2
	kill $client3
	kill $client4
	exit
}

trap ctrl_c SIGHUP SIGINT SIGTERM

echo "Press [CTRL+C] to stop.."
while :
do
	sleep 1
done

