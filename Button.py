import pygame

class Button():
    def __init__(self,screen,bgcolor,txtcolor,font,posx,posy,width,height):
        self.screen = screen
        self.bgcolor = bgcolor
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