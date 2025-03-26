import pygame
import os
import sys

import time
import subprocess





# Adiciona os caminhos (suas pastas de constantes, páginas, procedimentos, etc.)
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


from constants.dados import *
from pages.strategy_screen import StrategyScreen
from procedures.Ponto import Ponto

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    screen.fill((255, 255, 255))
    pygame.display.update()
    tamanho_ponto = 3
    distancia = 200
    running = True
    while running:

        for event in pygame.event.get():         
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    running = False
                if event.key == pygame.K_e:
                    screen.fill((0, 0, 0))
                    pygame.display.update()
                    ponto = Ponto(0, 0, tamanho_ponto, (240, 240, 174), distancia)  
                    ponto.plotarPonto()              
                    pygame.display.update()
        
