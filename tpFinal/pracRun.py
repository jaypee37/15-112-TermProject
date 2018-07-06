import pygame
from newpygame import PygameGame
from GameObject import GameObject
from fighter import Player
from bullet import Bullet
from bullet import Fireball
from enemy import Enemy
from wall import Wall
from wall import Slant

from HomingMissle import HomingMissle
from StartScreen import StartScreen
from Button import Button
from HealthBar import HealthBar
from GameOver import GameOver
import math
import os
import random
'''
This code was inspired by Lukas Peraza's Game.py
'''
class Background(pygame.sprite.Sprite):
    backs = []
    counter= 0
    trigger = 0

    @staticmethod
    def setBackground():
        
        for file in os.listdir("images/background"):
            Background.backs.append(pygame.transform.scale(pygame.image.load('images/background/%s' % file),(800,500)))

    def __init__(self,image,coor,width,height):
        pygame.sprite.Sprite.__init__(self)  
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = coor
        self.counter,self.trigger = 0,0

    @staticmethod
    def change():
        Background.counter += 1
        if Background.counter == 5:
            Background.trigger+=1
            Background.counter = 0
            if Background.trigger == 8:
                Background.trigger = 0
        return Background.trigger

class Target(pygame.sprite.Sprite):

    count = 0
    trigger = 0

    
    

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  
        self.image = pygame.image.load('images/target1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(40,40))
        w, h = self.image.get_size()
        self.width, self.height = w, h

    def rotate(self,num):
        self.image = pygame.image.load('images/target%s.png' % num).convert_alpha()
        self.image = pygame.transform.scale(self.image,(40,40))
        w, h = self.image.get_size()
        self.width, self.height = w, h
        return self.image

class Blood(pygame.sprite.Sprite):

    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self) 
        self.x,self.y = x,y 
        self.image = pygame.image.load('images/blood.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(30,20))
        w, h = self.image.get_size()
        self.w, self.h = w, h
        self.rect = pygame.Rect(self.x-w//2,self.y+h//3,w,h)





class Game(PygameGame):
    GameDrops = pygame.sprite.Group()
    def init(self):
        super(Game,self).__init__()
        self.s = StartScreen()
        self.bgColor = (0, 0, 0)
        Enemy.poses()
        #HomingMissle.createCurve([[300,300],[400,200],[500,250]])
        Background.setBackground()
        self.slant = Slant(400,360,800,200,800,360)
        
        self.bulletGroup = pygame.sprite.Group()       
        self.player = Player(self.width / 2, 340,"Stand",False)
        self.players = pygame.sprite.GroupSingle(self.player)
        self.enemies = pygame.sprite.Group()
        self.gravity = True
        self.walls = [Wall(0,360,self.width,self.height),Slant(400,360,800,200,800,360)]
        self.BackGround = Background.backs[0]
        self.jumpingUp = False
        self.jumpCounter = 0
        self.runCounter = 0
        self.dir = "Right"
        self.jumpingCounter = 0
        self.shooting = False
        self.shootCounter = 0
        self.falling = None
        self.jumpingRight = False
        self.jumpingLeft = False
        self.health = 100
        self.scrollX = 0
        #self.gravityR = True
      


    def keyPressed(self, keyCode, modifier):  
        


        if keyCode == pygame.K_UP or keyCode == "X" :
            if self.isKeyPressed(pygame.K_RIGHT) or self.moveRight("Right"):
                self.jumpingRight = True
            elif self.isKeyPressed(pygame.K_LEFT) or self.moveLeft("Left") :
                self.jumpingLeft = True
            else:
                self.jumpingUp = True

        # shoots bullet
        
       


    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)



   
        
    def mouseMotion(self, x, y):
        pass
        #print(self.slant.rect.collidepoint(x,y))
    def mousePressed(self,x,y):
        #spawn enemy at mouse xy
        pass

   
    

    def timerFired(self, dt):
        #print(self.isKilled)
        self.BackGround = Background.backs[Background.change()]

        



       
           #activate gravity
        for wall in self.walls:
            slope = ((500-wall.y2) - (500-wall.y1)) / (wall.x2-wall.x1)
            
            #print(slope)

            if wall.rect.collidepoint(self.player.x,self.player.bottom) :
                
                
                if type(wall).__name__ == "Wall":
                    self.gravity = False
                    self.gravityR =False
                elif type(wall).__name__ == "Slant":
                    y = 500 - ((slope * self.player.x+self.scrollX) - 20)
                    
                    if self.player.bottom >= y:
                        self.player.y = y - 20
                    #if self.player.bottom >= y:
                        self.gravity = False
                        self.gravityR =False
                    #else:
                     #   self.player.move(-10,"y")

            #self.player.updateRect()
            
       

        #activate gravity
        if self.gravity:
            self.player.move(10.0,"y")

      
        #sequence for jumping with momentum to the right
        if self.jumpingRight:
            

            if self.dir == "Right":
                self.player.change("jump2",self.dir)
            else:
                self.player.change("jump2", self.dir)

            self.gravityR = False
            self.jumpCounter+= 1

            self.player.move(-10,"y")
            self.player.move(10,"x")
            self.scrollX += 5
            
            if self.jumpCounter == 7:
                self.jumpingRight = False
                
                self.jumpCounter = 0
        #sequence for jumpping to the left with momentum
        elif self.jumpingLeft :
            if self.dir == "Right":
                self.player.change("jump2",self.dir)
            else:
                self.player.change("jump2", self.dir)

            self.gravityL = False
            self.jumpCounter+= 1


            self.player.move(-10,"y")
            self.player.move(-10,"x")
            self.scrollX -= 5

            

            
            if self.jumpCounter == 7:
                self.jumpingLeft = False
                
                self.jumpCounter = 0


        #sequence for jumoing straight up
        elif self.jumpingUp :
            if self.dir == "Right":
                self.player.change("jump2",self.dir)
            else:
                self.player.change("jump2", self.dir)


            self.gravity = False
            self.jumpCounter+= 1


            self.player.move(-10,"y")
            

            
            if self.jumpCounter == 7:
                self.jumpingUp = False
                
                self.jumpCounter = 0


            # if im not jumping, player is shooting or standing still
        elif not self.jumpingUp and not self.jumpingLeft and not self.jumpingRight :




            if self.player.bottom >= self.height :
                self.gravity = False
                
            else:
                self.gravity = True
            #change poses if shooting based on direction
            if self.shooting:
                self.shootCounter += 1
                if self.dir == "Right":
                    self.player.change("Shoot",self.dir)
                else:
                    self.player.change("Shoot", self.dir)

                if self.shootCounter == 10:
                    self.shootCounter = 0
                    self.shooting = False




            else:
                #chnage pose to running rightb
                if self.isKeyPressed(pygame.K_RIGHT) or self.moveRight("Right"):
                    self.dir = "Right"
                    self.runCounter += 1
                    self.scrollX += 5
                    if self.runCounter == 0 :

                        self.player.change("Stand",self.dir)

                    else:
                        if self.runCounter >5:
                            self.runCounter = 1
                        state = "run%s" % self.runCounter
                        self.player.change(state,self.dir) 
                    self.player.move(10,"x")




                    #change pose to running left
                elif self.isKeyPressed(pygame.K_LEFT) or self.moveLeft("Left"): #method for switching run image state
                    self.dir = "Left"
                    self.runCounter += 1
                    self.scrollX -= 5
                    if self.runCounter == 0 :

                        self.player.change("Stand",self.dir)

                    else:
                        if self.runCounter >5:
                            self.runCounter = 1
                        state = "run%s" % self.runCounter
                        self.player.change(state,self.dir) 
                    self.player.move(-10,"x")
           
                
                #change pose to standing left or right
                elif not self.isKeyPressed(pygame.K_LEFT) and self.dir == "Left" : 
                    self.player.change("Stand",self.dir)
                elif not self.isKeyPressed(pygame.K_RIGHT) and self.dir == "Right" :
                    self.player.change("Stand",self.dir)


            #else:
             #   self.player = Player(self.player.x,self.player.y,"fall", False)

                        

    def redrawAll(self, screen):

        
        #draw all walls,players, enemies, and bullets
        
        for wall in self.walls:
            wall.draw(screen,self.scrollX)


        #screen.blit(self.BackGround,(0 - self.scrollX,0))
        

        self.player.draw(screen)

        
        

    @staticmethod
    def runGame():
        

        t,s ,c= StartScreen(800,500).run()
        
       
        Game(800, 500).run(t,c,s)
        GameOver(800,500).run(t,c,s)
        


Game.runGame()


