import pygame, random
from pygame import mixer
from Button import Button

ScreenSize = (800,600)
Difficulty = 1
Multiplier = 25
#MaxScuares = (38,24)
#MineSize = (20,20)

class Scuare(pygame.sprite.Sprite):
    def __init__(self, image, rect, size):
        super().__init__()
        self.visible = False
        self.flagged = False
        self.type = "empty"
        self.image = image
        self.rect = rect
        self.size = size
        self.checked = False
        self.arround = []

class Grid():
    def __init__(self, screen, mines, cuantity, startpos, size):
        self.screen = screen
        self.mines = mines
        self.started = False
        self.cuantity = cuantity
        self.size = size
        self.startpos = startpos

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
        matrix = [[Scuare(self.scuare,(0,0),(0,0)) for y in range(cuantity[1])] for x in range(cuantity[0])]
        for x in range(cuantity[0]):
            for y in range(cuantity[1]):
                matrix[x][y] = Scuare(self.scuare,(startpos[0]+(x*size[0]),startpos[1]+(y*size[1])),size)
                self.grid.add(matrix[x][y])
        #connects all the scuares arround eachother
        for x in range(cuantity[0]):
            for y in range(cuantity[1]):
                left = False
                right = False
                up = False
                down = False
                if x != 0:
                    matrix[x][y].arround.append(matrix[x-1][y])
                    left = True
                if x != cuantity[0]-1:
                    matrix[x][y].arround.append(matrix[x+1][y])
                    right = True
                if y != 0:
                    matrix[x][y].arround.append(matrix[x][y-1])
                    up = True
                if y != cuantity[1]-1:
                    matrix[x][y].arround.append(matrix[x][y+1])
                    down = True
                if up:
                    if left:
                        matrix[x][y].arround.append(matrix[x-1][y-1])
                    if right:
                        matrix[x][y].arround.append(matrix[x+1][y-1])
                if down:
                    if left:
                        matrix[x][y].arround.append(matrix[x-1][y+1])
                    if right:
                        matrix[x][y].arround.append(matrix[x+1][y+1])

    def image(self, scuare):
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

    def leftclick(self, pos):
        if self.started:
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
        else:
            self.defineall(pos)

    def defineall(self,pos):
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
                            if (x < scuare.rect[0]-20 or scuare.rect[0]+20 < x) and (y < scuare.rect[1]-20 or scuare.rect[1]+20 < y):
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

    def search(self):
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
                        
    def rightclick(self, pos, flags):
        for scuare in self.grid:
            if pygame.Rect.collidepoint(pygame.Rect(scuare.rect[0],scuare.rect[1],scuare.size[0],scuare.size[1]),pos):
                if not scuare.visible:
                    if scuare.flagged:#flag to scuare
                        scuare.flagged = False
                        self.image(scuare)
                        flags += 1
                    elif flags>0 and not scuare.flagged:#scuare to flag
                        scuare.flagged = True
                        self.image(scuare)
                        flags -= 1
        return flags
    
    def revealmines(self):
        for scuare in self.grid:
            if scuare.type == "mine":
                scuare.visible = True
                scuare.image = self.mine
                self.image(scuare)
    
    def revealall(self):
        for scuare in self.grid:
            scuare.visible = True
            self.image(scuare)
    
    def winlose(self):
        gamestate = "playing"
        flaggedmines = 0
        for scuare in self.grid:
            if scuare.type == "explodedmine":
                gamestate = "lose"
            elif scuare.type == "mine":
                if scuare.flagged:
                    flaggedmines += 1
        if flaggedmines == self.mines:
            gamestate = "win"
        if gamestate != "playing":
            print(gamestate)
        return gamestate

    def show(self):
        #shows all scuares in the grid
        self.grid.draw(self.screen)
        #grid divisory lines
        for x in range(self.startpos[0],self.startpos[0]+760+1,self.size[0]):
            pygame.draw.line(self.screen,(0,100,0),(x,self.startpos[1]),(x,self.startpos[1]+480))
        for y in range(self.startpos[1],self.startpos[1]+480+1,self.size[1]):
            pygame.draw.line(self.screen,(0,100,0),(self.startpos[0],y),(self.startpos[0]+760,y))

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
                self.state = "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                state = pygame.mouse.get_pressed()
                mousepos = pygame.mouse.get_pos()
                if state[0]:#left click
                    if self.exitbutton.check_click(mousepos):
                        self.state = "start"
                    elif self.grid.started:
                        if self.flagsbutton.check_click(mousepos):
                            self.grid.revealall()
                        if self.autobutton.check_click(mousepos):
                            print("wip")
                    if self.state == "playing":
                        self.grid.leftclick(mousepos)
                if state[2]:#right click
                    if self.grid.started and self.state == "playing":
                        self.flags = self.grid.rightclick(mousepos, self.flags)
                if self.state == "playing":
                    self.state = self.grid.winlose()

    def show(self):
        #background
        self.screen.fill((169, 237, 43))
        #shows auto flags and exit
        self.autobutton.show("Auto")
        self.flagsbutton.show(f"Flags: {self.flags}")
        self.exitbutton.show("Exit")
        #shows grid
        self.grid.show()
        pygame.display.flip()

    def run(self):
        while self.state == "playing":
            self.events()
            self.show()
        if self.state == "loose":
            pygame.time.delay(3000)
        return self.state

def main():#start playing quit win loose
    pygame.init()
    mixer.pre_init(44100, 16, 2, 4096)
    mixer.init()
    pygame.event.set_allowed(pygame.QUIT)
    pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
    Screen = pygame.display.set_mode(ScreenSize)
    pygame.display.set_caption("Mine Sweeper + Auto")
    pygame.font.init()
    Font = pygame.font.SysFont('Comic Sans MS', 30)
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