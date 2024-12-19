#!/usr/bin/python
## coding=utf-8
"""
The ni_usb_6003 is a digital IO module for USB from National Instruments.
Unfortunately their Linux driver does not exist.

This python driver is inspired on Marc Schutz's pioneer work on c driver of ni-usb-6003 and Teppo Koskinen work on python drive 
(https://github.com/schuetzm/ni-usb-6501)
(https://github.com/orlof/NI_USB-6501)

INSTALLATION
1. Install the latest PyUSB (at least version 1.0.a3) from http://sourcceforge.net/projects/pyusb/

2. Change the permissions of the USB device node by creating a udev rule.
   e.g. add the following line (and file) to a file in /etc/udev/rules.d/usb.rules
   SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_device", MODE="0664", GROUP="usbusers"

   This will set the owner of the device node to root:usbusers rather than root:root
   After that add user to the usbusers group for enabling access to the device.
   adduser _<user>_ usbusers
  (Make sure you have group usbusers)

...and you are good to go.

"""
import usb.core
import usb.util

ID_VENDOR = 0x3923
ID_PRODUCT = 0x76c6

def get_adapter(**kwargs):
    """
    Returns NiUsb6003 handler if only single adapter is connected to PC.
    Forwards all parameters to pyusb (  )
    """
    device = usb.core.find(idVendor=ID_VENDOR, idProduct=ID_PRODUCT, **kwargs)
    if not device:
        raise ValueError('Device not found')

    return NiUsb6003(device)


    """
    Returns NiUsb6003 handle for every adapter that is connected to PC.
    Forwards all parameters to pyusb (http://pyusb.sourceforge.net/docs/1.0/tutorial.html)
    """
def find_adapters(**kwargs):
    devices = usb.core.find(find_all=True, idVendor=ID_VENDOR, idProduct=ID_PRODUCT, **kwargs)
    if not devices:
        raise ValueError('Device not found')

    return [NiUsb6003(dev) for dev in devices]


class NiUsb6003:
    """
    Typical usage:
      adapter = get_adapter()
      adapter.set_io_mode(0b00000000, 0x11111111, 0x01010101) # one bit per port 1=write, 0=read
      # start calling adapter.read_port(port) and adapter.write_port(port, values)
    """
    def __init__(self, device):
        """ used only internally via get_adapter() and find_adapters() """
        self.device = device
        cfg = self.device.get_active_configuration() 
        interface_number = cfg[(0,0)].bInterfaceNumber
        
        if self.device.is_kernel_driver_active(interface_number):
            self.device.detach_kernel_driver(interface_number)
        # set the active configuration. With no arguments, the first
        # configuration will be the active one
        self.device.set_configuration()
        # This is needed to release interface, otherwise attach_kernel_driver fails 
        # due to "Resource busy"
        usb.util.dispose_resources(self.device)

    def set_io_mode(self, channel, mode, config, freq, sample_base):
        """
        channel: 0 to 8
        mode: 0 finite, 1 on demand, 2 continous
        config: 0 differential, 1 asymetric
        freq: 1 to 1e5
        sample: 1 to +inf
        """

        freq = hex(int(80000000/freq)).split("x")[1]

        sample = hex(sample_base).split("x")[1]

        buf0 = list("\x0d\x30\x00\x00")
        buf0 = ''.join(buf0)

        req0 = self.send_request(0x09, buf0)
        print(req0)

        buf1 = list("\x0d\x30\x00\x00\x00\x03\x00\x00")
        buf1[6] = chr(8+channel)
        buf1 = ''.join(buf1)


        req1 = self.send_request(0x08, buf1)
        print(req1)

        buf2 = list("\x0d\x60\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\x00\x01\x00")
        n = len(freq)
        buf2[7] = freq[-2:]
        for i in range(2, n, 2):
            buf2[7-i//2] = chr(int(freq[-2-i:-i], 16))
        
        m = len(sample)
        buf2[11] = sample[-2:]
        for i in range(2, m, 2):
            buf2[11-i//2] = chr(int(sample[-2-i:-i], 16))

        buf2 = ''.join(buf2)
        req2 = self.send_request(0x09, buf2)
        print(req2)

        buf3 = list("\x00\x02\x00\x02\x00\x00\x00\x00")
        buf3[6] = chr(8+channel)

        sample = hex(2*sample_base).split("x")[1]
        m = len(sample)
        buf3[7] = sample[-2:]
        for i in range(2, m, 2):
            buf3[7-i//2] = chr(int(sample[-2-i:-i], 16))

        buf3 = ''.join(buf3)

        req3 = self.send_request(0x08, buf3)
        print(req3)

        buf4 = list("\x0d\x60\x00\x00")
        buf4 = ''.join(buf4)

        req4 = self.send_request(0x0a, buf4)
        print(req4)

        buf5 = list("\x0d\x60\x00\x00\x00\x00\x00\x00")
        buf5 = ''.join(buf5)

        req5 = self.send_request(0x0b, buf5)
        print(req5)

        buf6 = list("\x0d\x60\x00\x00")
        buf6 = ''.join(buf6)

        req6 = self.send_request(0x0c, buf6)
        print(req6)

        buf7 = list("\x0d\x60\x00\x00")
        buf7 = ''.join(buf7)

        req7 = self.send_request(0x0d, buf7)
        print(req7)

        buf8 = list("\x0d\x60\x00\x00")
        buf8 = ''.join(buf8)

        req8 = self.send_request(0x0e, buf8)
        print(req8)

        buf9 = list("\x0d\x60\x00\x00")
        buf9 = ''.join(buf9)

        req9 = self.send_request(0x0f, buf9)
        print(req9)

        return 0

    def read_port(self, port):
        """
        Read the value from all read-mode pins from one of the 8 PIN ports
        port is 0, 1 or 2
        """
        buf = list("\x02\x10\x00\x00\x00\x03\x00\x00")

        buf[6] = chr(port)
        buf = ''.join(buf)

        response = self.send_request(0x0e, buf)

        self.packet_matches(response,
                            "\x00\x0c\x01\x00\x00\x00\x00\x02\x00\x03\x00\x00",
                            "\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\xff")

        return ord(response[10])

    def write_port(self, port, value):
        """
        Write value to all write-mode pins in one of the 8 PIN ports
        port is 0, 1 or 2
        value is 8 bits represented by integer
        """
        buf = list("\x02\x10\x00\x00\x00\x03\x00\x00\x03\x00\x00\x00")

        buf[6] = chr(port)
        buf[9] = chr(value)
        buf = ''.join(buf)

        response = self.send_request(0x0f, buf)
        self.packet_matches(response,
                            "\x00\x08\x01\x00\x00\x00\x00\x02",
                            "\xff\xff\xff\xff\xff\xff\xff\xff")

        return response

    ##########################################################
    # INTERNAL UTILITY FUNCTIONS
    ##########################################################
    EP_IN, EP_OUT = 0x81, 0x01
    HEADER_PACKET, HEADER_DATA = 4, 4
    INTERFACE = 0

    def send_request(self, cmd, request):
        if len(request) + self.HEADER_PACKET + self.HEADER_DATA > 255:
            raise ValueError('Request too long (%d bytes)' % (len(request) + self.HEADER_PACKET + self.HEADER_DATA))

        buf = list("\x00\x01\x00\x00\x00\x00\x01\x00")

        buf[3] = chr(self.HEADER_PACKET + self.HEADER_DATA + len(request))
        buf[5] = chr(self.HEADER_DATA + len(request))
        buf[7] = chr(cmd)

        buf = ''.join(buf) + request

        if (not self.device.write(self.EP_OUT, buf, self.INTERFACE) == len(buf)):
            pass
        ret = self.device.read(self.EP_IN, len(buf), self.INTERFACE)

        return ''.join([chr(x) for x in ret])[self.HEADER_PACKET:]

    def packet_matches(self, actual, expected, mask):
        if len(actual) != len(expected):
            print(repr(actual))
            print(repr(expected))
            print(repr(mask))
            raise ValueError('Protocol error - invalid response length %d' % len(actual))

        for b, e, m in zip(actual, expected, mask):
            if (ord(b) & ord(m)) != (ord(e) & ord(m)):
                raise ValueError("""Protocol error - invalid response
                actual:   %s
                expected: %s
                mask:     %s
                """ % (repr(actual), repr(expected), repr(mask)))
    
    def release_interface(self):
        """
        Free all resources, then the device can be used once again
        """
        if self.device.is_kernel_driver_active(self.interface_number):
            self.device.detach_kernel_driver(self.interface_number)
        usb.util.release_interface(self.device, self.INTERFACE)
        usb.util.dispose_resources(self.device)
        self.device.reset()
        self.device = None

#USAGE EXAMPLE
if __name__ == "__main__":
    dev = get_adapter()
    
    if not dev:
        raise Exception("No device found")
     
    dev.set_io_mode(1, 0,0,100, 10)
    # 
    # dev.write_port(0, 0b11001100)
    # dev.write_port(1, 0b10101010)
    # 
    # print(bin(dev.read_port(2)))
    # 
    # ret = dev.set_io_mode(0, 255, 0)      # set all pins between 3-6 & 27-30 as output pins
    # example has special fokus on port 3 & 30, the values ot the others are all set to high
    # bitmask: 247: 1111 0111
    # 27: 1     low byte
    # 28: 1     
    # 29: 1     
    # 30: 0
    #  6: 1    
    #  5: 1     
    #  4: 1     
    #  3: 1     high byte

    #   ret = dev.write_port(1, 0)  # both zero
    #   print(dev.read_port(1))
    #   
    #   ret = dev.write_port(1, 247)  # 30 low
    #   print(dev.read_port(1))
    #   
    #   ret = dev.write_port(1, 127)  # 3 low
    #   print(dev.read_port(1))
    #   
    #   ret = dev.write_port(1, 247)  # 30 low
    #   print(dev.read_port(1))
    #   
    #   ret = dev.write_port(1, 127)  # 3 low
    #   print(dev.read_port(1))
    #   
    #   ret = dev.write_port(1, 0)  # both zero
    #   print(dev.read_port(1))
    #   
    #   ret = dev.write_port(1, 255)  # both high
    #   print(dev.read_port(1))
    #   
    #   dev.release_interface()     # clean exit, allows direct reuse without to replug the ni6501
    #   del dev
