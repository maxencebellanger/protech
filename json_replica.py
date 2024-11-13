import json
import usb.core
import usb.util

# Replace with actual vendor and product ID
DEVICE_VENDOR_ID = 0x1234
DEVICE_PRODUCT_ID = 0x5678

# Load the JSON data from the file
with open('Dev1ai0_Continu_Différentielle_10-10_100-10.json') as f:
    packets = json.load(f)

# # Find the USB device
# device = usb.core.find(idVendor=DEVICE_VENDOR_ID, idProduct=DEVICE_PRODUCT_ID)

# if device is None:
#     raise ValueError("Device not found")

def send_usb_control_transfer(device, packet):
    try:
        setup_data = packet["_source"]["layers"].get("Setup Data")
        if setup_data:
            # Extract control transfer fields from JSON packet data
            bmRequestType = int(setup_data["usb.bmRequestType"], 16)
            bRequest = int(setup_data["usb.setup.bRequest"], 10)
            wValue = int(setup_data.get("usb.DescriptorIndex", "0"), 16) << 8 | int(setup_data.get("usb.bDescriptorType", "0"), 16)
            wIndex = int(setup_data.get("usb.LanguageId", "0"), 16)
            wLength = int(setup_data["usb.setup.wLength"], 10)

            # Send control transfer to the USB device
            # response = device.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, wLength)
            print(f"Sent control transfer type {bmRequestType}: bmRequestType={bmRequestType}, bRequest={bRequest}, wValue={wValue}, wIndex={wIndex}, wLength={wLength}")
    except usb.core.USBError as e:
        print("USB Error:", e)

# Loop over packets and send only host-to-device messages
device =0
for packet in packets:
    usb_layer = packet["_source"]["layers"]["usb"]
    if usb_layer["usb.src"] == "host":
        send_usb_control_transfer(device, packet)
