import pygame
from settings import ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT
from assets import enemy_type1_img, enemy_type2_img, enemy_type3_img

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.speed = ENEMY_SPEED

    def move(self):
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))

class EnemyType1(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.dx = self.speed
        self.image = enemy_type1_img

    def move(self):
        self.x += self.dx
        if self.x <= 0 or self.x + self.width >= SCREEN_WIDTH:
            self.dx *= -1

class EnemyType2(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.dy = self.speed
        self.image = enemy_type2_img

    def move(self):
        self.y += self.dy
        if self.y >= SCREEN_HEIGHT:
            self.reset()

    def reset(self):
        self.y = -self.height  # Reset to top if it goes beyond the screen

class EnemyType3(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.dx = self.speed
        self.dy = self.speed
        self.image = enemy_type3_img

    def move(self):
        self.x += self.dx
        self.y += self.dy
        if self.x <= 0 or self.x + self.width >= SCREEN_WIDTH:
            self.dx *= -1
        if self.y < 0 or self.y + self.height >= SCREEN_HEIGHT:
            self.dy *= -1

class GameManager:
    def __init__(self, enemies):
        self.enemies = enemies
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.enemy_width = ENEMY_WIDTH
        self.enemy_height = ENEMY_HEIGHT

    def update(self):
        for enemy in self.enemies:
            enemy.move()

# Example usage
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    enemies = [EnemyType1(100, 100), EnemyType2(300, 100), EnemyType3(500, 100)]
    manager = GameManager(enemies)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        manager.update()

        screen.fill((0, 0, 0))
        for enemy in enemies:
            enemy.draw(screen)

        pygame.display.flip()
    pygame.quit()
