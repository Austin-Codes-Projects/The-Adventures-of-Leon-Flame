import pygame
from pygame.locals import *
import pygame.freetype as pyft
import sys, random
#import os #Remove hashtag before this import if downloaded

pygame.init()
DISPLAYSURF = pygame.display.set_mode((600, 400))
FPS = 60
clock = pygame.time.Clock()
pyt = pygame.transform
updown = 295
fb_active = False
spawn = False
flagStop = False
enemySelect = True
gmov = False
SCORE = 0
spawntime = 0
font = pyft.SysFont('lucidasanstypewriter', 0)
#os.chdir('') #Remove hashtag before this function if downloaded and enter full file directory for the game folder in the quotations, gotten by opening the game folder and copying the directory from the navigation bar at the top


class Background():
    def __init__(self):  #initialization
        self.bgimage = pyt.scale(pygame.image.load('bg.png'), (4551, 400))
        self.rectBGimg = self.bgimage.get_rect()

        self.bgY1 = 0
        self.bgX1 = 0

        self.bgY2 = 0
        self.bgX2 = self.rectBGimg.width

    def update(self, speed):  #Updating the position
        self.bgX1 -= speed
        self.bgX2 -= speed
        if self.bgX1 <= (-1 * self.rectBGimg.width + 600):
            global flagStop
            flagStop = True
        if self.bgX2 <= (-1 * self.rectBGimg.width):
            self.bgX2 = self.rectBGimg.width

    def change(self):  #Rendering the position change
        DISPLAYSURF.blit(self.bgimage, (self.bgX1, 0))
        DISPLAYSURF.blit(self.bgimage, (self.bgX2, 0))

    def output(self):  #Used for testing if the position is changing
        print(self.bgX2)


class player(pygame.sprite.Sprite):
    run = [
        pyt.flip(pyt.scale(pygame.image.load('1.png'), (50, 65)), True, False),
        pyt.flip(pyt.scale(pygame.image.load('1.png'), (50, 65)), True, False),
        pyt.flip(pyt.scale(pygame.image.load('1.png'), (50, 65)), True, False),
        pyt.flip(pyt.scale(pygame.image.load('2.png'), (50, 65)), True, False),
        pyt.flip(pyt.scale(pygame.image.load('2.png'), (50, 65)), True, False),
        pyt.flip(pyt.scale(pygame.image.load('2.png'), (50, 65)), True, False)
    ]  #Running animation frames
    jump = pyt.flip(pyt.scale(pygame.image.load('3.png'), (50, 65)), True,
                    False)  #Jumping 'animation'
    jumpList = [
        1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, -1, -1, -1, -2, -2, -2, -2, -3, -3, -3, -3, -3, -3, -3, -4, -4
    ]  #Tells how much to change y by during jump

    def __init__(self, win):  #Initialization
        super().__init__()
        self.rect = self.run[0].get_rect()
        self.rect.left = 100
        self.rect.bottom = 357
        self.jumping = False
        self.jumpCount = 0
        self.runCount = 0


    def draw(self, win):  #Drawing the character and its animations
        if self.jumping:
            self.rect.bottom -= self.jumpList[self.jumpCount] * 1.2
            win.blit(self.jump, self.rect)
            self.jumpCount += 1
            if self.jumpCount > 42:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0
        else:
            self.rect.bottom = 357
            if self.runCount > 42:
                self.runCount = 0
            win.blit(self.run[self.runCount % 6], self.rect)
            self.runCount += 1


plyr = player(DISPLAYSURF)


class fireball(pygame.sprite.Sprite):
    imgfb = pyt.scale(pygame.image.load('fireball.png'), (36, 17))

    def __init__(self):  #initialization
        super().__init__()
        self.image = self.imgfb
        self.rect = self.image.get_rect()
        self.rect.left = 150
        self.rect.bottom = 400
        self.jumpCount = 0

    def blast(self, win):  #Shooting animation
        self.rect.top = plyr.rect.top + 20
        win.blit(self.image, self.rect)
        if self.rect.right < 600:
            self.rect.right += 10
            print(self.rect.right)
        elif self.rect.right >= 600:
            self.rect.left = 150
            self.rect.bottom = 400
            global fb_active
            fb_active = False

    def reset(self):
        self.rect.left = 150
        self.rect.bottom = 400


class BOB(pygame.sprite.Sprite):
    imgbob = pyt.scale(pygame.image.load("bob.png"), (40, 36))

    def __init__(self, pos): #Initialization
        super().__init__()
        self.pos = pos
        self.image = self.imgbob
        self.rect = self.image.get_rect()
        self.rect.left = 600 + 50 * (pos -1)
        self.rect.top = 328

    def move(self, win): #Movement
        if self.rect.right > 0:
            self.rect.right -= 5
            win.blit(self.image, self.rect)
        else:
            self.rect.left = 600
            global spawn
            spawn = False

    def reset(self):
        self.rect.left = 600 + 50 * (self.pos - 1)

class JEFF(pygame.sprite.Sprite):
    imgbob = pyt.scale(pygame.image.load("Jeff.png"), (40, 36))

    def __init__(self, pos): #Initialization
        super().__init__()
        self.pos = pos
        self.image = self.imgbob
        self.rect = self.image.get_rect()
        self.rect.left = 600 + 50 * (pos -1)
        self.rect.top = 258

    def move(self, win): #Movement
        if self.rect.right > 0:
            self.rect.right -= 7
            win.blit(self.image, self.rect)
        else:
            self.rect.left = 600
            global spawn
            spawn = False

    def reset(self):
        self.rect.left = 600 + 50 * (self.pos - 1)

bkg = Background()
fb = fireball()
enemies = pygame.sprite.Group() #Sprite group for the enemies
FireNation = pygame.sprite.GroupSingle() #Sprite group for the fireball
bob1 = BOB(1)
bob2 = BOB(2)
bob3 = BOB(3)
bob4 = BOB(4)
jeff1 = JEFF(0.5)
jeff2 = JEFF(1.5)
jeff3 = JEFF(2.5)
jeff4 = JEFF(3.5)
boblist = [bob1, bob2, bob3, bob4]
jefflist = [jeff1, jeff2, jeff3, jeff4]
enemies.add(bob1)
enemies.add(bob2)
enemies.add(bob3)
enemies.add(bob4)
enemies.add(jeff1)
enemies.add(jeff2)
enemies.add(jeff3)
enemies.add(jeff4)
FireNation.add(fb)
'''
This allows for the creation and adding of multiple enemies in a single wave
'''
active = pygame.sprite.Group()




while True: #Game Loop
    bkg.__init__()
    bkg.change()
    DISPLAYSURF.blit(pyt.scale(pygame.image.load("Menu (1).png"), (405,390)),(97,5))
    text1_rect = font.get_rect('BACKSPACE:', size = 10)
    text1_rect.midleft = (140, 296)
    font.render_to(DISPLAYSURF,text1_rect,'BACKSPACE:',fgcolor = (0,0,0),bgcolor = (255,255,255), style = 3, size = 10)
    text2_rect = font.get_rect('ENTER:', size = 10)
    text2_rect.midleft = (140, 170)
    font.render_to(DISPLAYSURF,text2_rect,'ENTER:',fgcolor = (0,0,0),bgcolor = (255,255,255), style = 3, size = 10)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.__dict__.get('key') == K_BACKSPACE: #Ends Game
                gmov = True
            elif event.__dict__.get('key') == K_RETURN: #Starts Game
                spawntime = 100
                while True:
                    for event in pygame.event.get():
                        if event.type == KEYDOWN:
                            if event.__dict__.get('key') == K_SPACE: #Tells the character to jump whe nthe space bar is pressed
                                if not (plyr.jumping):
                                    plyr.jumping = True
                            elif event.__dict__.get('key') == K_z: #Tells the character to shoot a fireball when 'z' is pressed
                                fb_active = True
                            elif event.__dict__.get('key') == K_BACKSPACE: #Ends Game
                                gmov = True
                    flagStop = False

                    bkg.update(1)
                    bkg.change()
                    plyr.draw(DISPLAYSURF)
                    text3_rect = font.get_rect('SCORE:            P', size = 10)
                    text3_rect.midleft = (10, 20)
                    font.render_to(DISPLAYSURF,text3_rect,'SCORE:{}'.format(SCORE),fgcolor = (0,0,0),bgcolor = (255,255,0), style = 3, size = 10)

                    if fb not in FireNation:
                        FireNation.add(fb)
                    if (spawn == False) and (bob1 not in enemies):
                        enemies.add(bob1)
                    if (spawn == False) and (bob2 not in enemies):
                        enemies.add(bob2)
                    if (spawn == False) and (bob3 not in enemies):
                        enemies.add(bob3)
                    if (spawn == False) and (bob4 not in enemies):
                        enemies.add(bob4)
                    if (spawn == False) and (jeff1 not in enemies):
                        enemies.add(jeff1)
                    if (spawn == False) and (jeff2 not in enemies):
                        enemies.add(jeff2)
                    if (spawn == False) and (jeff3 not in enemies):
                        enemies.add(jeff3)
                    if (spawn == False) and (jeff4 not in enemies):
                        enemies.add(jeff4)

                    if spawntime == 0:
                        spawntime = random.randint(100,150)
                        spawn = True
                    else:
                        spawntime -= 1

                    if fb_active == True: #Shoots the fireball when activated
                        fb.blast(DISPLAYSURF)

                    if enemySelect == True:
                        no = random.randint(1,4)
                        for n in range(no):
                            enemyType = random.randint(1,2)
                            if enemyType == 1:
                                active.add(boblist[n])
                            elif enemyType == 2:
                                active.add(jefflist[n])
                        enemySelect = False

                    if spawn == True: #Spawns an enemy wave
                        for enemy in active:
                            enemy.move(DISPLAYSURF)

                    for enemy in active:
                        if pygame.sprite.collide_rect(fb,enemy) == True:
                            fb.reset()
                            enemy.reset()
                            fb.kill()
                            enemy.remove(active)
                            SCORE += 1
                            fb_active = False
                        if pygame.sprite.collide_rect(enemy, plyr) == True:
                            gmov = True
                            break
                    if len(active) == 0:
                        spawn = False
                        enemySelect = True

                    if flagStop or gmov == True: #Stops the code when the character reaches the end
                        break

                    pygame.display.update()

                    clock.tick(FPS)
    if flagStop == True:
        DISPLAYSURF.fill((81,97,251))
        DISPLAYSURF.blit(pyt.scale(pygame.image.load("The End (1).png"),(540,372)),(30,14))
        text3_rect = font.get_rect('FINAL SCORE:            P', size = 40)
        text3_rect.midleft = (10, 20)
        font.render_to(DISPLAYSURF,text3_rect,'FINAL SCORE:{}'.format(SCORE),fgcolor = (91, 252, 159),bgcolor = (81,97,251), style = 3, size = 40)
        pygame.display.update()
        pygame.time.delay(5000)
        break
    if gmov == True:
        DISPLAYSURF.fill((0,0,0))
        DISPLAYSURF.blit(pyt.scale(pygame.image.load("Game Over (1).png"),(710,370)),(-55,15))
        pygame.display.update()
        pygame.time.delay(5000)
        break
