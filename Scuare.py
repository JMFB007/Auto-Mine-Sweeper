import pygame

#visible flagged type checked posiblemines probab arround
class Scuare(pygame.sprite.Sprite):
    def __init__(self, image, rect, size):
        super().__init__()
        self.visible = False
        self.flagged = False
        self.checked = False
        self.high = False
        self.image = image#
        self.rect = rect#
        self.size = size#
        self.posiblemines = 0
        self.probab = 0
        self.type = "empty"
        self.arround = []

    def copy(self):#the arround might annoy
        copy = Scuare(self.image, self.rect, self.size)
        copy.visible = self.visible
        copy.flagged = self.flagged
        copy.checked = self.checked
        copy.high = self.high
        copy.posiblemines = self.posiblemines
        copy.probab = self.probab
        copy.type = self.type
        copy.arround = self.arround
        return copy

    def __str__(self):
        return str(self.type)