import pygame
import time
import math
import os
import sys
import OPi.GPIO as GPIO



PIN_ENTRADA = 'PD22'

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

from dados import *


class Ponto:
    def __init__(self, xg, yg, tamanhoPonto, cor):
        # self.resolucaoX = 0.246875
        # self.resolucaoY = 0.250
        self.limiar_encontrado = False
        self.atenuacao = 27
        self.primeira_visualizacao = True
        self.response_received = False
        self.numero_cruzamentos = 0
        self.ultima_atenuacao_vista = 0
        self.ultima_atenuacao_nao_vista = 0
        self.delta = 0
        self.status = ""
        self.tamanhoPonto = tamanhoPonto / 2
        self.xg = xg
        self.yg = yg
        self.resolucaoX = 0.25
        self.resolucaoY = 0.25
        self.resolucao_video = 0.2599
        self.x = 0
        self.y = 0
        self.menu_active = False
        self.tempo_resposta = 0.0
        self.clock = pygame.time.Clock()

        self.cor = cor
        self.distanciaPacienteTela = 200
        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h
        self.surface = pygame.display.get_surface()

        xrad = math.radians(self.xg)
        xmm = self.distanciaPacienteTela * math.tan(xrad)
        yrad = math.radians(self.yg)
        ymm = self.distanciaPacienteTela * math.tan(yrad)
        self.pontoPix = self.tamanhoPonto / self.resolucao_video
        # Converte para pixels

        self.x = xmm / self.resolucaoX
        self.y = ymm / self.resolucaoY
        self.x = self.x + (self.screen_width / 2)
        self.y = self.y + (self.screen_height / 2)
        
      

    @staticmethod
    def db_para_intensidade(db, db_min=40, db_max=0, i_min=150, i_max=255):
        """Converte dB para intensidade de cor (escala logarítmica)."""
        norm_db = (db - db_min) / (db_max - db_min)  # Normaliza dB entre 0 e 1

        intensity = i_min + (i_max - i_min) * ((10 ** (norm_db) - 1) / (10**1 - 1))

        if intensity > 255:
            intensity = 255
        elif intensity < i_min:
            intensity = i_min
        cor = int(round(intensity))
        return (cor, cor, cor)

    def plotarPonto(self):
        pygame.draw.circle(self.surface, self.cor, (self.x, self.y), self.pontoPix)

    @staticmethod
    def plotarPontoStatic(xg, yg, tamanhoPonto, cor):

        tamanhoPonto = tamanhoPonto / 2
        resolucaoX = 0.25
        resolucaoY = 0.25
        resolucao_video = 0.2599
        x = 0
        y = 0
        distanciaPacienteTela = 200
        screen_width = pygame.display.Info().current_w
        screen_height = pygame.display.Info().current_h
        surface = pygame.display.get_surface()
        xrad = math.radians(xg)
        xmm = distanciaPacienteTela * math.tan(xrad)
        yrad = math.radians(yg)
        ymm = distanciaPacienteTela * math.tan(yrad)
        pontoPix = tamanhoPonto / resolucao_video
        # Converte para pixels
        x = xmm / resolucaoX
        y = ymm / resolucaoY
        x = x + (screen_width / 2)
        y = y + (screen_height / 2)
        pygame.draw.circle(surface, cor, (x, y), pontoPix)

    def desenha_quadrado(self):
        tamanho = (self.tamanhoPonto, self.tamanhoPonto)
        quadrado = pygame.Rect(0, 0, *tamanho)
        quadrado.center = (self.x, self.y)
        pygame.draw.rect(pygame.display.get_surface(), self.cor, quadrado)

    def testaPonto(self, tempo_exposicao, tempo_resposta_paciente):
        self.trial_start_time = pygame.time.get_ticks()
        self.stimulus_end_time = self.trial_start_time + int(tempo_exposicao * 1000)
        self.response_deadline = self.trial_start_time + int(tempo_resposta_paciente * 1000)
        self.response_received = False
        self.tempo_resposta = None  # Ainda não foi registrado
        self.exibindo_ponto = True  # Flag para controlar a exibição
        self.aguardando_resposta = True  # Flag para indicar que ainda estamos no tempo de resposta

    def apagarPonto(self):
        pygame.draw.circle(
            self.surface, Colors.BACKGROUND, (self.x, self.y), self.pontoPix
        )
        pygame.display.update()

    def encontrarPonto(self, id):
        if id == self.id_point:
            return self.x, self.y
        return False
