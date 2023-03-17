import pygame, sys, random
pygame.init()


SCREEN = pygame.display.set_mode((700, 600))
pygame.display.set_caption("Tennis 2k22")


BG = pygame.image.load("nadal2.jpeg")


FPS=60
WIDTH, HEIGHT = 700, 600


screen = pygame.display.set_mode((WIDTH, HEIGHT))
SCREEN = pygame.display.set_mode((700, 600))
pygame.display.set_caption("Tennis 2k22")


clock = pygame.time.Clock()
start_sound = pygame.mixer.Sound("start.mp3")
multi_sound = pygame.mixer.Sound("multi.mp3")
gui_font = pygame.font.Font(None, 30)


WHITE = (255, 255, 255)
RED = (255,0,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
GREEN=(0,255,0)


COURT= pygame.transform.scale(pygame.image.load('claycourt.jpg'),(WIDTH,HEIGHT+20))


PADDLE_WIDTH, PADDLE_HEIGHT = 50, 60
BALLW, BALLH = 30, 30


opponent_speed = 70


ball = pygame.Rect(WIDTH//2 - 10, HEIGHT//2 - 10,20,20)
speedx = 6 * random.choice((1, -1))
speedy = 6 * random.choice((1, -1))


plob_sound = pygame.mixer.Sound("bounce.wav")
score_sound = pygame.mixer.Sound("point.wav")


basic_font = pygame.font.Font('font.ttf', 32)










class Ballblock(pygame.sprite.Sprite):
   def __init__(self,path,x_pos,y_pos):
       super().__init__()
       self.image = pygame.transform.scale(pygame.image.load(path),((BALLW, BALLH)))
       self.rect = self.image.get_rect(center = (x_pos,y_pos))




class Block(pygame.sprite.Sprite):
   def __init__(self,path,x_pos,y_pos):
       super().__init__()
       self.image = pygame.transform.scale(pygame.image.load(path),((PADDLE_WIDTH, PADDLE_HEIGHT)))
       self.rect = self.image.get_rect(center = (x_pos,y_pos))




class Player(Block):
   def __init__(self,path,x_pos,y_pos,speed):
       super().__init__(path,x_pos,y_pos)
       self.speed = speed
       self.movementx = 0
       self.movementy = 0




   def screen_constrain(self):
       if self.rect.left<=0.5*WIDTH + 5:
           self.rect.left=0.5*WIDTH + 5
       if self.rect.right>=WIDTH:
           self.rect.right=WIDTH
       if self.rect.top <= 65:
           self.rect.top = 65
       if self.rect.bottom >= HEIGHT-5:
           self.rect.bottom = HEIGHT-5


   def update(self,ball_group):
       self.rect.x += self.movementx
       self.rect.y += self.movementy
       self.screen_constrain()




class Ball(Ballblock):
   def __init__(self,path,x_pos,y_pos,speed_x,speed_y,paddles):
       super().__init__(path,x_pos,y_pos)
       self.speed_x = 0.2*speed_x * random.choice((-1,1))
       self.speed_y = 0.2*speed_y * random.choice((-1,1))
       self.paddles = paddles
       self.active = False
       self.score_time = 0


   def update(self):
       if self.active:
           self.rect.x += self.speed_x
           self.rect.y += self.speed_y
           self.collisions()
       else:
           self.restart_counter()
      
   def collisions(self):
       if self.rect.top <= 50 or self.rect.bottom >= HEIGHT-5:
           pygame.mixer.Sound.play(plob_sound)
           self.speed_y *= -1


       if pygame.sprite.spritecollide(self,self.paddles,False):
           pygame.mixer.Sound.play(plob_sound)
           collision_paddle = pygame.sprite.spritecollide(self,self.paddles,False)[0].rect
           if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
               self.speed_x *= -1
           if abs(self.rect.left - collision_paddle.right) < 10 and self.speed_x < 0:
               self.speed_x *= -1
           if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_y < 0:
               self.rect.top = collision_paddle.bottom
               self.speed_y *= -1
           if abs(self.rect.bottom - collision_paddle.top) < 10 and self.speed_y > 0:
               self.rect.bottom = collision_paddle.top
               self.speed_y *= -1


   def reset_ball(self):
       self.active = False
       self.speed_x *= random.choice((-1,1))
       self.speed_y *= random.choice((-1,1))
       self.score_time = pygame.time.get_ticks()
       self.rect.center = (WIDTH/2,HEIGHT/2)
       pygame.mixer.Sound.play(score_sound)


   def restart_counter(self):
       current_time = pygame.time.get_ticks()
       countdown_number = 3


       if current_time - self.score_time <= 700:
           countdown_number = 3
       if 700 < current_time - self.score_time <= 1400:
           countdown_number = 2
       if 1400 < current_time - self.score_time <= 2100:
           countdown_number = 1
       if current_time - self.score_time >= 2100:
           self.active = True


       time_counter = basic_font.render(str(countdown_number),True,BLACK)
       time_counter_rect = time_counter.get_rect(center = (WIDTH/2,HEIGHT/2 + 50))
       pygame.draw.rect(screen,GREEN,time_counter_rect)
       screen.blit(time_counter,time_counter_rect)




class Opponent(Block):
   def __init__(self,path,x_pos,y_pos,speed):
       super().__init__(path,x_pos,y_pos)
       self.speed = speed


   def update(self,ball_group):
       if self.rect.top < ball_group.sprite.rect.y:
           self.rect.y += self.speed
       if self.rect.bottom > ball_group.sprite.rect.y:
           self.rect.y -= self.speed
       self.constrain()


   def constrain(self):
       if self.rect.top <= 65: self.rect.top = 65
       if self.rect.bottom >= HEIGHT-5: self.rect.bottom = HEIGHT-5




class PlayerTwo(Block):
   def __init__(self,path,x_pos,y_pos,speed):
       super().__init__(path,x_pos,y_pos)
       self.speed = speed


   def screen_constrain(self):
       if self.rect.right>=0.5*WIDTH - 5:
           self.rect.right=0.5*WIDTH - 5
       if self.rect.top <= 65:
           self.rect.top = 65
       if self.rect.bottom >= HEIGHT-5:
           self.rect.bottom = HEIGHT-5


   def update(self,ball_group):
       positionMouse= pygame.mouse.get_pos()
       self.rect.x=positionMouse[0]
       self.rect.y=positionMouse[1]
       self.screen_constrain()




class GameManager:
   def __init__(self,ball_group,paddle_group):
       self.player_score = 0
       self.opponent_score = 0
       self.ball_group = ball_group
       self.paddle_group = paddle_group


   def run_game(self):
       # Drawing the game objects
       self.paddle_group.draw(screen)
       self.ball_group.draw(screen)


       # Updating the game objects
       self.paddle_group.update(self.ball_group)
       self.ball_group.update()
       self.reset_ball()
       self.draw_score()


   def reset_ball(self):
       if self.ball_group.sprite.rect.right >= WIDTH:
           self.opponent_score += 1
           self.ball_group.sprite.reset_ball()
       if self.ball_group.sprite.rect.left <= 0:
           self.player_score += 1
           self.ball_group.sprite.reset_ball()


   def draw_score(self):
       player_score = basic_font.render(str(self.player_score),True,BLACK)
       opponent_score = basic_font.render(str(self.opponent_score),True,BLACK)


       player_score_rect = player_score.get_rect(midleft = (WIDTH / 2 + 40,75))
       opponent_score_rect = opponent_score.get_rect(midright = (WIDTH / 2 - 40,75))


       screen.blit(player_score,player_score_rect)
       screen.blit(opponent_score,opponent_score_rect)




class Button():
   def __init__(self, width, height, pos, post, text_input, font, base_color, hovering_color):
       self.x_pos = post[0]
       self.y_pos = post[1]
       self.font = font
       self.base_color, self.hovering_color = base_color, hovering_color
       self.text_input = text_input
       self.text = self.font.render(self.text_input, True, self.base_color)
       self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
       self.top_rect = pygame.Rect(pos,(width,height))


   def draw(self, screen):
       pygame.draw.rect(screen,"Black", self.top_rect,border_radius = 12)
       screen.blit(self.text, self.text_rect)


   def update(self, screen):
       screen.blit(self.text, self.text_rect)


   def checkForInput(self, pos):
       if self.top_rect.collidepoint(pos):
           return True
       return False


   def changeColor(self, pos):
       if self.top_rect.collidepoint(pos):
           self.text = self.font.render(self.text_input, True, self.hovering_color)
       else:
           self.text = self.font.render(self.text_input, True, self.base_color)










def get_font(size): # Returns Press-Start-2P in the desired size
   return pygame.font.Font(None, size)






def singleplayer():
   p1 = Player('goatlogo.png', WIDTH - 20, HEIGHT/2, 5)
   opponent = Opponent('goatlogo.png',20,WIDTH/2,5)
   paddle_group = pygame.sprite.Group()
   paddle_group.add(p1)
   paddle_group.add(opponent)


   ball = Ball('Ball.png',WIDTH/2,HEIGHT/2,4,4,paddle_group)
   ball_sprite = pygame.sprite.GroupSingle()
   ball_sprite.add(ball)
   game_manager = GameManager(ball_sprite,paddle_group)


   while True:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()
           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_UP:
                   p1.movementy -= p1.speed
               if event.key == pygame.K_DOWN:
                   p1.movementy += p1.speed
           if event.type == pygame.KEYUP:
               if event.key == pygame.K_UP:
                   p1.movementy += p1.speed
               if event.key == pygame.K_DOWN:
                   p1.movementy -= p1.speed


           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_LEFT:
                   p1.movementx -= p1.speed
               if event.key == pygame.K_RIGHT:
                   p1.movementx += p1.speed
           if event.type == pygame.KEYUP:
               if event.key == pygame.K_LEFT:
                   p1.movementx += p1.speed
               if event.key == pygame.K_RIGHT:
                   p1.movementx -= p1.speed


       # Background Stuff
       screen.fill(BLACK)
       screen.blit(COURT,(0,0))
      
       # Run the game
       game_manager.run_game()


       pygame.display.flip()


  


def multiplayer():
   p1 = Player('goatlogo.png', WIDTH - 20, HEIGHT/2, 5)
   opponent = PlayerTwo('goatlogo.png',20,WIDTH/2,5)
   paddle_group = pygame.sprite.Group()
   paddle_group.add(p1)
   paddle_group.add(opponent)


   ball = Ball('Ball.png',WIDTH/2,HEIGHT/2,4,4,paddle_group)
   ball_sprite = pygame.sprite.GroupSingle()
   ball_sprite.add(ball)
   game_manager = GameManager(ball_sprite,paddle_group)


   while True:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()
           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_UP:
                   p1.movementy -= p1.speed
               if event.key == pygame.K_DOWN:
                   p1.movementy += p1.speed
           if event.type == pygame.KEYUP:
               if event.key == pygame.K_UP:
                   p1.movementy += p1.speed
               if event.key == pygame.K_DOWN:
                   p1.movementy -= p1.speed


           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_LEFT:
                   p1.movementx -= p1.speed
               if event.key == pygame.K_RIGHT:
                   p1.movementx += p1.speed
           if event.type == pygame.KEYUP:
               if event.key == pygame.K_LEFT:
                   p1.movementx += p1.speed
               if event.key == pygame.K_RIGHT:
                   p1.movementx -= p1.speed


       # Background Stuff
       screen.fill(BLACK)
       screen.blit(COURT,(0,0))
      
       # Run the game
       game_manager.run_game()


       pygame.display.flip()






def main_menu():
   while True:
       SCREEN.blit(BG, (-320, -5))


       MENU_MOUSE_POS = pygame.mouse.get_pos()


       font_path = 'font.ttf' # or wherever your font file is
       size = 100
       my_font = pygame.font.Font(font_path, size)
       MENU_TEXT = my_font.render("TENNIS 2K22", True, "#b68f40")
       MENU_RECT = MENU_TEXT.get_rect(center=(350, 100))


       SINGLE_BUTTON = Button(500,80, (100, 200), (350, 242),
                           "SINGLE PLAYER", get_font(75), "#bac564", "White")
       MULT_BUTTON = Button(400, 80, (150, 320), (353, 362),
                           "MULTI PLAYER", get_font(75), "#bac564", "White")
       QUIT_BUTTON = Button(200, 80, (250, 440), (347, 485),
                           "QUIT", get_font(75), "#bac564", "White")


       SCREEN.blit(MENU_TEXT, MENU_RECT)


       for button in [SINGLE_BUTTON, MULT_BUTTON, QUIT_BUTTON]:
           button.changeColor(MENU_MOUSE_POS)
           button.draw(SCREEN)
      
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()
           if event.type == pygame.MOUSEBUTTONDOWN:
               if SINGLE_BUTTON.checkForInput(MENU_MOUSE_POS):
                   singleplayer()
               if MULT_BUTTON.checkForInput(MENU_MOUSE_POS):
                   multiplayer()
               if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                   pygame.quit()
                   sys.exit()


       pygame.display.update()


main_menu()