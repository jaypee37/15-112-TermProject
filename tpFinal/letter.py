import pygame


class Letter(object):
	def __init__(self,x,y,letter,bold = True,font = "Algerian" ):
		self.x,self.y = x,y
		self.x1 = x
		self.a = -12
		
		self.velocity = 100
		self.rect = pygame.Rect(self.x,self.y,20,20)
		self.t = 0
		self.myfont = pygame.font.SysFont(font,(30),bold )
		self.text = self.myfont.render('%s' %letter, False, (255,0,0))
		self.textW, self.textH = self.text.get_size()


	def move(self):
		self.t+= 1
		if self.t <10:
			self.x = (self.velocity * self.t) + (.5 * -9 * (self.t**2)) + self.x1 
			self.rect = pygame.Rect(self.x,self.y,20,20)


	def draw(self,screen):
		screen.blit(self.text,(self.x,self.y))



