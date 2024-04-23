import pygame
import random
import time
import sys\

class SpaceInvadersBase:
    def __init__(self, enemy_speed, bullet_speed, initial_enemy_count, enemy_count_increase_per_wave, boss_health, spawn_delay, spawn_delay_decrease_per_wave, enemy_speedup_per_wave):
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080))
        self.enemy_speed = enemy_speed
        self.bullet_speed = bullet_speed
        self.initial_enemy_count = initial_enemy_count
        self.boss_health = boss_health
        self.enemy_count_increase_per_wave = enemy_count_increase_per_wave
        self.spawn_delay = spawn_delay
        self.spawn_delay_decrease_per_wave = spawn_delay_decrease_per_wave
        self.enemy_speedup_per_wave = enemy_speedup_per_wave

        self.enemies = []
        self.initialize_game()

    def initialize_game(self):
        # Initialize game settings like loading images, setting up fonts, etc.

        # Screen dimensions
        self.SCREEN_WIDTH = 1920
        self.SCREEN_HEIGHT = 1080

        # Set up the display
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.DOUBLEBUF)
        pygame.display.set_caption('Space Invaders Wave System')

        # Load images w
        self.background_img = pygame.image.load("assets/wwwww.jpg").convert_alpha()
        self.player_img = pygame.image.load("assets/spaceship.png").convert_alpha()
        self.bullet_img = pygame.image.load("assets/bullet.png").convert_alpha()
        self.enemy_img1 = pygame.image.load("assets/alien551.gif").convert_alpha()
        self.enemy_img2 = pygame.image.load("assets/enemy2.png").convert_alpha()
        self.enemy_img3 = pygame.image.load("assets/enemy32.png").convert_alpha()
        self.boss_img = pygame.image.load("assets/spaceboss2.png").convert_alpha()
        self.wave_font = pygame.font.Font("assets/font.ttf", 70)
        self.score_font = pygame.font.Font("assets/font.ttf", 30)



        self.bwave = 5

        self.player_width, self.player_height = self.player_img.get_size()
        self.player_width -= 20
        self.player_height -= 20
        self.player_x = 960 #self.SCREEN_WIDTH // 2 - self.player_width // 2
        self.player_y = 800
        self.player_speed = 10

        # Bullet settings
        self.bullet_width, self.bullet_height = self.bullet_img.get_size()
        #self.bullet_speed = 20
        self.bullet_state = "ready"
        self.bullet_x = 0
        self.bullet_y = 0
        self.last_bullet_time = 0  # Timestamp of the last bullet fired
        self.fire_rate = 200  # Milliseconds between shots

        # Enemy settings
        self.enemy_width, self.enemy_height = self.enemy_img2.get_size()
        #self.enemy_speed = 3
        #self.enemy_speedup_per_wave = 0.5
        self.enemies = []

        # Boss settings
        #self.boss_health = 35
        self.boss_active = False
        self.boss_x = 200#self.SCREEN_WIDTH // 2 - self.enemy_width // 2
        self.boss_y = -100
        self.boss_last_shot_time = 0
        self.boss_shoot_interval = 2000  # milliseconds
        self.boss_width, self.boss_height = self.boss_img.get_size()
        self.boss_dx = 2  # Assuming boss_dx is the boss's delta x for movement

        # Wave settings
        self.wave_number = 0
        #self.enemy_count_increase_per_wave = 3
        #self.initial_enemy_count = 10
        #self.spawn_delay = 1
        #self.spawn_delay_decrease_per_wave = 0.1
        self.current_enemy_spawn_count = 0
        self.max_enemies_per_wave = 0
        self.wave_in_progress = False
        self.wave_delay = 2
        self.last_spawn_time = 0
        self.last_wave_time = 0 # Assuming bwave is used for something specific in wave handling
        self.enemy_boss_max = 1050

        # Score
        self.score = 0
        self.high_score = 0

        # Movement flags
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False

        # Game state
        self.running = True
        self.boss_laser_visible = False
        self.boss_laser_last_toggle_time = 0
        self.laser_orientation = 'horizontal'  # Could be 'horizontal' or 'vertical'
        self.laser_position = 0  # Position where the laser will be fired
        self.boss_laser_duration = 3000  # Laser visible for 3000 milliseconds (including warning)
        self.warning_duration = 2000  # Warning visible for 2000 milliseconds
        self.laser_size = 100

        # Health Bar settings
        self.BOSS_HEALTH_BAR_WIDTH = 50
        self.BOSS_HEALTH_BAR_HEIGHT = 500 
        self.BOSS_HEALTH_BAR_X = 100  # Distance from the left side of the screen
        self.BOSS_HEALTH_BAR_Y = 50  # Distance from the top of the screen

    def spawn_enemy(self):
        if not self.boss_active:
            if self.current_enemy_spawn_count < self.max_enemies_per_wave:
                enemy_type = random.randint(1, 3)  # Assuming type 3 are minions
                if self.SCREEN_WIDTH > self.enemy_width:  # Check if there's enough space to spawn the enemy
                    enemy_x = random.randint(0, self.SCREEN_WIDTH - self.enemy_width)
                else:
                    enemy_x = 0  # Default to 0 if not enough space
                enemy = {
                    'x': enemy_x,
                    'y': 0,
                    'dx': random.choice([-self.enemy_speed, self.enemy_speed]),
                    'dy': self.enemy_speed,
                    'type': enemy_type,
                }
                self.enemies.append(enemy)
                self.current_enemy_spawn_count += 1
                self.last_spawn_time = time.time() #pygame.time.get_ticks()  # Update the time of the last spawn
        else:
            # If the boss is active, spawn enemies differently
            enemy_type = random.randint(1, 3)
            enemy = {
                'x': random.randint(0, self.SCREEN_WIDTH - self.enemy_width),
                'y': random.randint(0, 200),  # Random Y within the upper part of the screen
                'dx': random.choice([-self.enemy_speed, self.enemy_speed]),
                'dy': self.enemy_speed,
                'type': enemy_type 
            }
            self.enemies.append(enemy)
            self.spawn_delay = 1  # Faster spawn rate when the boss is active
            self.current_enemy_spawn_count += 1
            self.last_spawn_time = time.time()#pygame.time.get_ticks()  # Use real-time timestamp for boss enemy spawns


    def run(self):
        while self.running:
            self.screen.blit(self.background_img, (0, 0))

            # Boss conditions and drawing
            if self.boss_active:
                self.screen.blit(self.background_img, (0, 0))
                self.screen.blit(self.boss_img, (self.boss_x, 0))
                self.boss_attack()
                self.draw_boss_health_bar()
                if pygame.time.get_ticks() - self.last_spawn_time > self.spawn_delay:
                    self.spawn_enemy()
                if self.bullet_state == "fire":
                    if self.bullet_x < self.boss_x + self.boss_width and self.bullet_x + self.bullet_width > self.boss_x and \
                    self.bullet_y < self.boss_y + self.boss_height and self.bullet_y + self.bullet_height > self.boss_y:
                        self.bullet_state = "ready"
                        self.bullet_y = self.player_y - self.bullet_height
                        self.boss_health -= 1
                        if self.boss_health <= 0:
                            self.boss_active = False
                            self.wave_in_progress = False
                            self.last_wave_time = time.time()

            # Check if wave is not in progress or if boss is defeated then stop the game
            if (not self.wave_in_progress and not self.boss_active) and (time.time() - self.last_wave_time > self.wave_delay):
                self.reset_wave()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.move_left = True
                    elif event.key == pygame.K_d:
                        self.move_right = True
                    elif event.key == pygame.K_w:
                        self.move_up = True
                    elif event.key == pygame.K_s:
                        self.move_down = True
                    elif event.key == pygame.K_SPACE and self.bullet_state == "ready":
                        self.fire_bullet(self.player_x, self.player_y)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.move_left = False
                    elif event.key == pygame.K_d:
                        self.move_right = False
                    elif event.key == pygame.K_w:
                        self.move_up = False
                    elif event.key == pygame.K_s:
                        self.move_down = False
                self.current_time = pygame.time.get_ticks()  # Get the current time

            if self.move_left:
                self.player_x -= self.player_speed
            if self.move_right:
                self.player_x += self.player_speed
            if self.move_up:
                self.player_y -= self.player_speed
            if self.move_down:
                self.player_y += self.player_speed

            self.player_x = max(0, min(self.SCREEN_WIDTH - self.player_width, self.player_x))
            self.player_y = max(0, min(self.SCREEN_HEIGHT - self.player_height, self.player_y))

            if self.bullet_state == "fire":
                self.bullet_y -= self.bullet_speed
                if self.bullet_y <= 0:
                    self.bullet_state = "ready"

            if self.bullet_state == "fire" and self.boss_active:
                if self.bullet_x < self.boss_x + self.boss_width and self.bullet_x + self.bullet_width > self.boss_x and self.bullet_y < self.boss_y + self.boss_height and self.bullet_y + self.bullet_height > self.boss_y:
                    self.bullet_state = "ready"
                    self.bullet_y = self.player_y - self.bullet_height
                    self.boss_health -= 1
                    if self.boss_health <= 0:
                        self.boss_active = False
                        self.wave_in_progress = False
                        self.last_wave_time = time.time()

            if self.show_wave_message():
                pygame.display.flip()
                continue

            if not self.wave_in_progress and time.time() - self.last_wave_time > self.wave_delay:
                self.reset_wave()

            if self.current_enemy_spawn_count < self.max_enemies_per_wave and time.time() - self.last_spawn_time > self.spawn_delay:
                self.spawn_enemy()
            elif len(self.enemies) == 0 and self.current_enemy_spawn_count >= self.max_enemies_per_wave:
                self.wave_in_progress = False
                self.last_wave_time = time.time()

            for enemy in self.enemies[:]:
                if enemy['type'] == 1:
                    enemy['x'] += enemy['dx']
                    if enemy['x'] <= 0 or enemy['x'] >= self.SCREEN_WIDTH - self.enemy_width:
                        enemy['dx'] *= -1
                elif enemy['type'] == 2:
                    enemy['y'] += enemy['dy']
                    if enemy['y'] > self.SCREEN_HEIGHT:
                        self.enemies.remove(enemy)
                elif enemy['type'] == 3:
                    enemy['x'] += enemy['dx']
                    enemy['y'] += enemy['dy']
                    if enemy['x'] < 0 or enemy['x'] > self.SCREEN_WIDTH - self.enemy_width:
                        enemy['dx'] *= -1
                        enemy['x'] = max(0, min(self.SCREEN_WIDTH - self.enemy_width, enemy['x']))
                    if enemy['y'] < 0 or enemy['y'] > self.SCREEN_HEIGHT - self.enemy_height:
                        enemy['dy'] *= -1
                        enemy['y'] = max(0, min(self.SCREEN_HEIGHT - self.enemy_height, enemy['y']))

            if self.bullet_state == "fire":
                for enemy in self.enemies[:]:
                    if self.bullet_x < enemy['x'] + self.enemy_width and self.bullet_x + self.bullet_width > enemy['x'] and \
                    self.bullet_y < enemy['y'] + self.enemy_height and self.bullet_y + self.bullet_height > enemy['y']:
                        self.bullet_state = "ready"
                        self.bullet_y = self.player_y - self.bullet_height
                        self.enemies.remove(enemy)
                        self.update_score(1)
                        break

            for enemy in self.enemies[:]:
                if self.player_x < enemy['x'] + self.enemy_width and self.player_x + self.player_width > enemy['x'] and \
                self.player_y < enemy['y'] + self.enemy_height and self.player_y + self.player_height > enemy['y']:
                    self.game_over()
                if (self.player_x < self.boss_x + self.boss_width and self.player_x + self.player_width > self.boss_x and  \
                self.player_y < self.boss_y + self.boss_height and \
                self.player_y + self.player_height > self.boss_y):
                    self.game_over()

            self.screen.blit(self.player_img, (self.player_x, self.player_y))

            if self.bullet_state == "fire":
                self.screen.blit(self.bullet_img, (self.bullet_x, self.bullet_y))

            for enemy in self.enemies:
                if enemy['type'] == 1:
                    self.screen.blit(self.enemy_img1, (enemy['x'], enemy['y']))
                elif enemy['type'] == 2:
                    self.screen.blit(self.enemy_img2, (enemy['x'], enemy['y']))
                elif enemy['type'] == 3:
                    self.screen.blit(self.enemy_img3, (enemy['x'], enemy['y']))

            self.display_score()

            pygame.display.flip()
            pygame.time.Clock().tick(60)

        pygame.quit()
        sys.exit()

    def update_game_state(self):
        # Add game logic for updating positions, checking collisions, etc.
        pass
    def draw_boss_health_bar(self):
        if self.boss_active:
            # Calculate the current health proportion
            current_health_ratio = self.boss_health / (20 + (self.wave_number // 10 * 5))
            current_health_height = int(self.BOSS_HEALTH_BAR_HEIGHT * current_health_ratio)
            
            # Draw the background of the health bar (empty part)
            pygame.draw.rect(self.screen, (128, 128, 128), (self.BOSS_HEALTH_BAR_X, self.BOSS_HEALTH_BAR_Y, self.BOSS_HEALTH_BAR_WIDTH, self.BOSS_HEALTH_BAR_HEIGHT))
            
            # Draw the current health (filled part)
            pygame.draw.rect(self.screen, (0, 128, 0), (self.BOSS_HEALTH_BAR_X, self.BOSS_HEALTH_BAR_Y + self.BOSS_HEALTH_BAR_HEIGHT - current_health_height, self.BOSS_HEALTH_BAR_WIDTH, current_health_height))


    def boss_attack(self):
        current_time = pygame.time.get_ticks()

        # Toggle laser visibility and set warning phase
        if current_time - self.boss_laser_last_toggle_time > self.boss_laser_duration + self.warning_duration:
            self.boss_laser_visible = not self.boss_laser_visible
            self.boss_laser_last_toggle_time = current_time
            # Randomly decide orientation and position of the laser
            self.laser_orientation = random.choice(['horizontal', 'vertical'])
            if self.laser_orientation == 'horizontal':
                self.laser_position = random.randint(0, self.SCREEN_HEIGHT)
            else:
                self.laser_position = random.randint(0, self.SCREEN_WIDTH)

        # Draw warning
        if self.boss_laser_visible and current_time - self.boss_laser_last_toggle_time < self.warning_duration:
            color = (242, 158, 145)  # Warning color
            if self.laser_orientation == 'horizontal':
                pygame.draw.line(self.screen, color, (0, self.laser_position), (self.SCREEN_WIDTH, self.laser_position), self.laser_size)
            else:
                pygame.draw.line(self.screen, color, (self.laser_position, 0), (self.laser_position, self.SCREEN_HEIGHT), self.laser_size)

        # Fire the laser after the warning duration
        if self.boss_laser_visible and current_time - self.boss_laser_last_toggle_time > self.warning_duration:
            color = (255, 0, 0)  # Laser color
            if self.laser_orientation == 'horizontal':
                pygame.draw.line(self.screen, color, (0, self.laser_position), (self.SCREEN_WIDTH, self.laser_position), self.laser_size)
                # Check if player is hit by the laser
                if self.player_y <= self.laser_position <= self.player_y + self.player_height:
                    self.game_over()
            else:
                pygame.draw.line(self.screen, color, (self.laser_position, 0), (self.laser_position, self.SCREEN_HEIGHT), self.laser_size)
                # Check if player is hit by the laser
                if self.player_x <= self.laser_position <= self.player_x + self.player_width:
                    self.game_over()

    def fire_bullet(self, x, y):
        self.bullet_state = "fire"
        self.bullet_x = x + self.player_width // 2 - self.bullet_width // 2
        self.bullet_y = y

    def show_wave_message(self):
        if time.time() - self.last_wave_time < self.wave_delay:
            wave_text = self.wave_font.render(f"Wave {self.wave_number}", True, (255, 255, 255))
            self.screen.blit(wave_text, (self.SCREEN_WIDTH // 2 - wave_text.get_width() // 2,
                                        self.SCREEN_HEIGHT // 2 - wave_text.get_height() // 2))
            return True
        return False

    def reset_wave(self):
        self.player_x = 960
        self.player_y = 900
        self.wave_number += 1

        if self.wave_number % self.bwave == 0:
            self.boss_health = 20 + (self.wave_number // 10 * 5)
            self.boss_active = True
            self.wave_in_progress = True  # Ensure wave is considered 'in progress' while the boss is active
            self.max_enemies_per_wave = 20  # No normal enemies this wave
        else:
            self.boss_active = False
            self.wave_in_progress = True  # Regular waves are in progress
            self.max_enemies_per_wave = self.initial_enemy_count + self.enemy_count_increase_per_wave * (self.wave_number - 1)
            self.enemy_speed += self.enemy_speedup_per_wave
            self.enemy_speed = min(self.enemy_speed, 10)

        self.current_enemy_spawn_count = 0
        self.last_spawn_time = time.time()
        self.last_wave_time = time.time()
        self.spawn_delay = max(0.2, self.spawn_delay - self.spawn_delay_decrease_per_wave)


    def update_score(self, points):
        self.score += points
        self.high_score = max(self.high_score, self.score)

    def display_score(self):
        score_text = self.score_font.render("Score: " + str(self.score), True, (255, 255, 255))
        high_score_text = self.score_font.render("High Score: " + str(self.high_score), True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(high_score_text, (self.SCREEN_WIDTH - high_score_text.get_width() - 10, 10))

    def game_over(self):
        from gameover import game_is_over
        game_is_over(self.score)
        self.running = False

class EasyLevel(SpaceInvadersBase):
    def __init__(self):
        super().__init__(enemy_speed=3, bullet_speed=20, initial_enemy_count=3, enemy_count_increase_per_wave=2, boss_health=20, spawn_delay=1, spawn_delay_decrease_per_wave=0.1, enemy_speedup_per_wave=0.2)

class NormalLevel(SpaceInvadersBase):
    def __init__(self):
        super().__init__(enemy_speed=5, bullet_speed=20, initial_enemy_count=10, enemy_count_increase_per_wave=5, boss_health=35, spawn_delay=0.5, spawn_delay_decrease_per_wave=0.2, enemy_speedup_per_wave=0.5)

class HardLevel(SpaceInvadersBase):
    def __init__(self):
        super().__init__(enemy_speed=20, bullet_speed=30, initial_enemy_count=25, enemy_count_increase_per_wave=7, boss_health=100, spawn_delay=0.5, spawn_delay_decrease_per_wave=0.3, enemy_speedup_per_wave=1)

if __name__ == "__main__":
    level = NormalLevel()  # Change this to EasyLevel or NormalLevel as needed
    level.run()
