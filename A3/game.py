import pygame as pg
from obj import Obj
from enemies import Goomba

AZUL = (135, 206, 235)
VERDE = (34, 139, 34)

class Game:
    def __init__(self, largura, altura):
        self.LARGURA = largura
        self.ALTURA = altura

        self.change_scene = False
        self.gravidade = 1
        self.vel_y = 0
        self.vel_x = 0
        self.no_chao = True

        # Mario
        self.mario = Obj("Assets/Sprites/Mario.png", 50, altura - 120)

        # Goomba
        self.goomba = Goomba(250, altura - 45)
        self.goomba_vivo = True

    def draw(self, window):
        window.fill(AZUL)

        # Chão
        pg.draw.rect(window, VERDE, (0, self.ALTURA - 30, self.LARGURA, 30))

        # Mario
        self.mario.draw(window)

        # Goomba
        if self.goomba_vivo:
            self.goomba.draw(window)

    def update(self):
        # Atualizar posição do Mario
        self.mario.update_position(self.vel_x, self.vel_y)
        self.vel_y += self.gravidade

        mario_rect = self.mario.get_rect()
        if mario_rect.bottom >= self.ALTURA - 30:
            mario_rect.bottom = self.ALTURA - 30
            self.vel_y = 0
            self.no_chao = True

        # Atualizar Goomba
        if self.goomba_vivo:
            self.goomba.update(self.LARGURA)

        # Colisão com Goomba
        if self.goomba_vivo and mario_rect.colliderect(self.goomba.rect):
            if self.vel_y > 0 and mario_rect.bottom <= self.goomba.rect.top + 10:
                # Pula na cabeça do Goomba
                self.goomba_vivo = False
                self.vel_y = -8  # Mario pula depois de esmagar
            else:
                print("Mario foi atingido pelo Goomba!")

    def events(self, event):
        keys = pg.key.get_pressed()
        self.vel_x = 0

        if keys[pg.K_LEFT]:
            self.vel_x = -4
        elif keys[pg.K_RIGHT]:
            self.vel_x = 4

        if keys[pg.K_SPACE] and self.no_chao:
            self.vel_y = -12
            self.no_chao = False
