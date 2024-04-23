import pygame

class GameObject:
    def __init__(self, image, position):
        self.image = image
        self.rect = self.image.get_rect(topleft=position)
        self.velocity = pygame.math.Vector2(0, 0)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def update(self):
        self.rect.topleft += self.velocity

class Player(GameObject):
    def __init__(self, image, position):
        super().__init__(image, position)
        self.speed = 10

    def move(self, direction):
        if direction == "left":
            self.velocity.x = -self.speed
        elif direction == "right":
            self.velocity.x = self.speed
        elif direction == "stop":
            self.velocity.x = 0

class Bullet(GameObject):
    def __init__(self, image, position):
        super().__init__(image, position)
        self.velocity.y = -20

class Enemy(GameObject):
    def __init__(self, image, position, enemy_type):
        super().__init__(image, position)
        self.enemy_type = enemy_type
        self.set_behavior()

    def set_behavior(self):
        if self.enemy_type == 1:
            self.velocity.x = 3
        elif self.enemy_type == 2:
            self.velocity.y = 3
        elif self.enemy_type == 3:
            self.velocity = pygame.math.Vector2(2, 2)

class Boss(Enemy):
    def __init__(self, image, position):
        super().__init__(image, position, 'boss')
        self.health = 100
