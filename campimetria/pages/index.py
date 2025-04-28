import pygame,os,sys,importlib

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


if 'strategy_screen' not in globals():
    strategy_screen = importlib.import_module("pages.strategy_screen")
    globals()['strategy_screen'] = strategy_screen
else:
    strategy_screen = globals()['strategy_screen']
    
if 'config_screen' not in globals():
    config_screen = importlib.import_module("pages.config_screen")
    globals()['config_screen'] = config_screen
else:
    config_screen = globals()['config_screen']
    

class Index:
    def __init__(self, game):
        self.game = game
        self.button_selected = 0  
        self.font = game.font_main
        self.cor_fundo = game.cor_fundo
        self.cor_botao = game.cor_botao
        self.cor_botao_hover = game.cor_botao_hover
        self.cor_texto = game.cor_texto 




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
                        self.game.change_screen(strategy_screen.StrategyScreen(self.game))
                    elif self.button_selected == 1:
                        self.game.change_screen(config_screen.ConfigScreen(self.game))
                    
                elif event.key == pygame.K_j:
                    self.game.running = False
     

    def update(self):
        pass

    def draw(self, surface):
        
        surface.fill(self.cor_fundo)

        label_text = self.font.render("BEM-VINDO", True, self.cor_texto)
        surface.blit(label_text, (self.game.width // 2 - label_text.get_width() // 2, int(self.game.height * 0.2)))
        

        largura_botao = 502
        altura_botao = 129
        espacamento = altura_botao + 70
        
        self.draw_button(surface, "NOVO EXAME", self.game.width // 2 - largura_botao//2 , 623 - espacamento,largura_botao, altura_botao, self.button_selected == 0)
        self.draw_button(surface, "CONFIGURAÇÕES",  self.game.width  // 2 - largura_botao//2, 623 ,largura_botao, altura_botao, self.button_selected == 1)
        
        
       
    def draw_button(self, surface, text,x, y, width, height, selected,visible = True):
        if visible:
            cor_atual = self.cor_botao_hover if selected else self.cor_botao
            pygame.draw.rect(surface, cor_atual, (x, y, width, height), border_radius=10)
            texto_render = self.font.render(text, True, self.cor_fundo)
            text_rect = texto_render.get_rect(center=(x + width // 2, y + height // 2))       
            surface.blit(texto_render, text_rect)