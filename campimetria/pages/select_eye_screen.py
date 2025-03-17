import pygame
from dados import DadosExame, Constantes
from CAMPScreening import Screening
from CAMPFullThreshold import FullThreshold
from strategy_screen import StrategyScreen



class SelectEyeScreen:
    def __init__(self, game):
        self.game = game
        self.width, self.height = game.width, game.height

        # Fontes utilizadas na tela
        self.fonte_titulo = pygame.font.Font(None, int(self.height * 0.08))
        self.fonte_opcoes = pygame.font.Font(None, int(self.height * 0.06))
        self.fonte_numero = pygame.font.Font(None, int(self.height * 0.07))
        self.fonte_botao = pygame.font.Font(None, int(self.height * 0.06))
        
        # Cores e configurações visuais
        self.cor_texto = (255, 255, 255)
        self.cor_texto_fade = (100, 100, 100)
        self.cor_caixa = (50, 50, 50)
        self.cor_caixa_selecao = (70, 70, 70)
        self.cor_botao = (0, 200, 0)
        self.cor_botao_hover = (0, 255, 0)
        self.cor_font_olho = (255, 255, 255)
        self.cor_fundo = game.cor_fundo

        # Opções de olho
        self.opcoes = ["Olho Esquerdo", "Olho Direito"]
        self.opcao_selecionada = 0

        # Controle de qual item está selecionado:
        # Pode ser "opcoes", "numero" ou "botao"
        self.selecao_atual = "opcoes"
        
        # Caixa numérica (para exame screening)
        self.numero = 25
        self.NUMERO_MIN = 0
        self.NUMERO_MAX = 40

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:  # Volta para o menu ou sai
                    self.game.change_screen(StrategyScreen(self.game))
                elif event.key == pygame.K_x:
                    if self.selecao_atual == "numero":
                        self.selecao_atual = "opcoes"
                    elif self.selecao_atual == "botao":
                        if DadosExame.exame_selecionado == Constantes.screening:
                            self.selecao_atual = "numero"
                        else:
                            self.selecao_atual = "opcoes"
                elif event.key == pygame.K_e:
                    if self.selecao_atual == "opcoes":
                        if DadosExame.exame_selecionado == Constantes.screening:
                            self.selecao_atual = "numero"
                        else:
                            self.selecao_atual = "botao"
                    elif self.selecao_atual == "numero":
                        self.selecao_atual = "botao"
                    elif self.selecao_atual == "botao":
                        # Ao confirmar no botão, inicia o exame conforme a estratégia selecionada
                        if DadosExame.exame_selecionado == Constantes.screening:
                            DadosExame.atenuacao_screening = self.numero
                            exame = Screening(self.game)
                            exame.iniciar_screening()
                            # Após o exame, retorna ao menu
                            self.game.change_screen(StrategyScreen(self.game))
                        elif DadosExame.exame_selecionado == Constantes.fullthreshold:
                            exame = FullThreshold()
                            exame.main()
                            self.game.change_screen(StrategyScreen(self.game))
                        else:
                            print("Exame não implementado!")
                elif self.selecao_atual == "opcoes":
                    if event.key == pygame.K_LEFT:
                        self.opcao_selecionada = 0
                        DadosExame.olho = Constantes.olho_esquerdo
                    elif event.key == pygame.K_RIGHT:
                        self.opcao_selecionada = 1
                        DadosExame.olho = Constantes.olho_direito
                elif self.selecao_atual == "numero":
                    if event.key == pygame.K_LEFT and self.numero > self.NUMERO_MIN:
                        self.numero -= 1
                    elif event.key == pygame.K_RIGHT and self.numero < self.NUMERO_MAX:
                        self.numero += 1

    def update(self):
        # Atualizações de animações ou lógicas adicionais podem ser inseridas aqui
        pass

    def draw(self, surface):
        surface.fill(self.cor_fundo)
        # Garante um valor default para teste (pode ser removido se necessário)
        DadosExame.olho = Constantes.olho_direito
        
        # Renderiza as opções de olho no topo
        pos_y_opcoes = self.height * 0.2
        if self.selecao_atual == "opcoes":
            self.cor_font_olho = (255, 255, 255)
        else:
            self.cor_font_olho = (0, 255, 0)
        
        texto_esquerda = self.fonte_opcoes.render(
            self.opcoes[0],
            True,
            self.cor_font_olho if self.opcao_selecionada == 0 else self.cor_texto_fade
        )
        texto_direita = self.fonte_opcoes.render(
            self.opcoes[1],
            True,
            self.cor_font_olho if self.opcao_selecionada == 1 else self.cor_texto_fade
        )
        surface.blit(texto_esquerda, (self.width * 0.25 - texto_esquerda.get_width() // 2, pos_y_opcoes))
        surface.blit(texto_direita, (self.width * 0.75 - texto_direita.get_width() // 2, pos_y_opcoes))
        
        # Renderiza a caixa numérica (se o exame selecionado for Screening)
        if DadosExame.exame_selecionado == Constantes.screening:
            cor_caixa_atual = self.cor_caixa_selecao if self.selecao_atual == "numero" else self.cor_caixa
            pos_y_numero = self.height * 0.4
            rect_box = pygame.Rect(self.width // 2 - 100, pos_y_numero, 200, 100)
            pygame.draw.rect(surface, cor_caixa_atual, rect_box, border_radius=10)
            texto_numero = self.fonte_numero.render(str(self.numero), True, self.cor_texto)
            surface.blit(texto_numero, (self.width // 2 - texto_numero.get_width() // 2, pos_y_numero + 25))
            if self.selecao_atual == "numero":
                pygame.draw.rect(surface, (255, 255, 255), rect_box, 5, border_radius=10)
        
        # Renderiza o botão "Iniciar Exame"
        pos_y_botao = self.height * 0.6
        cor_botao_atual = self.cor_botao_hover if self.selecao_atual == "botao" else self.cor_botao
        rect_botao = pygame.Rect(self.width // 2 - 150, pos_y_botao, 300, 80)
        pygame.draw.rect(surface, cor_botao_atual, rect_botao, border_radius=10)
        texto_botao = self.fonte_botao.render("Iniciar Exame", True, self.cor_fundo)
        surface.blit(texto_botao, (self.width // 2 - texto_botao.get_width() // 2, pos_y_botao + 20))
        if self.selecao_atual == "botao":
            pygame.draw.rect(surface, (255, 255, 255), rect_botao, 5, border_radius=10)
    
    def draw_button(self, surface, text, y, width, height, selected):
        x = (self.game.width - width) // 2
        cor_atual = self.cor_botao_hover if selected else self.cor_botao
        pygame.draw.rect(surface, cor_atual, (x, y, width, height), border_radius=10)
        texto_render = self.font.render(text, True, self.cor_fundo)
        text_rect = texto_render.get_rect(center=(x + width // 2, y + height // 2))
        surface.blit(texto_render, text_rect)