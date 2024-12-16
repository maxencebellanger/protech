import nidaqmx
from nidaqmx.constants import AcquisitionType, READ_ALL_AVAILABLE
import matplotlib.pyplot as plt

#with nidaqmx.Task() as task:
#  task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
#  task.timing.cfg_samp_clk_timing(1000.0, sample_mode=AcquisitionType.FINITE, samps_per_chan=50)
#  data = task.read(READ_ALL_AVAILABLE)
#
#  plt.plot(data)
#  plt.ylabel('Amplitude')
#  plt.title('Waveform')
#  plt.show()

connected_devices = nidaqmx.system.System.local().devices
print(connected_devices.device_names)a