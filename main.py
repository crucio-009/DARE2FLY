import random  # random number generation
import sys  # used sys.exit() to exit the program
import pygame
from pygame.locals import *  # basic pygame imports

# Global variables for the game
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUND_Y = SCREENHEIGHT*0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'Gallery/SPRITES/h2.png'
BACKGROUND = 'Gallery/SPRITES/background.png'
PIPE = 'Gallery/SPRITES/pipe.png'
CLOUD = 'Gallery/SPRITES/pipe2.png'


def welcome_screen():
    """Shows welcome image on the screen"""
    message_x = 0
    message_y = 0
    base_x = 0
    while True:
        for event in pygame.event.get():
                # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

                # If the user presses space or up key, start the game for them
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return

            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['message'], (message_x, message_y))
                SCREEN.blit(GAME_SPRITES['base'], (base_x, GROUND_Y))
                pygame.display.update()
                FPS_CLOCK.tick(FPS)


def main_game():
    SCORE = 0
    player_x = int(SCREENWIDTH/5)
    player_y = int(SCREENHEIGHT/2)
    base_x = 0

    """Create 2 pipes for blitting on screen"""
    new_pipe1 = get_Random_Pipe()
    new_pipe2 = get_Random_Pipe()

    """my list of upper pipe"""
    upper_pipes = [{'x': SCREENWIDTH+200, 'y': new_pipe1[0]['y']},
                   {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y': new_pipe2[0]['y']}]

    """my list of lower pipes"""
    lower_pipes = [{'x': SCREENWIDTH+200, 'y': new_pipe1[1]['y']},
                   {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y': new_pipe2[1]['y']}]
    pipe_vel_x = -4
    player_vel_y = -9
    player_max_vel_y = 10
    player_min_vel_y = -8
    player_acc_y = 1
    player_fly_accv = -8
    """velocity while flying"""
    player_fly = False
    """true only when player is flying"""
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN or (event.type == K_SPACE or event.type == K_UP):
                if player_y > 0:
                    player_vel_y = player_fly_accv
                    player_fly = True
                    GAME_SOUNDS['wing'].play()
        crash_test = is_collide(player_x, player_y, upper_pipes, lower_pipes)
        """it will return true if the player has crashed"""
        if crash_test:
            return

        """check for score"""
        player_mid_pos = player_x + GAME_SPRITES['player'].get_width()/2
        for pipe in upper_pipes:
            pipe_mid_pos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipe_mid_pos <= player_mid_pos < pipe_mid_pos+4:
                SCORE += 1
                print(f"Your score is {SCORE}")
                GAME_SOUNDS['point'].play()

        if player_vel_y < player_max_vel_y and not player_fly:
            player_vel_y += player_acc_y

        if player_fly:
            player_fly = False

        player_height = GAME_SPRITES['player'].get_height()
        player_y = player_y + min(player_vel_y, GROUND_Y - player_y - player_height)

        """move pipes to the left"""
        for upper_pipe, lower_pipe in zip(upper_pipes, lower_pipes):
            upper_pipe['x'] += pipe_vel_x
            lower_pipe['x'] += pipe_vel_x

        """Add a new pipe when the first pipe is about to go out of screen"""
        if 0 < upper_pipes[0]['x'] < 5:
            new_pipe = get_Random_Pipe()
            upper_pipes.append(new_pipe[0])
            lower_pipes.append(new_pipe[1])

        """if the pipe is out of the screen, remove it"""
        if upper_pipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upper_pipes.pop(0)
            lower_pipes.pop(0)

        """Let's blit our sprites"""
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upper_pipe, lower_pipe in zip(upper_pipes, lower_pipes):
            SCREEN.blit(GAME_SPRITES['pipe'][1], (upper_pipe['x'], upper_pipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][0], (lower_pipe['x'], lower_pipe['y']))
        SCREEN.blit(GAME_SPRITES['base'], (base_x, GROUND_Y))
        SCREEN.blit(GAME_SPRITES['player'], (player_x, player_y))
        SCREEN.blit(GAME_SPRITES['base'], (base_x, GROUND_Y))
        my_digits = [int(x) for x in list(str(SCORE))]
        width = 0
        for digit in my_digits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        x_offset = (SCREENWIDTH - width)/2
        for digit in my_digits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (x_offset, SCREENHEIGHT*0.12))
            x_offset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def is_collide(player_x, player_y, upper_pipes, lower_pipes):
    if player_y > GROUND_Y-25 or player_y < 0:
        GAME_SOUNDS['hit'].play()
        return True
    for pipe in upper_pipes:
        pipe_height = GAME_SPRITES['pipe'][0].get_height()
        if player_y < pipe_height + pipe['y'] and abs(player_x - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    for pipe in lower_pipes:
        if player_y + GAME_SPRITES['player'].get_height() > pipe['y'] and abs(player_x - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    return False


def get_Random_Pipe():
    """generate positions of two pipes for blitting on the screen one building and a cloud"""
    pipe_height = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipe_x = SCREENWIDTH + 10
    y1 = pipe_height - y2 + offset
    pipe = [{'x': pipe_x, 'y': -y1},  # upper pipe
            {'x': pipe_x, 'y': y2}]
    return pipe


if __name__ == '__main__':
    """This is the main function from where the game will start"""
    pygame.init()  # initialise all pygame modules
    FPS_CLOCK = pygame.time.Clock()
    pygame.display.set_caption('Dare2Fly by Manish Kumar')

    # Game Sprites

    GAME_SPRITES['numbers'] = (
        pygame.image.load('Gallery/SPRITES/00.png').convert_alpha(),
        pygame.image.load('Gallery/SPRITES/11.png').convert_alpha(),
        pygame.image.load('Gallery/SPRITES/22.png').convert_alpha(),
        pygame.image.load('Gallery/SPRITES/33.png').convert_alpha(),
        pygame.image.load('Gallery/SPRITES/44.png').convert_alpha(),
        pygame.image.load('Gallery/SPRITES/55.png').convert_alpha(),
        pygame.image.load('Gallery/SPRITES/66.png').convert_alpha(),
        pygame.image.load('Gallery/SPRITES/77.png').convert_alpha(),
        pygame.image.load('Gallery/SPRITES/88.png').convert_alpha(),
        pygame.image.load('Gallery/SPRITES/99.png').convert_alpha(),
    )
    GAME_SPRITES['message'] = pygame.image.load('Gallery/SPRITES/Message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('Gallery/SPRITES/ground.png').convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.image.load(PIPE).convert_alpha(), pygame.image.load(CLOUD).convert_alpha())
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    # Game Sounds

    GAME_SOUNDS['die'] = pygame.mixer.Sound('Gallery/AUDIO/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('Gallery/AUDIO/hit.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('Gallery/AUDIO/wing.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('Gallery/AUDIO/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('Gallery/AUDIO/swoosh.wav')

    while True:
        welcome_screen()  # show welcome screen to the user until he presses a button
        main_game()  # This the main game function
