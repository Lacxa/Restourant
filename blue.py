import bluetooth
from escpos.printer import Usb

def connect_to_printer(address):
    try:
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((address, 1))
        print("Connected to Bluetooth printer")
        return sock
    except bluetooth.btcommon.BluetoothError as e:
        print(f"Error connecting to Bluetooth printer: {e}")
        return None

def print_order_bluetooth(sock, order_data):
    try:
        # Send data to Bluetooth printer
        sock.send(order_data)

        # Additional printing code if needed
        # ...

        print("Order sent to Bluetooth printer")
    except Exception as e:
        print(f"Error printing order: {e}")

    finally:
        if sock:
            sock.close()  # Close the Bluetooth connection

# Replace 'XX:XX:XX:XX:XX:XX' with the actual Bluetooth address of your printer
printer_address = '14:50:51:0D:CF:0B'

# Example order data
order_data = "Order: Burger, Fries, Drink"

# Connect to the Bluetooth printer
bluetooth_socket = connect_to_printer(printer_address)

# Print order if the connection is successful
if bluetooth_socket:
    print_order_bluetooth(bluetooth_socket, order_data)
