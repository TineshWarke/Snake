import pygame
import random
import os

pygame.mixer.init()

pygame.init()
# Colours
white1 = ( 255, 255, 255 )
white = ( 0, 255, 0)
# green = ( 0, 255, 0)

red = (255, 0, 0)
black = (0, 0, 0)

screen_width = 900
screen_height = 600
# Creating Window
gameWindow = pygame.display.set_mode((screen_width, screen_height))

bgimg = pygame.image.load('bgimage.jpg')
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

pygame.display.set_caption("Snake Game by Tinesh")
pygame.display.update()

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)

def show_score(text, colour, x, y):
    show_score = font.render(text, True, colour)
    gameWindow.blit(show_score, (x, y))

def plot_snake(gameWindow, colour, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, colour, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((0, 255, 255))
        gameWindow.blit(bgimg, (0, 0))
        show_score("Welcome to Snakes", white1, 440, 500)
        show_score("Press Space Bar to Play", white1, 490, 545)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # pygame.mixer.music.load('music.mp3')
                    # pygame.mixer.music.play()
                    gameloop()

        pygame.display.update()
        clock.tick(60)

# Game Loop
def gameloop():
    # Game Specific Variables
    exit_game = False
    game_over = False
    snake_x = 50
    snake_y = 50
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_lenght = 1
    if(not os.path.exists("snk_highscore.txt")):
        with open("snk_highscore.txt", "w") as f:
            f.write("0")
    with open("snk_highscore.txt", "r") as f:
        snk_highscore = f.read()

    food_x = random.randint(20, screen_width - 20)
    food_y = random.randint(20, screen_height - 20)
    score = 0
    init_velocity = 5

    snake_size = 20
    fps = 60

    while not exit_game:
        if game_over :
            with open("snk_highscore.txt", "w") as f:
                f.write(str(snk_highscore))

            gameWindow.fill(white)
            show_score("GAME OVER !!", black, 325, 50)
            show_score(f"Score : {str(score)}", black, 150, 150)
            show_score(f"Highscore : {str(snk_highscore)}", black, 150, 250)
            show_score("Press Enter to Continue....", black, 400, 500)
            # pygame.mixer.music.load('music.mp3')
            # pygame.mixer.music.play()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameloop()
                        # welcome()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        # snake_x = snake_x + 10
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        # snake_x = snake_x - 10
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        # snake_y = snake_y - 10
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        # snake_y = snake_y + 10
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_q:
                        score += 10

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x) < 15 and abs(snake_y - food_y) < 15 :
                pygame.mixer.music.load('beep.mp3')
                pygame.mixer.music.play()
                score += 10
                food_x = random.randint(20, screen_width - 20)
                food_y = random.randint(20, screen_height - 20)
                snk_lenght += 5
                if score > int(snk_highscore):
                    snk_highscore = score

            gameWindow.fill(white)
            show_score("Score : " + str(score) + "                                Highscore : "+str(snk_highscore), black, 100, 10)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_lenght:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load('over.mp3')
                pygame.mixer.music.play()

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                # print("Game Over....")
                pygame.mixer.music.load('over.mp3')
                pygame.mixer.music.play()

            # pygame.draw.rect(gameWindow, black, [snake_x, snake_y, snake_size, snake_size])
            plot_snake(gameWindow, black, snk_list, snake_size)

        pygame.display.update()
        clock.tick(fps)


    pygame.quit()
    quit()

welcome()