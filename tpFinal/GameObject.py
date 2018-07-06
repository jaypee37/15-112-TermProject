
import pygame

class GameObject(pygame.sprite.Sprite):

	def __init__(self,x,y,image,radius,sx = 0):
		super(GameObject, self).__init__()
		self.x,self.y,self.image,self.radius = x,y,image,radius
		self.bottom = self.updateRect(sx)

	def updateRect(self,sx):
		w, h = self.image.get_size()
		self.width, self.height = w, h
		self.rect = pygame.Rect(self.x - w//8 -sx , self.y - h//8, w/8, h/8)
		self.platformRect = pygame.Rect(self.x - w//2, self.y - h//2, w, h)
		self.zoneRect = pygame.Rect(self.x-(2*w),self.y- h//4,4*w,h//2)
		self.hitMarker = pygame.Rect(self.x-w//4,self.y-h//2,w//2,h)
		self.missileRect = pygame.Rect(self.x - 30+sx, self.y -30 , 60, 60)
		self.dropRect = pygame.Rect(self.x+sx ,self.y,20,30)
		return self.y + h/2 

	def move(self):
		pass

	