import pygame as pg

class Menu:
    def __init__(self):
        # Fontes para título e opções
        self.fonte_titulo = pg.font.SysFont("Arial", 40)
        self.fonte_opcao = pg.font.SysFont("Arial", 25)
        self.change_scene = False  # Indica se deve mudar para o jogo

    def desenhar_texto(self, window, texto, fonte, cor, centro):
        """Renderiza e desenha o texto na tela centralizado no ponto dado."""
        superficie = fonte.render(texto, True, cor)
        retangulo = superficie.get_rect(center=centro)
        window.blit(superficie, retangulo)
        return retangulo

    def draw(self, window):
        """Desenha o menu principal."""
        window.fill((0, 0, 0))  # Limpa a tela com preto (boa prática)
        self.desenhar_texto(window, "Mario Bros", self.fonte_titulo, (255, 255, 255), (window.get_width() // 2, 80))
        self.desenhar_texto(window, "Pressione ENTER para começar", self.fonte_opcao, (255, 255, 255), (window.get_width() // 2, 180))

    def events(self, event):
        """Processa eventos, detecta o ENTER para mudar a cena."""
        if event.type == pg.KEYDOWN:
            if event.key in (pg.K_RETURN, pg.K_KP_ENTER):
                self.change_scene = True
