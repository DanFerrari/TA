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
from MenuPausa import MenuPausa
from strategy_screen import StrategyScreen


class Screening:

    def __init__(self, game):
        self.game = game
        self.running = True
        self.pontos = self.criar_pontos()
        self.indice_atual = 0
        self.menu = MenuPausa()
        self.voltar_ao_menu_inicial = False

        self.estado = "inicio"
        self.teste_fixacao = True
        self.aviso_inicial_respondido: bool = None

        self.mancha_cega = TesteLimiarManchaCega()

    def media_de_tempo_de_resposta_paciente(self, tempos):
        tempo_medio = sum(tempos) / len(tempos)
        if tempo_medio < 1.0:
            tempo_medio = 1.0
        if tempo_medio > 2.0:
            tempo_medio = 2.0
        return tempo_medio

    def criar_pontos(self):
        return [Ponto(x, y, 3, (255, 255, 255)) for x, y in cordenadas_30]

    def testa_mancha_cega(self, ponto):
        x, y = ponto
        teste = Ponto(x, y, 3, pygame.Color("red"))
        teste.testaPonto(0.2, 2.0)
        if teste.response_received:
            return 1.0
        else:
            return 0.0

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

            ponto.cor = ponto.db_para_intensidade(DadosExame.atenuacao_screening)
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

            if ponto.menu_active:
                selecionando = True
                while selecionando:
                    self.menu.handle_event()
                    self.menu.draw()
                    self.menu.update()
                    if not self.menu.selecionando:
                        if not self.menu.sair:
                            self.menu = MenuPausa(self.game)
                        selecionando = False
            if self.menu.sair:
                self.running = False
                break
        DadosExame.matriz_pontos = self.pontos

    def iniciar_screening(self):

        self.exame_screening(fixacao=self.teste_fixacao)
        if self.menu.sair:
            return

        end_time = pygame.time.get_ticks() - start_time
        DadosExame.duracao_do_exame = end_time
        ResultadoScreening.desenha_pontos()
        pygame.display.flip()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:  # Volta para o menu ou sai
                    print("entrei no for")
                    while self.menu.selecionando:
                        self.menu.handle_event()
                        self.menu.draw()
                        self.menu.update()
                    self.menu.selecionando = True
                    if self.menu.sair:
                        self.voltar_ao_menu_inicial = True
                        return

    def update(self):
        pygame.display.update()
        if self.voltar_ao_menu_inicial:
            self.game.change_screen(StrategyScreen(self.game))

    def draw(self, surface):
        if self.estado == "inicio":
            self.aviso_inicial_respondido = ContagemRegressiva.iniciar_contagem(5)
            if self.aviso_inicial_respondido == False:
                self.voltar_ao_menu_inicial = True
                
            else:
                self.estado = "encontrando_mancha"
                

        elif self.estado == "encontrando_mancha":
            self.mancha_cega.teste_mancha_cega()
            if self.mancha_cega.encontrou_mancha != None:
                if self.mancha_cega.encontrou_mancha:
                    self.teste_fixacao = True
                elif self.mancha_cega.encontrou_mancha == False:
                    self.teste_fixacao = False
                self.estado = "exame"
                

            

        elif self.estado == "exame":
            print("Iniciando exame")
            
