import pygame, random, time, os, sys, math
from PIL import Image, ImageDraw
import numpy as np


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


class ResultadoFullthreshold:
    @staticmethod
    def desenhar_mapa():
        # Criar imagem branca
        img = Image.new("RGB", (960,540), "white")
        
        # Carregar bitmaps (Certifique-se de que os arquivos existem!)
        texturas = []
        for i in range(1, 11):
            caminho = f"campimetria/utils/images/bitmaps/{i}.bmp"
            if os.path.exists(caminho):
                texturas.append(Image.open(caminho))
            else:
                print(f"⚠️ Aviso: {caminho} não encontrado!")
                texturas.append(Image.new("RGB", (50, 50), (200, 200, 200)))  # Placeholder cinza

        # Tamanho de cada célula na grade
        cell_width = 84
        cell_height = 84

        # Criar objeto de desenho
        for ponto in DadosExame.matriz_pontos:                
                # Escolher a textura com base no atenuacao
                if ponto.atenuacao <= -90:
                    textura = None  # Branco (deixamos sem preenchimento)
                elif ponto.atenuacao <= 0:
                    textura = texturas[0]
                elif ponto.atenuacao < 6:
                    textura = texturas[1]
                elif ponto.atenuacao < 11:
                    textura = texturas[2]
                elif ponto.atenuacao < 16:
                    textura = texturas[3]
                elif ponto.atenuacao < 21:
                    textura = texturas[4]
                elif ponto.atenuacao < 26:
                    textura = texturas[5]
                elif ponto.atenuacao < 31:
                    textura = texturas[6]
                elif ponto.atenuacao < 36:
                    textura = texturas[7]
                elif ponto.atenuacao < 41:
                    textura = texturas[8]
                else:
                    textura = texturas[9]
                ponto.x = int(ponto.x * 960 / 1920)  # Reduzindo a coordenada X
                ponto.y = int(ponto.y * 540 / 1080)  # Reduzindo a coordenada Y
                # Coordenadas do retângulo onde a textura será desenhada
                x, y = int(ponto.x) - int(cell_width / 2), int(ponto.y) -  int(cell_height / 2)
                textura_quadrado = Image.new("RGB",(cell_width,cell_height))                
                for i in range(0, cell_width, textura.width):
                    for j in range(0, cell_height, textura.height):
                        textura_quadrado.paste(textura, (i, j))
                img.paste(textura_quadrado,(x,y))

        # Salvar e exibir imagem
        img.save("mapa_gerado.png")
        img.show()
            
    @staticmethod
    def exibir_resultados():
        pygame.font.init()

        fonte = pygame.font.Font(None, 24)

        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # Desenhar pontos e labels
        for ponto in DadosExame.matriz_pontos:
            ponto.cor = pygame.Color("blue")
            ponto.plotarPonto()
            label = fonte.render(f"{ponto.atenuacao}", True, (255, 255, 255))
            pygame.display.get_surface().blit(
                label, (ponto.x - 10, ponto.y + 10)
            )  # Adicionar texto abaixo
        pygame.display.get_surface().fill(Colors.BACKGROUND)
        
        pygame.display.flip()
