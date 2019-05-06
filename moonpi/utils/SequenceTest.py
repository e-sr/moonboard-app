from bibliopixel.animation.matrix import Matrix
from bibliopixel.colors import COLORS


class SequenceTest(Matrix):
    def __init__(self, layout):
        super().__init__(layout)
        self.colors = [COLORS.Red, COLORS.Green, COLORS.Blue]

    def step(self, amt=1):
        self.layout.all_off()
        already_on = 0
        max_light_on = self.cur_step % self.layout.numLEDs
        color_index = (self.cur_step // self.layout.numLEDs) % len(self.colors)
        for y in range(self.height):
            for x in range(self.width):
                if not already_on == max_light_on:
                    self.layout.set(x, y, self.colors[color_index])
                    already_on += 1
        self._step += amt

