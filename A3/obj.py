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

        # Carregar imagem do Mario
        mario_img = pg.image.load("mario.png").convert_alpha()
        mario_rect = mario_img.get_rect()
        mario_rect.topleft = (100, 800 - 150)

    
    def drawing(self, window):
        self.group.draw(window)
