class TextLine:

    def __init__(self, screen_size, text, font):
        self.screen_size = screen_size
        self.text = text + '      '
        self.font = font
        self.x_shift_max, _ = font.getsize(self.text)
        self.text += self.text[:12]
        self.width_list = [font.getsize(ch)[0] for ch in self.text]
        self.x_offset_list = [sum(self.width_list[:i]) for i in range(len(self.width_list))]
        self.x_shift = 0
        self.shift_wait = 20

    def draw(self, draw, x_offset, y_offset, fill=255):
        for i, ch in enumerate(self.text):
            x1 = self.x_shift + x_offset + self.x_offset_list[i]
            x2 = self.x_shift + x_offset + self.x_offset_list[i] + self.width_list[i]

            if x2 < 0 or x1 > self.screen_size[0]:
                continue
            
            draw.text((x1, y_offset), ch, font=self.font, fill=fill)

    def shift(self, amount=1):
        if self.shift_wait > 0:
            self.shift_wait -= 1
            return

        self.x_shift -= amount
        if self.x_shift < -self.x_shift_max:
            self.x_shift = 0
            self.shift_wait = 10