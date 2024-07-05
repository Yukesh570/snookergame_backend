import serial
import time
from django.dispatch import Signal
from django.http import JsonResponse
from .views import stop_timer,start_timer,Check_timer,watch_timer
from django.shortcuts import render ,get_object_or_404
from .models import *
from decimal import Decimal

button_state_changed = Signal()

# Define a global variable to store the button state
global_button_state = ""
running = False
toople=False
def read_button_state(serial_port,request,pk):
    table=get_object_or_404(Table,tableno=pk)

    global global_button_state, running,toople
    try:
        while True:
            if serial_port.in_waiting > 0:
                button_state = serial_port.readline().decode('utf-8').strip()

        

                if button_state == "1":
                
                        # Start action
                        print("Started")
                        start_timer(request,pk)
                        watch_timer(request,pk)
                        toople=True
                    

                        
                elif button_state == "0":
                    if toople:
                        print("Stopped")
                        stop_timer(request,pk)
                      
                        toople=False
                        
                        
                        break   
                

                # elif button_state==1:
                #             if button_state == "0":
                #                 if not running:
                #                     # Start action
                #                     print("Started")
                #                     toople=True
                #                 else:
                #                     # Stop action
                #                     running = False

                #                     print("Stopped")
                #                     break
                #             elif button_state == "1":
                #                 if toople:
                #                     running = True

                    # Wait for the next "1" to toggle state
                    
                print(toople)
                global_button_state = button_state
                button_state_changed.send(sender=None, button_state=button_state)
                print(f"The button state is: {button_state}")
                
    except KeyboardInterrupt:
        print("Exiting program")

def call_read_button_state(request,pk):
    arduino_port = 'COM7'
    baud_rate = 9600

    try:
        serial_port = serial.Serial(arduino_port, baud_rate, timeout=1)
        print(f"Connected to {arduino_port} at {baud_rate} baud.")
        read_button_state(serial_port,request,pk)
        return JsonResponse({'status': 'success'})
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)})
# import serial
# from django.dispatch import Signal

# button_state_changed = Signal()

# # Define global variables to store the button states
# button_state_1 = ""
# button_state_2 = ""
# running = False

# def read_button_states(serial_port):
#     global button_state_1, button_state_2
#     try:
#         while True:
#             if serial_port.in_waiting > 0:
#                 line = serial_port.readline().decode('utf-8').strip()
#                 states = line.split(',')
#                 if len(states) == 2:
#                     button_state_2,button_state_1  = states
#                     button_state_1 = button_state_1.strip()
#                     button_state_2 = button_state_2.strip()
                    
#                     if button_state_1 == "1" :
#                             print("Started")
#                     if button_state_2 == "1":
#                             print("Stopped")
                            

#                     button_state_changed.send(sender=None, button_state_1=button_state_1, button_state_2=button_state_2)
#                     print(f"Button states are: {button_state_1}, {button_state_2}")
                
#     except KeyboardInterrupt:
#         print("Exiting program")
#     finally:
#         serial_port.close()
#         print("Serial port closed.")

# if __name__ == '__main__':
#     # Replace 'COM7' with the correct serial port for your Arduino
#     arduino_port = 'COM7'
#     baud_rate = 9600

#     try:
#         serial_port = serial.Serial(arduino_port, baud_rate, timeout=1)
#         print(f"Connected to {arduino_port} at {baud_rate} baud.")
#         read_button_states(serial_port)
#     except serial.SerialException as e:
#         print(f"Error opening serial port: {e}")
# import serial
# import time

# # Define the serial port (adjust this to your specific port)
# ser = serial.Serial('COM7', 9600, timeout=1)  # COM3 is an example, adjust to your Arduino's port

# # Wait for the serial connection to establish
# time.sleep(2)

# try:
#     while True:
#         # Send a request to read button states
#         ser.write(b'r\n')
        
#         # Read the response
#         response = ser.readline().decode('utf-8').strip()
        
#         # Print the response (format: buttonState1,buttonState2)
#         print(response)
        
#         # Delay before next read
        

# except KeyboardInterrupt:
#     ser.close()  # Close the serial port on Ctrl+C
#     print("Serial connection closed.")
