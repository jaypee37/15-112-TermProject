import pygame

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
        self.landed = None
        self.flip = flip
        self.isDead = False
       

        self.updateImage()

    def move(self,dt,dir):
        if dir == "x":
            self.x += dt
        elif dir =="y":
            self.y+= dt
        self.bottom = self.updateImage()

    def updateImage(self):
        self.image = Enemy.poseLst[self.runTrigger]
        w, h = self.image.get_size()
        self.rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)

    def change(self):
        if self.runTrigger == 5:
            self.runTrigger = 0
        else:
            self.runCounter += 1
        if self.runCounter == 5:
            self.runTrigger += 1
            self.updateImage()
            self.runCounter = 0



