import pygame
pygame.init()
import random
import os
pygame.mixer.init()


# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
aqua = (0, 128, 128)
green = (0, 255, 0)
yellow = (255, 255, 0)

# Creating window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

#background image
bgimg = pygame.image.load("bg.png")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

# Game Title
pygame.display.set_caption("Snakes By Ashish")
pygame.display.update()

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)



def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


#score
def screen_score(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(aqua)
        screen_score("WELCOME TO SNAKES", white, 240, 280)
        screen_score("PRESS SPACE KEY TO CONTINUE", white, 160, 350)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('Powerup.mp3')
                    pygame.mixer.music.play()
                    gameloop()

            pygame.display.update()
            clock.tick(40)




# Game Loop
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    snake_size = 18
    fps = 40
    velocity_x = 0
    velocity_y = 0
    init_velocity = 4
    score = 0
    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)
    snk_lst = []
    snk_length = 1

    #check if file exists
    if(not os.path.exists("hiscore.txt")):
        with open("hiscore.txt","w") as f:
            f.write("0")


    with open("hiscore.txt", "r") as f:
        highscore = f.read()

    while not exit_game:
        if game_over:
            with open("hiscore.txt", "w") as f:
                f.write(str(highscore))
            gameWindow.fill(white)
            screen_score("GAME OVER!PRESS ENTER TO CONTINUE", red, 80, 300)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.load('Powerup.mp3')
                        pygame.mixer.music.play()
                        gameloop()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

            snake_x += velocity_x
            snake_y += velocity_y



            if abs(snake_x - food_x)<8 and abs(snake_y - food_y)<8:
                score += 50
                pygame.mixer.music.load('eat.mp3')
                pygame.mixer.music.play()
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snk_length += 5
                if score > int(highscore):
                    highscore = score

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_lst.append(head)

            if len(snk_lst)> snk_length:
                del snk_lst[0]

            if head in snk_lst[:-1]:
                game_over = True
                pygame.mixer.music.load('gameover.mp3')
                pygame.mixer.music.play()


            gameWindow.fill(black)
            screen_score("SCORE: " + str(score) + "  HIGH SCORE: " + str(highscore), white, 5, 5)


            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y<0 or snake_y>screen_height:
                game_over = True
                pygame.mixer.music.load('gameover.mp3')
                pygame.mixer.music.play()

            plot_snake(gameWindow, green, snk_lst, snake_size)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])
        pygame.display.update()
        clock.tick(fps)


    pygame.quit()
    quit()

welcome()

