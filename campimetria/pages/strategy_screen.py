import pygame,os,sys,json




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


class StrategyScreen:
    def __init__(self, game):
        self.game = game
        self.button_strategy_selected = 0  # 0 = Screening, 1 = FullThreshold
        self.button_program_selected = 0
        self.font = game.font_main
        self.cor_fundo = game.cor_fundo
        self.cor_botao = game.cor_botao
        self.cor_botao_hover = game.cor_botao_hover
        self.cor_texto = game.cor_texto
        self.strategy_selected = False
        
    



    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    from TelaCalibracao import Config
                    self.game.change_screen(Config(self.game))
                if event.key == pygame.K_LEFT:
                    if not self.strategy_selected:
                        self.button_strategy_selected = 0
                    if self.strategy_selected:
                        if self.button_program_selected >= 1:
                            self.button_program_selected -= 1                      
                    
                elif event.key == pygame.K_RIGHT:
                    if not self.strategy_selected:
                        self.button_strategy_selected = 1
                    if self.strategy_selected:
                        if self.button_program_selected < 2 and self.button_strategy_selected == 0:
                            self.button_program_selected += 1
                        elif self.button_program_selected < 1 and self.button_strategy_selected == 1:
                            self.button_program_selected += 1
                elif event.key == pygame.K_e:  # Confirma a seleção
                    if self.button_strategy_selected == 0:
                        DadosExame.exame_selecionado = Constantes.screening
                    elif self.button_strategy_selected == 1:
                        DadosExame.exame_selecionado = Constantes.fullthreshold
                    # Troca para a tela de seleção de olho e configuração  
                    if self.button_program_selected == 0:
                        DadosExame.programa_selecionado = Constantes.central30
                    elif self.button_program_selected == 1:
                        DadosExame.programa_selecionado = Constantes.central24
                    elif self.button_program_selected == 2 and self.button_strategy_selected == 0:
                        DadosExame.programa_selecionado = Constantes.central75
                    elif self.button_program_selected == 2 and self.button_strategy_selected == 1:
                        DadosExame.programa_selecionado = Constantes.central10                      
                        
                    if self.strategy_selected:                                                                                   
                        from select_eye_screen import SelectEyeScreen
                        self.game.change_screen(SelectEyeScreen(self.game))
                    self.strategy_selected = True
                elif event.key == pygame.K_j:
                    self.game.running = False
                elif event.key == pygame.K_r:
                    self.strategy_selected = False

    def update(self):
        pass

    def draw(self, surface):
        surface.fill(self.cor_fundo)
        # Renderiza o título centralizado
        label_text = self.font.render("SELECIONE UMA ESTRATEGIA", True, self.cor_texto)
        surface.blit(label_text, (self.game.width // 2 - label_text.get_width() // 2, int(self.game.height * 0.2)))
        
        # Define dimensões dos botões
        largura_botao = 502
        altura_botao = 129
        espacamento = 510
        exame_id = DadosExame.exame_id if DadosExame.exame_id != 0 else self.game.config["exame_id"]
        
        #label exame_id
        fonte_exame = pygame.font.Font(None, 48)
        label_exame_id_texto = fonte_exame.render(f"EXAME ID {exame_id}", True,self.cor_texto)
        label_exame_id_pos = label_exame_id_texto.get_rect(center=(960,800))
        label_exame_id_pos.y = 303
        surface.blit(label_exame_id_texto,label_exame_id_pos)
        
        # Desenha os botões
        self.draw_button(surface, "SCREENING", (self.game.width - largura_botao) // 2 - espacamento, 475,largura_botao, altura_botao, self.button_strategy_selected == 0)
        self.draw_button(surface, "FULLTHRESHOLD",  (self.game.width - largura_botao) // 2 + espacamento, 475,largura_botao, altura_botao, self.button_strategy_selected == 1)
        
        
        largura_botao_programa = 386
        altura_botao_programa = 100
        
        self.draw_button(surface, "30°", 1920//2 - largura_botao_programa // 2, 627,largura_botao_programa, altura_botao_programa, self.button_program_selected == 0,self.strategy_selected)
        self.draw_button(surface, "24°", 1920//2 - largura_botao_programa // 2, 762,largura_botao_programa, altura_botao_programa, self.button_program_selected == 1,self.strategy_selected)
        if self.button_strategy_selected == 0:
            self.draw_button(surface, "75°", 1920//2 - largura_botao_programa // 2, 897,largura_botao_programa, altura_botao_programa, self.button_program_selected == 2,self.strategy_selected)
        # elif self.button_strategy_selected == 1:
        #     self.draw_button(surface, "10°", 1920//2 - largura_botao_programa // 2, 897,largura_botao_programa, altura_botao_programa, self.button_program_selected == 2,self.strategy_selected)

    def draw_button(self, surface, text,x, y, width, height, selected,visible = True):
        if visible:
            cor_atual = self.cor_botao_hover if selected else self.cor_botao
            pygame.draw.rect(surface, cor_atual, (x, y, width, height), border_radius=10)
            texto_render = self.font.render(text, True, self.cor_fundo)
            text_rect = texto_render.get_rect(center=(x + width // 2, y + height // 2))       
            surface.blit(texto_render, text_rect)