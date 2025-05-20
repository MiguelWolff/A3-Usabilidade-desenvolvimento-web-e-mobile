import pygame as pg
from obj import Obj
import random

AZUL = (135, 206, 235)
VERDE = (34, 139, 34)
BRANCO = (255, 255, 255)
VERDE_CLARO = (0, 200, 0)

class Game:
    def __init__(self):
        pass

    def jogo():
    
        vel_x = 0
        gravidade = 1
        vel_y = 0
        no_chao = True

        rodando = True

    def controles():
        # Controles
        teclas = pg.key.get_pressed()
        vel_x = 0
        if teclas[pg.K_LEFT]:
            vel_x = -5
        if teclas[pg.K_RIGHT]:
            vel_x = 5
        if teclas[pg.K_SPACE] and no_chao:
            vel_y = -15
            no_chao = False

        # Movimento
        mario_rect.x += vel_x
        mario_rect.y += vel_y
        vel_y += gravidade

        # Colisão com chão
        if mario_rect.bottom >= ALTURA - 50:
            mario_rect.bottom = ALTURA - 50
            vel_y = 0
            no_chao = True

        # Desenha chão
        pygame.draw.rect(tela, VERDE, (0, ALTURA - 50, LARGURA, 50))

        # Desenha Mario
        tela.blit(mario_img, mario_rect)