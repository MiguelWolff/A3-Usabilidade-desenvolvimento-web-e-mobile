import pygame
import sys

pygame.init()

# Configurações da tela
LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Mario Bros")

# Cores
AZUL = (135, 206, 235)
VERDE = (34, 139, 34)
BRANCO = (255, 255, 255)
VERDE_CLARO = (0, 200, 0)

# Fonte
fonte_titulo = pygame.font.SysFont("Arial", 60)
fonte_opcao = pygame.font.SysFont("Arial", 40)

# FPS
relogio = pygame.time.Clock()

# Função para desenhar texto centralizado
def desenhar_texto(texto, fonte, cor, centro):
    superficie = fonte.render(texto, True, cor)
    retangulo = superficie.get_rect(center=centro)
    tela.blit(superficie, retangulo)
    return retangulo

# Menu principal
def menu_principal():
    while True:
        tela.fill(AZUL)

        desenhar_texto("Mario Bros", fonte_titulo, BRANCO, (LARGURA // 2, 150))
        botao_jogar = desenhar_texto("Jogar", fonte_opcao, VERDE_CLARO, (LARGURA // 2, 300))
        botao_sair = desenhar_texto("Sair", fonte_opcao, VERDE_CLARO, (LARGURA // 2, 400))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_jogar.collidepoint(evento.pos):
                    return  # Inicia o jogo
                elif botao_sair.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# Função do jogo principal
def jogo():
    # Carregar imagem do Mario
    mario_img = pygame.image.load("mario.png").convert_alpha()
    mario_rect = mario_img.get_rect()
    mario_rect.topleft = (100, ALTURA - 150)

    vel_x = 0
    gravidade = 1
    vel_y = 0
    no_chao = True

    rodando = True
    while rodando:
        tela.fill(AZUL)

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

        # Colisão com chão
        if mario_rect.bottom >= ALTURA - 50:
            mario_rect.bottom = ALTURA - 50
            vel_y = 0
            no_chao = True

        # Desenha chão
        pygame.draw.rect(tela, VERDE, (0, ALTURA - 50, LARGURA, 50))

        # Desenha Mario
        tela.blit(mario_img, mario_rect)

        pygame.display.update()
        relogio.tick(60)

    pygame.quit()
    sys.exit()

# Inicia o menu e depois o jogo
menu_principal()
jogo()