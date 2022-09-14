from math import gcd
import pygame, random
from pygame import mixer
from Button import Button
from Tree import Tree

ScreenSize = (800,600)
Difficulty = 6
Multiplier = 25
#MaxScuares = (38,24)
#MineSize = (20,20)
pygame.init()
Font = pygame.font.SysFont('Comic Sans MS', 30)
LilFont = pygame.font.SysFont('Comic Sans MS',10)
Screen = pygame.display.set_mode(ScreenSize)

class Scuare(pygame.sprite.Sprite):#visible flagged type checked posiblemines probab arround
    def __init__(self, image, rect, size):
        super().__init__()
        self.visible = False
        self.flagged = False
        self.checked = False
        self.high = False
        self.image = image
        self.rect = rect
        self.size = size
        self.posiblemines = 0
        self.probab = 0
        self.type = "empty"
        self.arround = []

    def __str__(self):
        return str(self.type)

class Grid():#(38,24),(20,100),(20,20)
    def __init__(self, screen, mines, cuantity, startpos, size):
        self.screen = screen
        self.mines = mines
        self.flags = mines
        self.started = False
        self.cuantity = cuantity
        self.size = size
        self.startpos = startpos
        #creates all images
        self.scu1 = pygame.transform.smoothscale(pygame.image.load('Data/Graphics/1.png').convert(), size)
        self.scu2 = pygame.transform.smoothscale(pygame.image.load('Data/Graphics/2.png').convert(), size)
        self.scu3 = pygame.transform.smoothscale(pygame.image.load('Data/Graphics/3.png').convert(), size)
        self.scu4 = pygame.transform.smoothscale(pygame.image.load('Data/Graphics/4.png').convert(), size)
        self.scu5 = pygame.transform.smoothscale(pygame.image.load('Data/Graphics/5.png').convert(), size)
        self.scu6 = pygame.transform.smoothscale(pygame.image.load('Data/Graphics/6.png').convert(), size)
        self.scu7 = pygame.transform.smoothscale(pygame.image.load('Data/Graphics/7.png').convert(), size)
        self.scu8 = pygame.transform.smoothscale(pygame.image.load('Data/Graphics/8.png').convert(), size)
        self.flag = pygame.transform.smoothscale(pygame.image.load('Data/Graphics/flag.png').convert(), size)
        self.scuare = pygame.transform.smoothscale(pygame.image.load('Data/Graphics/scuare.png').convert(), size)
        self.empty = pygame.transform.smoothscale(pygame.image.load('Data/Graphics/empty.png').convert(), size)
        self.mine = pygame.transform.smoothscale(pygame.image.load('Data/Graphics/mine.png').convert(), size)
        self.explodedmine = pygame.transform.smoothscale(pygame.image.load('Data/Graphics/exploded mine.png').convert(), size) 
        #creates all the scuare objects
        self.grid = pygame.sprite.Group()
        self.matrix = [[Scuare(self.scuare,(0,0),(0,0)) for y in range(cuantity[1])] for x in range(cuantity[0])]
        for x in range(cuantity[0]):
            for y in range(cuantity[1]):
                self.matrix[x][y] = Scuare(self.scuare,(startpos[0]+(x*size[0]),startpos[1]+(y*size[1])),size)
                self.grid.add(self.matrix[x][y])
        #connects all the scuares arround eachother
        for x in range(cuantity[0]):
            for y in range(cuantity[1]):
                left = False
                right = False
                up = False
                down = False
                if x != 0:
                    self.matrix[x][y].arround.append(self.matrix[x-1][y])
                    left = True
                if x != cuantity[0]-1:
                    self.matrix[x][y].arround.append(self.matrix[x+1][y])
                    right = True
                if y != 0:
                    self.matrix[x][y].arround.append(self.matrix[x][y-1])
                    up = True
                if y != cuantity[1]-1:
                    self.matrix[x][y].arround.append(self.matrix[x][y+1])
                    down = True
                if up:
                    if left:
                        self.matrix[x][y].arround.append(self.matrix[x-1][y-1])
                    if right:
                        self.matrix[x][y].arround.append(self.matrix[x+1][y-1])
                if down:
                    if left:
                        self.matrix[x][y].arround.append(self.matrix[x-1][y+1])
                    if right:
                        self.matrix[x][y].arround.append(self.matrix[x+1][y+1])

    def image(self, scuare):#x
        if not scuare.visible:
            if scuare.flagged:
                scuare.image = self.flag
            else:
                scuare.image = self.scuare
        else:
            if scuare.type == "empty":
                scuare.image = self.empty
            elif scuare.type == "mine":
                scuare.image = self.mine
            elif scuare.type == "explodedmine":
                scuare.image = self.explodedmine
            elif scuare.type == 1:
                scuare.image = self.scu1
            elif scuare.type == 2:
                scuare.image = self.scu2
            elif scuare.type == 3:
                scuare.image = self.scu3
            elif scuare.type == 4:
                scuare.image = self.scu4
            elif scuare.type == 5:
                scuare.image = self.scu5
            elif scuare.type == 6:
                scuare.image = self.scu6
            elif scuare.type == 7:
                scuare.image = self.scu7
            elif scuare.type == 8:
                scuare.image = self.scu8

    def leftclick(self, pos):#x
        if self.started:
            for scuare in self.grid:
                scuare.high = False
                scuare.posiblemines = 0
            for scuare in self.grid:
                if pygame.Rect.collidepoint(pygame.Rect(scuare.rect[0],scuare.rect[1],scuare.size[0],scuare.size[1]),pos):
                    if not scuare.visible and not scuare.flagged:
                        if scuare.type == "mine":
                            scuare.type = "explodedmine"
                            self.revealmines()
                        scuare.visible = True
                        if scuare.type == "empty":
                            self.search()
                        self.image(scuare)
        elif self.startpos[0]<pos[0] and pos[0]<self.startpos[0]+(self.cuantity[0]*self.size[0]) and self.startpos[1]<pos[1] and pos[1]<self.startpos[1]+(self.cuantity[1]*self.size[1]):
            self.defineall(pos)
    
    def rightclick(self, pos):#x
        for scuare in self.grid:
            scuare.high = False
            scuare.posiblemines = 0
        for scuare in self.grid:
            if pygame.Rect.collidepoint(pygame.Rect(scuare.rect[0],scuare.rect[1],scuare.size[0],scuare.size[1]),pos):
                if not scuare.visible:
                    if scuare.flagged:#flag to scuare
                        scuare.flagged = False
                        self.image(scuare)
                        self.flags += 1
                    elif self.flags>0 and not scuare.flagged:#scuare to flag
                        scuare.flagged = True
                        self.image(scuare)
                        self.flags -= 1

    def defineall(self,pos):#x
        #places the mines
        for scuare in self.grid:
            if pygame.Rect.collidepoint(pygame.Rect(scuare.rect[0],scuare.rect[1],scuare.size[0],scuare.size[1]),pos):
                if not scuare.visible and not scuare.flagged:
                    scuare.image = self.empty
                    scuare.visible = True
                    for i in range(self.mines):
                        added = False
                        while not added:
                            added = False
                            x = self.startpos[0] + (random.randint(0,self.cuantity[0]-1)*(self.size[0]))
                            y = self.startpos[1] + (random.randint(0,self.cuantity[1]-1)*(self.size[1]))
                            if not((scuare.rect[0]-21 < x and x < scuare.rect[0]+21) and (scuare.rect[1]-21 < y and y < scuare.rect[1]+21)):
                                for subscuare in self.grid:
                                    if subscuare.type != "mine" and pygame.Rect.collidepoint(pygame.Rect(subscuare.rect[0],subscuare.rect[1],subscuare.size[0],subscuare.size[1]),(x,y)):
                                        subscuare.type = "mine"
                                        added = True
        #adds mine proximity counter
        for scuare in self.grid:
            if scuare.type == "mine":
                influence = [(scuare.rect[0]-20,scuare.rect[1]-20),(scuare.rect[0]+20,scuare.rect[1]-20),(scuare.rect[0]-20,scuare.rect[1]+20),(scuare.rect[0]+20,scuare.rect[1]+20),(scuare.rect[0]-20,scuare.rect[1]),(scuare.rect[0]+20,scuare.rect[1]),(scuare.rect[0],scuare.rect[1]-20),(scuare.rect[0],scuare.rect[1]+20)]
                for i in influence:
                    for subscuare in self.grid:
                        if pygame.Rect.collidepoint(pygame.Rect(subscuare.rect[0],subscuare.rect[1],subscuare.size[0],subscuare.size[1]),i):
                            if subscuare.type == "empty":
                                subscuare.type = 1
                            elif type(subscuare.type) == int:
                                subscuare.type += 1
        self.started = True
        for scuare in self.grid:
            scuare.checked = False
        self.search()

    def search(self):#x
        looking = True
        while looking:
            looking = False
            #ciclo de busqueda por cuadro
            for scuare in self.grid:
                if scuare.type == "empty" and scuare.visible and not scuare.checked:
                    scuare.checked = True
                    for a in scuare.arround:
                        if not a.visible:
                            looking = True
                        a.visible = True
                        self.image(a)
                        
    def revealmines(self):#x
        for scuare in self.grid:
            if scuare.type == "mine":
                scuare.visible = True
                scuare.image = self.mine
                self.image(scuare)
    
    def revealall(self):#x
        for scuare in self.grid:
            scuare.visible = True
            self.image(scuare)
    
    def minesleft(self):#x
        minesleft = self.mines
        lost = False
        for scuare in self.grid:
            if scuare.type == "mine" and scuare.flagged:
                minesleft -= 1
            if scuare.type == "explodedmine":
                lost = True
        if lost:
            minesleft = -1
        return minesleft
    
    def FlagNReveal(self, scuare):
        update = False
        notvisible = 0
        flags = 0
        closemines = int(scuare.type)
        for s in scuare.arround:#counts non visible and flagged scuares arround
            if not s.visible:
                notvisible += 1
        if closemines == notvisible:# flags mines
            update = True
            scuare.checked = True
            for s in scuare.arround:
                if not s.visible:
                    s.checked = True
                    s.flagged = True
                    self.image(s)
                    flags -= 1
        for s in scuare.arround:
            if s.flagged:
                flags += 1
        if closemines == flags:# reveals non mines
            update = True
            scuare.checked = True
            for s in scuare.arround:
                if not s.visible and not s.flagged:
                    if s.type == "mine":
                        s.type = "explodedmine"
                    s.visible = True
                    self.image(s)
                    if s.type == "empty":
                        self.search()
        #if neither probable = True
        self.image(scuare)
        return update

    def Auto(self):#make show flags in real time
        for scuare in self.grid:
            scuare.high = False
            scuare.posiblemines = 0
        self.show()
        workin = True
        probable = False
        #Shows with the 100% or 0% logic
        while workin and not probable:
            probable = True
            for scuare in self.grid:
                scuare.high = True
                update = False
                #does all the flagging and revealing
                if not scuare.checked and scuare.visible and isinstance(scuare.type, int):#convertir minas a rojas
                    update = self.FlagNReveal(scuare)
                    if update:
                        probable = False
                if update:
                    self.grid.draw(self.screen)
                    for x in range(self.startpos[0],self.startpos[0]+760+1,self.size[0]):
                        pygame.draw.line(self.screen,(0,100,0),(x,self.startpos[1]),(x,self.startpos[1]+480))
                    for y in range(self.startpos[1],self.startpos[1]+480+1,self.size[1]):
                        pygame.draw.line(self.screen,(0,100,0),(self.startpos[0],y),(self.startpos[0]+760,y))
                for sc in self.grid:
                    if sc.high:
                        pygame.draw.rect(self.screen,(0,100,0),pygame.Rect(sc.rect,sc.size),1)
                pygame.display.flip()
            minesleft = self.minesleft()
            if minesleft<1:
                workin = False
            self.flags = minesleft
            for scuare in self.grid:
                scuare.high = False
            if probable:
                for scuare in self.grid:
                    number = False
                    for sc in scuare.arround:
                        if isinstance(sc.type, int) and sc.visible:
                            number = True
                    if not scuare.visible and not scuare.flagged and number:
                        scuare.high = True
            print(workin, update)
            self.show()
            pygame.display.flip()
        #Shows otherwise
        if probable:
            for scuare in self.grid:
                if scuare.high:
                    scuare.checked = True
                else:
                    scuare.checked = False
            #makes groups for each section of probability
            groups = []
            for scuare in self.grid:
                if scuare.checked:
                    groups.append(self.Group(scuare))
                if scuare.high:
                    n = 0
                    for sc in scuare.arround:
                        if isinstance(sc.type, int) and sc.visible:
                            ammount = 0
                            for subsc in sc.arround:
                                if subsc.flagged:
                                    ammount += 1
                            n += int(sc.type) - ammount
                    scuare.posiblemines = n
            print("group ammount: ",len(groups))
            #make all mine arangements and count # of mines used for each
            for g in groups:
                group = g[:]
                group = self.Tree(group)
                for sc, psc in zip(g, group):
                    sc.probab = psc.probab
                    print(sc.posiblemines,": ",sc.probab)
            #final probability

    def Prob(self,g):
        for i in g:
            i.checked = True
        for sc in g:#cuadro
            obvio = False
            tienemina = False
            for subsc in sc.arround:#es obvio? (alrededor del inicial) x
                if subsc.visible and not subsc.flagged and isinstance(subsc.type, int) and not subsc.checked:
                    ammount = int(subsc.type)
                    invis = 0
                    for a in sc.arround:#conteo banderas y vacios por alrededor del inicial
                        if a.flagged:
                            ammount -= 1
                        elif not a.visible:
                            invis += 1
                    if ammount == invis:
                        obvio = True
                        tienemina = True
                    elif ammount == 0:
                        obvio = True
                        tienemina = False
            if obvio:#SI
                if tienemina:#ejecuta
                    sc.flagged = True
                    sc.probab += 1
                else:
                    sc.visible = True
            else:#NO
                gx = g[g.index(sc):]
                gx[0].flagged = True
                gx = self.Prob(gx)
                gy = g[g.index(sc):]
                gy[0].visible = True
                gy = self.Prob(gy)
                ind = g.index(sc)
                for x, y in zip(gx, gy):
                    g[ind].probab = x.probab + y.probab
                    ind += 1
                break
        return g

    def Group(self, scuare):#highlighted = not checked
        scuare.checked = False
        g = [scuare]
        done = False
        while not done:
            done = True
            for sc in g:
                for subsc in sc.arround:
                    if subsc.checked:
                        done = False
                        subsc.checked = False
                        g.append(subsc)
        return g

    def show(self):#x
        #shows all scuares in the grid
        self.grid.draw(self.screen)
        for sc in self.grid:
            if sc.posiblemines != 0:
                text = LilFont.render(str(sc.posiblemines),True, (0,0,0))
                text_rect = text.get_rect(center=(sc.rect[0]+sc.size[0]/2,sc.rect[1]+sc.size[1]/2))
                self.screen.blit(text, text_rect)
        #grid divisory lines
        for x in range(self.startpos[0],self.startpos[0]+760+1,self.size[0]):
            pygame.draw.line(self.screen,(0,100,0),(x,self.startpos[1]),(x,self.startpos[1]+480))
        for y in range(self.startpos[1],self.startpos[1]+480+1,self.size[1]):
            pygame.draw.line(self.screen,(0,100,0),(self.startpos[0],y),(self.startpos[0]+760,y))
        #show highlight
        for sc in self.grid:
            if sc.high:
                pygame.draw.rect(self.screen,(0,0,0),pygame.Rect(sc.rect,sc.size),2)
        return self.flags

class Start():
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.state = "start"
        self.playbutton = Button(screen,(63, 97, 1),(0,0,0),self.font,20,20,240,60)
        self.exitbutton = Button(screen,(63, 97, 1),(0,0,0),self.font,540,20,240,60)
  
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousepos = pygame.mouse.get_pos()
                if self.playbutton.check_click(mousepos):
                    self.state = "playing"
                if self.exitbutton.check_click(mousepos):
                    self.state = "quit"

    def show(self):
        #background
        self.screen.fill((169, 237, 43))
        #shows start and exit
        self.playbutton.show("Play")
        self.exitbutton.show("Exit")
        pygame.display.flip()

    def run(self):
        while self.state == "start":
            self.events()
            self.show()
        return self.state

class Game():#playing leave win loose
    def __init__(self, screen, font, difficulty, multiplier):
        self.screen = screen
        self.font = font
        self.state = "playing"
        self.mines = difficulty*multiplier
        self.flags = difficulty*multiplier
        self.autobutton = Button(screen,(63, 97, 1),(0,0,0),self.font,20,20,240,60)
        self.flagsbutton = Button(screen,(63, 97, 1),(168, 27, 27),self.font,280,20,240,60)
        self.exitbutton = Button(screen,(63, 97, 1),(0,0,0),self.font,540,20,240,60)
        self.grid = Grid(screen,self.mines,(38,24),(20,100),(20,20))

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                state = pygame.mouse.get_pressed()
                mousepos = pygame.mouse.get_pos()
                if state[0]:#left click
                    if self.exitbutton.check_click(mousepos):
                        self.state = "start"
                    if self.grid.started and self.flagsbutton.check_click(mousepos):
                        self.grid.revealall()
                    if self.grid.started and self.autobutton.check_click(mousepos):
                        self.grid.Auto()
                    if self.state == "playing":
                        if 20<=mousepos[0] and mousepos[0]<=(20+(38*20)) and 100<=mousepos[1] and mousepos[1]<=(100+(24*20)):#agregar valores predet
                            self.grid.leftclick(mousepos)
                if state[2]:#right click
                    if self.grid.started and self.state == "playing":
                        self.flags = self.grid.rightclick(mousepos)
                if self.state == "playing":
                    minesleft = self.grid.minesleft()
                    if minesleft == -1:
                        self.state = "lose"
                    elif minesleft == 0:
                        self.state = "win"
                    else:
                        self.state = "playing"
                    
    def show(self):
        #background
        self.screen.fill((169, 237, 43))
        #shows grid
        self.flags = self.grid.show()
        #shows auto flags and exit
        self.autobutton.show("Auto")
        self.flagsbutton.show(f"Flags: {self.flags}")
        self.exitbutton.show("Exit")
        pygame.display.flip()

    def run(self):
        while self.state == "playing":
            self.events()
            self.show()
        if self.state == "lose" or self.state == "win":
            print(self.state)
            pygame.time.delay(2000)
        return "start"

def main():#start playing quit win loose
    """mixer.pre_init(44100, 16, 2, 4096)
    mixer.init()"""
    pygame.event.set_allowed(pygame.QUIT)
    pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
    pygame.display.set_caption("Mine Sweeper + Auto")
    pygame.font.init()
    gamestate = "start"
    while gamestate != "quit":
        if gamestate == "start":
            start = Start(Screen,Font)
            gamestate = start.run()
        if gamestate == "playing":
            game = Game(Screen,Font,Difficulty,Multiplier)
            gamestate = game.run()
    pygame.quit()

if __name__ == "__main__":
    main()