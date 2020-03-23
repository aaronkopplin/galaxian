import pygame

class Game:
	def __init__(self):
		pygame.init()
		# pygame.key.set_repeat(50)
		# self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode((800, 600))
		# self.balls = pygame.sprite.Group()

class Ball:
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((10, 10))

if __name__ == "__main__":
	game = Game()