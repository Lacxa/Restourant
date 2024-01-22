import bluetooth

target_address = '00:11:22:33:44:55'  # Replace with your POS device's Bluetooth address

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((target_address, 1))


from escpos.printer import Usb

printer = Usb(0x0416, 0x5011)  # Replace with your printer's USB vendor and product IDs

# Send print commands
printer.text("Order: Burger, Fries, Drink\n")
printer.cut()


try:
    # Your Bluetooth and printing code here
    pass
except Exception as e:
    print("Error:", str(e))
finally:
    sock.close()  # Close the Bluetooth connection

