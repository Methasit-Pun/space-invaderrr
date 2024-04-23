class Bullet():
  def __init__(self, bullet_img):
    self.width, self.height = bullet_img.get_size()
    self.speed = 20
    self.state = "ready"
    self.x = 0
    self.y = 0

    self.last_bullet_time = 0  # Timestamp of the last bullet fired
    self.fire_rate = 200  # Milliseconds between shots

  def get_state(self):
    return self.state
  
  