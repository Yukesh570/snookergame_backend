import serial
import time
from django.dispatch import Signal

button_state_changed = Signal()

# Define a global variable to store the button state
global_button_state = ""

def read_button_state(serial_port):
    global global_button_state
    try:
        while True:
            if serial_port.in_waiting > 0:
                button_state = serial_port.readline().decode('utf-8').strip()
                global_button_state = button_state
                button_state_changed.send(sender=None, button_state=button_state)
                print(f"the value is= {button_state}")
                
    except KeyboardInterrupt:
        print("Exiting program")

if __name__ == '__main__':
    # Replace 'COM7' with the correct serial port for your Arduino
    arduino_port = 'COM7'
    baud_rate = 9600

    try:
        serial_port = serial.Serial(arduino_port, baud_rate, timeout=1)
        print(f"Connected to {arduino_port} at {baud_rate} baud.")
        read_button_state(serial_port)
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
