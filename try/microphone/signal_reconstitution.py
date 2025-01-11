import numpy as np
from scipy.io.wavfile import write

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




