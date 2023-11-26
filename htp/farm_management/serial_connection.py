import serial
import threading
import re
from datetime import datetime
from .models import Measurement


def read_serial(port, baudrate):
    try:
        ser = serial.Serial(port, baudrate)
        while True:
            data = ser.readline().decode('utf-8').strip()
            print(f"Received: {data}")

            # Check if the received data contains a number using regular expression
            match = re.search(r'\d+', data)
            if match:
                number = int(match.group())
                print(f"Detected Number: {number}")

                measurement = Measurement.objects.create(
                    date_time=datetime.now(),
                    detected_number=number
                )
                measurement.save()

    except serial.SerialException as e:
        print(f"Error: {e}")


def start_measurement_thread():
    port_name = 'COM8'
    baud_rate = 115200

    # Create a separate thread for reading serial data
    serial_thread = threading.Thread(target=read_serial, args=(port_name, baud_rate),
                                     daemon=True)
    serial_thread.start()


if __name__ == "__main__":
    start_measurement_thread
