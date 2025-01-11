import usb.core
import usb.util

# Locate the NI 6003 device
dev = usb.core.find(idVendor=0x3923, idProduct=0x76c6)

# Check if the device is connected
if dev is None:
    raise ValueError("Device not found")

# Initialize the device
try:
    dev.ctrl_transfer(
        bmRequestType=0x00,   # OUT direction, Standard type, Device recipient
        bRequest=0x09,        # Initialization request
        wValue=0x0100,        # Configuration value
        wIndex=0x00,          # Interface index
        data_or_wLength=0,    # No data for setup phase
        timeout=5000          # Set timeout to handle potential delays
    )
except usb.core.USBError as e:
    print(f"Error during initialization: {e}")
    raise

# Send a data request packet to ask for data from the NI 6003
try:
    request_type_in = usb.util.build_request_type(
        usb.util.CTRL_IN, usb.util.CTRL_TYPE_STANDARD, usb.util.CTRL_RECIPIENT_DEVICE
    )

    data_packet = dev.ctrl_transfer(
        request_type_in,
        0x06,                # GET_DESCRIPTOR request to request data
        (0x03 << 8 ),         # Descriptor type (0x03) and index (0x00)
        0x0409,              # Language ID
        18,                  # Expected length of response
        timeout=5000         # Timeout to avoid hanging
    )

    print("Received data:", data_packet)

except usb.core.USBError as e:
    print(f"Error during data request: {e}")