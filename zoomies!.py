import pygame, math, time
from random import choices, choice, randint
from sys import exit

class Cat(pygame.sprite.Sprite): # Cat sprite!
    def __init__(self):
        super().__init__()

        # Frames
        self.frames = []
        self.frames.append(pygame.image.load('cat/frame1.png').convert_alpha())
        self.frames.append(pygame.image.load('cat/frame2.png').convert_alpha())
        self.frames.append(pygame.image.load('cat/frame3.png').convert_alpha())
        self.frames.append(pygame.image.load('cat/frame4.png').convert_alpha())
        self.cat_jump = pygame.image.load('cat/jump.png').convert_alpha()
        self.frame_index = 0

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(midbottom = (80, 370))
        self.jump_meow = pygame.mixer.Sound('sounds/cat_jump.mp3')

        self.gravity = 0
        self.velocity = 0
        self.acceleration = 0.02
        self.is_moving = False
        

    def control_input(self): # Allows our cat to jump!
        
        keys = pygame.key.get_pressed()
        if game_active:
            
            self.is_moving = True
            self.velocity = 0
            if keys[pygame.K_SPACE] and self.rect.bottom >= 370:
                self.gravity = -7
                
                if randint(1, 10) == 10:
                    self.jump_meow.play()
                    self.jump_meow.set_volume(0.15)
        else:
            
            self.is_moving = False

            if keys[pygame.K_RIGHT]:
                self.is_moving = True
                self.rect.x += 2
                if self.rect.left > 800: self.rect.right = -100
                self.velocity += self.acceleration
                if self.velocity > 2: self.velocity = 2
            else: 
                if self.rect.bottom < 370: self.is_moving = True
                else: self.is_moving = False
                
                self.velocity -= self.acceleration
                if self.velocity < 0: self.velocity = 0

            self.rect.x += self.velocity
            

            if keys[pygame.K_UP] and self.rect.bottom >= 370:
                self.gravity = -7

    def add_gravity(self): # Makes our cat fall!
        self.gravity += 0.1
        self.rect.y += self.gravity 
        if self.rect.bottom >= 370: self.rect.bottom = 370

    def reset_position(self):
        self.gravity = 0
        self.rect.midbottom = (80, 370)

    def animate(self):
        if self.is_moving:

            if self.rect.bottom < 370:
                self.image = self.cat_jump

            else:
                self.frame_index += 0.075
                if self.frame_index >= len(self.frames): self.frame_index = 0
                self.image = self.frames[int(self.frame_index)]

        else: self.image = self.frames[0]

    def update(self): # Updates all methods of our cat sprite!
        self.control_input()
        self.add_gravity()
        self.animate()
        
class Obstacles(pygame.sprite.Sprite):
    def __init__(self, object):
        super().__init__()
    
        ground_objects = {'trash'   : pygame.image.load('obstacles/trash.png').convert_alpha(),
                          'cone'    : pygame.image.load('obstacles/cone.png').convert_alpha(),
                          'mail1'   : pygame.image.load('obstacles/mail1.png').convert_alpha(),
                          'mail2'   : pygame.image.load('obstacles/mail2.png').convert_alpha()}
                 
        flying_objects = {'plane'   : pygame.image.load('obstacles/plane.png').convert_alpha(),
                          'balloon' : pygame.image.load('obstacles/balloon.png').convert_alpha()}
        
        self.speed = 2 + (current_time // 15) * 0.2

        self.object = object
        if object in ground_objects:
            self.image = ground_objects[object]
            y_pos = 375
        else:
            self.image = flying_objects[object]
            y_pos = 200
            self.phase_shift = randint(0, 360)
        
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

    def clear(self):
        if self.rect.x <= -100: self.kill()

    def update(self):
        print(self.speed, concrete_scroll_speed)

        self.speed = 2 + (current_time // 15) * 0.2
        self.rect.x -= self.speed
        self.clear()

        if self.object == 'plane' or self.object == 'balloon': 
            phase_to_radians = math.radians(self.phase_shift)
            y_oscillation = 25 * math.sin(0.004 * pygame.time.get_ticks() + phase_to_radians)
            self.rect.y = 180 + y_oscillation

def show_score():
    global current_time
    current_time = (pygame.time.get_ticks() - start_time) // 1000
    
    score_surface = font.render(f"Score: {current_time}", True, (255, 233, 229))
    score_drop_surface = font.render(f"Score: {current_time}", True, (100, 83, 78))
    score_rect = score_surface.get_rect(center = (400, 35))
    score_drop_rect = score_drop_surface.get_rect(center = (402, 37))
    
    screen.blit(score_drop_surface, score_drop_rect)
    screen.blit(score_surface, score_rect)
    

    return current_time

def collisions():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        player.sprite.reset_position()
        time.sleep(0.75)
        return False
    return True
        
def music_loop():
    if not pygame.mixer.music.get_busy():
            
            global prev_song, bg_music

            bg_music = choice([song for song in bg_songs if song != prev_song])
            prev_song = bg_music
            pygame.mixer.music.load(bg_music)
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(0.2)

# == SETUP ==

pygame.init()

screen_width = 800
screen_height = 400

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Zoomies!')
clock = pygame.time.Clock()
font = pygame.font.Font('font/ubuntu.medium.ttf', 35)
game_active = False


start_time = 0
score = 0

# == MUSIC ==
bg_songs = ['music/track1.mp3', 'music/track2.mp3', 'music/track3.mp3 ']
bg_music = (choice(bg_songs))
prev_song = bg_music

pygame.mixer.music.load(bg_music)
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.2)

# == SURFACES ==
concrete_surface = pygame.image.load('concrete.png').convert()
concrete_surface_width = concrete_surface.get_width()
concrete_surface_rect = concrete_surface.get_rect(center = (400, 375))

bg_surface = pygame.image.load('city_bg.png').convert()
bg_surface_width = bg_surface.get_width()
bg_surface_rect = bg_surface.get_rect(center = (400, 175))

city_surfaces = []

for num in range(1, 4):
    city_surface = pygame.image.load(f'city_layer{num}.png').convert_alpha()
    city_surfaces.append(city_surface)

# == VARIABLES == 
bg_scroll, concrete_scroll, city_scroll1, city_scroll2, city_scroll3 = 0, 0, 0, 0, 0
tiles = (screen_width // bg_surface_width) + 1

# == GROUPS ==
player = pygame.sprite.GroupSingle()
player.add(Cat())

obstacle_group = pygame.sprite.Group()

# == OBSTACLE TIMER ==     (controls enemy spawn rate)
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

obstacle_types = ['trash', 'cone', 'mail1', 'mail2', 'plane', 'balloon']
obstacle_probabilities = [0.21, 0.21, 0.21, 0.1, 0.21, 0.06]


# == GAME LOOP == 
while True:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_choice = choices(obstacle_types, weights=obstacle_probabilities)[0]
                obstacle_group.add(Obstacles(obstacle_choice))

        else: 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # pygame.time.wait(2000)
                game_active = True
                player.sprite.reset_position()
                start_time = pygame.time.get_ticks()

    # == MAIN GAME ==
    if game_active:

        # Randomly Loop Through Music
        music_loop()

        # Draw Scrolling Background
        screen.blit(bg_surface, (0, 0))

        for i in range(tiles): screen.blit(city_surfaces[0], (i * bg_surface_width - city_scroll1, 0))
        for i in range(tiles): screen.blit(city_surfaces[1], (i * bg_surface_width - city_scroll2, 0))
        for i in range(tiles): screen.blit(city_surfaces[2], (i * bg_surface_width - city_scroll3, 0))

        # Draw Concrete Surface
        for i in range(tiles): screen.blit(concrete_surface, (i * concrete_surface_width - concrete_scroll, 350))
        
        # Show our score
        score = show_score()

        # Scroll Background
        bg_scroll += 0.1
        city_scroll1 += 0.2
        city_scroll2 += 0.22
        city_scroll3 += 0.24
        concrete_scroll_speed = 2 + (((pygame.time.get_ticks() - start_time) // 1000) // 15) * 0.2 
        concrete_scroll += concrete_scroll_speed

        if bg_scroll >= bg_surface_width: bg_scroll = 0
        if city_scroll1 >= bg_surface_width: city_scroll1 = 0
        if city_scroll2 >= bg_surface_width: city_scroll2 = 0
        if city_scroll3 >= bg_surface_width: city_scroll3 = 0
        if concrete_scroll >= concrete_surface_width: concrete_scroll = 0

        # Draw our player
        player.draw(screen)
        player.update()

        # Draw Obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Collision
        game_active = collisions()


    # == TITLE SCREEN ==
    else:
        # Scroll Reset
        bg_scroll, concrete_scroll, city_scroll1, city_scroll2, city_scroll3 = 0, 0, 0, 0, 0

        # Draw Surfaces
        screen.blit(bg_surface, (0, 0))
        screen.blit(concrete_surface, concrete_surface_rect)
        for num in range(0, 3):
            screen.blit(city_surfaces[num], (0, 0))
        
       
        # Show Score
        your_score = font.render(f"Your score: {score}", True, (255, 233, 229))
        your_score_drop = font.render(f"Your score: {score}", True, (100, 83, 78))
        
        your_score_rect = your_score.get_rect(midbottom = (400, 300))
        your_score_drop_rect = your_score_drop.get_rect(midbottom = (402, 302))

        if score > 0: 
            screen.blit(your_score_drop, your_score_drop_rect)
            screen.blit(your_score, your_score_rect)

        # Controllable Cat!
        player.draw(screen)
        player.update()

    # == SCREEN UPDATE ==
    pygame.display.update()
    clock.tick(144)