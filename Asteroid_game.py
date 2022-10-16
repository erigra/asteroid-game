import pygame, sys 
from random import randint, uniform

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

    def meteor_collison_check(self):
        if pygame.sprite.spritecollide(self, meteor_group, True):
            pygame.quit()
            sys.exit

    def update(self):
        self.laser_timer()
        self.shoot_laser()
        self.input_position()
        self.meteor_collison_check()


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/laser.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0,-1)
        self.speed = 600

    def laser_hit_check(self):
        if pygame.sprite.spritecollide(self, meteor_group, True):
            self.kill()

    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        self.laser_hit_check()  

class Meteor(pygame.sprite.Sprite):
    def __init__(self, start_pos, groups):
        super().__init__(groups)
        # make random scaled meteor
        scale = randint(50,150)
        self.scaled_image = pygame.transform.scale(pygame.image.load('graphics/meteor.png').convert_alpha(), (scale,scale))
        self.image = self.scaled_image
        self.rect = self.image.get_rect(midbottom = start_pos)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(uniform(-0.5,0.5),1)
        self.speed = randint(300,600)
        self.rotation = 0
        self.rotation_speed = randint(20,50)

    def rotate(self):
        self.rotation += self.rotation_speed *dt
        rotated_meteor = pygame.transform.rotozoom(self.scaled_image, self.rotation,1)
        self.image = rotated_meteor
        self.rect = self.image.get_rect(center = self.rect.center)


    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        self.rotate()

class Score():
    def __init__(self):
        self.font = pygame.font.Font("graphics/subatomic.ttf",30)        

    def display(self, surface):
        self.score_text = f"Score: {pygame.time.get_ticks() //1000}"
        self.text_surf = self.font.render(self.score_text, True, (255,255,255))
        self.text_rect = self.text_surf.get_rect(midbottom = (WINDOW_WIDTH/2, WINDOW_HEIGHT -80))
        surface.blit(self.text_surf, self.text_rect)
        pygame.draw.rect(surface, (255,255,255), self.text_rect.inflate(30,30), width = 5, border_radius=5)


# " a basic setup"
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Asteroid game!")
clock = pygame.time.Clock()
meteor_spawn_time = pygame.time.get_ticks()
meteor_time_rate = 500

# background
background_surf = pygame.image.load("graphics/background.png").convert()

# sprite groups
spaceship_group = pygame.sprite.GroupSingle()
laser_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()

# a sprite creation
ship= Ship(spaceship_group)

#score creation
score = Score()


# Game loop 
while True:

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit

        #delta time
        dt = clock.tick() / 1000
       
        # meteor timer
        current_time = pygame.time.get_ticks()
        if current_time - meteor_spawn_time > meteor_time_rate:
            Meteor((randint(-100,WINDOW_WIDTH +100), randint(-150,0)), meteor_group)
            meteor_spawn_time = pygame.time.get_ticks()

        # Background draw
        display_surface.blit(background_surf, (0,0))

        # Update
        spaceship_group.update()
        laser_group.update()
        meteor_group.update()

        # score
        score.display(display_surface)

        # graphics 
        laser_group.draw(display_surface)
        spaceship_group.draw(display_surface)
        meteor_group.draw(display_surface)

        # draw the frame
        pygame.display.update()
             