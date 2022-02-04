import pygame
import os
pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HIGHT = 1000, 600
WIN = pygame.display.set_mode((WIDTH, HIGHT))
pygame.display.set_caption('First Game')
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
FBS = 60
velocity = 5
Bullet_velocity = 15
MAX_bullets = 6
BLUE_HIT = pygame.USEREVENT + 1
YELLOW_HIT = pygame.USEREVENT + 2
BORDER = pygame.Rect(WIDTH / 2 - 2, 0, 4, HIGHT)
SPACESHIP_WIDTH, SPACESHIP_HIGHT = 50, 50
BLUE_SPACESHIP_IMAGE = pygame.image.load(os.path.join('blue_spaceship.png'))
BLUE_SPACESHIP = pygame.transform.scale(BLUE_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HIGHT))
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('yellow_spaceship.png'))
YELLOW_SPACESHIP = pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HIGHT))
SPACE_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('space_background.jpg')), (WIDTH, HIGHT))
GAME_OVER_IMAGE = pygame.transform.scale(pygame.image.load('game_over.png'), (400, 200))
SHOOTING_SOUND = pygame.mixer.Sound('shoot_sound.mp3')
GETTING_SHOOT_SOUND = pygame.mixer.Sound('explosion.mp3')
GAME_OVER_SOUND = pygame.mixer.Sound('game_over_sound.mp3')
Blue_life = 5
Yellow_life = 5
game_end = False


def window(Blue, Yellow, Blue_bullets, Yellow_bullets):
    WIN.blit(SPACE_BACKGROUND, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    Blue_life_text = pygame.font.SysFont('comicsans', 50).render('Life: ' + str(Blue_life), 1, WHITE)
    Yellow_life_text = pygame.font.SysFont('comicsans', 50).render('Life: ' + str(Yellow_life), 1, WHITE)
    Blue_winner_text = pygame.font.SysFont('comicsans', 100).render('BLUE WINS', 1, BLUE)
    Yellow_winner_text = pygame.font.SysFont('comicsans', 100).render('ORANGE WINS', 1, (255, 69, 0))
    WIN.blit(Blue_life_text, (225, 20))
    WIN.blit(Yellow_life_text, (725, 20))

    WIN.blit(BLUE_SPACESHIP, (Blue.x, Blue.y))
    WIN.blit(YELLOW_SPACESHIP, (Yellow.x, Yellow.y))
    global game_end
    if Blue_life <= 0:
        WIN.blit(GAME_OVER_IMAGE, (300, 100))
        WIN.blit(Yellow_winner_text, (275, 350))
        GAME_OVER_SOUND.play()
        game_end = True
    elif Yellow_life <= 0:
        WIN.blit(GAME_OVER_IMAGE, (300, 100))
        WIN.blit(Blue_winner_text, (310, 350))
        game_end = True
        GAME_OVER_SOUND.play()

    else:
        for bullet in Blue_bullets:
            pygame.draw.rect(WIN, BLUE, bullet)
        for bullet in Yellow_bullets:
            pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def Keys_Control(keys_pressed, Blue, Yellow):
    if not game_end:
        # MOVE BLUE SPACESHIP
        if keys_pressed[pygame.K_a] and Blue.x >= 0:  # blue_spaceship left
            Blue.x -= velocity
        if keys_pressed[pygame.K_d] and Blue.x <= WIDTH / 2 - 2 - SPACESHIP_WIDTH:  # blue_spaceship right
            Blue.x += velocity
        if keys_pressed[pygame.K_w] and Blue.y >= 0:  # blue_spaceship up
            Blue.y -= velocity
        if keys_pressed[pygame.K_s] and Blue.y <= HIGHT - SPACESHIP_HIGHT:  # blue_spaceship down
            Blue.y += velocity

        # MOVE YELLOW SPACESHIP
        if keys_pressed[pygame.K_LEFT] and Yellow.x >= WIDTH / 2 + 2:  # blue_spaceship left
            Yellow.x -= velocity
        if keys_pressed[pygame.K_RIGHT] and Yellow.x != WIDTH - SPACESHIP_WIDTH:  # blue_spaceship right
            Yellow.x += velocity
        if keys_pressed[pygame.K_UP] and Yellow.y >= 0:  # blue_spaceship up
            Yellow.y -= velocity
        if keys_pressed[pygame.K_DOWN] and Yellow.y <= HIGHT - SPACESHIP_HIGHT:  # blue_spaceship down
            Yellow.y += velocity


def get_shoot(Blue_bullets, Yellow_bullets, blue, yellow):
    for bullet in Blue_bullets:
        bullet.x += Bullet_velocity
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            Blue_bullets.remove(bullet)
            GETTING_SHOOT_SOUND.play()
            global Yellow_life
            global game_end
            if Yellow_life != 0 and game_end == False:
                Yellow_life -= 1
        elif bullet.x > WIDTH:
            Blue_bullets.remove(bullet)

    for bullet in Yellow_bullets:
        bullet.x -= Bullet_velocity
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            Yellow_bullets.remove(bullet)
            GETTING_SHOOT_SOUND.play()
            global Blue_life
            # global game_end
            if Blue_life != 0 and game_end == False:
                Blue_life -= 1
        elif bullet.x < 0:
            Yellow_bullets.remove(bullet)


def main():
    Blue = pygame.Rect(200, 300, SPACESHIP_WIDTH, SPACESHIP_HIGHT)
    Yellow = pygame.Rect(800, 300, SPACESHIP_WIDTH, SPACESHIP_HIGHT)
    clock = pygame.time.Clock()
    Yellow_bullets = []
    Blue_bullets = []
    run = True
    global game_end
    while run:
        clock.tick(FBS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if not game_end:
                    if event.key == pygame.K_f and len(Blue_bullets) < MAX_bullets:
                        bullet = pygame.Rect(Blue.x + SPACESHIP_WIDTH, Blue.y + SPACESHIP_HIGHT / 2 - 3, 12, 6)
                        Blue_bullets.append(bullet)
                        SHOOTING_SOUND.play()
                    if event.key == pygame.K_RCTRL and len(Yellow_bullets) < MAX_bullets:
                        bullet = pygame.Rect(Yellow.x, Yellow.y + SPACESHIP_HIGHT / 2 - 3, 12, 6)
                        Yellow_bullets.append(bullet)
                        SHOOTING_SOUND.play()
                global Blue_life
                global Yellow_life

                if event.key == pygame.K_SPACE and (Blue_life == 0 or Yellow_life == 0):
                    Blue_life = 5
                    Yellow_life = 5
                    game_end = False
                    pygame.mixer.stop()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
        keys_pressed = pygame.key.get_pressed()
        Keys_Control(keys_pressed, Blue, Yellow)

        get_shoot(Blue_bullets, Yellow_bullets, Blue, Yellow)
        window(Blue, Yellow, Blue_bullets, Yellow_bullets)
    main()


if __name__ == '__main__':
    main()
