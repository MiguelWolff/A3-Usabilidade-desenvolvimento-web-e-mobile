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

        # Posição lógica do Mario no mundo
        self.mario_world_x = 0
        self.mario_screen_x = 50  # posição fixa na tela
        self.mario_y = altura - 120

        # Mario (posição inicial)
        self.mario = Obj("Assets/Sprites/Mario.png", self.mario_screen_x, self.mario_y)

        # Goomba no mundo
        self.goomba = Goomba(300, altura - 45)
        self.goomba_vivo = True

    def draw(self, window):
        window.fill(AZUL)

        # Câmera segue a posição lógica do Mario
        camera_x = self.mario_world_x - self.mario_screen_x

        # Chão (bem longo, exemplo 2000px)
        pg.draw.rect(window, VERDE, (0 - camera_x, self.ALTURA - 30, 2000, 30))

        # Goomba (movido com a câmera)
        if self.goomba_vivo:
            self.goomba.draw(window, camera_x)

        # Mario sempre fixo na tela
        self.mario.sprite.rect.x = self.mario_screen_x
        self.mario.draw(window)

    def update(self):
        # Atualiza posição no mundo
        self.mario_world_x += self.vel_x
        self.mario.update_position(0, self.vel_y)  # x = 0, pois posição X está fixa
        self.vel_y += self.gravidade

        # Gravidade e chão
        mario_rect = self.mario.get_rect()
        if mario_rect.bottom >= self.ALTURA - 30:
            mario_rect.bottom = self.ALTURA - 30
            self.vel_y = 0
            self.no_chao = True

        # Atualizar Goomba
        if self.goomba:
            self.goomba.update(2000)

        # Colisão com Goomba
        camera_x = self.mario_world_x - self.mario_screen_x
        mario_real_rect = mario_rect.copy()
        mario_real_rect.x = self.mario_world_x  # posição no mundo

        if self.goomba:
            camera_x = self.mario_world_x - self.mario_screen_x
            mario_real_rect = mario_rect.copy()
            mario_real_rect.x = self.mario_world_x  # posição no mundo

            if mario_real_rect.colliderect(self.goomba.rect):
                # Verifica se Mario está caindo e acima do Goomba
                if self.vel_y > 0 and mario_real_rect.bottom <= self.goomba.rect.top + 10:
                    print("Goomba derrotado!")
                    self.vel_y = -8  # Mario pula após pisar
                    self.goomba = None  # Remove o Goomba
                    self.goomba_vivo = False
                else:
                    print("Mario colidiu com o Goomba (lado ou baixo)")
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
