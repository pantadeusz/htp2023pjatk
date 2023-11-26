// Firmware for controlling the sensor 

const int ledPinGreen = 13;
const int ledPinRed = 12;
const int waterLevelPin = A0;  // Analog pin for water level sensor
const int tempLevelPin = A2;  // Analog pin for water level sensor

// Define LCD address and dimensions
const int lcdAddress = 0x27;  // I2C address for the LCD
const int lcdColumns = 16;
const int lcdRows = 2;

void setup() {
  // put your setup code here, to run once:
  pinMode(ledPinGreen, OUTPUT);
  pinMode(ledPinRed, OUTPUT);
  // Start the serial communication
  Serial.begin(115200);
  Serial.println("I am board created for Hack The Planet");
}

bool polution_detected = false;

void loop() {
  // Read water level (assuming analog sensor)
  int waterLevel = analogRead(waterLevelPin);
  int tempLevel = analogRead(tempLevelPin);
  
   if (waterLevel > 600) {
    Serial.println("Polution detected int the Haalandsvatnet in sensor id:0!");
    digitalWrite(ledPinGreen, LOW);
    digitalWrite(ledPinRed, HIGH);
  }
  else {
    Serial.println("Clean Water!");
    digitalWrite(ledPinGreen, HIGH);
    digitalWrite(ledPinRed, LOW);
  }

  Serial.println("Water Level: ");
  Serial.println(waterLevel);

  Serial.println("Temperature Level ok ");
  //Serial.println(tempLevel);
    // Wait for 1 second
  delay(1000);
}
