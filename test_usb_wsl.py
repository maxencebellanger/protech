import usb.core
import usb.util
import serial.tools.list_ports

def list_usb_devices():
    # List all connected USB devices
    devices = usb.core.find(find_all=True)
    print("Connected USB devices:")
    for device in devices:
        print(f"Device: {device.idVendor}:{device.idProduct}, Bus: {device.bus}, Address: {device.address}")

def list_serial_ports():
    # List all serial ports in use
    ports = serial.tools.list_ports.comports()
    print("\nSerial ports in use:")
    for port in ports:
        print(f"{port.device} - {port.description}")

if __name__ == "__main__":
    list_usb_devices()
    list_serial_ports()
