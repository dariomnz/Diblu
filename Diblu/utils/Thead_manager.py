import copy
import threading
import pygame
from pygame.locals import *
import time
import random
import sys

def rand_color():
    return [random.randrange(0,230) for i in range(0,3)]

global MESSAGE_TO_GUI
MESSAGE_TO_GUI=[]
class Hanoi(threading.Thread):
    def __init__(self,n,MESSAGE_TO_GUI):
        self.MESSAGE_TO_GUI=MESSAGE_TO_GUI
        threading.Thread.__init__(self)
        self.hanoi=[[],[],[]]
        self.hanoi[0]=range(n,0,-1)
    def grubu_tasi(self,kaynak,hedef):
            for tas in copy.copy(self.hanoi[kaynak]):
                self.tasi_tasi(tas ,hedef)
    def tasi_tasi(self,tas,hedef):
        for sopa in self.hanoi:
            if sopa.count(tas):
                kaynak=self.hanoi.index(sopa)
        if tas==1:
            self.hanoi[kaynak].pop()
            self.hanoi[hedef].append(1)
        else:
            hedefler=[0,1,2]
            hedefler.remove(kaynak)
            hedefler.remove(hedef)
            yeni_hedef=hedefler[0]
            for yeni_tas in copy.copy(self.hanoi[kaynak][self.hanoi[kaynak].index(tas)+1:]):
                self.tasi_tasi(yeni_tas,yeni_hedef)
            self.hanoi[kaynak].pop()
            self.hanoi[hedef].append(tas)
        time.sleep(1)
        while self.MESSAGE_TO_GUI:
            pass
        self.MESSAGE_TO_GUI.append({"from":kaynak,"to":hedef})
    def run(self):
        time.sleep(1)
        self.grubu_tasi(0,1)




class Sprite(object):
    def __init__(self):
        self.image=None
        self.rect=None
        self.xleftover=0
        self.yleftover=0
        self.placexleftover=0
        self.placeyleftover=0
 #       self.added=False
    def update(self,*args):
        pass
    def move(self,x,y):
        x+=self.xleftover
        y+=self.yleftover
        self.xleftover=x-int(x)
        self.yleftover=y-int(y)
        self.rect=self.rect.move(x,y)
    def move_to(self, **cor):
        cor[cor.keys()[0]]+=self.placexleftover
        cor[cor.keys()[1]]+=self.placeyleftover
        x=cor[cor.keys()[0]]
        y=cor[cor.keys()[1]]
        self.placexleftover=x-int(x)
        self.placeyleftover=y-int(y)
        self.rect=self.image.get_rect(**cor)
        
    def draw(self,surface,change):
        surface.blit(self.image,self.rect.move(change))
class Text(Sprite):
    def __init__(self,font,text,cor):
        self.image=font.render(text,1,(0,0,0))
        self.rect=self.image.get_rect(**cor)
DISK_H=20
class Disk(Sprite):
    def __init__(self,peg,n):
        self.image=pygame.Surface((50+(n*10),DISK_H))
        pygame.draw.rect(self.image, rand_color(), (0, 0, 50+(n*10),DISK_H))
        self.rect=self.image.get_rect()
        self.place(peg)
    def place(self,peg):
        self.peg=peg
        self.rect.centerx=self.peg.rect.centerx
        try:
            self.rect.centery=self.peg.disks[-1].rect.centery-DISK_H
        except:
            self.rect.centery=self.peg.rect.bottom-DISK_H

class Peg(Sprite):
    def __init__(self,n,cor,max):
        self.image=pygame.Surface((10,(max*DISK_H)+50))
        pygame.draw.rect(self.image, (0,0,0), (0, 0,10,(max*DISK_H)+50))
        self.rect=self.image.get_rect(**cor)
        self.disks=[]
        for disk in range(n+1,1,-1):
            self.disks.append(Disk(self,disk))
    def draw(self,surface,change):
        super(Peg , self).draw(surface,change)
        for disk in self.disks:
            disk.draw(surface,change)


pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Tower of Hanoi')
pygame.mouse.set_visible(1)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((255, 255, 255))
clck=pygame.time.Clock()
font = pygame.font.SysFont(pygame.font.get_default_font(),22)

####################SCENE 1########################


def scene1():
    global n
    text1=Text(font,"enter number of disks (max=20):",{"centerx":400,"centery":300})
    number=""
    text2=Text(font,number,{"left":text1.rect.right+5,"centery":300})
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    sys.exit()
                if event.key==K_RETURN:
                    if int(number)<=20:
                        n=int(number)
                        running=0
                        return 2
                if event.key==K_BACKSPACE:
                    number=number[:-1]
                    text2=Text(font,number,{"left":text1.rect.right+5,"centery":300})
                else:
                    try:
                        key= pygame.key.name(event.key)
                        if "1234567890".count(key) and len(number)<2:
                            number+=key
                            text2=Text(font,number,{"left":text1.rect.right+5,"centery":300})
                    except:
                        pass
            
        screen.fill((0,0,0))
        screen.blit(background, (0, 0))
    #    print MESSAGE_TO_GUI
        text1.draw(screen,(0,0))
        text2.draw(screen,(0,0))
        clck.tick(25)
        pygame.display.flip()


def scene2():
    hanoi=Hanoi(n,MESSAGE_TO_GUI)
    dis_between=((50+(n*10)))+15
    peg1=Peg(n,{"centerx":150,"bottom":550},n)
    peg2=Peg(0,{"centerx":150+dis_between,"bottom":550},n)
    peg3=Peg(0,{"centerx":150+(2*dis_between),"bottom":550},n)
    pegs=[peg1,peg2,peg3]
    text1=Text(font,"press SPACE to pause / continue",{"left":10,"top":10})
    text2=Text(font,"completed %0",{"left":20,"top":30})
    text3=Text(font,"",{"left":text1.rect.right+30,"top":10})
    hanoi.start()
    
    paused=0
    moves=0
    total_moves=float((2**n)-1)
    per=0
    ###################SCENE 2###########################
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    sys.exit()
                if event.key== K_SPACE and per<100:
                    paused=not paused
                    if paused:
                        text3=Text(font,"paused",{"left":text1.rect.right+30,"top":10})
                    else:
                        text3=Text(font,"",{"left":text1.rect.right+30,"top":10})
                if event.key== K_RETURN and per==100:
                    return 1
        screen.fill((0,0,0))
        screen.blit(background, (0, 0))
        text1.draw(screen,(0,0))
        text2.draw(screen,(0,0))
        text3.draw(screen,(0,0))
    #    print MESSAGE_TO_GUI
        if MESSAGE_TO_GUI and not paused:
            ms=MESSAGE_TO_GUI[0]
            fr=pegs[ms["from"]]
            to=pegs[ms["to"]]
            to_remove=fr.disks[-1]
            fr.disks.pop()
            to_remove.place(to)
            to.disks.append(to_remove)
            MESSAGE_TO_GUI.remove(ms)
            moves+=1
            per=(moves/total_moves)*100
            if per==100:
                text1=Text(font,"press ENTER to restart",{"left":10,"top":10})
            text2=Text(font,"completed %"+str(per),{"left":20,"top":30})
            
        for peg in pegs:peg.draw(screen,(0,0))
        clck.tick(25)
        pygame.display.flip()
scene=scene1
match={1:scene1,2:scene2}
while 1:
    reply=scene()
    scene=match[reply]


        