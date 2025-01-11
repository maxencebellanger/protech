import numpy as np
from scipy.io.wavfile import write
import matplotlib.pyplot as plt

sample_rate = 44100  

with open('Micrologs.txt', 'r') as file:
    content = file.read()

blocks = content.split("------")

all_audio_data = []

for i, block in enumerate(blocks):
    data = block.strip().split()
    if not data:
        continue

    try:
        audio_data = np.array(list(map(int, data)), dtype=np.int16)
        all_audio_data.append(audio_data)
    except ValueError:
        print(f"Skipping block {i} due to non-integer values.")
        continue

combined_audio = np.concatenate(all_audio_data)

output_filename = "combined_audio.wav"
write(output_filename, sample_rate, combined_audio)
print(f"Saved combined audio file as {output_filename}")


normalized_audio = combined_audio / np.max(combined_audio)
fft_audio = np.fft.fft(normalized_audio)
fft_audio = fft_audio[:sample_rate//2]
fft_audio_normalized = fft_audio / np.max(fft_audio)

plt.figure()
plt.subplot(1,2,1)
plt.plot(normalized_audio)
plt.title("Sound wave")

plt.subplot(1,2,2)
plt.plot(fft_audio_normalized)
for k in range(1, 51):
    if k == 1:
        plt.axvline(x=440 * k, color='r', linestyle='--', linewidth=0.8, label="'A' harmonics")
    else:
        plt.axvline(x=440 * k, color='r', linestyle='--', linewidth=0.8)

plt.axvline(x=np.where(fft_audio_normalized==1), color="g", label="Max")
plt.legend(loc="upper right")
plt.title("Fourier Transform")
plt.show()




