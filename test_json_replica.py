import json

# Load the JSON data from the file
with open('test.json') as f:
    packets = json.load(f)

def print_usb_control_transfer(setup_data, dest):
    """Print control transfer details."""
    bmRequestType = int(setup_data["usb.bmRequestType"], 16)
    bRequest = int(setup_data["usb.setup.bRequest"], 10)
    wValue = (int(setup_data.get("usb.DescriptorIndex", "0"), 16) << 8) | int(setup_data.get("usb.bDescriptorType", "0"), 16)
    wIndex = int(setup_data.get("usb.LanguageId", "0"), 16)
    wLength = int(setup_data["usb.setup.wLength"], 10)
    
    print(f"Control Transfer: dest={dest}, bmRequestType={bmRequestType}, bRequest={bRequest}, "
          f"wValue={wValue}, wIndex={wIndex}, wLength={wLength}")

def print_usb_bulk_transfer(endpoint, data_len, dest):
    """Print bulk transfer details."""
    print(f"Bulk Transfer: dest={dest}, endpoint={endpoint}, data_length={data_len}")

def print_usb_interrupt_transfer(endpoint, data_len, dest):
    """Print interrupt transfer details."""
    print(f"Interrupt Transfer: dest={dest}, endpoint={endpoint}, data_length={data_len}")

# Loop over packets and print based on type
for packet in packets:
    usb_layer = packet["_source"]["layers"]["usb"]

    if usb_layer["usb.src"] == "host":  # Only process packets sent from host
        transfer_type = usb_layer["usb.transfer_type"]
        dest = usb_layer["usb.dst"]  # Get destination address

        # Handle control transfers (0x00)
        if transfer_type == "0x02" and "Setup Data" in packet["_source"]["layers"]:
            print_usb_control_transfer(packet["_source"]["layers"]["Setup Data"], dest)

        # Handle bulk transfers (0x02)
        elif transfer_type == "0x03":
            endpoint = int(usb_layer["usb.endpoint_address"], 16)
            data_len = int(usb_layer["usb.data_len"])
            print_usb_bulk_transfer(endpoint, data_len, dest)

        # Handle interrupt transfers (0x03)
        elif transfer_type == "0x01":
            endpoint = int(usb_layer["usb.endpoint_address"], 16)
            data_len = int(usb_layer["usb.data_len"])
            print_usb_interrupt_transfer(endpoint, data_len, dest)
