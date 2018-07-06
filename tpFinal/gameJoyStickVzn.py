import pygame
from newpygame import PygameGame
from GameObject import GameObject
from fighter import Player
from bullet import Bullet
from bullet import Fireball
from enemy import Enemy
from wall import Wall
from wall import *

from HomingMissle import HomingMissle
from StartScreen import StartScreen
from Button import Button
from HealthBar import HealthBar
from GameOver import GameOver
from letter import Letter
import math
import os
import random
'''
This code was inspired by Lukas Peraza's Game.py
'''
class Background(pygame.sprite.Sprite):
    

    
    def setBackground(self,folder):
        
        for file in os.listdir("images/%s" %folder):
            self.backs.append(pygame.transform.scale(pygame.image.load('images/%s/%s' % (folder,file)),(800,500)))

    def __init__(self,folder):
        self.counter = 0
        self.trigger = 0
        self.backs = []
        self.setBackground(folder)
        self.image = self.backs[0]


    
    def change(self,limit = 5):
        self.counter += 1
        if self.counter == limit:
            self.trigger+=1
            self.counter = 0
            if self.trigger == len(self.backs):
                self.trigger = 0
        return self.trigger

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
        #self.image = pygame.image.load('images/target%s.png' % num).convert_alpha()
        #self.image = pygame.transform.scale(self.image,(40,40))
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
    def levelUpInit(self):
        self.letterX = 0
        self.lvl = 1
        self.letterLst = ["%s" %self.lvl,":","l","e","v","e","L"]
        self.letterIndex = -1

        
        self.letters = []
        self.letterCounter = 0
        self.letterNum = 0
        self.lvlUp = True
        self.letterTimer = 0
    GameDrops = pygame.sprite.Group()
    def init(self):
        self.levelUpInit()
        super(Game,self).__init__()
        self.s = StartScreen()
        self.bgColor = (0, 0, 0)
        Enemy.poses()
        #HomingMissle.createCurve([[300,300],[400,200],[500,250]])
        #Background.setBackground("background")
        self.startWall = Wall(0,360,400,360)
        self.endWall = Wall(1600,360,400,360)
        self.bulletGroup = pygame.sprite.Group()       
        self.player = Player(50, 340,"Stand",False)
        self.players = pygame.sprite.GroupSingle(self.player)
        self.enemies = pygame.sprite.Group()
        self.gravity = True
        self.walls = [self.startWall,Slant(400,360,800,300,800,360),Wall(800,300,400,360), Slant(1200,300,1600,360,1200,360),self.endWall]
        self.BackGround = Background("background")
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
        self.bloodGroup = pygame.sprite.Group()
        self.scrollX = 0
        self.lockedOn = False
        self.missiles = 0
        self.spawnCounter,self.spawnTrigger = 0,random.randint(5,25)
        self.health  = 160
        self.enemiesSpawned = 0
        self.enemyLimit = 10
        self.enemyNum = 10
        self.myfont = pygame.font.SysFont('Comic Sans MS',(30) )
        self.text = self.myfont.render('Enemies:  %s' %self.enemyNum, False, (0,0,0))
        self.textW, self.textH = self.text.get_size()
        self.enemyLevel = 0
        self.gameOver = False
        self.jumping = False
        self.v = 6.5
        self.gameWon = False
        self.Flash = False
        self.gameOverScreen = Background("Gameover")
        self.gameOverText = self.myfont.render('Press X to Restart', False,(0,0,0))
        self.gameWonScreen = Background("Gamewon")
        pygame.mixer.set_num_channels(2)
        pygame.mixer.init()
        pygame.mixer.music.load('images/backMusic.ogg')
        pygame.mixer.music.play()
        self.actived = pygame.mixer.Sound('images/missileActivated.ogg')
        self.endMusic = False
        self.pause = False
        self.pauseImage = pygame.transform.scale(pygame.image.load('images/pause.png'),(200,200))
        #print(self.letterIndex)        #screen.blit((text),(self.width//2 -w//2,470-h//2))

        
        



    def findY(self,x):
        for wall in self.walls:
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


    def recurse(self,lst):

        if len(lst) == 0:

            return []

        elif lst[0][1] != self.findY(lst[0][0])- 10:
            lst[0][1] = self.findY(lst[0][0])- 10

            return  [[lst[0][0],lst[0][1]] ]+ self.recurse(lst[1:])

        else:


            return [[lst[0][0],lst[0][1]] ]+ self.recurse(lst[1:])












    def checkBounds(self):
        x = random.randrange(0,self.width)
        if x < self.player.x - 50 or x > self.player.x + 50:
            return x
        else:
            return self.checkBounds()

    def spawn(self):
        self.spawnCounter+= 1
        if self.spawnCounter == self.spawnTrigger and self.enemiesSpawned < self.enemyLimit:
            x = self.checkBounds() + self.scrollX
            for wall in self.walls:

                if type(wall).__name__ == "Wall":
                    if wall.x1 < x < wall.x1 + wall.x2:

                        slope = ((500-wall.y2) - (500-wall.y1)) / (wall.x2)

                        y = wall.y1
                        if x   > self.player.x + self.scrollX:
                        
                            self.enemies.add(Enemy(x,y-20,False,"Right"))
                            #print("right",x ,"wall",self.player.x + self.scrollX)
                        else:
                            self.enemies.add(Enemy(x,y-20,True,"Left"))
                            #print("left",x ,"wall",self.player.x + self.scrollX)


                        
                elif type(wall).__name__ == "Slant":
                    if wall.x1 < x < wall.x2:
                        slope = ((500-wall.y2) - (500-wall.y1)) / ((wall.x2)-(wall.x1))



                        y = 500 - ((slope * (x-wall.x1)) + 140)
                        if slope<0:
                            y = 500 - ((slope * (x-wall.x1)) + 300)
                        if x > self.player.x+self.scrollX:
                        
                            self.enemies.add(Enemy(x,y-20,False,"Right"))
                            #print("right",x ,'slant',self.player.x + self.scrollX)
                        else:
                            self.enemies.add(Enemy(x,y-20,True,"Left"))
                        
                            #print("left",x,"slant",self.player.x + self.scrollX)
                 
            self.spawnCounter = 0
            self.spawnTrigger = random.randint(35,55)
            self.enemiesSpawned += 1

    

    def keyPressed(self, keyCode, modifier):  
        if keyCode == "START":
            self.pause = not self.pause
        
            

        
        if not self.gameOver and not self.pause:
            if keyCode == "Circle":
                self.Flash = True
            if keyCode == pygame.K_3:
                pass

            if keyCode == pygame.K_2 or keyCode == "L1" and self.missiles  > 0:
                self.aimMode = not self.aimMode
                if self.aimMode:
                    
                    pygame.mixer.music.pause()
                    self.actived.play()
                else:
                    if not pygame.mixer.get_busy:
                        pygame.mixer.music.unpause()

                    


            if self.aimMode and self.joystickMode:
                for e in self.enemies:
                    if e.rect.collidepoint(self.targetX,self.targetY) and keyCode == "X":
                        self.ex,self.ey = self.targetX+self.scrollX,self.targetY
                        e.lockedOn = True
                        self.lockedOn = True
                        self.aimMode = False
                        pygame.mixer.music.unpause()
             
             #lets character move jump with momentum

            else:
                
                if keyCode == pygame.K_UP or keyCode == "X" :
                    
                    self.jumping  =True
                
                elif keyCode == pygame.K_SPACE or keyCode == "R2":
                    self.shooting = True

                    if self.dir == "Right":
                    
                        self.bulletGroup.add(Bullet(self.player.x+ self.player.width//4 ,\
                            self.player.y-self.player.height//6-4, self.dir))
                        
                    else:
                        self.bulletGroup.add(Bullet(self.player.x- self.player.width//2 ,\
                            self.player.y-self.player.height//6-4, self.dir))
                        #print(self.player.x- self.scrollX)

                

                # shoots bullet
                
                elif keyCode == pygame.K_1 or keyCode == "R1" and self.missiles > 0:
                    #self.coor = self.player.missile()
                    if self.lockedOn:
                        
                        self.H.add(HomingMissle(self.player.x+self.scrollX,self.player.y))
                        
                        self.lockedOn = False
                        if self.missiles > 0:
                            self.missiles -= 1
                        print(self.missiles)

                        self.homing = True
        else:
            if keyCode == "X":
                self.gameOver = False
                self.init()


    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)



    def moveTarget(self,dir):
        if self.aimMode and self.joystickMode:
            if dir == "Left":
                self.targetX -= 5
            elif dir == "Right":
                self.targetX += 5
            elif dir == "Up":
                self.targetY -= 5
            elif dir == "Down":
                self.targetY += 5
        
    def mouseMotion(self, x, y):
        if self.aimMode and not self.joystickMode:
            self.targetX,self.targetY = x,y

    def mousePressed(self,x,y):
        #spawn enemy at mouse xy
        
        if not self.gameOver:
            if self.aimMode:
                for e in self.enemies:
                    if e.rect.collidepoint(x,y):
                        e.lockedOn = True
                        self.aimMode = False



        

    def followPlayer(self):

        '''for e in self.enemies:
            if e.x > self.player.x:
                e.flip = False
            else:
                e.flip = True'''
        for e in self.enemies:
            x = e.x

            
                #print(e.rect)
            if e.x > self.player.x + self.scrollX:
                x = x-5
            else:
                x = x + 5

           
    def enemyTimerFired(self):
        
        for enemy in pygame.sprite.groupcollide(self.enemies,self.bulletGroup,False,True):

            enemy.health -= 20
           
            if enemy.health <= 0:
                if enemy.lockedOn:
                    self.H.empty()
             #   enemy.isDead = True
                drop = enemy.drop()
                if drop != None:
                    Game.GameDrops.add(drop)
                
                else:
                    self.bloodGroup.add(Blood(enemy.x,enemy.y))

                enemy.kill()  
                self.enemyNum -= 1

                

              
        #change image if dead
      
        for enemy in self.enemies:
            #self.followPlayer()
            '''if enemy.isDead :
                            #enemy.deathCounter +=1 
                            #f enemy.deathCounter == 15:
                enemy.kill()  '''

            
            if self.player.zoneRect.colliderect(enemy.rect):
                enemy.change(self.scrollX,"attack")


                if enemy.shoot():
                    if enemy.x < self.player.x + self.scrollX:
                        self.enemyBulletGroup.add(Fireball(enemy.x ,enemy.y-12,"Right"))
                    elif enemy.x > self.player.x + self.scrollX:
                        self.enemyBulletGroup.add(Fireball(enemy.x ,enemy.y-12,"Left"))
                
                    #print(enemy.x-self.scrollX)
            
            else:   
                enemy.move(self.scrollX,self.player.x + self.scrollX,self.walls)
                enemy.change(self.scrollX)
                self.followPlayer()  
        for bullet in self.enemyBulletGroup:
            bullet.move(self.width,self.scrollX)
                    
 
    def levelUp(self):
        if self.lvlUp:
            if self.letterNum < 7:

                self.letterCounter += 1
                if self.letterCounter == 5:
                    #print(self.i)
                    self.letterIndex += 1
                    self.letterX -= 40
                    

                    self.letters.append(Letter(self.letterX,100,self.letterLst[self.letterIndex]))
                    self.letterNum +=1
                    
                    self.letterCounter = 0
            else:

                self.letterTimer+= 1
                if self.letterTimer == 40:
                    #print("stop")
                    self.lvlUp = False
                    self.letters = []
                    self.letterNum = 0
                    self.letterIndex = -1
                    self.letterTimer = 0
                    self.letterX = 0
                    
            for l in self.letters:
                l.move()

    def timerFired(self, dt):
        if self.health <= 0:
            self.gameOver = True
            pygame.mixer.music.stop()

        if self.lvl == 2:
            self.gameWon = True
            

                #screen.fill((0,0,0))

        if not self.gameOver and not self.gameWon and not self.pause:

            #print(self.isKilled)
            self.text = self.myfont.render('Enemies:  %s' %self.enemyNum, False, (0,0,0))
            self.BackGround.image = self.BackGround.backs[self.BackGround.change()]
            

            if self.enemyNum == 0:
                self.lvl += 1

                i = random.randint(self.enemyLimit+1,self.enemyLimit+10)
                self.enemyNum, self.enemyLimit = i,i
                self.enemiesSpawned = 0
                self.spawnCounter = 0 
                
                self.lvlUp = True

               
                self.letterLst = ["%s" %self.lvl,":","l","e","v","e","L"]
            self.levelUp()
            '''if self.isKeyPressed(pygame.K_RIGHT) :
                self.scrollX += 10

            elif self.isKeyPressed(pygame.K_LEFT) and (self.startWall.x1-self.scrollX) <0:
                self.scrollX -=10'''

            for enemy in self.enemies:
                enemy.updateImage(self.scrollX)
            



            if self.aimMode:

                Target.count += 1
                if Target.count == 4:
                    self.num += 1
                    Target.count = 0
                    if self.num == 5:
                        self.num = 1
                
                self.rotatedTarget = self.target.rotate(self.num)
                



                
            else:
                self.spawn()

                
                #pygame.sprite.groupcollide(self.H,self.enemies,True,True)
                
                   
                for bullet in self.enemyBulletGroup:

                    if self.player.hitMarker.colliderect(bullet.rect):
                        self.Flash = True
                        bullet.kill()
                        self.healthBar.hit()
                        self.health -= 10




                
                for p in self.H:
                    for e in self.enemies:
                        if e.lockedOn :
                            
                            p.move(e.x-20,e.y+10,self.scrollX,self.walls)
                            
                            if e.missileRect.colliderect(p.missileRect):
                                
                                self.homing = False
                                self.H.empty()
                                e.kill()
                                self.enemyNum -= 1

                for player in self.players:
                    for drop in Game.GameDrops:
                        if player.dropRect.colliderect(drop.missileRect):
                            if type(drop).__name__ == "HomingMissle":
                                
                                self.missiles  +=1
                            else:
                                self.healthBar.regain()
                                self.health+= 10
                            drop.kill()

                if not self.jumping:
                    y = self.findY(self.player.x+ self.scrollX)
                    #print(y,self.player.x)
                    if self.player.y != y:
                        self.player.y = y -15
                else:
                    self.player.y -= (self.v **2)
                    self.v-=1
                    if self.v <= 0:
                        self.player.y += (self.v**2)
                        self.v -=1

                    y = self.findY(self.player.x+ self.scrollX)
                    #print(y,self.player.x)
                    if self.player.y >= y:
                        self.player.y = y -15
                        self.jumping = False
                        self.v = 6.5

               
                self.enemyTimerFired()    

                
                for bullet in self.bulletGroup:
                    bullet.move(self.width,self.scrollX)

                for bullet in self.enemyBulletGroup:
                    if bullet.y > self.findY(bullet.x ):
                        bullet.kill()

                if self.shooting:
                    self.shootCounter += 1
                    if self.dir == "Right":
                        self.player.change("Shoot",self.dir,self.scrollX)
                    else:
                        self.player.change("Shoot", self.dir,self.scrollX)

                    if self.shootCounter == 10:
                        self.shootCounter = 0
                        self.shooting = False




                else:
                    #chnage pose to running rightb
                    if self.isKeyPressed(pygame.K_RIGHT) or self.moveRight("Right"):
                        self.dir = "Right"
                        self.runCounter += 1
                        if (self.endWall.x1 + self.endWall.x2 - self.scrollX) >800 and self.player.x>100:
                            self.scrollX += 10
                        if self.runCounter == 0 :

                            self.player.change("Stand",self.dir,self.scrollX)

                        else:
                            if self.runCounter >5:
                                self.runCounter = 1
                            state = "run%s" % self.runCounter
                            self.player.change(state,self.dir,self.scrollX) 
                        self.player.move(5,"x",self.scrollX)




                        #change pose to running left
                    elif self.isKeyPressed(pygame.K_LEFT) or self.moveLeft("Left"): #method for switching run image state
                        self.dir = "Left"
                        self.runCounter += 1
                        if (self.startWall.x1-self.scrollX) < 0 and self.player.x < 700:
                            self.scrollX -= 10
                        if self.runCounter == 0 :

                            self.player.change("Stand",self.dir,self.scrollX)

                        else:
                            if self.runCounter >5:
                                self.runCounter = 1
                            state = "run%s" % self.runCounter
                            self.player.change(state,self.dir,self.scrollX) 
                        self.player.move(-5,"x",self.scrollX)
               
                    
                    #change pose to standing left or right
                    elif not self.isKeyPressed(pygame.K_LEFT) and self.dir == "Left" : 
                        self.player.change("Stand",self.dir,self.scrollX)
                    elif not self.isKeyPressed(pygame.K_RIGHT) and self.dir == "Right" :
                        self.player.change("Stand",self.dir,self.scrollX)


        elif self.gameOver:
            self.gameOverScreen.image = self.gameOverScreen.backs[self.gameOverScreen.change()]

        elif self.gameWon:
            self.gameWonScreen.image = self.gameWonScreen.backs[self.gameWonScreen.change(1)]
            
                 #   self.player = Player(self.player.x,self.player.y,"fall", False)

                            

    def redrawAll(self, screen):

        if not self.gameOver and not self.gameWon:
        #draw all walls,players, enemies, and bullets
            screen.blit(self.BackGround.image,(0-self.scrollX ,0))
            screen.blit(self.BackGround.image,(800-self.scrollX ,0))
            screen.blit(self.BackGround.image,(1600-self.scrollX ,0))
            for wall in self.walls:
                wall.draw(screen,self.scrollX)


        
            for drop in Game.GameDrops:
                screen.blit(drop.image,(drop.x-self.scrollX,drop.y))
            #screen.blit(self.player.image,(self.player.x-self.scrollX,self.player.y))
            self.player.draw(screen,self.scrollX)

            for bullet in self.bulletGroup:
                bullet.draw(screen,self.scrollX)
            for b in self.enemyBulletGroup:
                b.draw(screen,self.scrollX)


            for enemy in self.enemies:
                screen.blit(enemy.image,(enemy.x-self.scrollX-enemy.w//2,enemy.y-enemy.h//2))
            
            for blood in self.bloodGroup:
                screen.blit(blood.image,(blood.x-self.scrollX-blood.w//2,blood.y+5))
            #self.enemies.draw(screen)
                
            if self.homing:
                #print("HOMINGGGGGG")
                for h in self.H:
                    h.draw(screen,self.scrollX)
       
            self.healthBar.draw(screen,self.missiles)
            if self.aimMode:
                screen.blit(self.rotatedTarget,(self.targetX-self.target.width//2,self.targetY-self.target.height//2))
            
            screen.blit(self.text,(400 - self.textW//2,470 - self.textH//2))     

            if self.lvlUp:
                for l in self.letters:
                    l.draw(screen)
            if self.Flash:
                screen.fill((255,0,0))
                self.Flash = False
            if self.pause:
                screen.blit(self.pauseImage,(300,150))
        elif self.gameOver:
            screen.fill((0,0,0))
            screen.blit(self.gameOverScreen.image,(0,0))
            screen.blit(self.gameOverText,(300,400))
        elif self.gameWon:
            screen.fill((0,0,0,))
            screen.blit(self.gameWonScreen.image,(0,0))
            text = Letter(100,100,"You Are A God!!!!",False,'Comic Sans MS')
            text.draw(screen)
            if not self.endMusic:
                pygame.mixer.music.load('images/kanye.ogg')
                pygame.mixer.music.play(-1)
                self.endMusic = True



    @staticmethod
    def runGame():
        

        t,s ,c= StartScreen(800,500).run()
        
       
        Game(800, 500).run(t,c,s)
        
        


Game.runGame()


