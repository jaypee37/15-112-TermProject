
from GameObject import GameObject
import pygame

class Bullet(GameObject):

    

    def __init__(self,x,y,dir,radius= 15,):
        self.dir = dir
        #self.playerX = playerX
        #self.startX = startX
        self.x,self.y,self.radius =x,y,radius
        image =  pygame.transform.scale(pygame.image.load('images/bullet.png').convert_alpha(),(20,10))        
        if dir:
            image = pygame.transform.flip(image,True,False)
        
        super(Bullet, self).__init__(x, y, image, radius // 2)

    

    def move(self,w ,sx,):
        if self.dir == "Right":

            self.x += 20

        else:
            self.x -= 20

        if self.x > w or self.x < 0:
            self.kill()

        self.updateRect(sx)
        self.rect = pygame.Rect(self.x,self.y,5,5)

    def draw(self,screen,sx):
        screen.blit(self.image,(self.x,self.y))



class Fireball(Bullet):


    def __init__(self,x,y,dir,radius= 15,):
        self.dir = dir
       
        self.x,self.y,self.radius =x,y,radius
        self.imageR =  pygame.transform.scale(pygame.image.load('images/fireball.png').convert_alpha(),(20,20))        
        self.imageL = pygame.transform.flip(self.imageR,True,False)
        self.image = self.imageL
        if dir :
            self.image = self.imageR
        super(Bullet, self).__init__(x, y, self.image, radius // 2)

    def move(self,w,sx):
        if self.dir == "Right":
            self.x += 5
            self.image = self.imageL
        else:
            
            self.x -= 5 

        if self.x-sx > w or self.x-sx <0:
            self.kill()
        self.updateRect(sx)

    def draw(self,screen,sx):
        screen.blit(self.image,(self.x-sx,self.y))


