# 场景类
import pygame
import random
Rate = 2

# 石头墙
class Brick(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('image/scene/brick.png')
		# self.image = pygame.image.load('image/walls.gif')
		# self.image = pygame.transform.scale(self.image, (self.image.get_width() / Rate, self.image.get_height() / Rate))
		self.rect = self.image.get_rect()
		self.kind = 'Brick'
		self.live = True

# 钢墙
class Iron(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('image/scene/iron.png')
		# self.image = pygame.image.load('image/steels.gif')
		# self.image = pygame.transform.scale(self.image, (self.image.get_width() / Rate, self.image.get_height() / Rate))
		self.rect = self.image.get_rect()
		self.kind = 'Iron'
		self.live = True

# 冰
class Ice(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.ice = pygame.image.load('image/scene/ice.png')
		self.rect = self.ice.get_rect()
		self.live = True

# 河流
class River(pygame.sprite.Sprite):
	def __init__(self, kind=None):
		pygame.sprite.Sprite.__init__(self)
		if kind is None:
			self.kind = random.randint(0, 1)
		self.rivers = ['image/scene/river1.png', 'images/scene/river2.png']
		self.river = pygame.image.load(self.rivers[self.kind])
		self.rect = self.river.get_rect()
		self.live = True

# 树
class Tree(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.tree = pygame.image.load('image/scene/tree.png')
		self.rect = self.tree.get_rect()
		self.live = True

# 地图
class Map():
	Map_list = []
	def __init__(self, stage=1):
		pass
	# 关卡一
	def create_stage1(self):
		for x in [2, 3, 6, 7, 18, 19, 22, 23]:
			for y in [2, 3, 4, 5, 6, 7, 8, 9, 10, 17, 18, 19, 20, 21, 22, 23]:
				brick = Brick()
				brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
				brick.live = True
				Map.Map_list.append(brick)

		for x in [10, 11, 14, 15]:
			for y in [2, 3, 4, 5, 6, 7, 8, 11, 12, 15, 16, 17, 18, 19, 20]:
				brick = Brick()
				brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
				brick.live = True
				Map.Map_list.append(brick)

		for x in [4, 5, 6, 7, 18, 19, 20, 21]:
			for y in [13, 14]:
				brick = Brick()
				brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
				brick.live = True
				Map.Map_list.append(brick)

		for x in [12, 13]:
			for y in [16, 17]:
				brick = Brick()
				brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
				brick.live = True
				Map.Map_list.append(brick)

		for x, y in [(11, 23), (12, 23), (13, 23), (14, 23), (11, 24), (14, 24), (11, 25), (14, 25)]:
			brick = Brick()
			brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
			brick.live = True
			Map.Map_list.append(brick)

		for x, y in [(0, 14), (1, 14), (12, 6), (13, 6), (12, 7), (13, 7), (24, 14), (25, 14)]:
			iron = Iron()
			iron.rect.left, iron.rect.top = 3 + x * 24, 3 + y * 24
			iron.being = True
			Map.Map_list.append(iron)
	# 关卡二
	def create_stage2(self):
		for x in [2, 3, 6, 7, 18, 19, 22, 23]:
			for y in [2, 3, 4, 5, 6, 7, 8, 9, 10, 17, 18, 19, 20, 21, 22, 23]:
				brick = Brick()
				brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
				brick.live = True
				Map.Map_list.append(brick)

		for x in [10, 11, 14, 15]:
			for y in [2, 3, 4, 5, 6, 7, 8, 11, 12, 15, 16, 17, 18, 19, 20]:
				brick = Brick()
				brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
				brick.live = True
				Map.Map_list.append(brick)

		for x in [4, 5, 6, 7, 18, 19, 20, 21]:
			for y in [13, 14]:
				brick = Brick()
				brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
				brick.live = True
				Map.Map_list.append(brick)

		for x in [12, 13]:
			for y in [16, 17]:
				brick = Brick()
				brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
				brick.live = True
				Map.Map_list.append(brick)

		for x, y in [(11, 23), (12, 23), (13, 23), (14, 23), (11, 24), (14, 24), (11, 25), (14, 25)]:
			brick = Brick()
			brick.rect.left, brick.rect.top = 3 + x * 24, 3 + y * 24
			brick.live = True
			Map.Map_list.append(brick)

		for x, y in [(0, 14), (1, 14), (12, 6), (13, 6), (12, 7), (13, 7), (24, 14), (25, 14)]:
			iron = Iron()
			iron.rect.left, iron.rect.top = 3 + x * 24, 3 + y * 24
			live = True
			Map.Map_list.append(iron)

	def protect_home(self):
		for x, y in [(11, 23), (12, 23), (13, 23), (14, 23), (11, 24), (14, 24), (11, 25), (14, 25)]:
			iron = Iron()
			iron.rect.left, iron.rect.top = 3 + x * 24, 3 + y * 24
			live = True
			# self.ironGroup.add(self.iron)
			Map.Map_list.append(iron)