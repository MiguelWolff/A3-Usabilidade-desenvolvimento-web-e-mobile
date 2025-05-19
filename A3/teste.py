import pygame
import sys

LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Mario Bros - Jogo Simples")

# Cores
AZUL = (135, 206, 235)
VERDE = (34, 139, 34)

# FPS
relogio = pygame.time.Clock()

# Carregar o sprite do Mario (substitua pelo seu arquivo)
mario_img = pygame.image.load("mario.png").convert_alpha()
mario_rect = mario_img.get_rect()
mario_rect.topleft = (100, ALTURA - 150)

# Velocidade
vel_x = 0
gravidade = 1
vel_y = 0
no_chao = True

# Loop principal
rodando = True
while rodando:
    tela.fill(AZUL)  # Céu

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Controles
    teclas = pygame.key.get_pressed()
    vel_x = 0
    if teclas[pygame.K_LEFT]:
        vel_x = -5
    if teclas[pygame.K_RIGHT]:
        vel_x = 5
    if teclas[pygame.K_SPACE] and no_chao:
        vel_y = -15
        no_chao = False

    # Movimento
    mario_rect.x += vel_x
    mario_rect.y += vel_y
    vel_y += gravidade

    # Colisão com o chão
    if mario_rect.bottom >= ALTURA - 50:
        mario_rect.bottom = ALTURA - 50
        vel_y = 0
        no_chao = True

    # Desenhar chão
    pygame.draw.rect(tela, VERDE, (0, ALTURA - 50, LARGURA, 50))

    # Desenhar Mario
    tela.blit(mario_img, mario_rect)

    # Atualizar
    pygame.display.update()
    relogio.tick(60)

# Finalizar
pygame.quit()
sys.exit()