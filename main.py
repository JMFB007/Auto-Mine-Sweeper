import pygame, random
from pygame import mixer

ScreenSize = (800,600)
Difficulty = 5#multiplies by 15
#MaxScuares = (38,24)
#MineSize = (20,20)

class Button():
    def __init__(self,screen,bgcolor,txt,txtcolor,font,posx,posy,width,height):
        self.screen = screen
        self.bgcolor = bgcolor
        self.txt = txt
        self.txtcolor = txtcolor
        self.font = font
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.button = pygame.draw.rect(self.screen,self.bgcolor,pygame.Rect(self.posx,self.posy,self.width,self.height))
    
    def check_click(self,pos):
        if pygame.Rect.collidepoint(self.button,pos):
            return True
        return False

    def show(self, txt):
        pygame.draw.rect(self.screen,self.bgcolor,pygame.Rect(self.posx,self.posy,self.width,self.height))
        text = self.font.render(txt,True, self.txtcolor)
        text_rect = text.get_rect(center=(self.posx+self.width/2,self.posy+self.height/2))
        self.screen.blit(text, text_rect)

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
        self.grid = pygame.sprite.Group()
        for x in range(startpos[0],startpos[0]+cuantity[0]*size[0],size[0]):
            for y in range(startpos[1],startpos[1]+cuantity[1]*size[1],size[1]):
                self.grid.add(Scuare(self.scuare,(x,y),size))

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
        self.search()

    def search(self):
        for scuare in self.grid:
            scuare.checked = False
        looking = True
        while looking:
            looking = False
            #ciclo de busqueda por cuadro
            for scuare in self.grid:
                if scuare.type == "empty" and scuare.visible and not scuare.checked:
                    scuare.checked = True
                    #cuadros que se encuentran alrededor del original
                    for subscuare in self.grid:
                        rect = pygame.Rect(subscuare.rect[0],subscuare.rect[1],subscuare.size[0],subscuare.size[1])
                        area = [(scuare.rect[0]-20,scuare.rect[1]+20),(scuare.rect[0],scuare.rect[1]+20),(scuare.rect[0]+20,scuare.rect[1]+20),(scuare.rect[0]-20,scuare.rect[1]),(scuare.rect[0]+20,scuare.rect[1]),(scuare.rect[0]-20,scuare.rect[1]-20),(scuare.rect[0],scuare.rect[1]-20),(scuare.rect[0]+20,scuare.rect[1]-20)]
                        for a in area:
                            if pygame.Rect.collidepoint(rect,a):
                                    looking = True
                                    subscuare.visible = True
                        self.image(subscuare)
    
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
        gamestate = 1
        flaggedmines = 0
        for scuare in self.grid:
            if scuare.type == "explodedmine":
                gamestate = "lose"
                print(gamestate)
            elif scuare.type == "mine":
                if scuare.flagged:
                    flaggedmines += 1
        if flaggedmines == self.mines:
            gamestate = "win"
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

class Game():
    def __init__(self, screen, font, difficulty):
        self.screen = screen
        self.font = font
        self.state = 1
        self.mines = difficulty*15
        self.flags = difficulty*15
        self.autobutton = Button(screen,(63, 97, 1),"Auto",(0,0,0),self.font,20,20,240,60)
        self.flagsbutton = Button(screen,(63, 97, 1),f"Flags: {self.flags}",(168, 27, 27),self.font,280,20,240,60)
        self.exitbutton = Button(screen,(63, 97, 1),"Exit",(0,0,0),self.font,540,20,240,60)
        self.grid = Grid(screen,self.mines,(38,24),(20,100),(20,20))
  
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = 2
            if event.type == pygame.MOUSEBUTTONDOWN:
                state = pygame.mouse.get_pressed()
                mousepos = pygame.mouse.get_pos()
                if state[0]:#left click
                    if self.exitbutton.check_click(mousepos):
                        self.state = 2
                    elif self.flagsbutton.check_click(mousepos):#show all
                        if self.grid.started:
                            self.grid.revealall()
                    elif self.autobutton.check_click(mousepos):#automate
                        if self.grid.started:
                            print("wip")
                            #self.grid.revealall()
                    else:
                        self.grid.leftclick(mousepos)
                if state[2]:#right click
                    if self.grid.started:
                        self.flags = self.grid.rightclick(mousepos, self.flags)
                if self.state != 2:
                    self.state = self.grid.winlose()
                    if self.state != 1:
                        if self.state == "win":
                            self.state = 2
                        if self.state == "lose":
                            self.state = 2

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

    def run(self):#1 = playing 2 = leave
        while self.state == 1:
            self.events()
            self.show()
        return self.state

def main():
    pygame.init()
    mixer.pre_init(44100, 16, 2, 4096)
    mixer.init()
    pygame.event.set_allowed(pygame.QUIT)
    pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
    Screen = pygame.display.set_mode(ScreenSize)
    pygame.display.set_caption("Mine Sweeper + Auto")
    pygame.font.init()
    Font = pygame.font.SysFont('Comic Sans MS', 30)
    game = Game(Screen,Font,Difficulty)#starts the game loop, 1=main menu, 2=game, 3=restart or exit
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()