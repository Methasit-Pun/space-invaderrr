from spaceinv.utils.singleton import Singleton
from spaceinv.game import Game

game = Game()

class Player(metaclass=Singleton):
  def __init__(self, player_img, screen_width, padding=20, speed=10):
    self.player_img = player_img
    self.width, self.height = self.player_img.get_size()
    self.width -= padding
    self.height -= padding
    self.x = screen_width // 2 - self.width // 2
    self.y = int(700 * game.SCREEN_DOWNSCALE) - self.height
    self.speed = speed

  def move(self, direction):
    if direction == 'left':
      self.x -= self.speed
    elif direction == 'right':
      self.x += self.speed
    elif direction == 'up':
      self.y -= self.speed
    elif direction == 'down':
      self.y += self.speed

  def get_rect(self):
    return self.player_img.get_rect(topleft=(self.x, self.y))
  
  def get_position(self):
    return (self.x, self.y)
  
  def get_size(self):
    return (self.width, self.height)

  def fire_bullet(self, bullet):
    bullet.state = "fire"
    bullet.x = self.x + self.width // 2 - bullet.width // 2
    bullet.y = self.y
