import os
import pygame
import pygame_menu
import time

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = pygame.display.set_mode((600, 400))

#Variables
WIDTH = 1200
HEIGHT = 600
BORDER = 20
VELOCITY = 5
user_score = -1
ai_score = -1
bgColor = pygame.Color('black')
fgColor = pygame.Color('white')


# Define my classes
class Ball:
    bounce = 0  
    RADIUS = 20
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy =vy

    def Show(self, color):
        global screen
        pygame.draw.circle(screen, color, (self.x, self.y), self.RADIUS)


    def Update(self, paddle):
        global fgColor, bgColor, user_score

        newx = self.x + self.vx
        newy = self.y + self.vy

        # Check if ball hits paddle
        if  paddle.y-Paddle.HEIGHT//2 <= newy <= paddle.y+Paddle.HEIGHT//2 and newx >= WIDTH-paddle.WIDTH:
            if self.vx > 0:
                self.vx += 1
            else:
                self.vx += -1
            if self.vy > 0:
                self.vy += 1
            else:
                self.vy += -1
            self.vx = -self.vx
            self.vy = -self.vy

        # Check if ball moves past right wall
        elif newx > WIDTH-paddle.WIDTH and not paddle.y-Paddle.HEIGHT//2 <= newy <= paddle.y+Paddle.HEIGHT//2:
            self.Show(bgColor)
            user_score = 0
            pygame.draw.rect(screen, fgColor, pygame.Rect((0,0),(WIDTH,BORDER)))
            myfont = pygame.font.SysFont("monospace", 16)
            scoretext = myfont.render("Score = "+str(user_score), 1, (0,0,0))
            screen.blit(scoretext, (20, 0))
            pygame.display.flip()


            #Ball.countdown()
            self.x = WIDTH-Ball.RADIUS-Paddle.WIDTH
            self.y = HEIGHT//2
            self.vx = -VELOCITY
            self.vy = -VELOCITY
            time.sleep(1)
            self.Show(fgColor)


        # Check if ball hits left wall 
        elif newx < BORDER+self.RADIUS:
            if self.vx > 0:
                self.vx += 1
            else:
                self.vx += -1
            Ball.score()
            self.vx = -self.vx

        # Check if ball hits top or bottom
        elif newy < BORDER+self.RADIUS or newy > HEIGHT-BORDER-self.RADIUS:
            self.vy = -self.vy
        else:
            self.Show(bgColor)
            self.x = self.x + self.vx
            self.y = self.y + self.vy
            self.Show(fgColor)

    def countdown():
        global screen

        white = (255, 255, 255)
        black = (0, 0, 0)
        mylist = ['3','2','1']

        font = pygame.font.Font('freesansbold.ttf', 32)

        for i in mylist:
            text = font.render(i, True, white)
            textRect = text.get_rect()
            textRect.center = (WIDTH // 2, HEIGHT // 2)
            screen.blit(text, textRect)
            #time.sleep(1)
            text = erase.render(i, True, black)
            screen.blit(text, textRect)

    def score():
        global user_score

        user_score = user_score + 1
        pygame.draw.rect(screen, fgColor, pygame.Rect((0,0),(WIDTH,BORDER)))
        myfont = pygame.font.SysFont("monospace", 16)
        scoretext = myfont.render("Score = "+str(user_score), 1, (0,0,0))
        screen.blit(scoretext, (20, 0))


class Paddle:
    WIDTH = 20
    HEIGHT = 100
    

    def __init__(self, y):
        self.y = y

    def show(self, color):
        global screen
        pygame.draw.rect(screen, color, pygame.Rect((WIDTH-self.WIDTH,self.y-self.HEIGHT//2),(self.WIDTH,self.HEIGHT)))

    def update(self):
        self.show(pygame.Color("black"))
        self.y = pygame.mouse.get_pos()[1]
        self.show(pygame.Color("white"))




def start_the_game():
    """
    Function that starts a game. This is raised by the menu button,
    here menu can be disabled, etc.
    """
    global fgColor, bgColor
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((WIDTH,HEIGHT))



    screen.fill(bgColor)

    pygame.draw.rect(screen, fgColor, pygame.Rect((0,0),(WIDTH,BORDER)))
    pygame.draw.rect(screen, fgColor, pygame.Rect((0,0),(BORDER,HEIGHT)))
    pygame.draw.rect(screen, fgColor, pygame.Rect((0,HEIGHT-BORDER),(WIDTH,BORDER)))

    ball = Ball(WIDTH-Ball.RADIUS-Paddle.WIDTH, HEIGHT//2, -VELOCITY , -VELOCITY)
    paddle = Paddle(HEIGHT//2)

    paddle.show(fgColor)
    ball.Show(fgColor)

    clock = pygame.time.Clock()
    FRAMERATE = clock.get_fps()


    sample = open("game.csv", "w")
    print("x,y,vx,vy,paddle.y", file=sample)
    Ball.score()

    while True:
        e = pygame.event.poll()
        if e.type == pygame.QUIT:
            screen = pygame.display.set_mode((600, 400))
            break
        clock.tick(60)
        pygame.display.flip()
        paddle.update()
        ball.Update(paddle)

        print(f"{ball.x},{ball.y},{ball.vx},{ball.vy},{paddle.y}", file=sample)

menu = pygame_menu.Menu(height=300,
                        width=400,
                        theme=pygame_menu.themes.THEME_BLUE,
                        title='Welcome')

menu.add_text_input('Name: ', default='John Doe')
menu.add_button('Play', start_the_game)
menu.add_button('Quit', pygame_menu.events.EXIT)

if __name__ == '__main__':
    menu.mainloop(screen)