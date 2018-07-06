'''
pygamegame.py
created by Lukas Peraza
This code was inspired by the Lukas Peraza
'''




  

import module_manager

module_manager.review()
from Button import *
import pygame

class Background(pygame.sprite.Sprite):

    def __init__(self,image,coor,width,height):
        pygame.sprite.Sprite.__init__(self)  
        self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(),(width,height))
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = coor
    def draw(self,screen):
        screen.blit(self.image,(0,0))


class StartScreen(object):

    def init(self):
        self.bye =0
        self.buttonLst = []
        mid = self.height//2
        factor = self.height//6
        for i in range(mid+factor,self.height-1,factor):
            if i == self.height//2  + self.height//6:
                self.buttonLst.append(StartButton(self.width//2,i,"e"))


            else:
                self.buttonLst.append(Instructions(self.width//2,i,"e"))
        self.BackGround = Background("images/StartScreen.png",(0,0),self.width,self.height)

        self.buttonLoc = 0
        self.buttonLst[self.buttonLoc].highlight = True
        self.instructions = False
        self.image =self.BackGround.image
        self.instructionPic = pygame.transform.scale(pygame.image.load('images/controller.png'),(820,490))
        TitleFont = pygame.font.SysFont('Algerian', 40)
        TitleFont.set_underline(True)
        self.textsurface = [[TitleFont.render('The 112 ', False, (0, 0, 0)),(50,80)],[TitleFont.render('Gates of Hell', False, (0, 0, 0)),(500,80)]]
        TextFont =  pygame.font.SysFont('Comic Sans MS', 40)
        self.directionText = TextFont.render('Press Circle to Go Back ', False, (0,0,0))
        self.backButton = Back(700,400,"e")
        

    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier,screen = None):

       
        if keyCode == "Down":
            
            self.buttonLoc = 1
        elif keyCode == "Up":
            self.buttonLoc = 0
        for i in range(len(self.buttonLst)):
            if i == self.buttonLoc:

                self.buttonLst[i].highlight = True
            else:
                self.buttonLst[i].highlight = False
        if keyCode == "X" :
            #screen.fill((0,0,0))
            if not self.instructions:
                if type(self.buttonLst[self.buttonLoc]).__name__ == "StartButton":

                    self.bye += 1
                elif type(self.buttonLst[self.buttonLoc]).__name__ == "Instructions":
                    self.instructions = True
                    screen.fill((255,255,255))

                    self.image = self.instructionPic
            else:
                self.instructions = False
                self.image = self.BackGround.image


            
        

        if keyCode == "Circle" and self.instructions:
            self.instructions = False
            self.image = self.BackGround.image
        
            





    
    def keyReleased(self, keyCode, modifier):
        pass
    def moveLeft(self,state):
        if self.joystickMode:
            return self.dirs[state]

    def moveRight(self,state):
        if self.joystickMode:
        
            
            return self.dirs[state]
    def moveTarget(self,dir):
        pass

    def timerFired(self, dt):
        pass

    def redrawAll(self, screen):
       # screen.fill((0,0,0))
        
        screen.blit(self.image,(0,0))

        if not self.instructions:
            for button in self.buttonLst:

                button.draw(screen)
            for i in self.textsurface:

                screen.blit(i[0],i[1])
        else:
            self.backButton.draw(screen)


        

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=800, height=500, fps=50, title="112 Pygame Game"):
        self.width,self.height = width,height
        self.bgColor = (255, 255, 255)
        self.fps = fps
        #self.b = Button(3,4,"98")
        pygame.init()
        if pygame.joystick.get_count() > 0:
            self.joystickMode = True
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            self.buttons = self.joystick.get_numbuttons()
            self.buttonNames = ["Square","X", "Circle","Triangle","L1","R1","L2","R2"]
            self.hatSigns = ["Left","Right","Up","Down"]
            self.dirs = {"Left" : False, "Right":False}


            self.axes  = self.joystick.get_numaxes()
            self.hats = self.joystick.get_numhats()
            print(self.hats)
        else:
            self.joystickMode = False

    def run(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((800, 500))
        # set the title of the window
        pygame.display.set_caption("112 Gates of Hell")

        

        # stores all the keys currently being held down
        self._keys = dict()
        

        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            
            time = clock.tick(self.fps)
            self.timerFired(time)
            if self.bye > 0:
                playing = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                    #print("yes")
                
                elif event.type == pygame.JOYBUTTONDOWN:
                    for i in range(self.buttons):
                        if self.joystick.get_button(i):
                            self.keyPressed(self.buttonNames[i],None,screen)

                elif event.type == pygame.JOYHATMOTION:
                    coor =self.joystick.get_hat(0)
                    if coor[0] == -1:
                        self.keyPressed(self.hatSigns[0],None)
                    elif coor[0] == 1:
                        self.keyPressed(self.hatSigns[1],None)
                    elif coor[1] == 1:
                        self.keyPressed(self.hatSigns[2],None)
                    elif coor[1] == -1:
                        self.keyPressed(self.hatSigns[3],None)





                elif event.type == pygame.JOYAXISMOTION:
                    for i in range(2):
                        if i == 0:
                            if self.joystick.get_axis(i) < -.5 :
                                self.moveTarget("Left")
                                self.dirs["Left"] = True
                                self.dirs["Right"] = False
                            elif self.joystick.get_axis(i) > .5:
                                self.moveTarget("Right")  
                                self.dirs["Right"] = True
                                self.dirs["Left"] = False
                            elif -.5 < self.joystick.get_axis(i) < .5:
                                self.dirs["Right"] = False
                                self.dirs["Left"] = False

                        else : 
                            if self.joystick.get_axis(i) < -.5 :
                                
                                self.moveTarget("Up")
                            elif self.joystick.get_axis(i) > .5:
                                self.moveTarget("Down")  
                            
                        
                    
                        

                elif event.type == pygame.QUIT:
                    playing = False
            
            self.redrawAll(screen)
            pygame.display.flip()
           
        return time,screen,clock


def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()