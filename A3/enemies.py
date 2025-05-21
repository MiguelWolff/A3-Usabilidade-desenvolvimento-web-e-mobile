import pygame as pg

class Goomba(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = []
        for i in range(2):  # número de quadros da animação
            image = pg.image.load(f"Assets/Sprites/Goomba_{i}.png").convert_alpha()
            self.frames.append(image)

        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.animation_timer = 0
        self.speed = 2
        self.direction = -1  # -1 para esquerda, 1 para direita

    def update(self, largura_tela):
        # Animação
        self.animation_timer += 1
        if self.animation_timer >= 10:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.animation_timer = 0

        # Movimento horizontal ida e volta dentro dos limites da tela
        self.rect.x += self.speed * self.direction
        if self.rect.left <= 0 or self.rect.right >= largura_tela:
            self.direction *= -1

    def draw(self, window):
        window.blit(self.image, self.rect)