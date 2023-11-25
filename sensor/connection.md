The following document provide manual for connecting the peripherals to the 
microcontrollers.

Connections:

    Water Level Sensor:
        Connect the signal pin of the water level sensor to A0 on the Arduino.
        Connect the VCC pin to the 5V pin on the Arduino.
        Connect the GND pin to the GND pin on the Arduino.

    Temperature Sensor:
        Connect the signal pin of the temperature sensor to A1 on the Arduino.
        Connect the VCC pin to the 5V pin on the Arduino.
        Connect the GND pin to the GND pin on the Arduino.

    LED:
        Connect one leg of the LED to pin 13 on the Arduino.
        Connect the other leg to a current-limiting resistor (e.g., 220Ω).
        Connect the other end of the resistor to the GND pin on the Arduino.

    LCD Display (using I2C):
        Connect the SDA pin on the LCD to the SDA pin on the Arduino.
        Connect the SCL pin on the LCD to the SCL pin on the Arduino.
        Connect the VCC pin on the LCD to the 5V pin on the Arduino.
        Connect the GND pin on the LCD to the GND pin on the Arduino.

Note:

    Ensure you have the LiquidCrystal_I2C library installed in your Arduino IDE.
    The I2C address of the LCD may vary depending on the module. The 0x27 address is commonly used. If it doesn't work, try 0x3F.