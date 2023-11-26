import serial
import threading


def read_serial(port, baudrate):
    try:
        ser = serial.Serial(port, baudrate)
        while True:
            data = ser.readline().decode('utf-8').strip()
            print(f"Received: {data}")
    except serial.SerialException as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Replace 'COM8' and '9600' with your actual serial port and baud rate
    port_name = 'COM8'
    baud_rate = 115200

    # Create a separate thread for reading serial data
    serial_thread = threading.Thread(target=read_serial, args=(port_name, baud_rate), daemon=True)
    serial_thread.start()

    try:
        # Your main application code can go here
        # For this example, we'll just wait for the serial thread to finish
        serial_thread.join()
    except KeyboardInterrupt:
        # Handle Ctrl+C to gracefully exit the program
        print("Exiting program.")