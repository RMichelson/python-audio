import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt

CHUNK = 1024 * 4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK,
    input_device_index=3
)

plt.ion()  # Enable interactive mode

fig, ax = plt.subplots()

x = np.arange(0, 2 * CHUNK, 2)
line, = ax.plot(x, np.random.rand(CHUNK))
ax.set_ylim(-32768, 32767)  # Set y-axis limits based on the possible range of audio data
ax.set_xlim(0, CHUNK)

# Initialize a buffer for moving average
buffer_size = 10000
buffer = np.zeros(buffer_size)

while True:
    data = stream.read(CHUNK)
    data_int = np.frombuffer(data, dtype=np.int16)
    
    # Update the moving average buffer
    buffer[:-1] = buffer[1:]
    buffer[-1] = np.mean(np.abs(data_int))
    # Adjust y-axis limits dynamically based on the moving average
    y_max = np.max(buffer)
    ax.set_ylim(-y_max, y_max)

    line.set_ydata(data_int)
    fig.canvas.draw()
    fig.canvas.flush_events()
