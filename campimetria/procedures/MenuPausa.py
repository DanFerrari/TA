import pygame, os, sys


sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "constants"))
)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "pages")))
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "procedures"))
)
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "strategies"))
)

from ContagemRegressiva import ContagemRegressiva

class MenuPausa:

    def __init__(self):
      
        self.botao_selecionado = 0
        self.selecionando = True
        self.sair = False
        self.usuario = "operador"
        self.fixacao = "central"
        
    def update(self):      
        pygame.display.update()


    def draw(self):
        self.quadrado_menu()
        if self.botao_selecionado == 0:
            self.draw_button(540,180,"Continuar", (0,255,0),True)
            self.draw_button(540,-100,"Sair", (255,0,0),False)
        elif self.botao_selecionado == 1:
            self.draw_button(540,180,"Continuar", (0,255,0),False)
            self.draw_button(540,-100,"Sair", (255,0,0),True)
        if self.selecionando == False and self.sair == False:            
            teste = ContagemRegressiva.iniciar_contagem(5,fixacao=self.fixacao)
            if teste == False:
                self.sair = True
                self.selecionando = False
            
       

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_LEFT:
                    self.botao_selecionado = 0
                if event.key == pygame.K_RIGHT:
                    self.botao_selecionado = 1
                if event.key == pygame.K_e:
                    if self.botao_selecionado == 0:                        
                        self.selecionando = False         
                        self.sair = False               
                    if self.botao_selecionado == 1:                        
                        self.sair = True
                        self.selecionando = False
                    event.key = None
        


    def quadrado_menu(self):
        width = 800
        height = 600
        rect = pygame.Rect(960 - width / 2, 540 - height / 2, width, height)
        pygame.draw.rect(pygame.display.get_surface(), (220, 220, 220), rect, 0, 25)

        font = pygame.font.Font(None, 56)
        text = font.render(f"Exame parado pelo {self.usuario}", 1, (255, 0, 0))
        textpos = text.get_rect(centerx=960, centery=540 - 200)
        pygame.display.get_surface().blit(text, textpos)
        
        

        
        
    def draw_button(self,x,y,name,cor_fundo,selecionado):
        width = 540
        height = 50
        centerx =  x / 2
        centery =  y / 2
        rect = pygame.Rect(960 - centerx, 540 - centery, width, height)
        pygame.draw.rect(pygame.display.get_surface(), cor_fundo, rect, 0, 5)
        
        font = pygame.font.Font(None, 42)
        text = font.render(name, 1, (255, 255, 255))
        textpos = text.get_rect()
        textpos.center = rect.center
        pygame.display.get_surface().blit(text, textpos)
        
        if selecionado:
            pygame.draw.rect(pygame.display.get_surface(), (0, 0, 0), rect, 2, 5)
        else:
            pass

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.get_surface().fill((255, 255, 255))

    menu = MenuPausa()

    pygame.display.flip()
    while menu.testando:
        menu.handle_event()
        menu.draw()
        menu.update()
        
