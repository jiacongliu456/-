# 大本营类
import pygame
Rate = 2

# 大本营类
class Home(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.images = ['image/home/home1.png', 'image/home/home2.png', 'image/home/home_destroyed.png']
		self.image = pygame.image.load(self.images[0])
		# self.image = pygame.transform.scale(self.image, (self.image.get_width() / Rate, self.image.get_height() / Rate))
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = (3 + 12 * 24, 3 + 24 * 24)
		self.live = True
	# 大本营置为摧毁状态
	def set_dead(self):
		self.image = pygame.image.load(self.images[-1])
		self.live = False