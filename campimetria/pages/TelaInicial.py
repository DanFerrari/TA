import pygame
import os
import sys
import numpy as np

# Adiciona os caminhos (suas pastas de constantes, páginas, procedimentos, etc.)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "constants")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "pages")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "procedures")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "strategies")))

from CAMPScreening import Screening
from dados import *
from CAMPFullThreshold import FullThreshold


class Game:
    def __init__(self):
        pygame.init()
        # Configura a tela em FULLSCREEN e captura dimensões
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width, self.height = self.screen.get_size()
        pygame.display.set_caption("Seleção de Estratégia")
        self.clock = pygame.time.Clock()
        self.running = True

        # Definições de cores e fontes
        self.cor_fundo = (20, 20, 20)
        self.cor_botao = (122, 122, 122)
        self.cor_botao_hover = (255, 255, 255)
        self.cor_texto = (255, 255, 255)
        self.font_main = pygame.font.Font(None, int(self.height * 0.07))
        
        # Estado inicial: tela de seleção de estratégia
        self.current_screen = StrategyScreen(self)

    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            # Delegamos o tratamento de eventos, atualização e desenho para a tela ativa
            self.current_screen.handle_events(events)
            self.current_screen.update()
            self.current_screen.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def change_screen(self, new_screen):
        self.current_screen = new_screen



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
                            exame = Screening()
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




if __name__ == "__main__":
    game = Game()
    game.run()
    
    caminho = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', "mainTA.py"))
    os.execvp("python", ["python", caminho])
