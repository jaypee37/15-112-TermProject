import pygame
from pygamegame import PygameGame
from GameObject import GameObject
from fighter import Player
from bullet import Bullet
from bullet import Fireball
from enemy import Enemy
from wall import Wall
from HomingMissle import HomingMissle
from StartScreen import StartScreen
from Button import Button
from HealthBar import HealthBar
import math
'''
This code was inspired by Lukas Peraza's Game.py
'''
class Background(pygame.sprite.Sprite):

    def __init__(self,image,coor,width,height):
        pygame.sprite.Sprite.__init__(self)  
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = coor

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




class Game(PygameGame):
    def init(self):
        super(Game,self).__init__()
        self.s = StartScreen()
        self.bgColor = (0, 0, 0)
        Enemy.poses()
        #HomingMissle.createCurve([[300,300],[400,200],[500,250]])
        
        self.bulletGroup = pygame.sprite.Group()       
        self.player = Player(self.width / 2, 340,"Stand",False)
        self.players = pygame.sprite.GroupSingle(self.player)
        self.enemies = pygame.sprite.Group()
        self.gravity = True
        self.walls = [Wall(0,360,self.width,self.height)]
        self.BackGround = Background("images/background.png",(0,0),self.width,self.height)
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
        #self.gravityR = True
        #self.gravityL = True
        self.enemyRunCounter = 0
        self.H = pygame.sprite.GroupSingle()
        self.num = 1
        self.aimMode = False
        self.target = Target()
        self.rotatedTarget = self.target.rotate(self.num)
        self.targetX,self.targetY = 100,100
        self.healthBar = HealthBar(0,0,self.width,self.height)
        self.homing = False
        self.isKilled = False
        self.enemyBulletGroup = pygame.sprite.Group()

        self.i = 1

        

    

    def keyPressed(self, keyCode, modifier):  

        if keyCode == pygame.K_2:
            self.aimMode = not self.aimMode

        if self.aimMode:
            pass
         
         #lets character move jump with momentum

        else:
            if keyCode == pygame.K_SPACE:
                self.shooting = True

                if self.dir == "Right":
                
                    self.bulletGroup.add(Bullet(self.player.x+ self.player.width//4,\
                        self.player.y-self.player.height//6-4, True))
                else:
                    self.bulletGroup.add(Bullet(self.player.x- self.player.width//2,\
                        self.player.y-self.player.height//6-4, False))

            elif keyCode == pygame.K_UP:
                if self.isKeyPressed(pygame.K_RIGHT):
                    self.jumpingRight = True
                elif self.isKeyPressed(pygame.K_LEFT):
                    self.jumpingLeft = True
                else:
                    self.jumpingUp = True

            # shoots bullet
            
            elif keyCode == pygame.K_1:
                #self.coor = self.player.missile()
                self.H.add(HomingMissle(self.player.x,self.player.y))
                self.homing = True



    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        print(self._keys)
        return self._keys.get(key, False)
    def mouseMotion(self, x, y):
        if self.aimMode:
            self.targetX,self.targetY = x,y

    def mousePressed(self,x,y):
        #spawn enemy at mouse xy
        if self.aimMode:
            for e in self.enemies:
                if e.rect.collidepoint(x,y):
                    e.lockedOn = True
                    self.aimMode = False



        else:
            #self.healthBar.hit()
            if x > self.player.x:
                self.enemies.add(Enemy(x,y,False,False))
            else:
                self.enemies.add(Enemy(x,y,True,True))

    def followPlayer(self):
        for e in self.enemies:
            if e.x > self.player.x:
                e.flip = False
            else:
                e.flip = True

    

    def enemyTimerFired(self):
        self.followPlayer()
        #print(pygame.sprite.groupcollide(self.enemies,self.bulletGroup,False,False))

        #print(self.enemies)
        #enemies fall until hitting platform
        for wall in self.walls:
            for enemy in self.enemies :
                if not wall.rect.collidepoint(enemy.x,enemy.y+25):
                    enemy.move(10,"y")
                else:
                    enemy.landed = True
                
        #kill sequence for enemies
        for enemy in pygame.sprite.groupcollide(self.enemies,self.bulletGroup,False,True):

            enemy.health -= 20
           
            if enemy.health <= 0:
                if enemy.lockedOn:
                    self.H.empty()
             #   enemy.isDead = True
                enemy.kill()            
              
        #change image if dead
      
        for enemy in self.enemies:
            if enemy.isDead :
                            #enemy.deathCounter +=1 
                            #f enemy.deathCounter == 15:
                enemy.kill()  

            elif enemy.landed:
                if self.player.zoneRect.colliderect(enemy.rect):
                    enemy.change("attack")


                    if enemy.shoot():
                        self.enemyBulletGroup.add(Fireball(enemy.x,enemy.y-12,enemy.flip))
                    
                else:

                    enemy.change()
                    if enemy.dir =="Right":
                    
                        enemy.move(5,"x")
                    else:
                        enemy.move(-5,"x")
        for bullet in self.enemyBulletGroup:
            bullet.move(self.width)
                    



    def timerFired(self, dt):
        #print(self.isKilled)


        if self.aimMode:
            Target.count += 1
            if Target.count == 4:
                self.num += 1
                Target.count = 0
                if self.num == 5:
                    self.num = 1
            
            self.rotatedTarget = self.target.rotate(self.num)
            
        else:

            
            #pygame.sprite.groupcollide(self.H,self.enemies,True,True)
            for enemy in pygame.sprite.groupcollide(self.enemies,self.players,False,False):
                if enemy.lockedOn:
                    self.H.empty()
               
            for e in self.enemyBulletGroup:

                if self.player.hitMarker.colliderect(e.rect):
                    e.kill()
                    self.healthBar.hit()


            
            for p in self.H:
                for e in self.enemies:
                    if e.lockedOn :
                        p.move(e.x,e.y)
                        if e.rect.colliderect(p.rect):
                            
                            self.homing = False
                            self.H.empty()
                            e.kill()
                                



           #activate gravity
            for wall in self.walls:
                if self.player.platformRect.colliderect(wall.rect) :
                    self.gravity = False
                    self.gravityR =False
                
            self.enemyTimerFired()    

            #activate gravity
            if self.gravity:
                self.player.move(10.0,"y")

            #move bullets
            for bullet in self.bulletGroup:
                bullet.move(self.width)

            #sequence for jumping with momentum to the right
            if self.jumpingRight:
                

                if self.dir == "Right":
                    self.player.change("jump2",self.dir)
                else:
                    self.player.change("jump2", self.dir)

                self.gravityR = False
                self.jumpCounter+= 1

                self.player.move(-14,"y")
                self.player.move(10,"x")
                
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


                self.player.move(-14,"y")
                self.player.move(-10,"x")

                

                
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


                self.player.move(-14,"y")
                

                
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
                    #chnage pose to running right
                    if self.isKeyPressed(pygame.K_RIGHT):
                        self.dir = "Right"
                        self.runCounter += 1
                        if self.runCounter == 0 :

                            self.player.change("Stand",self.dir)

                        else:
                            if self.runCounter >5:
                                self.runCounter = 1
                            state = "run%s" % self.runCounter
                            self.player.change(state,self.dir) 
                        self.player.move(10,"x")




                        #change pose to running left
                    elif self.isKeyPressed(pygame.K_LEFT): #method for switching run image state
                        self.dir = "Left"
                        self.runCounter += 1
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
            wall.draw(screen)

        screen.blit(self.BackGround.image,(0,0))

        self.player.draw(screen)

        self.bulletGroup.draw(screen)
        self.enemyBulletGroup.draw(screen)
        self.enemies.draw(screen)
        if self.homing:
            #print("HOMINGGGGGG")
            self.H.draw(screen)
   
        self.healthBar.draw(screen)
        if self.aimMode:
            screen.blit(self.rotatedTarget,(self.targetX-self.target.width//2,self.targetY-self.target.height//2))
        

    @staticmethod
    def runGame():
        

        #t,s ,c= StartScreen(800,500).run()
        
       
        Game(800, 500).run()
        


Game.runGame()


