int sensorValue = 0;  // variable to store the value coming from the sensor
int sensorPin = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  // read the value from the sensor:
  sensorValue = analogRead(sensorPin);
  Serial.print("pot0:");
  Serial.println(sensorValue);
  delay(500); // delay for stability
}
