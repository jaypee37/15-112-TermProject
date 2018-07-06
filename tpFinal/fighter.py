import pygame
import os
from GameObject import GameObject



class Player(GameObject):


    @staticmethod
    def setPoses():
        Player.poses = dict()
    
    

    def __init__(self, x, y, state,flip ):
        #sets pose based on state and direction
        self.mx,self.my = None,None
        self.flip = flip

        self.player = pygame.transform.scale(pygame.image.load('images/meganManPoses/' +state+ '.png').convert_alpha(),(50,50))
            
        if flip:
            self.player = pygame.transform.flip(self.player,True,False)

        super(Player, self).__init__(x, y, self.player, 30)
        self.health =  100
        



    def move(self,dt,dir,sx):
        if dir == "x":
            self.x += dt
        elif dir =="y":
            self.y+= dt

        Player.x = self.x
        Player.y = self.y
        self.bottom = self.updateRect(sx)

    def draw(self,screen,sx):
        
        screen.blit(self.player,(self.x-self.width//2,self.y-self.height//2))
        
        self.bottom = self.updateRect(sx)



    def change(self,state, dir,sx):
        self.player = pygame.transform.scale(pygame.image.load('images/meganManPoses/%s.png' %state).convert_alpha(),(50,50))
        if not dir == "Right":
            self.player = pygame.transform.flip(self.player,True,False)
        
        self.updateRect(sx)


    def missile(self):
        self.mx,self.my= int(self.x),int(self.y)
        return self.mx,self.my


        

    


