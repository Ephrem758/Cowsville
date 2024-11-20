import serial
import time

def send_to_gsm_module(string_to_send, port='COM11', baud_rate=115200):
    try:
        # Open the serial port
        ser = serial.Serial(port, baud_rate, timeout=1)
        time.sleep(2)  # Wait for the connection to establish

        # Send the string to the GSM module
        ser.write(string_to_send.encode())

        # Optionally, read response from the GSM module
        response = ser.readline().decode().strip()
        print(f"GSM module responded with: {response}")

        ser.close()
    except Exception as e:
        print(f"Error: {e}")
