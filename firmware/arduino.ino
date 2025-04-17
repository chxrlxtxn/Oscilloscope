float lowVoltageReadings[50];
float highVoltageReadings[50];
int count = 0;

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(230400);
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input on analog pin 0:
  int lowVoltage = 0;
  int highVoltage = 0;
  lowVoltage = analogRead(A0);
  highVoltage = analogRead(A1); 
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  float voltage5 = 0.0;
  float voltage24 = 0.0;
  voltage5 = lowVoltage * (5.0 / 1023.0);
  voltage24 = highVoltage * ( 5.0 / 1023.0 );
  if (count < 50) {
    lowVoltageReadings[count] = voltage5;
    highVoltageReadings[count] = voltage24;
    count++;
  }

  if (count >= 50) {
    count = 0;
    for (int i = 0; i < 50; i++) {
      Serial.print(lowVoltageReadings[i]);
      Serial.print(", ");
    }
    for (int i = 0; i < 50; i++) {
      if (i < 49) {
        Serial.print(highVoltageReadings[i]);
        Serial.print(", ");
      } else {
        Serial.println(highVoltageReadings[i]);
      }
    }
  }
}

// Author: Sri Tirumalaraju