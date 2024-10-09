import usb.core
import usb.util

try:
    # Trouver le périphérique USB
    dev = usb.core.find(idVendor=0x3923, idProduct=0x76c6)
    if dev is None:
        raise ValueError('Device not found')

    # Configurer le périphérique
    dev.set_configuration()
    print("Configuration set successfully")

    ## Lire les configurations, interfaces et points de terminaison
    #for cfg in dev:
    #    for i in cfg:
    #        for e in i:
    #            print(e)

    # Lire les données à partir du périphérique
    endpoint = dev[0][(0,0)][0]
    data = dev.ctrl_transfer(0x80, 0x06, 0x0100, 0x0000, 64)
    print(data)

except usb.core.USBError as e:
    print(f"USBError: {e}")
except Exception as e:
    print(f"Error: {e}")