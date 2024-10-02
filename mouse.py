import usb.core
import usb.util
import sys

# Find the USB mouse (HID device)
dev = usb.core.find(idVendor=0x046d, idProduct=0xc08d)  # Logitech USB mouse (example)

if dev is None:
    raise ValueError("Mouse not found. Make sure it's connected.")

# Check if the kernel driver is active on interface 0 and detach it
if dev.is_kernel_driver_active(0):
    try:
        dev.detach_kernel_driver(0)
        print("Kernel driver detached")
    except usb.core.USBError as e:
        raise RuntimeError(f"Could not detach kernel driver: {str(e)}")

# Set the active configuration (some devices need this to start communication)
dev.set_configuration()

# Get the first endpoint
cfg = dev.get_active_configuration()
interface = cfg[(0, 0)]

# USB HID devices generally have at least one IN endpoint
endpoint = usb.util.find_descriptor(
    interface,
    custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
)

if endpoint is None:
    raise ValueError("Endpoint not found.")

# Main loop to read data from the mouse
print("Reading data from the mouse... (press Ctrl+C to stop)")
try:
    while True:
        try:
            # Read data from the endpoint
            data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
            # Parse the data (raw HID report)
            print(f"Raw Data: {data}")
        except usb.core.USBError as e:
            if e.errno == 110:  # Timeout error (no data received)
                continue
            else:
                raise e
except KeyboardInterrupt:
    print("\nExiting...")

# Release the device and reattach the kernel driver
usb.util.dispose_resources(dev)
try:
    dev.attach_kernel_driver(0)
    print("Kernel driver reattached")
except usb.core.USBError as e:
    print(f"Could not reattach kernel driver: {str(e)}")
