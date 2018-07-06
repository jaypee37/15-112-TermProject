import pygame
from GameObject import GameObject
import math

class HomingMissle (GameObject):

    def __init__(self,x,y,radius= 30):
        
        self.x,self.y,self.radius = x,y,radius
        self.startX,self.startY = x,y
        self.count = 0
        self.trigger = 0
        slope = (500 - self.y)/self.x
        
        angle = math.atan(slope)
        angle = angle * (180/math.pi)
        
         
        self.imageUnrotated =  pygame.transform.scale(pygame.image.load('images/missile.png').convert_alpha(),(25,20)) 
        self.image =  pygame.transform.rotate(self.imageUnrotated, angle)      
       
        super(HomingMissle, self).__init__(x, y, self.image, radius // 2)

    def formula(self,x1,x2,x3,t):
        return ((1-t)**2)*x1 + 2*(1-t)*(t)*x2+ (t**2)*x3
       
    def createCurve(self,x,y,x3,y3,t=0):

        if t == 110:
            return []

        else:
            x2 = x + (x3-x)//2
            y2 = (y3 - y)//2 + y

            x = int(self.formula(x,x2,x3,t/100))
            y = int(self.formula(y-30,y2,y3,t/100))
            

            return [[x,y-50]] + self.createCurve(x,y,x3,y3,t+5)

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

                    y = 500 - ((slope * (x-wall.x1)) + 140)
                    if slope<0:
                        y = 500 - ((slope * (x-wall.x1)) + 300)
                    return y


    def recurse(self,lst,walls):

        if len(lst) == 0:

            return []

        elif lst[0][1] < self.findY(lst[0][0],walls)+ 10:
            lst[0][1] += 1

            return  self.recurse(lst,walls)

        else:


            return [[lst[0][0],lst[0][1]] ]+ self.recurse(lst[1:],walls)

    def move(self,x3,y3,sx,walls):
        self.count += 1
        if self.count == 4:
            self.trigger += 1
            self.count = 0


        coors = self.createCurve(self.startX,self.startY,x3,y3)
        #coors = self.recurse(coors,walls)

        if self.trigger == len(coors):
            self.trigger= 0



        self.x,self.y = coors[self.trigger][0], coors[self.trigger][1]

        if self.x < coors[len(coors)-1][0] and self.y > self.findY(self.x,walls) - 5 :
            self.y =self.findY(self.x,walls) - 5
        slope = (500 - self.y)/self.x
        
        angle = math.atan(slope)
        angle = angle * (180/math.pi)
        
        
        self.image = pygame.transform.rotate(self.imageUnrotated,angle)
        if  y3 < self.x:
            #print("yes")
            self.image = pygame.transform.rotate(self.imageUnrotated,-angle)



        self.updateRect(sx)

    def draw(self,screen,sx):
        screen.blit(self.image,(self.x-sx,self.y))



    



