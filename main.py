import pygame
import sys

# setup for dimensions of screen
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

RED = (255, 127, 80)
BLUE = (0, 120, 255)
WHITE = (255, 255, 255)


'''class for player and respective methods'''
class Player:
    def __init__(self, x, y, color, controls):
        self.x = x
        self.y = y
        self.controls = controls
        
        # dimensions
        self.body_w, self.body_h = 40, 60
        self.head_size = 30
        
        # create Placeholders ( replace with PIXILART images later)
        self.body_surf = pygame.Surface((self.body_w, self.body_h))
        self.body_surf.fill(color)

        self.head_surf = pygame.Surface((self.head_size, self.head_size))
        self.head_surf.fill((200, 200, 200)) # grey head for now
        
        # physics constants: https://api.arcade.academy/en/3.3.1/tutorials/platform_tutorial/step_05.html
        self.vel_y = 0
        self.speed = 7
        self.jump_power = -16
        self.gravity = 0.8
        self.floor_y = 550


    def move(self):
        keys = pygame.key.get_pressed()
        if keys[self.controls['left']]: 
            self.x -= self.speed
        if keys[self.controls['right']]: 
            self.x += self.speed
        if keys[self.controls['up']] and self.y + self.body_h >= self.floor_y:
            self.vel_y = self.jump_power
        self.y += self.vel_y
        if self.y + self.body_h < self.floor_y:
            self.vel_y += self.gravity
        else:
            self.y = self.floor_y - self.body_h
            self.vel_y = 0



    def draw(self, screen):
        # draw Body
        screen.blit(self.body_surf, (self.x, self.y))
        # draw Head (centered on top)
        head_x = self.x + (self.body_w // 2) - (self.head_size // 2)
        head_y = self.y - self.head_size
        screen.blit(self.head_surf, (head_x, head_y))


# --- MAIN GAME LOOP ---
pygame.init()

#https://gemini.google.com/share/71d2166bcb58
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()

# Setup Player 1
p1_keys = {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w}
player1 = Player(250, 400, BLUE, p1_keys)

#Setup Player 2
p2_keys = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP}
player2 = Player(750, 400, RED, p2_keys)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    player1.move()
    player2.move()


    screen.fill((30, 30, 30)) 
    pygame.draw.line(screen, WHITE, (0, 550), (1000, 550), 2) # Floor line
    player1.draw(screen)
    player2.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)