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
		pygame.draw.rect( self.window, self.color, (self.coorX, self.coorY, self.width, self.height) )

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

	def restart(self):
		self.points = '0'
		self.label = self.font.render(self.points, 0, WHITE)

class Reflection:
	def between_ball_and_racket1(self, ball, racket):
		ballX = ball.coorX
		ballY = ball.coorY
		racketX = racket.coorX
		racketY = racket.coorY

		if ballY + ball.diameter > racketY and ballY - ball.diameter < racketY + racket.height:
			if ballX - ball.diameter <= racketX + racket.width:

				return True

		return False

	def between_ball_and_racket2(self, ball, racket):
		ballX = ball.coorX
		ballY = ball.coorY
		racketX = racket.coorX
		racketY = racket.coorY

		if ballY + ball.diameter > racketY and ballY - ball.diameter < racketY + racket.height:
			if ballX + ball.diameter >= racketX:
				return True

		return False

	def between_ball_and_walls(self, ball):
		ballY = ball.coorY

		if ballY - ball.diameter <= 0:
			return True

		if ballY + ball.diameter >= HEIGHT:
			return True

		return False

	def between_ball_and_goal1(self, ball):
		return ball.coorX + ball.diameter <= 0

	def between_ball_and_goal2(self, ball):
		return ball.coorX - ball.diameter >= WIDTH


WIDTH, HEIGHT = 900, 500
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

pygame.init()
window = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption('PONG')

def draw_board():
	window.fill( BLACK )
	pygame.draw.line( window, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 5 )

def restart():
	draw_board()
	score1.restart()
	score2.restart()
	ball.restart_coor()
	racket1.restart_coor()
	racket2.restart_coor()

draw_board()

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

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_p and not playing:
				ball.start()
				playing = True

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
			print('WALL reflection')
			ball.wall_collision()

		# racket1 reflection
		if reflection.between_ball_and_racket1(ball, racket1):
			print('reflection WITH racket 1')
			ball.racket_collision()

		# racket2 reflection
		if reflection.between_ball_and_racket2(ball, racket2):
			print('reflection WITH racket 2')
			ball.racket_collision()

		# GOAL OF PLAYER 1 !
		if reflection.between_ball_and_goal2(ball):
			draw_board()
			score1.increase()
			ball.restart_coor()
			racket1.restart_coor()
			racket2.restart_coor()
			playing = False

		# GOAL OF PLAYER 2!
		if reflection.between_ball_and_goal1(ball):
			draw_board()
			score2.increase()
			ball.restart_coor()
			racket1.restart_coor()
			racket2.restart_coor()
			playing = False

	score1.show()
	score2.show()

	clock.tick(40)
	pygame.display.update()
