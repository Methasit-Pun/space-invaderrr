class Button():
    def __init__(self, pos, text_input=None, font=None, image=None, base_color=None, hovering_color=None):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input
        self.image = image

        if self.text_input:
            self.text = self.font.render(self.text_input, True, self.base_color)
            self.rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        elif self.image:
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.text_input:
            screen.blit(self.text, self.rect)
        elif self.image:
            screen.blit(self.image, self.rect)

    def checkForInput(self, position):
        if self.rect.collidepoint(position):
            return True
        return False

    def changeColor(self, position):
        if self.rect.collidepoint(position):
            if self.text_input:
                self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            if self.text_input:
                self.text = self.font.render(self.text_input, True, self.base_color)

