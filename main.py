import pygame
import random

# https://nick.sarbicki.com/blog/learn-pygame-with-pong/
# We purposefully messed up some code in the below program so that the game would not run properly. To get the game running again, use the asks in Activities in code to fix the errors.


class Paddle(pygame.Rect):

  def __init__(self, velocity, up_key, down_key, *args, **kwargs):
    self.velocity = velocity
    self.up_key = up_key
    self.down_key = down_key
    super().__init__(*args, **kwargs)

  def move_paddle(self, board_height):
    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[self.up_key]:
      if self.y - self.velocity > 0:
        self.y -= self.velocity

    if keys_pressed[self.down_key]:
      if self.y + self.velocity < board_height - self.height:
        self.y += self.velocity


class Ball(pygame.Rect):

  def __init__(self, velocity, *args, **kwargs):
    self.velocity = velocity
    self.angle = 0
    super().__init__(*args, **kwargs)

  def move_ball(self):
    self.x += self.velocity
    self.y += self.angle


class Pong:

  HEIGHT = 800
  # TODO (ACTIVITY 1): Correct the width of the screen to 800. Change the value of the variable WIDTH to 800.
  # HINT: The height of the screen is defined as 600 and is stored in the variable HEIGHT.
  WIDTH = 800

  PADDLE_WIDTH = 10
  PADDLE_HEIGHT = 100

  BALL_WIDTH = 10
  BALL_VELOCITY = 6
  BALL_ANGLE = 0

  # TODO (ACTIVITY 2): Change the color of Pong objects to Steel Blue. The RGB values for Steel blue are 70, 130, 180 respectively. Change the RGB Values for the varoable COLOR.
  # HINT: RGB value of White color is 255, 255, 255.
  COLOR = (50, 133, 168)

  LEFTSCORE = 0
  RIGHTSCORE = 0

  BALLXSTARTPOSITION = WIDTH / 2 - BALL_WIDTH / 2
  BALLYSTARTPOSITION = HEIGHT / 2 - BALL_WIDTH / 2

  def __init__(self):
    pygame.init()  # Start the pygame instance.

    # Setup the screen
    self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
    self.clock = pygame.time.Clock()

    # Create the player objects.

    self.paddles = []
    self.balls = []
    # TODO (Activity 3): Assign the "s" key to move left paddle down.
    # HINT: Key "w" is assigned to move paddle up
    self.paddles.append(
      Paddle(  # The left paddle
        self.BALL_VELOCITY, pygame.K_w, pygame.K_s, 0,
        self.HEIGHT / 2 - self.PADDLE_HEIGHT / 2, self.PADDLE_WIDTH,
        self.PADDLE_HEIGHT))
    # TODO (Activity 4): Assign the "UP" key to move right paddle up.
    self.paddles.append(
      Paddle(  # The right paddle
        self.BALL_VELOCITY, pygame.K_UP, pygame.K_DOWN,
        self.WIDTH - self.PADDLE_WIDTH,
        self.HEIGHT / 2 - self.PADDLE_HEIGHT / 2, self.PADDLE_WIDTH,
        self.PADDLE_HEIGHT))

    self.balls.append(
      Ball(self.BALL_VELOCITY, self.BALLXSTARTPOSITION,
           self.BALLYSTARTPOSITION, self.BALL_WIDTH, self.BALL_WIDTH))

    self.central_line = pygame.Rect(self.WIDTH / 2, 0, 1, self.HEIGHT)

  def draw_text(self, text, size, x, y):
    # TODO (Activity 5): Declare a variable called font_label which stores the name of font that you wish to see in Score board. Then set the value to a string 'arial' or any font you prefer. Then replace the parameter in match_font function to use the variable you declared.

    font_label = "roboto"
    font_name = pygame.font.match_font(font_label)
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, self.COLOR)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    self.screen.blit(text_surface, text_rect)

  def check_ball_hits_wall(self):
    for ball in self.balls:
      if ball.x > self.WIDTH:
        self.LEFTSCORE = self.LEFTSCORE + 1
        ball.x = self.BALLXSTARTPOSITION
        ball.y = self.BALLYSTARTPOSITION
        ball.velocity = -1 * self.BALL_VELOCITY
        ball.angle = self.BALL_ANGLE
      # TODO (Activity 6): Can you guess what should be the condition when the paddle at right would score when left paddle miss the ball? Fix the if condition below.
      if ball.x < 2:
        self.RIGHTSCORE = self.RIGHTSCORE + 1
        ball.x = self.BALLXSTARTPOSITION
        ball.y = self.BALLYSTARTPOSITION
        ball.velocity = self.BALL_VELOCITY
        ball.angle = self.BALL_ANGLE

      if ball.y > self.HEIGHT - self.BALL_WIDTH or ball.y < 0:
        ball.angle = -ball.angle

  def check_ball_hits_paddle(self):
    for ball in self.balls:
      for paddle in self.paddles:
        if ball.colliderect(paddle):
          ball.velocity = -ball.velocity
          ball.angle = random.randint(-10, 10)
          break

  def game_loop(self):
    while True:
      for event in pygame.event.get():
        # Add some extra ways to exit the game.
        # TODO (Activity 7): Currently to exit the Game you need to press BACKSPACE key. Can you change the Key to exit the game by pressing Escape?
        if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
          return

      self.check_ball_hits_paddle()
      self.check_ball_hits_wall()

      # Redraw the screen.
      self.screen.fill((0, 0, 0))

      for paddle in self.paddles:
        paddle.move_paddle(self.HEIGHT)
        pygame.draw.rect(self.screen, self.COLOR, paddle)

      # We know we're not ending the game so lets move the ball here.
      for ball in self.balls:
        ball.move_ball()
        pygame.draw.rect(self.screen, self.COLOR, ball)

      pygame.draw.rect(self.screen, self.COLOR, self.central_line)

      self.draw_text(str(self.LEFTSCORE), 36, 350, 10)
      self.draw_text(str(self.RIGHTSCORE), 36, 450, 10)

      pygame.display.flip()
      self.clock.tick(60)


if __name__ == '__main__':
  pong = Pong()
  pong.game_loop()
