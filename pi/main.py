# coding: utf-8
import pygame
import os
import platform
import sys
from itertools import chain, product

def drawRoundedRectangle(surface, color, rect, radius):
    x1,y1,x2,y2=rect
    pygame.draw.rect(surface,color,(x1+radius,y1,x2-(radius*2),y2))
    pygame.draw.rect(surface,color,(x1,y1+radius,x2,y2-(radius*2)))
    pygame.draw.circle(surface,color,(x1+radius,y1+radius),radius)
    pygame.draw.circle(surface,color,(x1+x2-radius,y1+radius),radius)
    pygame.draw.circle(surface,color,(x1+radius,y1+y2-radius),radius)
    pygame.draw.circle(surface,color,(x1+x2-radius,y1+y2-radius),radius)
    return pygame.Rect(rect)

class interfacePygame:
    def __init__(self):
        self.path = os.getcwd()
        self.os = platform.system()
        print(self.os)

        self.fenSize = (800, 480)
        self.sideBarWidth = 70
        self.screenSize = (self.fenSize[0]-self.sideBarWidth, self.fenSize[1])

        pygame.init()
        if self.os == 'Linux':
            pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
            self.mainSpace = pygame.display.set_mode(self.fenSize, pygame.NOFRAME)
        else:
            self.mainSpace = pygame.display.set_mode(self.fenSize)
        self.screen = pygame.Surface(self.screenSize)

        self.running = True
        
        self.needUpdate = True
        self.state="main"
        self.butClicked=0

        self.buttonsRect = []
        self.buttonActions = [self.drawMain,self.drawPasswd,self.drawWifi,self.drawSettings]
        
        self.drawMainBar()
        self.drawMain()

        while self.running:
            #_________________________________________Events/Input___________________________________________
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = event.pos
                    for index,button in enumerate(self.buttonsRect):
                        if button.collidepoint(mouse_pos):
                            self.butClicked = index
                            print('Button x:{} y:{} was pressed at {}, index {}'.format(button.x,button.y,mouse_pos,self.butClicked))
                            self.screen.fill((38,40,42))
                            self.buttonActions[self.butClicked]()
                            self.needUpdate = True
                    
                    screen_mouse_pos = (mouse_pos[0]-self.sideBarWidth,mouse_pos[1])
                    #print(mouse_pos)
                    
                    if self.state == "Settings":
                        if self.buttonOff.collidepoint(screen_mouse_pos):
                            print("Shutdown")
                            self.shutdown()
                        elif self.buttonReboot.collidepoint(screen_mouse_pos):
                            print("Reboot")
                            self.reboot()
                        elif self.buttonQuit.collidepoint(screen_mouse_pos):
                            print("Quit")
                            self.quit()
                        
            #_______________________________________Main loop_________________________________________________
            self.buttonActions[self.butClicked]()
            if self.needUpdate:
                self.needUpdate=False
                self.mainSpace.blit(self.screen,(self.sideBarWidth,0))
                pygame.display.update()
                self.drawMainBar()
        pygame.display.quit()

    def drawMainBar(self):
        self.screen.fill((38,40,42))
        self.mainSpace.fill((38,40,42))
        pygame.draw.rect(self.mainSpace,(50,50,52),(0,0,self.sideBarWidth,self.fenSize[1]))

        buttonContent=["home","lock","wifi","settings"]

        bOffX, bOffY = 5,10
        bSizeX = bSizeY = 60

        imgSize = 24
        imgOff = (bSizeY/2)-(imgSize/2)
        
        self.buttonsRect = []
        for i in range(len(buttonContent)):
            self.buttonsRect.append(pygame.draw.rect(self.mainSpace, (71,71,73), (bOffX, bOffX +(bOffY+bSizeX)*i,bSizeX,bSizeY)))
            img = pygame.image.load(self.path+"/Ui/"+buttonContent[i]+".png")
            self.mainSpace.blit(img,(bOffX + imgOff, bOffX +(bOffY+bSizeX)*i + imgOff))
        
        #self.mainSpace.blit(self.screen,(self.sideBarWidth,0))

    def drawMain(self):
        self.state="main"
        textRender = pygame.font.Font(None, 75).render("Accueil - WIP", 1, (71,71,73))
        self.screen.blit(textRender, (self.screenSize[0]/2-(textRender.get_width()/2),30))
    #____________________________________Password utilities____________________________________
    def drawPasswd(self):
        self.state="passwd"
        textRender = pygame.font.Font(None, 75).render("Passwords", 1, (71,71,73))
        self.screen.blit(textRender, (self.screenSize[0]/2-(textRender.get_width()/2),30))

        #for attempt in bruteforce(string.ascii_lowercase, 10):
    def bruteforce(charset, maxlength):
        return (''.join(candidate)
            for candidate in chain.from_iterable(product(charset, repeat=i)
            for i in range(1, maxlength + 1)))
    #_________________________Aircrack__________________________________
    def drawWifi(self):
        self.state="aircrack"
        textRender = pygame.font.Font(None, 75).render("Wifi cracking - WIP", 1, (71,71,73))
        self.screen.blit(textRender, (self.screenSize[0]/2-(textRender.get_width()/2),30))

    #______________________________________Reglages_____________________________________
    def drawSettings(self):
        self.state="Settings"
        textRender = pygame.font.Font(None, 75).render("Réglages", 1, (71,71,73))
        self.screen.blit(textRender, (self.screenSize[0]/2-(textRender.get_width()/2),30))

        bSizeX = 50
        bSizeY = bSizeX

        imgOff = pygame.image.load(self.path+"/Ui/off.png")
        self.buttonOff = self.screen.blit(imgOff,(50,100))

        imgRb = pygame.image.load(self.path+"/Ui/reboot.png")
        self.buttonReboot = self.screen.blit(imgRb,(50,200))

        imgQuit = pygame.image.load(self.path+"/Ui/quit.png")
        self.buttonQuit = self.screen.blit(imgQuit,(50,300))

    def shutdown(self):
        self.running = False
        pygame.quit()
        if self.os == 'Windows':
            print('Not going down')
            sys.exit()
            return
        os.system('sudo shutdown -h now')
        
    def reboot(self):
        self.running = False
        pygame.quit()
        if self.os == 'Windows':
            print('Not rebooting')
            sys.exit()
            return
        os.system('sudo reboot')
        
    def quit(self):
        self.running = False
        try:
            pygame.quit()
        except:
            raise "Cannot quit the application"
        sys.exit()
        return

interfacePygame()
