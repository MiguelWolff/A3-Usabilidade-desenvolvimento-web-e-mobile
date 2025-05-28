import pygame as pg
from obj import Obj, Bloco, Cogumelo
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

        self.mario_world_x = 0
        self.mario_screen_x = 50
        self.mario_y = altura - 120

        self.mario = Obj("Assets/Sprites/Mario.png", self.mario_screen_x, self.mario_y, animated=True)

        self.goomba = Goomba(300, altura - 45)
        self.cogumelo = Cogumelo(200, self.ALTURA - 45)

        # Blocos no mundo
        self.blocos = [
            Bloco(200, altura - 80, tipo="brown"),
            Bloco(250, altura - 80, tipo="castle"),
            Bloco(300, altura - 80, tipo="dark")
        ]

    def draw(self, window):
        window.fill(AZUL)
        camera_x = self.mario_world_x - self.mario_screen_x

        pg.draw.rect(window, VERDE, (0 - camera_x, self.ALTURA - 30, 2000, 30))

        for bloco in self.blocos:
            bloco.draw(window, camera_x)

        if self.goomba:
            self.goomba.draw(window, camera_x)

        if self.cogumelo:
            self.cogumelo.draw(window, camera_x)
            

        self.mario.sprite.rect.x = self.mario_screen_x
        self.mario.draw(window)

    def update(self):
        self.mario_world_x += self.vel_x
        self.mario.update_position(0, self.vel_y)
        self.vel_y += self.gravidade

        mario_rect = self.mario.get_rect()
        mario_real_rect = mario_rect.copy()
        mario_real_rect.x = self.mario_world_x

        # Colisão com o chão
        self.no_chao = True
        if mario_rect.bottom >= self.ALTURA - 30:
            mario_rect.bottom = self.ALTURA - 30
            self.vel_y = 0
            self.no_chao = True

        # Colisão com blocos
        for bloco in self.blocos:
            bloco_rect = bloco.get_rect()

            if mario_real_rect.colliderect(bloco_rect):
                if self.vel_y > 0 and mario_real_rect.bottom <= bloco_rect.top + 10:
                    # Encostou por cima
                    mario_rect.bottom = bloco_rect.top
                    self.vel_y = 0
                    self.no_chao = True
                elif self.vel_y < 0 and mario_real_rect.top >= bloco_rect.bottom - 10:
                    # Bateu por baixo
                    mario_rect.top = bloco_rect.bottom
                    self.vel_y = 0
                    print("Bloco atingido por baixo!")
                elif self.vel_x != 0:
                    # Colisão lateral
                    if self.vel_x > 0:
                        mario_real_rect.right = bloco_rect.left
                    else:
                        mario_real_rect.left = bloco_rect.right
                    self.vel_x = 0
                    self.mario_world_x = mario_real_rect.x

        if self.goomba:
            self.goomba.update(2000)

        if self.cogumelo:
            self.cogumelo.update(self.blocos, self.ALTURA)


        # Colisão com Goomba
        if self.goomba and mario_real_rect.colliderect(self.goomba.rect):
            if self.vel_y > 0 and mario_real_rect.bottom <= self.goomba.rect.top + 10:
                print("Goomba derrotado!")
                self.vel_y = -8
                self.goomba.morrer()
            else:
                print("Mario colidiu com o Goomba (lado ou baixo)")

        if self.goomba and not self.goomba.alive:
            self.goomba = None
        
        self.mario.animate(self.vel_x != 0)

        if self.cogumelo and mario_real_rect.colliderect(self.cogumelo.get_rect()):
            self.mario.crescer()
            self.cogumelo = None

    def events(self, event):
        keys = pg.key.get_pressed()
        self.vel_x = 0
    
        if keys[pg.K_LEFT]:
            self.vel_x = -4
            self.mario.facing_left = True
        elif keys[pg.K_RIGHT]:
            self.vel_x = 4
            self.mario.facing_left = False
    
        if keys[pg.K_SPACE] and self.no_chao:
            self.vel_y = -12
            self.no_chao = False
