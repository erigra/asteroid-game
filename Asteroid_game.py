from asyncio.proactor_events import _ProactorBaseWritePipeTransport
import pygame, sys

class Ship(pygame.sprite.Sprite):
    def __init__(self, groups):
        # 1. We have to init the parent class
        super().__init__(groups)
        # 2. We need a surface (called an image in the sprite class)
        self.image = pygame.image.load('graphics/ship.png').convert_alpha()
        # 3. We need a rect
        self.rect = self.image.get_rect(center = (WINDOW_WIDTH /2 , WINDOW_HEIGHT /2))
        # timer
        self.can_shoot = True
        self.shoot_time = None

    def laser_timer(self):
        if not self.can_shoot:    
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > 500:
                self.can_shoot = True
    
    def shoot_laser(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            Laser(self.rect.midtop, laser_group)
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def input_position(self):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos

    def update(self):
        self.laser_timer()
        self.shoot_laser()
        self.input_position()


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/laser.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0,-1)
        self.speed = 600

    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))  


# " a basic setup"
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Asteroid game!")
clock = pygame.time.Clock()

# background
background_surf = pygame.image.load("graphics/background.png").convert()

# sprite groups
spaceship_group = pygame.sprite.GroupSingle()
laser_group = pygame.sprite.Group()

# a sprite creation
ship= Ship(spaceship_group)


# Game loop 
while True:

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit

        #delta time
        dt = clock.tick() / 1000

        # Background draw
        display_surface.blit(background_surf, (0,0))

        # Update
        spaceship_group.update()
        laser_group.update()

        # graphics 
        laser_group.draw(display_surface)
        spaceship_group.draw(display_surface)

        # draw the frame
        pygame.display.update()
             