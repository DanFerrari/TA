import pygame, random, time, os, sys,math
from PIL import Image, ImageDraw

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

    def carregar_texturas(self):
        """Carrega as texturas das imagens e retorna uma lista de Surfaces do Pygame"""
        texturas = []
        caminho_base = "utils/images/bitmaps"
        
        for i in range(1, 11):
            caminho_imagem = os.path.join(caminho_base, f"{i}.bmp")
            if os.path.exists(caminho_imagem):
                textura = pygame.image.load(caminho_imagem)
                textura = pygame.transform.scale(textura, (20, 20))  # Ajuste do tamanho
            else:
                textura = pygame.Surface((20, 20))  # Criar um espaço vazio se a imagem não existir
                textura.fill((255, 255, 255))  # Branco
            texturas.append(textura)
        return texturas

  



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
