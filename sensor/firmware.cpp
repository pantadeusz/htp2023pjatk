#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Define pin numbers for LED, water level sensor, and temperature sensor
const int ledPin = 13;
const int waterLevelPin = A0;  // Analog pin for water level sensor
const int tempSensorPin = A1;  // Analog pin for temperature sensor

// Define LCD address and dimensions
const int lcdAddress = 0x27;  // I2C address for the LCD
const int lcdColumns = 16;
const int lcdRows = 2;
LiquidCrystal_I2C lcd(lcdAddress, lcdColumns, lcdRows);

void setup() {
  pinMode(ledPin, OUTPUT);

  // Initialize the LCD
  lcd.begin(lcdColumns, lcdRows);
  lcd.backlight();

  // Start the serial communication
  Serial.begin(9600);
}

void loop() {
  // Read water level (assuming analog sensor)
  int waterLevel = analogRead(waterLevelPin);

  // Read temperature (assuming analog sensor)
  int tempReading = analogRead(tempSensorPin);
  float temperature = map(tempReading, 0, 1023, 0, 500) / 10.0;  // Map the analog reading to temperature in degrees Celsius

  // Display data on LCD
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Water: ");
  lcd.print(waterLevel);

  lcd.setCursor(0, 1);
  lcd.print("Temp: ");
  lcd.print(temperature);
  lcd.print(" C");

  // Turn the LED on if water level is below a threshold (adjust as needed)
  if (waterLevel < 500) {
    digitalWrite(ledPin, HIGH);
  } else {
    digitalWrite(ledPin, LOW);
  }

  // Send data to host via serial port
  Serial.print("Water Level: ");
  Serial.print(waterLevel);
  Serial.print(", Temperature: ");
  Serial.print(temperature);
  Serial.println(" C");

  // Wait for 1 second
  delay(1000);
}
