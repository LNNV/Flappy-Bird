import pygame, sys, random

def new_chemny():
    pos = random.choice(chemny_hights)
    bot_chemny = chemny_img.get_rect(midtop = (700, pos))
    top_chemny = chemny_img.get_rect(midbottom = (700, pos - 170))
    return [bot_chemny, top_chemny, 0]

def move_chemny(chemnys):
    for chemny in chemnys:
        chemny[0].centerx -= 5
        chemny[1].centerx -= 5
    if len(chemnys) > 0:
        if chemnys[0][0].right < 0:
            chemnys.pop(0)
    return chemnys

def draw_chemny(chemnys):
    for chemny in chemnys:
        flip_chemny = pygame.transform.flip(chemny_img, False, True)
        screen.blit(chemny_img, chemny[0])
        screen.blit(flip_chemny, chemny[1])

def is_lose(chemnys):
    global score
    for chemny in chemnys:
        if bird_box.colliderect(chemny[0]) or bird_box.colliderect(chemny[1]):
            die_sound.play()
            return True
        if bird_box.left >= chemny[1].left and bird_box.left <= chemny[1].right and bird_box.top < 0:
            die_sound.play()
            return True
        if bird_box.right >= chemny[1].left and bird_box.right <= chemny[1].right and bird_box.top < 0:
            die_sound.play()
            return True
        if bird_box.left > chemny[1].right and chemny[2] == 0:
            point_sound.play()
            score += 1
            chemny[2] = 1
    if bird_box.bottom >= 600:
        die_sound.play() 
        return True
    return False

def score_display():
    if playing or start == True:
        score_surface = game_font.render(str(int(score)), True, (255,255,255))
        score_box = score_surface.get_rect(center = (300, 50))
        screen.blit(score_surface, score_box)
    else:
        score_surface = game_font.render("Score: " + str(int(score)), True, (255,255,255))
        score_box = score_surface.get_rect(center = (300, 50))
        screen.blit(score_surface, score_box)

        score_surface = game_font.render("High Score: " + str(int(high_score)), True, (255,255,255))
        score_box = score_surface.get_rect(center = (300, 100))
        screen.blit(score_surface, score_box)
        
        over_surface = game_font.render("Press Space to play again", True, (255,255,255))
        over_box = over_surface.get_rect(center = (300, 300))
        screen.blit(over_surface, over_box)

#Initialize pygame and screen
pygame.init()
screen = pygame.display.set_mode((600, 600))

#clock for limit fps
clock = pygame.time.Clock()

#game mech variables
gravity = 0.5
playing = False
score = 0
high_score = 0
start = True

#get high score
try:
    hs_file = open('high_score.txt', 'r')
    high_score = int(hs_file.read())
    hs_file.close()
except:
    hs_file = open('high_score.txt', 'w')
    hs_file.write('0')

#game font
game_font = pygame.font.Font("font/04B_19.ttf", 30)

#background
bg = pygame.image.load("images/background.png").convert()
bg = pygame.transform.scale(bg, (600,600))

#sound
jump_sound = pygame.mixer.Sound("sounds/wing_sfx.wav")
die_sound = pygame.mixer.Sound("sounds/die_sfx.wav")
point_sound = pygame.mixer.Sound("sounds/point_sfx.wav")

#bird
bird_img = pygame.image.load("images/bird.png").convert()
bird_img = pygame.transform.scale(bird_img, (40, 30))
bird_box = bird_img.get_rect(center = (50, 300))
bird_movement = 0

#chemny
chemny_img = pygame.image.load("images/chemny.png").convert()
chemny_img = pygame.transform.scale(chemny_img, (80, 400))
chemny_list = []
chemny_hights = [300, 350, 400, 450, 500]

#timer to spawn chemny
spawn_chemny = pygame.USEREVENT
pygame.time.set_timer(spawn_chemny, 1600)

#game loop
while True:
    screen.blit(bg, (0, 0))

    #catch event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and playing:
                jump_sound.play()
                bird_movement = -10
            if event.key == pygame.K_SPACE and playing == False and start == True:
                jump_sound.play()
                playing = True
                start = False
                bird_movement = -10
                chemny_list.clear()
                pygame.time.set_timer(spawn_chemny, 1600)
            if event.key == pygame.K_SPACE and playing == False and start == False:
                chemny_list.clear()
                bird_movement = 0
                bird_box.center = (50, 300)
                score = 0
                start = True
                pygame.time.set_timer(spawn_chemny, 1600)
        if event.type == spawn_chemny:
            chemny_list.append(new_chemny())
            if score == 9:
                pygame.time.set_timer(spawn_chemny, 1400)
            if score == 19:
                pygame.time.set_timer(spawn_chemny, 1200)
            if score == 29:
                pygame.time.set_timer(spawn_chemny, 1000)
            
    #start screen
    if start:
        screen.blit(bird_img, bird_box)
        start_surface = game_font.render("Press Space to star", True, (255,255,255))
        start_box = start_surface.get_rect(center = (300, 300))
        screen.blit(start_surface, start_box)
    
    if playing:
        #bird   
        bird_movement += gravity
        bird_box.centery += bird_movement
        screen.blit(bird_img, bird_box)

        #chemny
        chemny_list = move_chemny(chemny_list)
        draw_chemny(chemny_list)
        if is_lose(chemny_list):
            playing = False
            #update high score
            if score > high_score:
                high_score = score
                hs_file = open('high_score.txt', 'w')
                hs_file.write(str(score))
                hs_file.close()

    score_display() 

    pygame.display.update()
    clock.tick(60)
