from bibliopixel.animation import BaseMatrixAnim
from bibliopixel.colors import hue_helper

from moonpi.audio.audio_stream import AudioStream


class AudioVisualization(BaseMatrixAnim):
    def __init__(self, layout):
        super(AudioVisualization, self).__init__(layout)
        self.stream = AudioStream()
        self.stream.continuous_start()
        self.colors = [hue_helper(y, self.height, 0) for y in range(self.height)]

    def step(self, amt=1):
        self.layout.all_off()
        eq_data = self.stream.fft(self.width, self.height + 1)
        for x in range(self.width):
            for y in range(self.height):
                if y < int(eq_data[x]):
                    self.layout.set(x, self.height - y - 1, self.colors[y])
        # x = 0
        # for y in eq_data:
        #     self._led.drawLine(x, self._led.height - 1, x, self._led.height - int(y), colors.hue_helper(int(y), self._led.height, 0))
        #     x += 1
        self._step = amt
