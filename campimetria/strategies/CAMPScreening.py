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
from ManchaCega import TesteLimiarManchaCega
from cordenadas_30 import cordenadas_30
from ContagemRegressiva import ContagemRegressiva
from dados import *
from TelaResultadoScreening import ResultadoScreening
from fixacao_central import FixacaoCentral


class Screening:

    def __init__(self, game):
        self.game = game
        self.running = True
        self.pontos = self.criar_pontos()

    def media_de_tempo_de_resposta_paciente(self, tempos):
        tempo_medio = sum(tempos) / len(tempos)
        if tempo_medio < 1.0:
            tempo_medio = 1.0
        if tempo_medio > 2.0:
            tempo_medio = 2.0
        return tempo_medio

    def criar_pontos(self):
        return [Ponto(x, y, 3, (255, 255, 255), self.game) for x, y in cordenadas_30]

    def testa_mancha_cega(self, ponto):
        x, y = ponto
        teste = Ponto(x, y, 3, pygame.Color("red"))
        teste.testaPonto(0.2, 2.0)
        if teste.response_received:
            return 1.0
        else:
            return 0.0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:  # Volta para o menu ou sai
                    from strategy_screen import StrategyScreen
                    self.game.change_screen(StrategyScreen(self.game))

    def exame_screening(self, fixacao=False):
        
        random.shuffle(self.pontos)
        tempo_resposta = 2.0
        tempos = []
        # mancha_cega = ponto_mancha_cega
        mancha_cega = False

        teste_de_fixacao = fixacao
        pontos_vistos = []

        testemancha = 0
        testenegativo = 0
        testepositivo = 0

        for ponto in self.pontos:
            self.handle_events()
            ponto.cor = ponto.db_para_intensidade(DadosExame.atenuacao_screening)
            pygame.time.delay(100)  # Aguarda 100 ms para cada ponto
            ponto.testaPonto(0.2, tempo_resposta)
            DadosExame.total_de_pontos_testados += 1
            if ponto.response_received:
                pontos_vistos.append(ponto)
            ponto.limiar_encontrado = True
            tempos.append(ponto.tempo_resposta)
            testemancha += 1
            testenegativo += 1
            testepositivo += 1
            if testemancha == 10 and teste_de_fixacao:
                DadosExame.perda_de_fixacao += self.testa_mancha_cega(
                    DadosExame.posicao_mancha_cega
                )
                testemancha = 0
                DadosExame.total_testes_mancha += 1
                continue
            if testepositivo == 15 and len(pontos_vistos) > 1:
                pontos_vistos[-1].cor = Colors.BACKGROUND
                pontos_vistos[-1].plotarPonto()
                DadosExame.total_testes_falsos_positivo += 1
                if pontos_vistos[-1].response_received:
                    DadosExame.falso_positivo_respondidos += 1
                testepositivo = 0
            if testenegativo == 12 and len(pontos_vistos) > 1:
                pontos_vistos[-1].cor = Ponto.db_para_intensidade(25)
                pontos_vistos[-1].testaPonto(0.2, tempo_resposta)
                DadosExame.total_testes_falsos_negativo += 1
                if not pontos_vistos[-1].response_received:
                    DadosExame.falso_negativo_respondidos += 1
                testenegativo = 0

            if len(tempos) == 5:
                tempo_resposta = self.media_de_tempo_de_resposta_paciente(tempos)
                tempos = []

        DadosExame.matriz_pontos = pontos

    def iniciar_screening(self):
        running = True
        teste_fixacao = True

        while self.running:
            ContagemRegressiva.iniciar_contagem(5)
            pygame.display.get_surface().fill(Colors.BACKGROUND)
            pygame.display.update()
            FixacaoCentral.plotar_fixacao_central()
            # Captura eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Fecha ao clicar no botão de fechar
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_j:  # Fecha ao pressionar ESC
                        self.running = False

            pygame.time.delay(2000)
            mancha_cega = TesteLimiarManchaCega(self.game)
            mancha_cega.teste_mancha_cega(DadosExame.olho)

            if mancha_cega.resultado == True:
                continue
            elif mancha_cega.resultado == False:
                teste_fixacao = False
                pygame.time.delay(1500)
            start_time = pygame.time.get_ticks()

            self.exame_screening(
                 fixacao=teste_fixacao
            )
            end_time = pygame.time.get_ticks() - start_time
            DadosExame.duracao_do_exame = end_time
            ResultadoScreening.desenha_pontos()

            pygame.display.flip()
            self.running = False
        return
