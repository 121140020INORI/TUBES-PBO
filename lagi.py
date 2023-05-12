import pygame, sys, random
from abc import ABC, abstractmethod

class Pong(ABC):
    def __init__(self, window, color, coorX, coorY):
        self.window = window
        self.color = color
        self.coorX = coorX
        self.coorY = coorY

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def restart_coor(self):
        pass
	
class Racket(Pong):
	def __init__(self, window, color, coorX, coorY, width, height):
		super().__init__(window, color, coorX, coorY)
		self.width = width
		self.height = height
		self.state = 'stopped'
		self.draw()

	def draw(self):
		pygame.draw.rect( self.window, self.color, (self.coorX, self.coorY, self.width, self.height))

	def move(self):
		if self.state == 'up':
			self.coorY -= 10
		elif self.state == 'down':
			self.coorY += 10

	def clamp(self):
		if self.coorY <= 0:
			self.coorY = 0

		if self.coorY + self.height >= HEIGHT:
			self.coorY = HEIGHT - self.height

	def restart_coor(self):
		self.coorY = HEIGHT//2 - self.height//2
		self.state = 'stopped'
		self.draw()

class Ball(Pong):
	def __init__(self, window, color, coorX, coorY, diameter):
		super().__init__(window, color, coorX, coorY)
		self.dx = 0
		self.dy = 0
		self.diameter = diameter
		self.draw()

	def draw(self):
		pygame.draw.circle( self.window, self.color, (self.coorX, self.coorY), self.diameter )

	def start(self):
		self.dx = 15
		self.dy = 5

	def move(self):
		self.coorX += self.dx
		self.coorY += self.dy

	def wall_collision(self):
		self.dy = -self.dy

	def racket_collision(self):
		self.dx = -self.dx

	def restart_coor(self):
		self.coorX = WIDTH//2
		self.coorY = HEIGHT//2
		self.dx = 0
		self.dy = 0
		self.draw()

class Score:
	def __init__(self, window, points, coorX, coorY):
		self.window = window
		self.points = points
		self.coorX = coorX
		self.coorY = coorY
		self.font = pygame.font.SysFont("monospace", 80, bold=True)
		self.label = self.font.render(self.points, 0, WHITE)
		self.show()

	def show(self):
		self.window.blit(self.label, (self.coorX - self.label.get_rect().width // 2, self.coorY))

	def increase(self):
		points = int(self.points) + 1
		self.points = str(points)
		self.label = self.font.render(self.points, 0, WHITE)
  
		if points > 4:
			return "Winner"

	def restart(self):
		self.points = '0'
		self.label = self.font.render(self.points, 0, WHITE)

class Reflection:
	def between_ball_and_racket(self, ball, racket):
		ballX = ball.coorX
		ballY = ball.coorY
		racketX = racket.coorX
		racketY = racket.coorY

		if ballY + ball.diameter > racketY and ballY - ball.diameter < racketY + racket.height:
			if racket==racket1:
				if ballX - ball.diameter <= racketX + racket.width and ballX - ball.diameter > racketX + 15:
					return True
			if racket==racket2:
				if ballX + ball.diameter >= racketX and ballX + ball.diameter < racketX + (racket.width-15):
					return True
		return False
		

	def between_ball_and_walls(self, ball):
		ballY = ball.coorY

		if ballY - ball.diameter <= 0:
			return True
		if ballY + ball.diameter >= HEIGHT:
			return True

		return False

	def check_goal(self, ball):
		if ball.coorX + ball.diameter <= 0:
			return 'player2'
		elif ball.coorX - ball.diameter >= WIDTH:
			return 'player1'

class Button:
    def __init__(self, txt, coorx, coory):
        self.text = txt
        self.coorx = coorx
        self.coory = coory
        self.button = pygame.rect.Rect((self.coorx, self.coory), (253, 40))
        
    def draw(self):
        pygame.draw.rect(window, WHITE, self.button, 0, 5)
        #                                  coor x        coor y     w    h   border
        pygame.draw.rect(window, BLACK, [self.coorx, self.coory, 253, 40], 5, 5)
        text2 = font.render(self.text, True, BLACK)
        window.blit(text2, (self.coorx + 65, self.coory + 7))
        
    def check_clicked(self):
        if self.button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return True
        else:
            return False

WIDTH, HEIGHT = 900, 500
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (128, 0, 128)

pygame.init()
window = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption('PONG')
main_menu=False
font = pygame.font.SysFont("monospace", 24, bold=True)
menu_command=0

#gambar pada menu
image1 = pygame.image.load("opening.png")
image2 = pygame.image.load("info.png")

def draw_game():
    menu_btn = Button('Main Menu', WIDTH//3 + 18, HEIGHT-140)
    menu_btn.draw()
    menu = menu_btn.check_clicked()
    return menu

def draw_menu():
    window.fill( PURPLE )
    command = -1
    pygame.draw.rect(window, PURPLE, [100, 100, 300, 300])
    pygame.draw.rect(window, BLACK, [100, 100, 290, 280], 5)
    tema = pygame.font.SysFont("monospace", 40, bold=True)
    txt = tema.render("PONG GAME", True, WHITE)
    window.blit(txt, (142, 127))
    # menu exit button
    menu = Button("Exit Menu", 120, 300)
    menu.draw()
    button1 = Button("Play Game", 120, 180)
    button1.draw()
    button2 = Button("Information", 120, 240)
    button2.draw()
    if menu.check_clicked():
        command = 0
    if button1.check_clicked():
        command = 1
    if button2.check_clicked():
        command = 2
    return command

def draw_board():
	window.fill( PURPLE )
	pygame.draw.line(window, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 5)
  
def restart():
	draw_board()
	score1.restart()
	score2.restart()
	ball.restart_coor()
	racket1.restart_coor()
	racket2.restart_coor()

def show_game_over():
    font = pygame.font.SysFont(None, 48)
    text = font.render("Game Over", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    window.blit(text, text_rect)
    pygame.display.update()

racket1 = Racket( window, WHITE, 15, HEIGHT//2 - 60, 20, 120 )
racket2 = Racket( window, WHITE, WIDTH - 20 - 15, HEIGHT//2 - 60, 20, 120 )
ball = Ball( window, WHITE, WIDTH//2, HEIGHT//2, 12 )
reflection = Reflection()
score1 = Score( window, '0', WIDTH//4, 15 )
score2 = Score( window, '0', WIDTH - WIDTH//4, 15 )

playing = False
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

		#tampilkan menu
        window.fill(PURPLE)
        window.blit(image1, (WIDTH//3 + 20, HEIGHT//2 - 100))

        if main_menu:
            menu_command = draw_menu()
            if menu_command != -1:
                main_menu = False
                
        else:
            main_menu = draw_game()
            if menu_command == 1:
                pygame.draw.rect(window, PURPLE, [100, 100, WIDTH, 300])
                text = font.render('Lets play the game', True, 'black')
                ball.start()
                playing = True
                window.blit(text, (150, 100))
            if menu_command == 2:
                window.blit(image2, (WIDTH//3 + 20, HEIGHT//2 - 150))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and playing:
                restart()
                playing = False

            if event.key == pygame.K_w:
                racket1.state = 'up'

            if event.key == pygame.K_s:
                racket1.state = 'down'

            if event.key == pygame.K_UP:
                racket2.state = 'up'

            if event.key == pygame.K_DOWN:
                racket2.state = 'down'

        if event.type == pygame.KEYUP:
            racket1.state = 'stopped'
            racket2.state = 'stopped'

    if playing:
        draw_board()

        # ball
        ball.move()
        ball.draw()

        # racket 1
        racket1.move()
        racket1.clamp()
        racket1.draw()

        # racket 2
        racket2.move()
        racket2.clamp()
        racket2.draw()

        # wall reflection
        if reflection.between_ball_and_walls(ball):
            ball.wall_collision()

        # racket reflection
        if racket1 or racket2:
            if reflection.between_ball_and_racket(ball, racket1):
                ball.racket_collision()
            if reflection.between_ball_and_racket(ball, racket2):
                ball.racket_collision()

        # GOAL OF PLAYER !
        goal_player = reflection.check_goal(ball)
        if goal_player:
            draw_board()
            if goal_player == 'player1':
                cek = score1.increase()
                if cek == "Winner":
                    score1.show()
                    pygame.time.wait(1000)
                    window.fill(PURPLE)
                    show_game_over()
                    pygame.time.wait(1000)
                    sys.exit()

            else:
                cek = score2.increase()
                if cek == "Winner":
                    score2.show()
                    pygame.time.wait(1000)
                    window.fill(PURPLE)
                    show_game_over()
                    pygame.time.wait(1000)
                    sys.exit()

            ball.restart_coor()
            racket1.restart_coor()
            racket2.restart_coor()
            playing = False

            score1.show()
            score2.show()

    clock.tick(40)
    pygame.display.update()
