import pygame as pg

import pygame as pg

class Obj:
    def __init__(self, image_idle, x, y, animated=False):
        self.group = pg.sprite.Group()
        self.sprite = pg.sprite.Sprite(self.group)

        self.animated = animated
        self.image_idle = pg.image.load(image_idle).convert_alpha()

        if animated:
            self.frames = [
                pg.image.load(f"Assets/Sprites/MarioRun{i}.png").convert_alpha()
                for i in range(3)
            ]
            self.current_frame = 0
            self.animation_timer = 0
        else:
            self.frames = []

        self.facing_left = False  # controle do lado

        self.sprite.image = self.image_idle
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.topleft = (x, y)

    def draw(self, window):
        self.group.draw(window)

    def update_position(self, dx, dy):
        self.sprite.rect.x += dx
        self.sprite.rect.y += dy

    def animate(self, moving):
        if not self.animated:
            return
    
        if moving:
            self.animation_timer += 1
            if self.animation_timer >= 8:  # controla a velocidade da animação
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.animation_timer = 0
            frame = self.frames[self.current_frame]
            if self.facing_left:
                frame = pg.transform.flip(frame, True, False)
            self.sprite.image = frame
        else:
            idle_img = self.image_idle
            if self.facing_left:
                idle_img = pg.transform.flip(idle_img, True, False)
            self.sprite.image = idle_img


    def set_y(self, y):
        self.sprite.rect.y = y

    def get_rect(self):
        return self.sprite.rect


class Bloco:
    def __init__(self, x, y, tipo="brown"):
        if tipo == "brown":
            imagem = "BrickBlockBrown.png"
        elif tipo == "castle":
            imagem = "BrickBlockCastle.png"
        elif tipo == "dark":
            imagem = "BrickBlockDark.png"
        else:
            raise ValueError(f"Tipo de bloco desconhecido: {tipo}")

        self.image = pg.image.load(f"Assets/Sprites/{imagem}").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, window, camera_x):
        window.blit(self.image, (self.rect.x - camera_x, self.rect.y))

    def get_rect(self):
        return self.rect

