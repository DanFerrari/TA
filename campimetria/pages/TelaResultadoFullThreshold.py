import pygame, random, time, os, sys,math


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
from Ponto import Ponto



class Mapa:
    def __init__(self, tamanho_imagem, matriz_interpolada):
        self.tamanho_imagem = tamanho_imagem
        self.matriz_interpolada = matriz_interpolada
        self.texturas = self.carregar_texturas()



def exibir_resultados(pontos):
    pygame.font.init()
    
   
    fonte = pygame.font.Font(None, 24)
    

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Desenhar pontos e labels
    for ponto in pontos:
        ponto.cor = pygame.Color("blue")
        ponto.plotarPonto()
        label = fonte.render(f"{ponto.atenuacao}", True, (255, 255, 255))
        pygame.display.get_surface().blit(
            label, (ponto.x - 10, ponto.y + 10)
        )  # Adicionar texto abaixo

    pygame.display.flip()
