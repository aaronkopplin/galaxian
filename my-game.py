import pygame
import time
import random
import sys

# the controllable character
class player():
	def __init__(self, x, y):
		self.image = pygame.image.load("trump.png")
		self.x = x
		self.y = y
		self.lives = 3
		self.score = 0

	def moveLeft(self):
		self.x -= 1

	def moveRight(self):
		self.x += 1

# adversaries that the player gets points for killing
class virus():
	def __init__(self, x, y):
		self.image = pygame.image.load("outbreak.png")
		self.x = x
		self.y = y

	def moveLeft(self):
		self.x -= 1

	def moveRight(self):
		self.x += 1

	def fire(self):
		infections.append(infection(self.x, self.y + 1))

# pojectiles that the player fires
class dollar():
	def __init__(self, x, y):
		self.image = pygame.image.load("dollar.png")
		self.x = x
		self.y = y
		# thank u professor for the thud sound!
		self.sound = pygame.mixer.Sound('thud.wav')

	def moveUp(self):
		self.y -= 1

	def offGrid(self):
		return self.y < 0

	def playSound(self):
		self.sound.play()

# projectiles that the bat viruses fire
class infection():
	def __init__(self, x, y):
		self.image = pygame.image.load("virus.png")
		self.x = x
		self.y = y

	def moveDown(self):
		self.y += 1

	def offGrid(self):
		return self.y > gridWidth

# the window for the application and handles events
class game():
	def __init__(self):
		pygame.init()
		self.tileWidth = 32
		self.gridWidth = 15
		self.width = self.tileWidth * self.gridWidth
		self.height = self.tileWidth * self.gridWidth
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.font = pygame.font.Font(pygame.font.get_default_font(), 36)
		self.dollars = []
		self.infections = []
		self.player = player(7 ,12)
		self.viruses = [virus(2, 2), virus(4, 2), 
						virus(6, 2), virus(8, 2), 
						virus(10, 2), virus(12, 2),
						virus(2, 4), virus(4, 4),
						virus(6, 4), virus(8, 4),
						virus(10, 4), virus(12,4),
						virus(2, 6), virus(4, 6),
						virus(6, 6), virus(8, 6),
						virus(10, 6), virus(12, 6)]
		self.startGame()

	# put images on the screen
	def draw(self, image, x, y):
		self.screen.blit(image, (x * self.tileWidth, y * self.tileWidth))

	# handles the game loop and collisions and updating the screen
	def startGame(self):
        # game loop
		print("starting game")
		dollarStartTime = time.time()
		infectionStartTime = time.time()
		infectionMoveStartTime = time.time()
		virusMoveStartTime = time.time()
		virusMoveLeft = True
		running = True
		while running:
			dollarTime = time.time()
			infectionTime = time.time()
			infectionMoveTime = time.time()
			virusMoveTime = time.time()

			# set screen color
			self.screen.fill((100, 100, 100,))

			# handle events
			for event in pygame.event.get():
				
				# keyboard presses
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						if self.player.x > 0:
							self.player.moveLeft()
					if event.key == pygame.K_RIGHT:
						if self.player.x < self.gridWidth-1:
							self.player.moveRight()
					if event.key == pygame.K_UP:
						add = True
						for d in self.dollars:
							if self.player.y - d.y < 3:
								add = False
								print("add = false")
						if add:
							self.dollars.append(dollar(self.player.x, self.player.y - 1))
							print("appending dollar")

				# allow game to quit
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit(0)

			# allow viruses to move back and forth across the screen
			if virusMoveTime - virusMoveStartTime > 1:
				virusMoveStartTime = time.time()
				if virusMoveLeft:
					minX = self.gridWidth
					for v in self.viruses:
						if v.x < minX:
							minX = v.x
					if minX > 0:
						for v in self.viruses:
							v.x = v.x - 1
					else:
						virusMoveLeft = False
				else:
					maxX = 0
					for v in self.viruses:
						if v.x > maxX:
							maxX = v.x
					if maxX < self.gridWidth-1:
						for v in self.viruses:
							v.x = v.x + 1
					else:
						virusMoveLeft = True

			# fire infections
			if infectionTime - infectionStartTime > .8:
				var = random.randint(0, len(self.viruses)-1)
				vx = self.viruses[var].x
				vy = self.viruses[var].y
				self.infections.append(infection(vx, vy + 1))
				infectionStartTime = time.time()

			# collision detection
			for projectile in reversed(self.dollars):
				for enemy in reversed(self.viruses):
					if projectile.x == enemy.x and projectile.y == enemy.y:
						projectile.playSound()
						self.dollars.remove(projectile)
						self.viruses.remove(enemy)
						self.player.score += 1
						if len(self.viruses) == 0:
							print("game over!")
							pygame.quit()
							sys.exit(0)
					# remove projectiles when they go off screen
					if projectile.y < 0:
						self.dollars.remove(projectile)

			# end the game if the player gets hit
			for projectile in reversed(self.infections):
				if projectile.x == self.player.x and projectile.y == self.player.y:
					self.player.lives = self.player.lives - 1
					self.infections.remove(projectile)
					if self.player.lives == -1:
						print("game over!")
						pygame.quit()
						sys.exit(0)
				# remove projectile if it goes off screen
				if projectile.y > self.gridWidth:
					self.infections.remove(projectile)

			# remove dollars when they collide with infections
			for d in self.dollars:
				for i in self.infections:
					if d.x == i.x and d.y == i.y:
						self.dollars.remove(d)
						self.infections.remove(i)

			# draw game objects on top of background
			self.draw(self.player.image, self.player.x, self.player.y)
			for virus in self.viruses:
				self.draw(virus.image, virus.x, virus.y)
			if (dollarTime - dollarStartTime > .25):
				for projectile in self.dollars:
					dollarStartTime = time.time()
					projectile.moveUp()
			for projectile in reversed(self.dollars):
				self.draw(projectile.image, projectile.x, projectile.y)
				if projectile.offGrid():
					self.dollars.remove(projectile)
			if infectionMoveTime - infectionMoveStartTime > .25:
				for projectile in self.infections:
					infectionMoveStartTime = time.time()
					projectile.moveDown()
			for projectile in self.infections:
				self.draw(projectile.image, projectile.x, projectile.y)
			self.displayLives()
			self.displayScore()

			# update the screen
			pygame.display.update()

	# render text for score to screen
	def displayScore(self):
		text_surface = self.font.render('Score: ' + str(self.player.score), True, (255, 255, 255))
		self.screen.blit(text_surface, (0,0))

	# display a life icon for each remaining life in the bottom left of the screen
	def displayLives(self):
		for i in range(self.player.lives):
			self.draw(self.player.image, i, 14)


game = game()