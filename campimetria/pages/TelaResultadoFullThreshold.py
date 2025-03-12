import pygame, random, time, os, sys, math
from PIL import Image, ImageDraw
import numpy as np
from scipy.spatial import KDTree


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
    def calcular_tamanho_celula(ponto, pontos):
        """ Determina o tamanho da célula baseado na distribuição dos pontos, evitando lacunas e garantindo cobertura uniforme """
        if len(pontos) < 2:
            return 20  # Valor padrão mínimo caso haja poucos pontos

        tree = KDTree([(p.x, p.y) for p in pontos if p != ponto])
        dists, indices = tree.query((ponto.x, ponto.y), k=min(5, len(pontos)))

        if len(indices) == 0:
            return 20  # Se não há vizinhos, usa o mínimo padrão

        dist_mediana = np.median(dists)
        dist_max = np.max(dists)
        largura = max(10, int((dist_mediana + dist_max) / 2))
        altura = largura
        
        x = int(ponto.x - largura // 2)
        y = int(ponto.y - altura // 2)
        return x, y, largura, altura

    @staticmethod
    def calcular_atenuacao_interpolada(x, y, kdtree, pontos):
        """ Interpola a atenuação dentro da célula suavizando a transição para as vizinhas """
        dists, indices = kdtree.query((x, y), k=min(5, len(pontos)))
        
        if len(indices) == 0:
            return 0
        
        pesos = np.exp(-np.array(dists) / 10)
        pesos /= pesos.sum()

        atenuacao_interpolada = sum(pesos[i] * pontos[indices[i]].atenuacao for i in range(len(indices)))
        return atenuacao_interpolada

    @staticmethod
    def desenhar_mapa():
        """ Desenha o mapa ajustando o espaçamento das células para eliminar lacunas e melhorar o alinhamento """
        pygame.init()
      

        centro_x, centro_y = 960 // 2, 540 // 2
        raio = min(centro_x, centro_y) - 10
        
        texturas = []
        for i in range(1, 11):
            caminho = f"campimetria/utils/images/bitmaps/{i}.bmp"
            if os.path.exists(caminho):
                texturas.append((20 * i, 20 * i, 20 * i))
            else:
                texturas.append((200, 200, 200))

        for ponto in DadosExame.matriz_pontos:
            if ponto.xg == 21 and ponto.yg == 3:
                ponto.atenuacao = 0
            if ponto.xg == 21 and ponto.yg == -3:
                ponto.atenuacao = 24
            ponto.x = int(ponto.x * 960 / 1920)  
            ponto.y = int(ponto.y * 540 / 1080)  
        
        kdtree = KDTree([(p.x, p.y) for p in DadosExame.matriz_pontos])
        atenuacoes_cache = {}

        for x in range(960):
            for y in range(540):
                if (x - centro_x) ** 2 + (y - centro_y) ** 2 <= raio ** 2:
                    if (x, y) in atenuacoes_cache:
                        atenuacao_interpolada = atenuacoes_cache[(x, y)]
                    else:
                        atenuacao_interpolada = ResultadoFullthreshold.calcular_atenuacao_interpolada(x, y, kdtree, DadosExame.matriz_pontos)
                        atenuacoes_cache[(x, y)] = atenuacao_interpolada
                    
                    if atenuacao_interpolada <= 0:
                        cor = texturas[0]
                    elif atenuacao_interpolada < 6:
                        cor = texturas[1]
                    elif atenuacao_interpolada < 11:
                        cor = texturas[2]
                    elif atenuacao_interpolada < 16:
                        cor = texturas[3]
                    elif atenuacao_interpolada < 21:
                        cor = texturas[4]
                    elif atenuacao_interpolada < 26:
                        cor = texturas[5]
                    elif atenuacao_interpolada < 31:
                        cor = texturas[6]
                    elif atenuacao_interpolada < 36:
                        cor = texturas[7]
                    elif atenuacao_interpolada < 41:
                        cor = texturas[8]
                    else:
                        cor = texturas[9]
                    
                    pygame.display.get_surface().set_at((x, y), cor)
        
        pygame.draw.line(pygame.display.get_surface(), (0, 0, 0), (centro_x, centro_y - raio), (centro_x, centro_y + raio), 2)
        pygame.draw.line(pygame.display.get_surface(), (0, 0, 0), (centro_x - raio, centro_y), (centro_x + raio, centro_y), 2)
        
        pygame.display.flip()



            
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
