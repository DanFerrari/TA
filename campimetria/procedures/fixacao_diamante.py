import pygame
from Ponto import Ponto

class FixacaoDiamante:
    @staticmethod
    def plotar_fixacao_diamante():
        Ponto(0, 6, 3, pygame.Color("yellow")).plotarPonto()
        Ponto(0, -6, 3, pygame.Color("yellow")).plotarPonto()
        Ponto(6, 0, 3, pygame.Color("yellow")).plotarPonto()
        Ponto(-6, 0, 3, pygame.Color("yellow")).plotarPonto()