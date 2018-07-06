import pygame
from GameObject import GameObject

class HealthBar(GameObject):

	def __init__(self,x,y,width,height):
		self.health =self.startHealth =  (width//4)- 40
		self.x,self.y = x,y
		self.width,self.height = width , height
		super(GameObject,self).__init__()
		back1W,back1H = width//4,height//8
		self.back1 = pygame.Rect(x,y,back1W,back1H)

		self.back2 = pygame.Rect(10,10,back1W - 20,back1H-20)

		self.healthH = (height//8) - 40
		edgeW = (width//4)- 40
		self.healthW = self.health 
		self.healthBar = pygame.Rect(20,20,self.healthW,self.healthH)

		self.edge = [[20+edgeW,20],[20+edgeW,20+self.healthH],[(edgeW+20)*.8,20+self.healthH]]
		self.wEdge = [[edgeW+30,20],[30+edgeW,30+self.healthH],[(edgeW+20)*.8,30+self.healthH]]

		self.damage = self.health//15

		


	def draw(self,screen,missiles):
		#pygame.draw.rect(screen,(255,255,255),self.back1)
		self.healthW = self.health
		self.healthBar = pygame.Rect(20,20,self.healthW,self.healthH)
		pygame.draw.rect(screen,(0,0,0),self.back2)
		pygame.draw.rect(screen,(0,255,0),self.healthBar)
		pygame.draw.polygon(screen,(0,0,0),self.edge)
		myfont = pygame.font.SysFont('Comic Sans MS',20,True )
		text = myfont.render('HEALTH', False, (0,255,0))
		w, h = text.get_size()
		healthRect = pygame.Rect (10,50,100,30)
		

		pygame.draw.rect(screen,(0,0,0),healthRect)

		screen.blit((text),(20,50))
		missiles = myfont.render('MISSILES:%s'%missiles, False, (0,255,0))
		w, h = missiles.get_size()
		missilesRect = pygame.Rect(10,80,150,30)
		pygame.draw.rect(screen,(0,0,0),missilesRect)
		screen.blit((missiles),(20,80))

		#self.hit()
		#pygame.draw.polygon(screen,(255,255,255),self.wEdge)
	def hit(self):
		#damage = self.health//10
		if self.health > 0:
			self.health -= self.damage

	def regain(self):
		if self.health < self.startHealth:
			self.health += self.damage

		

