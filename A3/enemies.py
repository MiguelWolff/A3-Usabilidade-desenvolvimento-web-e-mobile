import pygame as pg

class Goomba(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = [
            pg.image.load("Assets/Sprites/Goomba_0.png").convert_alpha(),
            pg.image.load("Assets/Sprites/Goomba_1.png").convert_alpha()
        ]
        self.dead_image = pg.image.load("Assets/Sprites/DeadGoomba.png").convert_alpha()
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.animation_timer = 0
        self.speed = 2
        self.direction = -1
        self.alive = True
        self.death_timer = 0

    def update(self, world_width):
        if not self.alive:
            self.death_timer += 1
            if self.death_timer >= 60:  # 1 segundo a 60 FPS
                self.kill()
            return

        self.animation_timer += 1
        if self.animation_timer >= 10:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.animation_timer = 0

        self.rect.x += self.speed * self.direction
        if self.rect.left <= 0 or self.rect.right >= world_width:
            self.direction *= -1

    def morrer(self):
        self.alive = False
        self.image = self.dead_image
        self.death_timer = 0

    def draw(self, window, camera_x):
        if self.alive or self.death_timer < 60:
            window.blit(self.image, (self.rect.x - camera_x, self.rect.y))
