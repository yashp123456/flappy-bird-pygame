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
#Sanika 
text_surface = font.render('Use space to boost your bird higher', True, (0,0,0))
text_surface1 = font.render('to get through the pipes without touching them', True, (0,0,0))
text_rect = text_surface.get_rect()
text_rect1 = text_surface1.get_rect()
text_rect.center = (SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) - 150)
text_rect1.center = (SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) - 120)


game_state = "menu"
objects = []

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.speed = 5 
        self.started = False
        try:
            self.surf = pygame.image.load("bird.png").convert()
            self.surf = pygame.transform.scale(self.surf, (40, 40))
            self.surf.set_colorkey((135, 206, 250))
        except:
            self.surf = pygame.Surface((30, 30))
            self.surf.fill((255, 200, 0))
            
        self.rect = self.surf.get_rect(
            center=(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        )

    def update(self, pressed_keys):
        if pressed_keys[K_SPACE]:
            self.started = True
        
        if self.started:
            self.rect.move_ip(0, 5) 
            if pressed_keys[K_SPACE]:
                self.rect.move_ip(0, -self.speed - 15) 
            
            if self.rect.bottom > SCREEN_HEIGHT:
                self.kill()

class Pipe(pygame.sprite.Sprite):
    def __init__(self):
        super(Pipe, self).__init__()
        self.gap = 150
        self.width = 70
        self.top_height = random.randint(50, SCREEN_HEIGHT - self.gap - 50)

        try:
            img_top = pygame.image.load("top-pipe.png").convert()
            img_bottom = pygame.image.load("bottom-pipe.png").convert()
            img_top.set_colorkey((255, 255, 255))
            img_bottom.set_colorkey((255, 255, 255))
        except:
            img_top = pygame.Surface((self.width, SCREEN_HEIGHT))
            img_bottom = pygame.Surface((self.width, SCREEN_HEIGHT))
            img_top.fill((0, 255, 0))
            img_bottom.fill((0, 255, 0))

        self.top_surf = pygame.transform.scale(img_top, (self.width, self.top_height))
        self.top_rect = self.top_surf.get_rect(topleft=(SCREEN_WIDTH, 0))

        bot_height = SCREEN_HEIGHT - (self.top_height + self.gap)
        self.bottom_surf = pygame.transform.scale(img_bottom, (self.width, bot_height))
        self.bottom_rect = self.bottom_surf.get_rect(
            topleft=(SCREEN_WIDTH, self.top_height + self.gap)
        )

    def update(self):
        self.top_rect.move_ip(-5, 0)
        self.bottom_rect.move_ip(-5, 0)

        if self.top_rect.right < 0:
            self.kill()

    def draw(self, surface):
        surface.blit(self.top_surf, self.top_rect)
        surface.blit(self.bottom_surf, self.bottom_rect)

    
class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))
        objects.append(self)

    def process(self):
            mousePos = pygame.mouse.get_pos()
            self.buttonSurface.fill(self.fillColors['normal'])
            if self.buttonRect.collidepoint(mousePos):
                self.buttonSurface.fill(self.fillColors['hover'])
                if pygame.mouse.get_pressed(num_buttons=3)[0]:
                    self.buttonSurface.fill(self.fillColors['pressed'])
                    if self.onePress:
                        self.onclickFunction()
                    elif not self.alreadyPressed:
                        self.onclickFunction()
                        self.alreadyPressed = True
                else:
                    self.alreadyPressed = False
            self.buttonSurface.blit(self.buttonSurf, [
                self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
                self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
            ])
            screen.blit(self.buttonSurface, self.buttonRect)

def start_game():
    global game_state, player, pipes
    game_state = "playing"
    player = Player()
    pipes = pygame.sprite.Group()

def my_function():
    print("Button Pressed!")


easy_button = Button(350, 200, 100, 50, 'Easy', start_game)
hard_button = Button(350, 300, 100, 50, 'Hard', start_game)


ADDPIPE = pygame.USEREVENT + 1
pygame.time.set_timer(ADDPIPE, 1750)
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

    if game_state == "menu":
        screen.fill((135, 206, 250))
        screen.blit(text_surface, text_rect)
        screen.blit(text_surface1, text_rect1)
        for obj in objects:
            obj.process()
            
    elif game_state == "playing":
        screen.fill((135, 206, 250))

        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)

        if player.started:
            pipes.update()

        for pipe in pipes:
            pipe.draw(screen)
            if player.rect.colliderect(pipe.top_rect) or player.rect.colliderect(pipe.bottom_rect):
                running = False

        screen.blit(player.surf, player.rect)

        if player.rect.bottom > SCREEN_HEIGHT:
            running = False
            



    pygame.display.flip()
    clock.tick(30)


pygame.quit()
sys.exit()