import pygame as pg

class Obj:
    def __init__(self, image_idle, x, y, animated=False):
        self.group = pg.sprite.Group()
        self.sprite = pg.sprite.Sprite(self.group)

        self.animated = animated
        self.big = False  # novo estado
        self.facing_left = False

        self.image_idle = pg.image.load(image_idle).convert_alpha()

        if animated:
            self.frames = [
                pg.image.load(f"Assets/Sprites/MarioRun{i}.png").convert_alpha()
                for i in range(3)
            ]
            self.current_frame = 0
            self.animation_timer = 0
            self.sprite.image = self.image_idle
        else:
            self.sprite.image = self.image_idle

        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.topleft = (x, y)

    def crescer(self):
        self.big = True
        self.image_idle = pg.image.load("Assets/Sprites/SuperMario.png").convert_alpha()
        self.frames = [
            pg.image.load(f"Assets/Sprites/SuperMarioRun{i}.png").convert_alpha()
            for i in range(3)
        ]
        self.sprite.image = self.image_idle
        rect = self.sprite.rect
        self.sprite.rect = self.image_idle.get_rect(topleft=(rect.x, rect.y - 32))  # sobe o Mario para compensar o aumento

    def draw(self, window):
        self.group.draw(window)

    def update_position(self, dx, dy):
        self.sprite.rect.x += dx
        self.sprite.rect.y += dy

    def animate(self, moving):
        if not self.animated:
            return

        if moving:
            self.animation_timer += 1
            if self.animation_timer >= 8:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.animation_timer = 0
            frame = self.frames[self.current_frame]
            if self.facing_left:
                frame = pg.transform.flip(frame, True, False)
            self.sprite.image = frame
        else:
            image = self.image_idle
            if self.facing_left:
                image = pg.transform.flip(image, True, False)
            self.sprite.image = image

    def set_y(self, y):
        self.sprite.rect.y = y

    def get_rect(self):
        return self.sprite.rect


class Bloco:
    def __init__(self, x, y, tipo="brown"):
        if tipo == "brown":
            imagem = "BrickBlockBrown.png"
        elif tipo == "castle":
            imagem = "BrickBlockCastle.png"
        elif tipo == "dark":
            imagem = "BrickBlockDark.png"
        else:
            raise ValueError(f"Tipo de bloco desconhecido: {tipo}")

        self.image = pg.image.load(f"Assets/Sprites/{imagem}").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, window, camera_x):
        window.blit(self.image, (self.rect.x - camera_x, self.rect.y))

    def get_rect(self):
        return self.rect

class Cogumelo(Obj):
    def __init__(self, x, y):
        super().__init__("Assets/Sprites/Mushroom.png", x, y, animated=False)
        self.vel_x = 2
        self.vel_y = 0
        self.gravidade = 1
        self.no_chao = False

    def update(self, blocos, world_height):
        self.sprite.rect.y += self.vel_y
        self.vel_y += self.gravidade

        self.no_chao = False

        # Colisão vertical
        for bloco in blocos:
            if self.sprite.rect.colliderect(bloco.get_rect()):
                if self.vel_y > 0:
                    self.sprite.rect.bottom = bloco.get_rect().top
                    self.vel_y = 0
                    self.no_chao = True
                elif self.vel_y < 0:
                    self.sprite.rect.top = bloco.get_rect().bottom
                    self.vel_y = 0

        # Colisão com o chão
        if self.sprite.rect.bottom >= world_height - 30:
            self.sprite.rect.bottom = world_height - 30
            self.vel_y = 0
            self.no_chao = True

        # Movimento lateral
        self.sprite.rect.x += self.vel_x

        # Colisão horizontal
        for bloco in blocos:
            if self.sprite.rect.colliderect(bloco.get_rect()):
                if self.vel_x > 0:
                    self.sprite.rect.right = bloco.get_rect().left
                else:
                    self.sprite.rect.left = bloco.get_rect().right
                self.vel_x *= -1  # Inverte a direção

    def draw(self, window, camera_x=0):
        pos = (self.sprite.rect.x - camera_x, self.sprite.rect.y)
        window.blit(self.sprite.image, pos)

