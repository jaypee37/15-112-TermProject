import pygame
import random
from GameObject import GameObject
from HomingMissle import HomingMissle

class Enemy(pygame.sprite.Sprite):
    @staticmethod
    def poses():
        Enemy.poseLst = []
        for i in range (1,7):
            Enemy.poseLst.append(pygame.transform.scale(pygame.image.load('images/enemyPoses/run%s.png' % i).convert_alpha(),(50,50)))




    def __init__(self, x, y,flip,dir):
        super(Enemy, self).__init__()

        self.x, self.y = x, y
        self.dir = dir
        self.health =  100
        self.runTrigger = 0
        self.deathCounter = 0
        self.runCounter = 0
        self.landed = True
        self.flip = flip
        self.isDead = False
        self.lockedOn = False
        self.bulletCount = 24
        self.bulletTrigger = 0
        self.healthPackage = pygame.transform.scale(pygame.image.load('images/health.png'),(20,20))
        

        self.updateImage(sx = 0)
    def findY(self,x,walls):
        for wall in walls:
            #print(type(wall).__name__)
      
            if type(wall).__name__ == "Wall":
                if wall.x1 <= x < wall.x1 + wall.x2:
                    slope = 0
                    
                    return wall.y1

                    
            else:
                if wall.x1 <= x < wall.x2:

                    slope = ((500-wall.y2) - (500-wall.y1)) / (wall.x2-wall.x1)

                    y = 500 - ((slope * (x-wall.x1)) + (500 - wall.y1))
                    if slope<0:
                        y = 500 - ((slope * (x-wall.x1)) + (500 - wall.y1))
                    return y
                

    def move(self,sx,x,walls):

        if self.x < x -75:
            self.x +=5
            self.y = self.findY(self.x+5,walls) - 20
            self.flip = True
        elif self.x > x + 75:
            self.x -= 5
            self.y = self.findY(self.x-5,walls)-20
            self.flip = False


        '''if dir == "x":
            if self.flip:
                self.x -= dt
            else:
                self.x += dt
        elif dir =="y":
            self.y+= dt'''

        self.bottom = self.updateImage(sx)

    def updateImage(self,sx):
        self.image = Enemy.poseLst[self.runTrigger]
        if self.flip:
            self.image = pygame.transform.flip(self.image,True,False)
        w, h = self.image.get_size()
        
        self.w,self.h = w,h
        self.rect = pygame.Rect(self.x -( w //4)-sx, self.y - h / 2, w/2, h)
        self.bottom = self.y + h
        self.missileRect = pygame.Rect(self.x -20 + sx, self.y - 20, 40 ,40 )



    def change(self,sx,state = None):
        if state != None:
            self.image = pygame.transform.scale(pygame.image.load('images/enemyPoses/attack.png').convert_alpha(),(50,50))
            if self.flip:
                self.image = pygame.transform.flip(self.image,True,False)

        else:

            if self.runTrigger == 5:
                self.runTrigger = 0
            else:
                self.runCounter += 1
            if self.runCounter == 5:
                self.runTrigger += 1
                self.updateImage(sx)
                self.runCounter = 0
     

    def shoot(self):

        #self.bulletCount += 1
       # print(self.bulletCount==0)
        if self.bulletCount == 25 :

            self.bulletTrigger += 1
            self.bulletCount = -1

            return True
        self.bulletCount += 1

    def drop(self):
        missileDrop = HomingMissle(self.x,self.y)
        missileDrop.image = pygame.transform.rotate(missileDrop.imageUnrotated,90)
        missileDrop.rect = (self.x-5,self.y-5,10,10)
        healthdrop = Health(self.x,self.y)
        i = random.choice([1,0,2,1,0,1,0,2,0,1])
        if i == 1:
            return missileDrop
        elif i == 2:
            return healthdrop

        return None

class Health(GameObject):
    def __init__(self,x,y,radius= 30):
        self.x,self.y = x,y
        
         
        self.image =  pygame.transform.scale(pygame.image.load('images/health.png').convert_alpha(),(25,20)) 
      
       
        super(Health, self).__init__(x, y, self.image, radius // 2)


    




