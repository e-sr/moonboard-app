import threading
import time
from collections import deque

import numpy
import pyaudio

FORMAT = pyaudio.paInt16
# RATE = 44100
# INPUT_BLOCK_TIME = 0.05
# INPUT_FRAMES_PER_BLOCK = int(RATE * INPUT_BLOCK_TIME)

BUFFER_SIZE = 2 ** 12  # 4096 is a good buffer size
secToRecord = .1


class AudioStream:

    def __init__(self):
        self.maxVals = deque(maxlen=500)

        self.pa = pyaudio.PyAudio()
        device_index = self.find_input_device()
        device_info = self.pa.get_device_info_by_index(device_index)
        print('device info: %s' % device_info)
        self.rate = int(device_info['defaultSampleRate'])
        channels = device_info['maxInputChannels']
        self.stream = self.pa.open(format=FORMAT,
                                   channels=channels,
                                   rate=self.rate,
                                   input=True,
                                   output=False,
                                   input_device_index=device_index,
                                   frames_per_buffer=BUFFER_SIZE)

        self.buffersToRecord = int(self.rate * secToRecord / BUFFER_SIZE)
        if self.buffersToRecord == 0:
            self.buffersToRecord = 1
        self.samplesToRecord = int(BUFFER_SIZE * self.buffersToRecord)
        self.chunksToRecord = int(self.samplesToRecord / BUFFER_SIZE)
        self.secPerPoint = 1.0 / self.rate
        self.xsBuffer = numpy.arange(BUFFER_SIZE) * self.secPerPoint
        self.xs = numpy.arange(self.chunksToRecord * BUFFER_SIZE) * self.secPerPoint
        self.audio = numpy.empty((self.chunksToRecord * BUFFER_SIZE), dtype=numpy.int16)

    def find_input_device(self):
        device_index = None
        for i in range(self.pa.get_device_count()):
            dev_info = self.pa.get_device_info_by_index(i)
            print("Device %d: %s" % (i, dev_info["name"]))

            for keyword in ["usb", "mic", "input"]:
                if keyword in dev_info["name"].lower():
                    print("Found an input: device %d - %s" % (i, dev_info["name"]))
                    device_index = i
                    return device_index

        if device_index is None:
            print("No preferred input found; using default input device.")

        return device_index

    def close(self):
        """cleanly back out and release sound card."""
        self.pa.close(self.stream)

    def get_audio(self):
        """get a single buffer size worth of audio."""
        try:
            audio_stream = self.stream.read(BUFFER_SIZE)
        except IOError:
            print('Input overflow')
            audio_stream = numpy.empty((self.chunksToRecord * BUFFER_SIZE), dtype=numpy.int16)

        return numpy.fromstring(audio_stream, dtype=numpy.int16)

    def record(self, forever=True):
        """get a single buffer size worth of audio."""
        while True:
            for i in range(self.chunksToRecord):
                self.audio[i * BUFFER_SIZE:(i + 1) * BUFFER_SIZE] = self.get_audio()
            if not forever:
                break

    def continuous_start(self):
        """CALL THIS to start running forever."""
        self.t = threading.Thread(target=self.record)
        self.t.start()

    # Return power array index corresponding to a particular frequency
    def piff(self, val):
        return int(2 * BUFFER_SIZE * val / self.rate)

    def fft(self):
        data = self.get_audio().flatten()
        # Apply FFT - real data
        fourier = numpy.fft.rfft(data)
        # Remove last element in array to make it the same size as chunk
        fourier = numpy.delete(fourier, len(fourier) - 1)

        # Find average 'amplitude' for specific frequency ranges in Hz
        power = numpy.abs(fourier)
        matrix = [0, 0, 0, 0, 0, 0, 0, 0]
        weighting = [2, 8, 8, 16, 16, 32, 32, 64]

        matrix[0] = int(numpy.mean(power[self.piff(0):self.piff(156):1]))
        matrix[1] = int(numpy.mean(power[self.piff(156):self.piff(313):1]))
        matrix[2] = int(numpy.mean(power[self.piff(313):self.piff(625):1]))
        matrix[3] = int(numpy.mean(power[self.piff(625):self.piff(1250):1]))
        matrix[4] = int(numpy.mean(power[self.piff(1250):self.piff(2500):1]))
        matrix[5] = int(numpy.mean(power[self.piff(2500):self.piff(5000):1]))
        matrix[6] = int(numpy.mean(power[self.piff(5000):self.piff(10000):1]))
        matrix[7] = int(numpy.mean(power[self.piff(10000):self.piff(20000):1]))

        # Tidy up column values for the LED matrix
        matrix = numpy.divide(numpy.multiply(matrix, weighting), 1000000)
        # Set floor at 0 and ceiling at 8 for LED matrix
        matrix = numpy.interp(matrix, (0, matrix.max()), (0, 17)).astype(int)
        return matrix
