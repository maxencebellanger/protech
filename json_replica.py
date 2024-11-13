import json
import usb.core
import usb.util

# Load the JSON data from the file
with open('test.json') as f:
    packets = json.load(f)

# Replace with actual vendor and product ID of your target device
DEVICE_VENDOR_ID = 0x3923
DEVICE_PRODUCT_ID = 0x76c6

# Find the USB device
device = usb.core.find(idVendor=DEVICE_VENDOR_ID, idProduct=DEVICE_PRODUCT_ID)

if device is None:
    raise ValueError("Device not found")

def send_usb_control_transfer(device, setup_data, dest):
    """Send control transfer."""
    bmRequestType = int(setup_data["usb.bmRequestType"], 16)
    bRequest = int(setup_data["usb.setup.bRequest"], 10)
    wValue = (int(setup_data.get("usb.DescriptorIndex", "0"), 16) << 8) | int(setup_data.get("usb.bDescriptorType", "0"), 16)
    wIndex = int(setup_data.get("usb.LanguageId", "0"), 16)
    wLength = int(setup_data["usb.setup.wLength"], 10)
    
    print(f"Preparing Control Transfer to {dest}: bmRequestType={bmRequestType}, bRequest={bRequest}, "
          f"wValue={wValue}, wIndex={wIndex}, wLength={wLength}")
    
    try:
        # Send control transfer and get response
        response = device.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, wLength)
        print(f"Control Transfer to {dest}: bmRequestType={bmRequestType}, bRequest={bRequest}, "
              f"wValue={wValue}, wIndex={wIndex}, wLength={wLength}, Response: {response}")
    except usb.core.USBError as e:
        print(f"USB Error (Control): {e}")

def send_usb_bulk_transfer(device, endpoint, data_len, dest):
    """Send bulk transfer."""
    data = [0x00] * data_len  # Placeholder for bulk data, modify as needed
    print(f"Preparing Bulk Transfer to {dest}: endpoint={endpoint}, data_length={data_len}")
    
    try:
        # Write data to the device (bulk transfer)
        device.write(endpoint, data)
        print(f"Bulk Transfer to {dest}: endpoint={endpoint}, data_length={data_len}, Data: {data}")
    except usb.core.USBError as e:
        print(f"USB Error (Bulk Write): {e}")

def read_usb_bulk_transfer(device, endpoint, data_len, dest):
    """Read response for bulk transfer."""
    try:
        # Read the response from the device (on the same endpoint or another)
        response = device.read(endpoint, data_len)
        print(f"Bulk Transfer Response from {dest}: {response}")
    except usb.core.USBError as e:
        print(f"USB Error (Bulk Read): {e}")

def send_usb_interrupt_transfer(device, endpoint, data_len, dest):
    """Send interrupt transfer."""
    data = [0x00] * data_len  # Placeholder for interrupt data, modify as needed
    print(f"Preparing Interrupt Transfer to {dest}: endpoint={endpoint}, data_length={data_len}")
    
    try:
        device.write(endpoint, data)
        print(f"Interrupt Transfer to {dest}: endpoint={endpoint}, data_length={data_len}, Data: {data}")
    except usb.core.USBError as e:
        print(f"USB Error (Interrupt Write): {e}")

def read_usb_interrupt_transfer(device, endpoint, data_len, dest):
    """Read response for interrupt transfer."""
    try:
        response = device.read(endpoint, data_len)
        print(f"Interrupt Transfer Response from {dest}: {response}")
    except usb.core.USBError as e:
        print(f"USB Error (Interrupt Read): {e}")

# Loop over packets and send based on type
for packet in packets:
    usb_layer = packet["_source"]["layers"]["usb"]

    print(f"Processing packet: {packet}")
    
    # Check if the packet is from the host or the device
    if usb_layer["usb.src"] == "host":  # Only process packets sent from host
        transfer_type = usb_layer["usb.transfer_type"]
        dest = usb_layer["usb.dst"]  # Get destination address

        # Handle control transfers (0x00)
        if transfer_type == "0x02" and "Setup Data" in packet["_source"]["layers"]:
            print(f"Control Transfer found (sent to device): {usb_layer}")
            send_usb_control_transfer(device, packet["_source"]["layers"]["Setup Data"], dest)

        # Handle bulk transfers (0x02)
        elif transfer_type == "0x03":
            endpoint = int(usb_layer["usb.endpoint_address"], 16)
            data_len = int(usb_layer["usb.data_len"])
            print(f"Bulk Transfer found (sent to device): endpoint={endpoint}, data_len={data_len}")
            send_usb_bulk_transfer(device, endpoint, data_len, dest)

        # Handle interrupt transfers (0x03)
        elif transfer_type == "0x01":
            endpoint = int(usb_layer["usb.endpoint_address"], 16)
            data_len = int(usb_layer["usb.data_len"])
            print(f"Interrupt Transfer found (sent to device): endpoint={endpoint}, data_len={data_len}")
            send_usb_interrupt_transfer(device, endpoint, data_len, dest)

    else:  # Process packets from the device (response)
        transfer_type = usb_layer["usb.transfer_type"]
        dest = usb_layer["usb.dst"]  # Get destination address

        # Handle control transfers (0x00) - device response
        if transfer_type == "0x02" and "Setup Data" in packet["_source"]["layers"]:
            print(f"Control Transfer found (from device): {usb_layer}")
            send_usb_control_transfer(device, packet["_source"]["layers"]["Setup Data"], dest)

        # Handle bulk transfers (0x03) - device response
        elif transfer_type == "0x03":
            endpoint = int(usb_layer["usb.endpoint_address"], 16)
            data_len = int(usb_layer["usb.data_len"])
            print(f"Bulk Transfer found (from device): endpoint={endpoint}, data_len={data_len}")
            read_usb_bulk_transfer(device, endpoint, data_len, dest)

        # Handle interrupt transfers (0x03) - device response
        elif transfer_type == "0x01":
            endpoint = int(usb_layer["usb.endpoint_address"], 16)
            data_len = int(usb_layer["usb.data_len"])
            print(f"Interrupt Transfer found (from device): endpoint={endpoint}, data_len={data_len}")
            read_usb_interrupt_transfer(device, endpoint, data_len, dest)
