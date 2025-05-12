import pygame as pg

class Obj:
        
    def __init__(self, image, x, y):
        
        self.group = pg.sprite.Group()
        self.sprite = pg.sprite.Sprite(self.group)

        self.sprite.image = pg.image.load(image)
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect[0] = x
        self.sprite.rect[1] = y
        self.frame = 1
        self.tick = 0
    
    def drawing(self, window):
        self.group.draw(window)
