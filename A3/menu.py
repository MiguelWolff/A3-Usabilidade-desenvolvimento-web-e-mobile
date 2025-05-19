import pygame as pg
from obj import Obj
import sys


fonte_titulo = pg.font.SysFont("Arial", 60)
fonte_opcao = pg.font.SysFont("Arial", 40)

class Menu:

    def __init__(self):
        pass    

    def desenhar_texto(self, window, texto, fonte, cor, centro):
        superficie = fonte.render(texto, True, cor)
        retangulo = superficie.get_rect(center=centro)
        window.blit(superficie, retangulo)
        return retangulo

    def events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.change_scene = True