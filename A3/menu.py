import pygame as pg

class Menu:

    def __init__(self):
        self.fonte_titulo = pg.font.SysFont("Arial", 40)
        self.fonte_opcao = pg.font.SysFont("Arial", 25)
        self.change_scene = False

    def desenhar_texto(self, window, texto, fonte, cor, centro):
        superficie = fonte.render(texto, True, cor)
        retangulo = superficie.get_rect(center=centro)
        window.blit(superficie, retangulo)
        return retangulo

    def draw(self, window):
        self.desenhar_texto(window, "Mario Bros", self.fonte_titulo, (255, 255, 255), (200, 80))
        self.desenhar_texto(window, "Pressione ENTER para começar", self.fonte_opcao, (255, 255, 255), (200, 180))

    def events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key in (pg.K_RETURN, pg.K_KP_ENTER):
                self.change_scene = True
