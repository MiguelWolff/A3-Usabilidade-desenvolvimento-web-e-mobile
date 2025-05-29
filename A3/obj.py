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
    def __init__(self, x, y, tipo="brown", tema="brown"):
        self.tema = tema
        self.tipo = tipo  # pode ser útil depois

        if tipo == "brown":
            imagem = "BrickBlockBrown.png"
        elif tipo == "castle":
            imagem = "BrickBlockCastle.png"
        elif tipo == "dark":
            imagem = "BrickBlockDark.png"
        elif tipo == "question":
            # QuestionBlock não usa isso diretamente, mas evita erro
            imagem = f"QuestionBlock0.png"
        else:
            raise ValueError(f"Tipo de bloco desconhecido: {tipo}")

        self.image = pg.image.load(f"Assets/Sprites/{imagem}").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))


    def draw(self, window, camera_x):
        window.blit(self.image, (self.rect.x - camera_x, self.rect.y))

    def get_rect(self):
        return self.rect

class Cogumelo:
    def __init__(self, x, y):
        self.image = pg.image.load("Assets/Sprites/Mushroom.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 2
        self.direction = 1
        self.subindo = True
        self.alvo_y = y - 32  # sobe 32 pixels ao aparecer
        self.vel_y = 0
        self.gravidade = 1

    def update(self, world_width):
        # Se está subindo
        if self.subindo:
            self.rect.y -= 2
            if self.rect.y <= self.alvo_y:
                self.subindo = False
                self.vel_y = 0

        else:
            self.vel_y += self.gravidade
            self.rect.y += self.vel_y
            self.rect.x += self.speed * self.direction

            # Inverte direção nas bordas
            if self.rect.left <= 0 or self.rect.right >= world_width:
                self.direction *= -1

    def draw(self, window, camera_x):
        window.blit(self.image, (self.rect.x - camera_x, self.rect.y))

    def get_rect(self):
        return self.rect



class QuestionBlock(Bloco):
    def __init__(self, x, y, tema="brown", contem_cogumelo=False):
        self.ativo = True
        super().__init__(x, y, tipo="question", tema=tema)
        self.frames = self.load_frames(tema)
        self.current_frame = 0
        self.animation_timer = 0
        self.hit = False
        self.contem_cogumelo = contem_cogumelo
        self.tema = tema

    def load_frames(self, tema):
        prefix = "QuestionBlock"
        if tema == "castle":
            prefix = "QuestionBlockCastle"
        elif tema == "dark":
            prefix = "QuestionBlockDark"
        return [pg.image.load(f"Assets/Sprites/{prefix}{i}.png").convert_alpha() for i in range(6)]

    def update(self):
        if not self.hit:
            self.animation_timer += 1
            if self.animation_timer >= 8:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.animation_timer = 0
            self.image = self.frames[self.current_frame]

    def on_hit(self):
        self.hit = True

        if self.tema == "brown":
            self.image = pg.image.load("Assets/Sprites/EmptyBlock.png").convert_alpha()
        elif self.tema == "castle":
            self.image = pg.image.load("Assets/Sprites/EmptyBlockCastle.png").convert_alpha()
        elif self.tema == "dark":
            self.image = pg.image.load("Assets/Sprites/EmptyBlockDark.png").convert_alpha()
        else:
            self.image = pg.image.load("Assets/Sprites/EmptyBlock.png").convert_alpha()  # fallback

        return self.contem_cogumelo
    def ativar(self):
        if not self.ativo:
            return None
        self.ativo = False
        vazio = f"EmptyBlock{self.tema.capitalize() if self.tema != 'normal' else ''}.png"
        self.image = pg.image.load(f"Assets/Sprites/{vazio}").convert_alpha()
        if self.contem_cogumelo:
            # Cria um cogumelo logo acima do bloco
            return Cogumelo(self.rect.x, self.rect.y - 32)
        return None
