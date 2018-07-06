'''
pygamegame.py
created by Lukas Peraza
This code was inspired by the Lukas Peraza
'''




  

import module_manager

module_manager.review()
from Button import Button
import pygame

class Background(pygame.sprite.Sprite):

    def __init__(self,image,coor,width,height):
        pygame.sprite.Sprite.__init__(self)  
        self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(),(width,height))
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = coor


class GameOver(object):

    def init(self):
        self.bye =0
        self.buttonLst = []
        mid = self.height//2
        factor = self.height//6
        for i in range(mid+factor,self.height-1,factor):
            self.buttonLst.append(Button(self.width//2,i,"e"))
        self.BackGround = Background("images/Gameover.png",(0,0),self.width,self.height)


    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):

        self.bye += 1

    
    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        pass

    def redrawAll(self, screen):
        screen.blit(self.BackGround.image,(0,0))
        
        for button in self.buttonLst:
            button.draw(screen)
        

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)
    def moveLeft(self,state):
        if self.joystickMode:
            return self.dirs[state]

    def moveRight(self,state):
        if self.joystickMode:
        
            
            return self.dirs[state]
    def moveTarget(self,dir):
        pass

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
            self.hats = ["Left","Right","Up","Down"]
            self.dirs = {"Left" : False, "Right":False}


            self.axes  = self.joystick.get_numaxes()
        else:
            self.joystickMode = False

    def run(self,time,clock,screen):
        

        

        # stores all the keys currently being held down
        self._keys = dict()
        

        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            
            time = clock.tick(self.fps)
            self.timerFired(time)
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
                            self.keyPressed(self.buttonNames[i],None)
                
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
           
        pygame.quit()


def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()