import pygame,os,sys,importlib,subprocess






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

from dados import *  # Supondo que esses módulos estejam configurados


if 'testar_joystick' not in globals():
    testar_joystick = importlib.import_module("pages.testar_joystick")
    globals()['testar_joystick'] = testar_joystick
else:
    testar_joystick = globals()['testar_joystick']
    
if 'index' not in globals():
    index = importlib.import_module("pages.index")
    globals()['index'] = index
else:
    index = globals()['index']

    

class ConfigScreen:
    def __init__(self, game):
        self.game = game
        self.button_selected = 0  
        self.font = game.font_main
        self.cor_fundo = game.cor_fundo
        self.cor_botao = game.cor_botao
        self.cor_botao_hover = game.cor_botao_hover
        self.cor_texto = game.cor_texto 
        self.inicia_team = os.path.abspath(os.path.join(os.path.dirname(__file__),"scripts","inicia_teamviewer.sh"))




    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                   if self.button_selected > 0:
                       self.button_selected -= 1                       
                elif event.key == pygame.K_RIGHT:
                    if self.button_selected < 1:
                        self.button_selected += 1
                elif event.key == pygame.K_e:  # Confirma a seleção
                    if self.button_selected == 0:
                        self.game.change_screen(testar_joystick.TestarJoystick(self.game))
                    elif self.button_selected == 1:
                        subprocess.Popen([self.inicia_team])                    
                elif event.key == pygame.K_j:
                    self.game.change_screen(index.Index(self.game))
     

    def update(self):
        pass

    def draw(self, surface):
        
        surface.fill(self.cor_fundo)

        label_text = self.font.render("CONFIGURAÇÕES", True, self.cor_texto)
        surface.blit(label_text, (self.game.width // 2 - label_text.get_width() // 2, int(self.game.height * 0.2)))
        

        largura_botao = 502
        altura_botao = 129
        espacamento = altura_botao + 70
        
        self.draw_button(surface, "TESTAR JOYSTICK", self.game.width // 2 - largura_botao//2 , 623 - espacamento,largura_botao, altura_botao, self.button_selected == 0)
        self.draw_buttonTeam(surface, "TEAMVIEWER",  self.game.width  // 2 - largura_botao//2, 623 ,largura_botao, altura_botao, self.button_selected == 1)
        
       
    def draw_button(self, surface, text,x, y, width, height, selected,visible = True):
        if visible:
            cor_atual = self.cor_botao_hover if selected else self.cor_botao
            pygame.draw.rect(surface, cor_atual, (x, y, width, height), border_radius=10)
            texto_render = self.font.render(text, True, self.cor_fundo)
            text_rect = texto_render.get_rect(center=(x + width // 2, y + height // 2))       
            surface.blit(texto_render, text_rect)
    def draw_buttonTeam(self, surface, text,x, y, width, height, selected,visible = True):
        cor_selected = (28,81,237)
        cor_unselected = (5,16,47)
        cor_texto_unselected = (130, 135, 151)
        cor_texto_selected = (255, 255, 255)
        if visible:
            cor_atual = cor_selected if selected else cor_unselected
            pygame.draw.rect(surface, cor_atual, (x, y, width, height), border_radius=10)
            texto_render = self.font.render(text, True, cor_texto_selected if selected else cor_texto_unselected)
            text_rect = texto_render.get_rect(center=(x + width // 2, y + height // 2))       
            surface.blit(texto_render, text_rect)