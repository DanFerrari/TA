import pygame
import time
import math
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






class Screening:
    
    
    def __init__(self):
        pass
    def media_de_tempo_de_resposta_paciente(self,tempos):
        tempo_medio = sum(tempos) / len(tempos)
        if tempo_medio < 1.0:
            tempo_medio = 1.0
        if tempo_medio > 2.0:
            tempo_medio = 2.0
        return tempo_medio


    def criar_pontos(self):
        return [Ponto(x, y, 3, (255, 255, 255)) for x, y in cordenadas_30]


    def testa_mancha_cega(self,ponto):
        x, y = ponto
        teste = Ponto(x, y, 3, pygame.Color("red"))
        teste.testaPonto(0.2, 2.0)
        if teste.response_received:
            return 1.0
        else:
            return 0.0


    def exame_screening(self,ponto_mancha_cega=0, fixacao=False):
        pontos = self.criar_pontos()
        random.shuffle(pontos)
        tempo_resposta = 2.0
        tempos = []
        mancha_cega = ponto_mancha_cega
        teste_de_fixacao = fixacao
        perda_de_fixacao = 0.0
        testemancha = 0
        for ponto in pontos:
            ponto.cor = ponto.db_para_intensidade(DadosExame.atenuacao_screening)
            pygame.time.delay(100)  # Aguarda 100 ms para cada ponto
            ponto.testaPonto(0.2, tempo_resposta)
            ponto.limiar_encontrado = True
            tempos.append(ponto.tempo_resposta)
            testemancha += 1
            if testemancha == 10 and teste_de_fixacao:

                perda_de_fixacao += self.testa_mancha_cega(mancha_cega)
                testemancha = 0
                pygame.time.delay(1000)  # Aguarda 1 segundo para reiniciar o loop
                continue

            if len(tempos) == 5:
                tempo_resposta = self.media_de_tempo_de_resposta_paciente(tempos)
                tempos = []

        for ponto in pontos:
            if ponto.response_received:
                ponto.cor = pygame.Color("green")
                ponto.plotarPonto()
            elif not ponto.response_received:
                ponto.cor = pygame.Color("red")
                ponto.plotarPonto()
            teste_perda = perda_de_fixacao / 7.0
            if teste_perda >= 0:
                print(f"Perda de fixacao: {(teste_perda * 100) }%")

       

    def iniciar_screening(self):
        running = True
        sair = True
        teste_fixacao = True
        

        while running or sair:

            ContagemRegressiva.iniciar_contagem(5)
            pygame.display.get_surface().fill((120, 120, 120))
            pygame.display.update()
            Ponto(0, 0, 3, pygame.Color("yellow")).plotarPonto()
            # Captura eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Fecha ao clicar no botão de fechar
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Fecha ao pressionar ESC
                        running = False

            pygame.time.delay(2000)
            mancha_cega = TesteLimiarManchaCega().teste_mancha_cega(DadosExame.olho)
            if mancha_cega == True:
                ContagemRegressiva().iniciar_contagem(5)
                continue
            elif mancha_cega == False:
                teste_fixacao = False

            self.exame_screening(ponto_mancha_cega= DadosExame.posicao_mancha_cega, fixacao=teste_fixacao)

            pygame.time.delay(30000)
            pygame.display.flip()
            running = False




  

