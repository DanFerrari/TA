import pygame,os,sys




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
        self.botao_selecionado = 0  # 0 = Screening, 1 = FullThreshold
        self.font = game.font_main
        self.cor_fundo = game.cor_fundo
        self.cor_botao = game.cor_botao
        self.cor_botao_hover = game.cor_botao_hover
        self.cor_texto = game.cor_texto

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.botao_selecionado = 0
                elif event.key == pygame.K_RIGHT:
                    self.botao_selecionado = 1
                elif event.key == pygame.K_e:  # Confirma a seleção
                    if self.botao_selecionado == 0:
                        DadosExame.exame_selecionado = Constantes.screening
                    elif self.botao_selecionado == 1:
                        DadosExame.exame_selecionado = Constantes.fullthreshold
                    # Troca para a tela de seleção de olho e configuração                    
                    from select_eye_screen import SelectEyeScreen
                    self.game.change_screen(SelectEyeScreen(self.game))
                elif event.key == pygame.K_j:
                    self.game.running = False

    def update(self):
        pass

    def draw(self, surface):
        surface.fill(self.cor_fundo)
        # Renderiza o título centralizado
        label_text = self.font.render("Selecione a estratégia", True, self.cor_texto)
        surface.blit(label_text, (self.game.width // 2 - label_text.get_width() // 2, int(self.game.height * 0.2)))
        
        # Define dimensões dos botões
        largura_botao = int(self.game.width * 0.3)
        altura_botao = int(self.game.height * 0.1)
        espacamento = int(self.game.height * 0.15)
        
        # Desenha os botões
        self.draw_button(surface, "Screening", int(self.game.height * 0.4), largura_botao, altura_botao, self.botao_selecionado == 0)
        self.draw_button(surface, "FullThreshold", int(self.game.height * 0.4 + espacamento), largura_botao, altura_botao, self.botao_selecionado == 1)

    def draw_button(self, surface, text, y, width, height, selected):
        x = (self.game.width - width) // 2
        cor_atual = self.cor_botao_hover if selected else self.cor_botao
        pygame.draw.rect(surface, cor_atual, (x, y, width, height), border_radius=10)
        texto_render = self.font.render(text, True, self.cor_fundo)
        text_rect = texto_render.get_rect(center=(x + width // 2, y + height // 2))
        surface.blit(texto_render, text_rect)