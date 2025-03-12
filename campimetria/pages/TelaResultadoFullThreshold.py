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

        dist_mediana = np.median(dists)  # Usa a mediana para evitar distâncias muito pequenas ou grandes
        dist_max = np.max(dists)  # Distância máxima para verificar lacunas
        largura = max(10, int((dist_mediana + dist_max) / 2))  # Média entre mediana e máximo para suavizar
        altura = largura
        
        x = int(ponto.x - largura // 2)
        y = int(ponto.y - altura // 2)
        return x, y, largura, altura


    @staticmethod
    def calcular_atenuacao_interpolada(x, y, kdtree, pontos):
        """ Interpola a atenuação dentro da célula suavizando a transição para as vizinhas """
        dists, indices = kdtree.query((x, y), k=min(5, len(pontos)))  # Buscar até 5 vizinhos
        
        if len(indices) == 0:
            return 0  # Caso não haja vizinhos, retorna atenuação neutra
        
        pesos = np.exp(-np.array(dists) / 5)
        
        # Reduz a influência para suavizar a transição
        pesos /= pesos.sum()  # Normalizar pesos

        atenuacao_interpolada = sum(pesos[i] * pontos[indices[i]].atenuacao for i in range(len(indices)))
        return atenuacao_interpolada

    @staticmethod
    def desenhar_mapa():
        """ Desenha o mapa ajustando o espaçamento das células para eliminar lacunas e melhorar o alinhamento """
        img = Image.new("RGB", (960, 540), "white")
        texturas = []
        
        for i in range(1, 11):
            caminho = f"campimetria/utils/images/bitmaps/{i}.bmp"
            if os.path.exists(caminho):
                texturas.append(Image.new("RGB", (50, 50), (20 * i, 20 * i, 20 * i)))
            else:
                texturas.append(Image.new("RGB", (50, 50), (200, 200, 200)))

        for ponto in DadosExame.matriz_pontos:
            ponto.x = int(ponto.x * 960 / 1920)  
            ponto.y = int(ponto.y * 540 / 1080)  
        
        kdtree = KDTree([(p.x, p.y) for p in DadosExame.matriz_pontos])  # Criar KDTree uma única vez
        atenuacoes_cache = {}  # Cache para armazenar atenuações já calculadas

        for ponto in DadosExame.matriz_pontos:
            if ponto.atenuacao <= -90:
                continue  
            
            x, y, cell_width, cell_height = ResultadoFullthreshold.calcular_tamanho_celula(ponto, DadosExame.matriz_pontos)
            textura_quadrado = Image.new("RGB", (cell_width, cell_height))
            
            for i in range(cell_width):  # Aplicação uniforme da textura
                for j in range(cell_height):
                    posicao = (x + i, y + j)
                    if posicao in atenuacoes_cache:
                        atenuacao_interpolada = atenuacoes_cache[posicao]
                    else:
                        atenuacao_interpolada = ResultadoFullthreshold.calcular_atenuacao_interpolada(x + i, y + j, kdtree, DadosExame.matriz_pontos)
                        atenuacoes_cache[posicao] = atenuacao_interpolada
                    
                    if atenuacao_interpolada <= 0:
                        textura = texturas[0]
                    elif atenuacao_interpolada < 6:
                        textura = texturas[1]
                    elif atenuacao_interpolada < 11:
                        textura = texturas[2]
                    elif atenuacao_interpolada < 16:
                        textura = texturas[3]
                    elif atenuacao_interpolada < 21:
                        textura = texturas[4]
                    elif atenuacao_interpolada < 26:
                        textura = texturas[5]
                    elif atenuacao_interpolada < 31:
                        textura = texturas[6]
                    elif atenuacao_interpolada < 36:
                        textura = texturas[7]
                    elif atenuacao_interpolada < 41:
                        textura = texturas[8]
                    else:
                        textura = texturas[9]
                    
                    textura_quadrado.paste(textura, (i, j))  # Aplicação correta
            
            img.paste(textura_quadrado, (x, y))

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
