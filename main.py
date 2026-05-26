import pygame
import random
import sys


# --- 1. GAME SETUP ---
pygame.init()

# define constants for screen dimensions 
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# load custom title (ensure SpeedTagTitle.png is in your folder)
try:
    title_img = pygame.image.load("SpeedTagTitle.png").convert_alpha()
except:
    title_img = pygame.Surface((400, 100))
    title_img.fill((50, 50, 50))

# define colors using RGB tuples
RED = (255, 127, 80)
BLUE = (0, 120, 255)
WHITE = (255, 255, 255)
GREY = (235, 235, 235)
LIGHT_YELLOW = (255, 255, 100)
BLACK = (0, 0, 0)
SKY_BLUE = (136, 206, 235)

# define fonts
pygame.font.init()
FONT_LARGE = pygame.font.SysFont("Arial", 80, bold=True)
FONT_MED = pygame.font.SysFont("Arial", 40)
FONT_SMALL = pygame.font.SysFont("Arial", 30)

# define game states
HOME = 0
PLAYING = 1
RESULTS = 2
game_state = HOME

# default selections
selected_time = 60
selected_speed_label = "Med"
selected_speed_val = 5
start_ticks = 0
tag_cooldown = 0
win_text = ''




# --- 2. FUNCTIONS & CLASSES ---

'''function to draw the home screen with title, time and speed selection, and start prompt'''
def draw_home_screen(screen):
    screen.fill((30, 30, 30))
    
    # loading pixilart title and centering 
    img_rect = title_img.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(title_img, img_rect)

    # selecting time, default is 60 seconds
    time_text = FONT_MED.render("Select Time:", True, WHITE)
    screen.blit(time_text, (150, 250)) 
    
    # creating rectangles for time options
    time_options = {
        30: pygame.Rect(400, 250, 80, 50), 
        60: pygame.Rect(500, 250, 80, 50), 
        90: pygame.Rect(600, 250, 80, 50)
    }

    for t, rect in time_options.items():
        color = LIGHT_YELLOW if selected_time == t else GREY
        pygame.draw.rect(screen, color, rect, border_radius=5)
        txt = FONT_SMALL.render(str(t), True, BLACK)
        screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))

    # selecting speed, default is medium
    speed_text = FONT_MED.render("Select Speed:", True, WHITE)
    screen.blit(speed_text, (150, 350))
    
    speed_options = {
        "Slow": (3, pygame.Rect(400, 350, 100, 50)),
        "Med": (5, pygame.Rect(520, 350, 100, 50)),
        "Fast": (7, pygame.Rect(640, 350, 100, 50))
    }
    for label, (val, rect) in speed_options.items():
        if selected_speed_label == label:
            color = LIGHT_YELLOW
        else:
            color = GREY

        pygame.draw.rect(screen, color, rect, border_radius=5)
        txt = FONT_SMALL.render(label, True, BLACK)
        screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))

    # start prompt
    prompt = FONT_SMALL.render("Click anywhere else to Start! Lukas is my favorite dumpling btw!", True, WHITE)
    screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 500))

    return time_options, speed_options



'''class for player and respective methods'''
class Player:
    def __init__(self, x, y, color, controls, starts_tagged = False):
        self.x = x
        self.y = y
        self.controls = controls
        self.is_tagged = starts_tagged
        
        # dimensions
        self.body_w, self.body_h = 20, 15
        self.head_size = 15

        # create Placeholders ( replace with PIXILART images later)
        self.body_surf = pygame.Surface((self.body_w, self.body_h))
        self.body_surf.fill(color)

        self.head_surf = pygame.Surface((self.head_size, self.head_size))
        self.head_surf.fill((200, 200, 200)) # grey head for now
        
        # physics constants: https://api.arcade.academy/en/3.3.1/tutorials/platform_tutorial/step_05.html
        self.vel_y = 0
        self.reg_speed = 5
        self.tag_speed = 5.5
        self.jump_power = -16
        self.gravity = 0.8
        self.floor_y = 550
        
    '''method for player movement'''
    def move(self, platforms):
        keys = pygame.key.get_pressed()

        # tagger has increased speed
        speed = self.tag_speed if self.is_tagged else self.reg_speed

        if keys[self.controls['left']]: 
            self.x -= speed
        if keys[self.controls['right']]: 
            self.x += speed

        # restrict player movement
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.body_w))

        if keys[self.controls['up']] and self.y + self.body_h >= self.floor_y:
            self.vel_y = self.jump_power
        
        self.y += self.vel_y
        
        if self.y + self.body_h < self.floor_y:
            self.vel_y += self.gravity
        else:
            self.y = self.floor_y - self.body_h
            self.vel_y = 0

        # detect collisions with platforms
        player_rect = self.get_rect()
        for plat in platforms:
            if player_rect.colliderect(plat.rect):
                if self.vel_y > 0 and (self.y + self.body_h) < (plat.rect.top + 15):
                    self.y = plat.rect.top - self.body_h
                    self.vel_y = 0
                    if keys[self.controls['up']]:
                        self.vel_y = self.jump_power

    '''method for drawing player'''
    def draw(self, screen):
        # draw Body
        screen.blit(self.body_surf, (self.x, self.y))
        # draw Head (centered on top)
        head_x = self.x + (self.body_w // 2) - (self.head_size // 2)
        head_y = self.y - self.head_size
        screen.blit(self.head_surf, (head_x, head_y))

        if self.is_tagged:
            # draw small yellow triangle pointing down above the head
            tip = (head_x + self.head_size // 2, head_y - 10)
            left = (tip[0] - 8, tip[1] - 12)
            right = (tip[0] + 8, tip[1] - 12)
            pygame.draw.polygon(screen, (255, 255, 0), [tip, left, right])
    
    '''method for creating a rectangle that covers both the head and the body'''
    def get_rect(self):
        return pygame.Rect(self.x, self.y - self.head_size, self.body_w, self.body_h + self.head_size)


'''class for platform creation'''
class Platform:
    def __init__(self, x, y, width, height, color=GREY):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        # Add a little highlight on top for a 3D effect
        pygame.draw.line(screen, WHITE, (self.rect.x, self.rect.y), (self.rect.right, self.rect.y), 2)





# --- 3. INITIALIZE OBJECTS ---

# setup for Player 1
p1_keys = {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w}
player1 = Player(250, 400, BLUE, p1_keys)

# setup for Player 2
p2_keys = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP}
player2 = Player(750, 400, RED, p2_keys)

# list method for determining starting tagger: https://gemini.google.com/share/71d2166bcb58
players = [player1, player2]
random.choice(players).is_tagged = True

# creating map using platform class
platforms = [Platform(400, 400, 200, 20), Platform(100, 300, 150, 20), Platform(700, 250, 150, 20)]




# --- 4. MAIN GAME LOOP ---

while True:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_state == HOME:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get the UI rectangles to check for clicks
                t_btns, s_btns = draw_home_screen(screen)
                clicked_ui = False
                
                # check if a time box was clicked
                for t_val, rect in t_btns.items():
                    if rect.collidepoint(mouse_pos):
                        selected_time = t_val
                        clicked_ui = True
                
                # check if a speed box was clicked
                for label, (val, rect) in s_btns.items():
                    if rect.collidepoint(mouse_pos):
                        selected_speed_label = label
                        selected_speed_val = val
                        clicked_ui = True
                
                # if the user clicked the screen (but not a button), START, and keep regular settings if nothing edited
                if not clicked_ui:
                    for p in players:
                        p.reg_speed = selected_speed_val
                        p.tag_speed = selected_speed_val + 0.5
                    
                    start_ticks = pygame.time.get_ticks()
                    game_state = PLAYING

    # logic & drawing
    if game_state == HOME:
        draw_home_screen(screen)
        
    elif game_state == PLAYING:
        for p in players:
            p.move(platforms)

        # logic for player collisions
        rect1 = player1.get_rect()
        rect2 = player2.get_rect()
        if rect1.colliderect(rect2) and tag_cooldown <= 0:
            player1.is_tagged = not player1.is_tagged
            player2.is_tagged = not player2.is_tagged
            tag_cooldown = 30 # 0.5 second cooldown

        if tag_cooldown > 0:
            tag_cooldown -= 1

        # Timer Calculation
        seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
        time_left = max(0, selected_time - seconds_passed)

        # Drawing
        screen.fill((30, 30, 30)) 
        for plat in platforms:
            plat.draw(screen)
        
        # draw floor and players
        pygame.draw.line(screen, WHITE, (0, 550), (1000, 550), 2) # Floor line
        player1.draw(screen)
        player2.draw(screen)

        # draw UI Timer
        timer_text = FONT_MED.render(f"TIME: {time_left}", True, WHITE)
        screen.blit(timer_text, (SCREEN_WIDTH // 2 - timer_text.get_width() // 2, 20))

        #check for Game Over
        if time_left <= 0:
            game_state = RESULTS
            
            # in Speed Tag, the person who is not tagged at the end wins, same as original!
            if player1.is_tagged:
                win_text = "RED WINS!"
            elif player2.is_tagged:
                win_text = "BLUE WINS!"
            else:
                win_text = "DRAW!"

        
    if game_state == RESULTS:
        if event.type == pygame.MOUSEBUTTONDOWN:
            game_state = HOME  # Go back to menu on click
            

    if game_state == RESULTS:
        #still draw platforms on final screen
        screen.fill((30, 30, 30))
        for plat in platforms: plat.draw(screen)
        player1.draw(screen)
        player2.draw(screen)

        # draw a semi-transparent overlay to make text pop
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150) # Darken the background
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0,0))

        # render and draw full message
        full_message = f"{win_text} Click to restart! Lukas is my favorite dumpling!"
        # Use SKY_BLUE for winner text
        res_surf = FONT_SMALL.render(full_message, True, SKY_BLUE) 
        
        # center it
        res_rect = res_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(res_surf, res_rect)
            
            

    pygame.display.flip()
    clock.tick(60)
