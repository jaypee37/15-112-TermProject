'''
pygamegame.py
created by Lukas Peraza
This code was inspired by the Lukas Peraza
'''




  

import module_manager

module_manager.review()
import pygame
from StartScreen import StartScreen


class PygameGame(object):

    def init(self):
        self.s = StartScreen()
        self. p = pygame.transform.scale(pygame.image.load('images/background.png'), (200,200))
        
        self.e= self.p.subsurface(100,100,30,30)

    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        pass

    
    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        pass

    def redrawAll(self, screen):
        screen.blit(self.e,(100,100))

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=800, height=500, fps=20, title="112 Pygame Game"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        self.fps2 = 10
        pygame.init()

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
                elif event.type == pygame.QUIT:
                    playing = False
            screen.fill(self.bgColor)
            
            
            self.redrawAll(screen)
            pygame.display.flip()
           
        pygame.quit()


def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()