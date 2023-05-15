import pygame, sys
from abc import ABC, abstractmethod

pygame.init()
pygame.mixer.init()

#font untuk semuanya
font_score = pygame.font.SysFont('Monospace', 80, bold=True)
font_menu = pygame.font.SysFont('Rockwell', 24, bold=True)
font_bar= pygame.font.SysFont('Rockwell', 30, bold=True)

#warna
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (128, 0, 128)
YELLOW = (245,204,39)
  
#display window
WIDTH, HEIGHT = 900, 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
max_score=4
pygame.display.set_caption("Pong")

#sound effect
ballhit = pygame.mixer.Sound("C:\Belajar Python\TUBES PBO\mixkit-hitting-the-basketball-ball-2096.wav")
pointbs = pygame.mixer.Sound("C:\Belajar Python\TUBES PBO\sound2.mp3")
menubs  = pygame.mixer.Sound("C:\Belajar Python\TUBES PBO\sound1.mp3")
winbs = pygame.mixer.Sound("C:\Belajar Python\TUBES PBO\winbs.mp3")

winbs.set_volume(1)
menubs.set_volume(1)
pointbs.set_volume(1)
ballhit.set_volume(1) 
clock = pygame.time.Clock()    
FPS = 30

main_menu=False
menu_command=0

image1 = pygame.image.load("pgm.png")
image2 = pygame.image.load("info.png")
image3 = pygame.image.load("pgm2.png")
  
#Abstract class
class Pong(ABC):
    def __init__(self, posx, posy, speed, color):
        self.posx=posx
        self.posy=posy
        self.speed=speed
        self.color=color
        
    @abstractmethod 
    def display(self):
        pass
    
    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def reset(self):
        pass
    
    @abstractmethod
    def getRect():
        pass
    
class Racket(Pong):
        # Take the initial position, dimensions, speed and color of the object
    def __init__(self, posx, posy, speed, color, width, height):
        super().__init__(posx, posy, speed, color)
        self.width = width
        self.height = height
        self.__score = 0
        # Rect that is used to control the position and collision of the object
        self.__racketRect = pygame.Rect(posx, posy, width, height)
        # Object that is blit on the window
        self.display()
  
    # Used to display the object on the window
    def display(self):
        self.racket = pygame.draw.rect(window, self.color, self.__racketRect)
  
    def update(self, yFac):
        self.posy = self.posy + self.speed*yFac
  
        # Restricting the Racket to be below the top surface of the window
        if self.posy <= 0:
            self.posy = 0
        # Restricting the Racket to be above the bottom surface of the window
        elif self.posy + self.height >= HEIGHT:
            self.posy = HEIGHT-self.height
  
        # Updating the rect with the new values
        self.__racketRect = (self.posx, self.posy, self.width, self.height)
  
    def displayScore(self, score, x, y, color):
        text = font_score.render(str(score), False, color)
        textRect = text.get_rect()
        textRect.center = (x, y)
  
        window.blit(text, textRect)
    
    def reset(self):
        self.posy=HEIGHT//2 - self.height//2
    
    def setScore(self):
        self.__score=0
    
    def getScore(self):
        self.__score+=1
        return self.__score
  
    def getRect(self):
        return self.__racketRect
  
# Ball class
  
class Ball(Pong):
    def __init__(self, posx, posy, speed, color, radius):
        super().__init__(posx, posy, speed, color)
        self.radius = radius
        self.xFac = 1
        self.yFac = -1
        self.firstTime = 1
        self.display()
  
    def display(self):
        self.__ball = pygame.draw.circle(
            window, self.color, (self.posx, self.posy), self.radius)
  
    def update(self):
        self.posx += self.speed*self.xFac
        self.posy += self.speed*self.yFac
  
        # If the ball hits the top or bottom surfaces, 
        # then the sign of yFac is changed and 
        # it results in a reflection
        if self.posy <= 0 or self.posy >= HEIGHT:
            self.yFac *= -1
            ballhit.play()
  
        if self.posx <= 0 and self.firstTime:
            self.firstTime = 0
            pointbs.play()
            return 1
        elif self.posx >= WIDTH and self.firstTime:
            self.firstTime = 0
            pointbs.play()
            return -1
        else:
            return 0
  
    def reset(self):
        self.posx = WIDTH//2
        self.posy = HEIGHT//2
        self.xFac *= -1
        self.firstTime = 1
  
    # Used to reflect the ball along the X-axis
    def hit(self):
        self.xFac *= -1
        ballhit.play()
  
    def getRect(self):
        return self.__ball

class Button:
    def __init__(self, txt, posx, posy):
        self.text = txt
        self.posx = posx
        self.posy = posy
        self.button = pygame.rect.Rect((self.posx, self.posy), (253, 40))
        
    def draw(self,x, y, color):
        self.color=color
        pygame.draw.rect(window, self.color, self.button, 0, 5)
        pygame.draw.rect(window, BLACK, [self.posx, self.posy, 253, 40], 5, 5)
        text2 = font_menu.render(self.text, False, BLACK)
        window.blit(text2, (self.posx + x, self.posy + y))
        
    def check_clicked(self):
        if self.button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return True
        else:
            return False

def draw_menu():
    menubs.play()
    menu_btn = Button('Main Menu', WIDTH//3 + 18, HEIGHT-140)
    menu_btn.draw(65, 7, WHITE)
    menu = menu_btn.check_clicked()
    return menu

def draw_replay_bar():
    command = -1
    menu = Button("Back to Menu", 120, 300)
    menu.draw(50, 7, WHITE)
    button3 = Button("Countinue", 120, 240)
    button3.draw(65, 7, YELLOW)  
    if menu.check_clicked():
        command = 0
    if button3.check_clicked():
        command = 1
    return command

def draw_menu_bar():
    window.blit(image3, (0, 0)) 
    command = -1
    pygame.draw.rect(window, PURPLE, [100, 100, 300, 300])
    pygame.draw.rect(window, BLACK, [100, 100, 290, 280], 5)
    txt = font_bar.render("MAIN MENU", True, WHITE)
    window.blit(txt, (150, 127))
    # menu exit button
    menu = Button("Back to Menu", 120, 300)
    menu.draw(50, 7, WHITE)
    button1 = Button("Play Game", 120, 180)
    button1.draw(65, 7, WHITE)
    button2 = Button("Information", 120, 240)
    button2.draw(60, 7, WHITE)  
    if menu.check_clicked():
        command = 0
    if button1.check_clicked():
        command = 1
    if button2.check_clicked():
        command = 2
    return command

def draw_win_bar():
    command = -1
    menu = Button("Back to Menu", 40, HEIGHT-60)
    menu.draw(50, 7, WHITE)
    button4 = Button("Restart", WIDTH-290, HEIGHT-60)
    button4.draw(80, 7, YELLOW)  
    if menu.check_clicked():
        command = 0
    if button4.check_clicked():
        command = 1
    return command
  
def game_over(cek):
    winbs.play()
    racket1.setScore()
    racket2.setScore()
    text = font_score.render("WIN", False, YELLOW)
    if cek == 1:
        text_rect = text.get_rect(center=(WIDTH//4, HEIGHT//2))
    elif cek == 2:
        text_rect = text.get_rect(center=(WIDTH-WIDTH//4, HEIGHT//2))
    window.blit(text, text_rect)
    pygame.display.update()

    # Defining the objects
racket1 = Racket(20, HEIGHT//2-50, 10, WHITE, 13, 100)
racket2 = Racket(WIDTH-30, HEIGHT//2-50, 10, WHITE, 13, 100)
ball = Ball(WIDTH//2, HEIGHT//2, 10, YELLOW, 10)
  
racket_list = [racket1, racket2]
  
    # Initial parameters of the players
racket1_score, racket2_score = 0, 0
racket1YFac, racket2YFac = 0, 0

selesai=False
replay=False
running = False
run = True

while run and running == False:
    try:
        if main_menu:
            if replay == False and not selesai:
                menu_command = draw_menu_bar()
                if menu_command != -1:
                    main_menu = False
            elif replay == True and not selesai:
                menu_command = draw_replay_bar()
                if menu_command != -1:
                    main_menu = False
            elif replay == False and selesai:
                menu_command = draw_win_bar()
                racket1.reset()
                racket2.reset()
                if menu_command != -1:
                    main_menu = False
        
        else:
            window.fill(PURPLE)
            window.blit(image1, (0, 0))  
            main_menu = draw_menu()
            if menu_command == 0:
                
                replay = False
                selesai = False
                racket1_score=0
                racket1.setScore()
                racket2_score=0
                racket2.setScore()
                
            if menu_command == 1:
                window.fill(PURPLE)
                menubs.stop()
                winbs.stop()
                running = True
                selesai = False
            
            if menu_command == 2:
                window.blit(image2, (0, 0))
                draw_menu()
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.flip()
        
        while running and not selesai:    
            window.fill(PURPLE)   
            pygame.draw.line( window, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 5 )
                # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p and running:
                        running = False
                    if event.key == pygame.K_UP:
                        racket2YFac = -1
                    if event.key == pygame.K_DOWN:
                        racket2YFac = 1
                    if event.key == pygame.K_w:
                        racket1YFac = -1
                    if event.key == pygame.K_s:
                        racket1YFac = 1
                            
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        racket2YFac = 0
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        racket1YFac = 0
        
                # Collision detection
            for racket in racket_list:
                if pygame.Rect.colliderect(ball.getRect(), racket.getRect()):
                    ball.hit()
        
                # Updating the objects
            racket1.update(racket1YFac)
            racket2.update(racket2YFac)
            point = ball.update()
            
            #Penambahan point
            if point == -1:
                racket1_score=racket1.getScore()
            elif point == 1:
                racket2_score=racket2.getScore()

            #Reset posisi bola
            if point:   
                ball.reset()
        
                # Displaying the objects on the window
            racket1.display()
            racket2.display()
            ball.display()

            # Displaying the scores of the players
            racket1.displayScore( racket1_score, WIDTH//4, 35, WHITE)
            racket2.displayScore( racket2_score, WIDTH-WIDTH//4, 35, WHITE)

            if racket1_score > max_score and not selesai:
                game_over(1)
                running = False
                racket1_score=0
                racket2_score=0
                selesai=True
                main_menu=True
        
            elif racket2_score > max_score and not selesai:
                game_over(2)
                running = False
                racket1_score=0
                racket2_score=0
                selesai=True
                main_menu=True
                
            if running == False:
                if racket1_score <= max_score and racket2_score <= max_score and not selesai:
                    replay = True
                    main_menu=True
                    
            pygame.display.update()
            clock.tick(FPS)
            
    except pygame.error as error:
        print("Pygame Error", error)
        sys.exit()
        
    except Exception as error:
        print("An error occurred", error)
        sys.exit()
