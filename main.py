import pygame, sys
import random

from pygame.locals import (
    RLEACCEL,
    K_SPACE
)   
 
# Initialize pygame
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.SysFont('Arial', 20)
small_font = pygame.font.SysFont('Arial', 20)

background_img = pygame.image.load("flappybird-background.png").convert()
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

text_surface = font.render('Use space to boost your bird higher', True, (0,0,0))
text_surface1 = font.render('to get through the pipes without touching them', True, (0,0,0))
text_rect = text_surface.get_rect()
text_rect1 = text_surface1.get_rect()
text_rect.center = (SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) - 150)
text_rect1.center = (SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) - 120)

game_state = "menu"
score = 0
easy_high_score = 0
hard_high_score = 0
current_mode = "easy"
objects = []

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.speed = 15 
        self.started = False
        self.velocity = 0
        self.gravity = 1.5
        self.jump_power = -13
        self.can_jump = True
        
        try:
            def load_bird(path):
                img = pygame.image.load(path).convert()
                color_to_remove = img.get_at((0, 0))
                img.set_colorkey(color_to_remove)

                return pygame.transform.scale(img, (48, 37))

            self.frames = [
                load_bird("bird1.png"),
                load_bird("bird2.png"),
                load_bird("bird3.png"),
                load_bird("bird4.png"),
                load_bird("bird5.png")
            ]
        except:
            self.frames = [pygame.Surface((40, 40)) for _ in range(5)]
            for i, f in enumerate(self.frames): f.fill((255, 200, 10 * i))

        self.current_frame = 0
        self.surf = self.frames[self.current_frame]
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
        
        self.anim_speed = 0.2 
        self.anim_index = 0
        
    def animate(self):
        self.anim_index += self.anim_speed
        if self.anim_index >= len(self.frames):
            self.anim_index = 0
        self.current_frame = int(self.anim_index)
        self.surf = self.frames[self.current_frame]

    def update(self, pressed_keys):
        if pressed_keys[pygame.K_SPACE]:
            if self.can_jump:
                self.started = True
                self.velocity = self.jump_power
                self.can_jump = False  
        else:
            self.can_jump = True 

        if self.started:
            self.animate()
            self.velocity += self.gravity
            self.rect.move_ip(0, self.velocity)

            if self.rect.top <= 0:
                self.rect.top = 0
                self.velocity = 0
            
            if self.rect.bottom >= SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT
                self.velocity = 0

class Pipe(pygame.sprite.Sprite):
    def __init__(self):
        super(Pipe, self).__init__()
        self.gap = 150
        self.width = 70
        self.passed = False 
        self.top_height = random.randint(50, SCREEN_HEIGHT - self.gap - 50)
        try:
            img_top = pygame.image.load("top-pipe.png").convert()
            img_bottom = pygame.image.load("bottom-pipe.png").convert()
            img_top.set_colorkey((255, 255, 255))
            img_bottom.set_colorkey((255, 255, 255))
        except:
            img_top = pygame.Surface((self.width, SCREEN_HEIGHT)); img_top.fill((0, 255, 0))
            img_bottom = pygame.Surface((self.width, SCREEN_HEIGHT)); img_bottom.fill((0, 255, 0))

        self.top_surf = pygame.transform.scale(img_top, (self.width, self.top_height))
        self.top_rect = self.top_surf.get_rect(topleft=(SCREEN_WIDTH, 0))
        bot_height = SCREEN_HEIGHT - (self.top_height + self.gap)
        self.bottom_surf = pygame.transform.scale(img_bottom, (self.width, bot_height))
        self.bottom_rect = self.bottom_surf.get_rect(topleft=(SCREEN_WIDTH, self.top_height + self.gap))

    def update(self):
        self.top_rect.move_ip(-5, 0)
        self.bottom_rect.move_ip(-5, 0)
        if self.top_rect.right < 0:
            self.kill()

    def draw(self, surface):
        surface.blit(self.top_surf, self.top_rect)
        surface.blit(self.bottom_surf, self.bottom_rect)
    
class Button():
    def __init__(self, x, y, width, height, buttonText, onclickFunction, args, color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = buttonText
        self.onclick = onclickFunction
        self.args = args
        self.base_color = color
        objects.append(self)

    def process(self):
        mousePos = pygame.mouse.get_pos()
        color = self.base_color
        if self.rect.collidepoint(mousePos):
            color = (200, 200, 200)
            if pygame.mouse.get_pressed()[0]:
                self.onclick(self.args)
        
        pygame.draw.rect(screen, color, self.rect)
        txt = small_font.render(self.text, True, (0,0,0))
        screen.blit(txt, (self.rect.centerx - txt.get_width()//2, self.rect.centery - txt.get_height()//2))

def start_game(args):
    global game_state, player, pipes, score, current_mode
    pipe_frequency, mode = args
    game_state = "playing"
    score = 0
    current_mode = mode
    player = Player()
    pipes = pygame.sprite.Group()
    pygame.time.set_timer(ADDPIPE, pipe_frequency)

def menu(args=None):
    global game_state, player, pipes, score, current_mode
    game_state = "menu"
    title = font.render("Flappy Bird", True, (0,0,0))
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
    easy_button.process()
    hard_button.process()

def my_function():
    print("Button Pressed!")

easy_button = Button(350, 200, 100, 50, 'Easy', start_game, args=(2000, "easy"))
hard_button = Button(350, 260, 100, 50, 'Hard', start_game, args=(1500, "hard"))
retry_button = Button(350, 350, 130, 50, 'Restart', start_game, (2000, current_mode),(255, 238, 140))
change_button = Button(350, 410, 130, 50, 'Change Level', menu, None, (255, 238, 140)) 


ADDPIPE = pygame.USEREVENT + 1
pygame.time.set_timer(ADDPIPE, 2000)

# Variable to keep the main loop running
running = True

player = Player()
pipes = pygame.sprite.Group()
clock = pygame.time.Clock()

# Main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if game_state == "playing" and event.type == ADDPIPE:
            pipes.add(Pipe())
    screen.blit(background_img, (0, 0))

    if game_state == "menu":
        title = font.render("Flappy Bird", True, (0,0,0))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
        easy_button.process()
        hard_button.process()

    elif game_state == "playing":
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        if player.started:
            pipes.update()

        for pipe in pipes:
            pipe.draw(screen)

            if player.rect.colliderect(pipe.top_rect) or player.rect.colliderect(pipe.bottom_rect):
                game_state = "game_over"

            if not pipe.passed and pipe.top_rect.right < player.rect.left:
                score += 1
                pipe.passed = True

        screen.blit(player.surf, player.rect)

        if player.rect.bottom > SCREEN_HEIGHT or player.rect.top < 0:
            game_state = "game_over"

        score_txt = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_txt, (10, 10))
    elif game_state == "game_over":
        if current_mode == "easy":
            if score > easy_high_score: easy_high_score = score
            current_hi = easy_high_score
        else:
            if score > hard_high_score: hard_high_score = score
            current_hi = hard_high_score
        
        over_txt = font.render("GAME OVER", True, (200, 0, 0))
        sc_txt = font.render(f"Score: {score}", True, (0,0,0))
        hi_txt = font.render(f"High Score: {current_hi}", True, (0,0,0))
        
        screen.blit(over_txt, (SCREEN_WIDTH//2 - over_txt.get_width()//2, 150))
        screen.blit(sc_txt, (SCREEN_WIDTH//2 - sc_txt.get_width()//2, 220))
        screen.blit(hi_txt, (SCREEN_WIDTH//2 - hi_txt.get_width()//2, 260))
        retry_button.process()  

        change_button.process()            

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()