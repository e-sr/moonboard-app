import threading
import time
from collections import deque

import numpy
import pyaudio


class AudioStream:
    """Simple, cross-platform class to record from the microphone."""

    RATE = 48100
    """Desired refresh rate of the visualization (frames per second)"""
    BUFFER_SIZE = 2 ** 12  # 4069 is a good buffer size

    def __init__(self):
        """minimal garb is executed when class is loaded."""
        self.RATE = 48100
        self.BUFFER_SIZE = 2 ** 12  # 4069 is a good buffer size
        self.secToRecord = .1
        self.threadsDieNow = False
        self.newAudio = False
        self.maxVals = deque(maxlen=500)

    def setup(self):
        """initialize sound card."""
        self.buffersToRecord = int(self.RATE * self.secToRecord / self.BUFFER_SIZE)
        if self.buffersToRecord == 0: self.buffersToRecord = 1
        self.samplesToRecord = int(self.BUFFER_SIZE * self.buffersToRecord)
        self.chunksToRecord = int(self.samplesToRecord / self.BUFFER_SIZE)
        self.secPerPoint = 1.0 / self.RATE

        self.p = pyaudio.PyAudio()
        self.inStream = self.p.open(format=pyaudio.paInt16, channels=1, rate=self.RATE, input=True, output=False,
                                    frames_per_buffer=self.BUFFER_SIZE)

        self.xsBuffer = numpy.arange(self.BUFFER_SIZE) * self.secPerPoint
        self.xs = numpy.arange(self.chunksToRecord * self.BUFFER_SIZE) * self.secPerPoint
        self.audio = numpy.empty((self.chunksToRecord * self.BUFFER_SIZE), dtype=numpy.int16)

    def close(self):
        """cleanly back out and release sound card."""
        self.p.close(self.inStream)

    def get_audio(self):
        """get a single buffer size worth of audio."""
        audio_string = self.inStream.read(self.BUFFER_SIZE)
        return numpy.fromstring(audio_string, dtype=numpy.int16)

    def record(self, forever=True):
        """record secToRecord seconds of audio."""
        while True:
            if self.threadsDieNow: break
            for i in range(self.chunksToRecord):
                self.audio[i * self.BUFFER_SIZE:(i + 1) * self.BUFFER_SIZE] = self.get_audio()
            self.newAudio = True
            if not forever:
                break
            time.sleep(.001)

    def continuous_start(self):
        """CALL THIS to start running forever."""
        self.t = threading.Thread(target=self.record)
        self.t.start()

    def continuous_end(self):
        """shut down continuous recording."""
        self.threadsDieNow = True

    def fft(self, x_max, y_max):
        data = self.audio.flatten()

        left, right = numpy.split(numpy.abs(numpy.fft.fft(data)), 2)
        ys = numpy.add(left, right[::-1])

        # FFT max values can vary widely depending on the hardware/audio setup.
        # Take the average of the last few values which will keep everything
        # in a "normal" range (visually speaking). Also makes it volume independent.
        self.maxVals.append(numpy.amax(ys))

        ys = ys[:x_max]
        m = max(100000, numpy.average(self.maxVals))
        ys = numpy.rint(numpy.interp(ys, [0, m], [0, y_max - 1]))
        print(ys)
        return ys
