import pygame
from Gameobject import Gameobject



class Button(Gameobject):

	def __init__(self,x,y,text, radius = 50):
		super(Gameobject,self).__init__()
		self.x,self.y,self.text,self.radius= x,y,text,radius
		self.highlight = False

	def draw(self,screen):
		self.draw.polygon(screen,(255,0,56), ((100,30)(24,56),(78,99)), width = 5)

