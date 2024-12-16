import usb.core
import usb.util
import time

# Device Vendor and Product IDs (based on the descriptor you provided)
VENDOR_ID = 0x3923
PRODUCT_ID = 0x76c6

# Endpoint addresses (as per the descriptor)
BULK_IN_ENDPOINT_1 = 0x81  # First bulk IN endpoint
BULK_IN_ENDPOINT_2 = 0x82  # Second bulk IN endpoint (optional)
BULK_OUT_ENDPOINT_1 = 0x01  # First bulk OUT endpoint
BULK_OUT_ENDPOINT_2 = 0x03  # Second bulk OUT endpoint (optional)

# Find the USB device
dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

if dev is None:
    raise ValueError('Device not found')

# Set the active configuration. With no arguments, the first configuration will be the active one.
dev.set_configuration()

# Claim the interface (usually interface 0)
interface = 0
usb.util.claim_interface(dev, interface)

# Helper function to send a command (if required)
def send_command(command_data):
    """
    Sends a command to the device using the bulk OUT endpoint.
    """
    try:
        # Sending command data to the device over bulk OUT endpoint
        dev.write(BULK_OUT_ENDPOINT_2, command_data)
        print("Command sent:", command_data)
    except usb.core.USBError as e:
        print(f"Error sending command: {e}")

# Helper function to read data from the bulk IN endpoint
def read_data():
    """
    Reads data from the device using the bulk IN endpoint.
    """
    try:
        # Read from bulk IN endpoint 0x81 (this could be 0x82 for a second stream)
        data = dev.read(BULK_IN_ENDPOINT_2, 64, timeout=1000)
        print("Data read:", data)
        return data
    except usb.core.USBError as e:
        if e.errno == 110:  # Timeout error code
            print("Read timeout")
        else:
            print(f"Error reading data: {e}")

# Optional: You may need to send an initialization command or start the data stream
# This depends on reverse-engineering the device's protocol
# Example command (this is placeholder data - you'll need to determine the correct command)
init_command = [0x01, 0x00, 0x00]  # Example command bytes
send_command(init_command)

# Continuously read data (assuming a continuous stream from the device)
try:
    while True:
        data = read_data()
        if data:
            # Process or print the data here
            print("Received Data:", data)
        time.sleep(1)  # Adjust the sleep interval as needed
except KeyboardInterrupt:
    print("Data acquisition stopped")

# Release the device
usb.util.release_interface(dev, interface)
