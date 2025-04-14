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
    pygame.display.get_surface().fill((255, 255, 255))
    pygame.display.flip()
    tamanho_ponto = 3
    distancia = 100
    running = True
    from fixacao_central import FixacaoCentral
    FixacaoCentral.plotar_fixacao_central()

    from cordenadas_10 import cordenadas_10
    
    
    for x,y in cordenadas_10:
        Ponto(x,y,3,(0,0,0),distancia).plotarPonto()
    pygame.display.update()
    while running:

        for event in pygame.event.get():         
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    running = False
                if event.key == pygame.K_UP:
                    pygame.display.get_surface().fill((255, 255, 255))
                    distancia += 10
                    for x,y in cordenadas_10:
                        Ponto(x,y,3,(0,0,0),distancia).plotarPonto()
                    pygame.display.update()
                if event.key == pygame.K_DOWN:
                    pygame.display.get_surface().fill((255, 255, 255))
                    distancia -= 10
                    for x,y in cordenadas_10:
                        Ponto(x,y,3,(0,0,0),distancia).plotarPonto()
                    pygame.display.update()
                fonte = pygame.font.Font(None,30)
                texto = fonte.render(f"Distancia:{distancia}",True,(0,0,0))
                pygame.display.get_surface().blit(texto,(10,10))
                pygame.display.update()