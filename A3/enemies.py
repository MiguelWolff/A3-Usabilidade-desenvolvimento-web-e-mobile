import pygame as pg

class Goomba(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Carrega frames da animação do Goomba andando
        self.frames = [
            pg.image.load("Assets/Sprites/Goomba_0.png").convert_alpha(),
            pg.image.load("Assets/Sprites/Goomba_1.png").convert_alpha()
        ]
        # Imagem do Goomba morto
        self.dead_image = pg.image.load("Assets/Sprites/DeadGoomba.png").convert_alpha()
        
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.animation_timer = 0
        self.speed = 2
        self.direction = -1  # começa andando para a esquerda
        self.alive = True
        self.death_timer = 0

    def update(self, world_width):
        if not self.alive:
            self.death_timer += 1
            if self.death_timer >= 60:  # 1 segundo a 60 FPS
                self.kill()  # remove o sprite do grupo
            return

        # Atualiza animação andando
        self.animation_timer += 1
        if self.animation_timer >= 10:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.animation_timer = 0

        # Movimento horizontal
        self.rect.x += self.speed * self.direction
        # Inverte direção ao atingir limites do mundo
        if self.rect.left <= 0 or self.rect.right >= world_width:
            self.direction *= -1

    def morrer(self):
        self.alive = False
        self.image = self.dead_image
        self.death_timer = 0
        self.rect.topleft = (-1000, -1000)
        
    def draw(self, window, camera_x):
        # Desenha somente se vivo ou ainda dentro do tempo da animação da morte
        if self.alive or self.death_timer < 60:
            window.blit(self.image, (self.rect.x - camera_x, self.rect.y))


class Bowser(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = [
            pg.image.load("Assets/Sprites/Bowser0.png").convert_alpha(),
            pg.image.load("Assets/Sprites/Bowser1.png").convert_alpha()
        ]
        self.current_frame = 0
        self.animation_timer = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.direction = -1
        self.speed = 1
        self.alive = True
        self.death_timer = 0

    def update(self, world_width):
        if not self.alive:
            self.death_timer += 1
            if self.death_timer >= 60:  # 1 segundo a 60 FPS
                self.kill()  # remove o sprite do grupo
            return

        self.animation_timer += 1
        if self.animation_timer >= 10:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.animation_timer = 0

        self.rect.x += self.direction * self.speed

        if self.rect.left <= 0 or self.rect.right >= world_width:
            self.direction *= -1

    def draw(self, window, camera_x):
        if self.alive:
            window.blit(self.image, (self.rect.x - camera_x, self.rect.y))

    def get_rect(self):
        return self.rect

    def morrer(self):
        self.alive = False

class KoopaTroopa(pg.sprite.Sprite):
    def __init__(self, x, y, tipo="verde"):
        super().__init__()
        self.tipo = tipo
        self.frames = self.load_frames(tipo)
        self.current_frame = 0
        self.animation_timer = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.direction = -1
        self.speed = 1
        self.alive = True
        self.death_timer = 0
        self.visible = True

    def load_frames(self, tipo):
        base_path = "Assets/Sprites/"
        if tipo == "verde":
            return [
                pg.image.load(base_path + "KoopaTroopaG0.png").convert_alpha(),
                pg.image.load(base_path + "KoopaTroopaG1.png").convert_alpha()
            ]
        elif tipo == "verde_casco_azul":
            return [
                pg.image.load(base_path + "KoopaTroopaGB0.png").convert_alpha(),
                pg.image.load(base_path + "KoopaTroopaGB1.png").convert_alpha()
            ]
        elif tipo == "vermelho":
            return [
                pg.image.load(base_path + "KoopaTroopaR0.png").convert_alpha(),
                pg.image.load(base_path + "KoopaTroopaR1.png").convert_alpha()
            ]
        else:
            raise ValueError("Tipo de KoopaTroopa inválido.")

    def update(self, world_width):
        if not self.alive:
            self.death_timer += 1
            if self.death_timer >= 15:
                self.visible = False  # <- desativa visibilidade
            return

        self.animation_timer += 1
        if self.animation_timer >= 10:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.animation_timer = 0

        self.rect.x += self.direction * self.speed

        if self.rect.left <= 0 or self.rect.right >= world_width:
            self.direction *= -1

    def draw(self, window, camera_x):
        if self.alive:
            flipped_image = pg.transform.flip(self.image, self.direction == -1, False)
            window.blit(flipped_image, (self.rect.x - camera_x, self.rect.y))

    def get_rect(self):
        return self.rect

    def morrer(self):
        self.alive = False
