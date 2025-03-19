import pygame
import random
import sys
import os

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

from Ponto import Ponto
from cordenadas_mcdir import cordenadas_mcdir
from cordenadas_mcesq import cordenadas_mcesq
from dados import *
from fixacao_central import FixacaoCentral

pygame.font.init()
fonte = pygame.font.Font(None, 36)
cor_texto = (255, 255, 255)
cor_alerta = Colors.BACKGROUND  # Vermelho
cor_botao = (100, 100, 100)
cor_botao_hover = (150, 150, 150)
cor_borda_selecao = (255, 255, 255)  # Branco (para o botão selecionado)
botao_selecionado = 0


def desenhar_botao(texto, x, y, largura, altura, selecionado):
    cor_atual = cor_botao_hover if selecionado else cor_botao
    pygame.draw.rect(
        pygame.display.get_surface(),
        cor_atual,
        (x, y, largura, altura),
        border_radius=5,
    )

    # Se for o botão selecionado, desenha uma borda ao redor
    if selecionado:
        pygame.draw.rect(
            pygame.display.get_surface(),
            cor_borda_selecao,
            (x - 2, y - 2, largura + 4, altura + 4),
            2,
            border_radius=5,
        )

    texto_renderizado = fonte.render(texto, True, cor_texto)
    texto_rect = texto_renderizado.get_rect(center=(x + largura // 2, y + altura // 2))
    pygame.display.get_surface().blit(texto_renderizado, texto_rect)
    pygame.display.update()
    return pygame.Rect(x, y, largura, altura)  # Retorna a área do botão


def mostrar_alerta(botao_reiniciar_estado, botao_continuar_estado):
    largura, altura = 800, 600
    x, y = (pygame.display.get_surface().get_width() - largura) // 2, (
        pygame.display.get_surface().get_height() - altura
    ) // 2  # Centro da tela

    pygame.draw.rect(
        pygame.display.get_surface(),
        cor_alerta,
        (x, y, largura, altura),
        border_radius=10,
    )

    # Renderiza o texto da notificação
    texto = fonte.render(
        "Mancha cega nao encontrada, deseja continuar mesmo assim ou deseja reiniciar",
        True,
        cor_texto,
    )
    texto_rect = texto.get_rect(center=(960, 405))
    pygame.display.get_surface().blit(texto, texto_rect)

    # Desenha os botões com a seleção destacada
    botao_reiniciar = desenhar_botao(
        "Reiniciar", 960 - 150, 455, 120, 40, botao_reiniciar_estado
    )
    botao_continuar = desenhar_botao(
        "Continuar", 960 + 150, 455, 120, 40, botao_continuar_estado
    )
    pygame.display.update()
    return (
        botao_reiniciar,
        botao_continuar,
    )  # Retorna os retângulos dos botões para referência


class TesteLimiarManchaCega:

    def __init__(self):
        self.encontrou_mancha = None
        self.resultado = None
        self.indice_atual = 0
        self.pontos_naorespondidos = []
        self.matriz_mancha_cega = (
            cordenadas_mcdir
            if DadosExame.olho == Constantes().olho_direito
            else cordenadas_mcesq
        )
        random.shuffle(self.matriz_mancha_cega)
        self.total_pontos = len(self.matriz_mancha_cega)
        self.delay_entre_pontos = 100
        self.reiniciar = False

    def verifica_mensagem(self):
        rodando = True
        mostrar_mensagem = True
        botao_reiniciar = None
        botao_continuar = None
        pygame.display.get_surface().fill(Colors.BACKGROUND)
        pygame.display.update()
        botao_selecionado = 0
        botao_reiniciar, botao_continuar = mostrar_alerta(True, False)
        while rodando:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    rodando = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        mostrar_alerta(
                            botao_reiniciar_estado=True, botao_continuar_estado=False
                        )
                        botao_selecionado = 0
                    elif event.key == pygame.K_RIGHT:
                        mostrar_alerta(
                            botao_reiniciar_estado=False, botao_continuar_estado=True
                        )
                        botao_selecionado = 1
                    elif event.key == pygame.K_e and mostrar_mensagem:
                        if botao_selecionado == 0:
                            rodando = False  # Fecha o jogo
                            pygame.display.get_surface().fill(Colors.BACKGROUND)
                            FixacaoCentral.plotar_fixacao_central()
                            self.reiniciar = True
                            return
                        elif botao_selecionado == 1:
                            rodando = False  # Fecha o jogo
                            pygame.display.get_surface().fill(Colors.BACKGROUND)
                            FixacaoCentral.plotar_fixacao_central()
                            self.reiniciar = False
                            return
                        mostrar_mensagem = False  # Fecha a notificação

    def calculo_centro_de_massa(self):
        somaMx = 0
        somaMy = 0
        icont = 0
        if len(self.pontos_naorespondidos) == 0:
            return False
        for i in range(len(self.pontos_naorespondidos)):
            for pontoNaoRespondido in self.pontos_naorespondidos:
                x, y = pontoNaoRespondido
                somaMx += x
                somaMy += y
                icont += 1
                print(f"SOMAM {somaMx} SOMAMY: {somaMy} ICONT:{icont}")

        xcm = round(somaMx / icont)
        ycm = round(somaMy / icont)
        print(f"XCM1: {xcm}, YCM1: {ycm}")
        return xcm, ycm

    def teste_mancha_cega(self):        

        if self.indice_atual < self.total_pontos:

            ponto = self.matriz_mancha_cega[self.indice_atual]
            x, y = ponto
            cor_ponto = Ponto.db_para_intensidade(0)
            teste = Ponto(x, y, 3, cor_ponto)
            teste.testaPonto(0.2, 2)
            if not teste.response_received:
                self.pontos_naorespondidos.append((teste.xg, teste.yg))
            self.indice_atual += 1

        if self.indice_atual == self.total_pontos:

            if len(self.pontos_naorespondidos) == 0:
                self.verifica_mensagem()
                if self.reiniciar:
                    self.indice_atual = 0
                    self.pontos_naorespondidos = []
                    self.reiniciar = False
                else:
                    self.encontrou_mancha = False
            else:
                self.resultado = self.calculo_centro_de_massa()
                self.encontrou_mancha = True
                DadosExame.posicao_mancha_cega = self.resultado
