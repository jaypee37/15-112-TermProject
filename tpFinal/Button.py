import pygame
from GameObject import GameObject



class Button(GameObject):

	def __init__(self,x,y,text, Xradius = 50,Yradius = 25//2):
		super(GameObject,self).__init__()
		self.x,self.y,self.text,self.Xradius,self.Yradius= x,y,text,Xradius,Yradius
		self.highlight = False
		self.rect = pygame.Rect(self.x - self.Xradius,self.y-self.Yradius, 2*self.Xradius,2*self.Yradius)
		self.highlight = False
	def draw(self,screen):
		pygame.draw.rect(screen,(255,0,0), self.rect)
		
		if self.highlight:
			pygame.draw.rect(screen,(0,0,0), self.rect,5)

		

class StartButton(Button):
	def __init__(self,x,y,text, Xradius = 50,Yradius = 25//2):
		super().__init__(x,y,text)

	def draw(self,screen):
		super().draw(screen)
		myfont = pygame.font.SysFont('Comic Sans MS',(2*self.Yradius) - 5 )
		text = myfont.render('START', False, (0,0,0))
		w, h = text.get_size()
		screen.blit((text),(self.x -w//2,self.y-h//2))



class Instructions(Button):
	def __init__(self,x,y,text, Xradius = 75,Yradius = 25//2):
		super().__init__(x,y,text,100)
		self.instructions = pygame.image.load('images/controller.png')

	def draw(self,screen):
		super().draw(screen)
		myfont = pygame.font.SysFont('Comic Sans MS',(2*self.Yradius) - 5 )
		text = myfont.render('INSTRUCTIONS', False, (0,0,0))
		w, h = text.get_size()
		screen.blit((text),(self.x -w//2,self.y-h//2))

class Back(Button):
	def __init__(self,x,y,text, Xradius = 75,Yradius = 25//2):
		super().__init__(x,y,text,50)
		self.highlight = True
	def draw(self,screen):
		super().draw(screen)
		myfont = pygame.font.SysFont('Comic Sans MS',(2*self.Yradius) - 5 )
		text = myfont.render('Back', False, (0,0,0))
		w, h = text.get_size()
		screen.blit((text),(self.x -w//2,self.y-h//2))



	

		

