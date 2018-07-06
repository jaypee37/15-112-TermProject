import pygame
from GameObject import GameObject

class Wall(GameObject):

	def __init__(self,x1,y1,x2,y2):
		self.x1,self.y1,self.x2,self.y2 = x1,y1,x2,y2
		
		self.rect = pygame.Rect(x1,y1,x2,y2)

	def draw(self,screen,sx):
		self.rect = pygame.Rect(self.x1-sx,self.y1,self.x2,self.y2)

		pygame.draw.rect(screen,(165,42,42),self.rect)
		'''image = pygame.transform.scale(pygame.image.load('images/wall.jpg').convert_alpha(),(100,140))
		screen.blit(image,(0-sx,360))
		screen.blit(image,(100-sx,360))'''



class Slant(GameObject):
	def __init__(self,x1,y1,x2,y2,x3,y3):
		self.x1,self.y1,self.x2,self.y2,self.x3,self.y3 = x1,y1,x2,y2,x3,y3

		self.points = [[x1,y1],[x2,y2],[x3,y3]]
		surface = pygame.image.load("images/background.png")
		self.rect = pygame.Rect(x1,0,x2,500)

	def draw(self,screen,sx):
		slope = ((500-self.y2) - (500-self.y1)) / (self.x2-self.x1)
		factor = sx//10
		'''y = 500 - ((slope * self.x1+sx) - 20)
		self.y1 = y
		
		y = 500 - ((slope * self.x2+sx) - 20)
		self.y2 = y
		
		y = 500 - ((slope * self.x3+sx) - 20)
		self.y3 = y'''

		self.points =[[self.x1-sx,500],[self.x1-sx,self.y1],[self.x2-sx,self.y2],[self.x2-sx,500]]
		self.rect = pygame.Rect((self.x1-sx,0),(400,500))
	
		pygame.draw.polygon(screen,(165,42,42),self.points)

class Platform(GameObject):

	def __init__(self,x1,y1,x2,y2):
		self.x1,self.y1,self.x2,self.y2 = x1,y1,x2,y2
		
		self.rect = pygame.Rect(x1,y1,x2,y2)

	def draw(self,screen,sx):
		self.rect = pygame.Rect(self.x1-sx,self.y1,self.x2,self.y2)

		pygame.draw.rect(screen,(255,255,255),self.rect)








