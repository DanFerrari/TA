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
from cordenadas_30 import cordenadas_30


class ResultadoFullthreshold:
    matriz_interpolada = []
    LARGURA, ALTURA = 1920, 1080
    nova_largura, nova_altura = 960, 540       

    pontos_ajustados = DadosExame.matriz_pontos
    for ponto in pontos_ajustados:
        ponto.x = int(ponto.x * nova_largura / LARGURA)
        ponto.y = int(ponto.y * nova_altura / ALTURA)
        ponto.cor = (0, 0, 0)
    
    @staticmethod
    def gerar_matriz_interpolada():
        LARGURA, ALTURA = 1920, 1080
        nova_largura, nova_altura = 960, 540
        

        pontos_ajustados = DadosExame.matriz_pontos
        for ponto in pontos_ajustados:
            ponto.x = int(ponto.x * nova_largura / LARGURA)
            ponto.y = int(ponto.y * nova_altura / ALTURA)
            ponto.cor = (0, 0, 0)
            if ponto.xg == 23 and ponto.yg == -3:
                ponto.atenuacao = 0
                print("atenuei a mancha cega")
            ResultadoFullthreshold.matriz_interpolada.append(ponto)

        Ponto_inicial = Ponto(-27, -27, 1, (255, 0, 0))
        ponto_central = Ponto(0, 0, 1, (0, 0, 0))

        Ponto_finalx = Ponto(27, -27, 3, (0, 255, 0))
        tamanho_total = Ponto_finalx.x * 0.5 - Ponto_inicial.x * 0.5



        centro_x, centro_y = nova_largura // 2,270
        raio = 469 / 2  # Reduz um pouco para caber na tela
     
        # Criar pontos dentro do círculo
        for i in range(centro_x - int(raio), centro_x + int(raio),2):
            for j in range(centro_y - int(raio), centro_y + int(raio),2):
                # Cálculo da distância até o centro
                cor_ponto = (255,0,0)
                distancia = math.sqrt((i - centro_x) ** 2 + (j - centro_y) ** 2)
                fora_da_matriz_original = True
                
                # for ponto in pontos_ajustados:
                #     if ponto.x == i and ponto.y == j or ponto.x + 2 == i and ponto.y == j or ponto.x == i and ponto.y == j + 2 or ponto.x == i + 2 and ponto.y == j + 2:
                #         fora_da_matriz_original = False
                    
                
                if distancia <= raio and fora_da_matriz_original == True:  # Somente pontos dentro do círculo
                    ponto_novo = Ponto(0,0,3,cor_ponto)
                    ponto_novo.x = i
                    ponto_novo.y = j                    
                    ResultadoFullthreshold.matriz_interpolada.append(ponto_novo)
        
        ResultadoFullthreshold.interpolar()
        
    
    def interpolar():
        # Tamanho da matriz interpolada
        tam_eixo_x  = len(ResultadoFullthreshold.matriz_interpolada)
        tam_eixo_y = tam_eixo_x
        # Grau da interpolação
        grau_x = (tam_eixo_x + 8) // 9
        grau_y = (tam_eixo_y + 8) // 9
        
        # Índice máximo da interpolação
        ind_max_inter_x = grau_x - 1
        ind_max_inter_y = grau_y - 1        
        potencia = 6
        matriz_original = ResultadoFullthreshold.pontos_ajustados
     
                
        
        
        
        for ponto in matriz_original:
                i, j = ponto.x, ponto.y
                if ((i * ind_max_inter_x) + ind_max_inter_x < tam_eixo_x and (j * ind_max_inter_y) + ind_max_inter_y < tam_eixo_y) or \
                ((i * ind_max_inter_x) + ind_max_inter_x < tam_eixo_x and (j * ind_max_inter_y) + ind_max_inter_y < ind_max_inter_y):
                    for n in range(grau_y):
                        for m in range(grau_x):
                            acima_x = [p for p in matriz_original if p.x > i and p.y == j]
                            acima_y = [p for p in matriz_original if p.x == i and p.y > j]
                            acima_xy = [p for p in matriz_original if p.x > i and p.y > j]
                            ponto_direita = min(acima_x,key=lambda p: p.x)
                            ponto_abaixo = min(acima_y, key=lambda p: p.y)
                            ponto_diagonal = min(acima_xy,key=lambda p: p.x and p.y)
                            
                            
                            lim0 = ponto.atenuacao
                            lim1 = ponto_direita.atenuacao
                            lim2 = ponto_abaixo.atenuacao
                            lim3 = ponto_diagonal.atenuacao
                            
                            inv_dist_p0 = 1 / (math.sqrt((0 - m) ** potencia + (n - 0) ** potencia)) * 1000
                            inv_dist_p1 = 1 / (math.sqrt((m - ind_max_inter_x) ** potencia + (n - 0) ** potencia)) * 1000
                            inv_dist_p2 = 1 / (math.sqrt((m - 0) ** potencia + (n - ind_max_inter_y) ** potencia)) * 1000
                            inv_dist_p3 = 1 / (math.sqrt((m - ind_max_inter_x) ** potencia + (n - ind_max_inter_y) ** potencia)) * 1000
                            
                            pos_x = (i * ind_max_inter_x) + m
                            pos_y = (j * ind_max_inter_y) + n
                            
                            limiar_interpolado = ((inv_dist_p0 * lim0) + (inv_dist_p1 * lim1) + (inv_dist_p2 * lim2) + (inv_dist_p3 * lim3)) / \
                                                (inv_dist_p0 + inv_dist_p1 + inv_dist_p2 + inv_dist_p3)
                            
                            
                            ponto_matriz_interpolada = [p for p in ResultadoFullthreshold.matriz_interpolada if p.x == pos_x and p.y == pos_y]
                            
                            ponto_matriz_interpolada[0].atenuacao = round(limiar_interpolado)
                            
                        ponto_matriz_interpolada_central = [p for p in ResultadoFullthreshold.matriz_interpolada if p.x == (i * ind_max_inter_x) and p.y == (j * ind_max_inter_y)]
                        ponto_matriz_interpolada_central[0].x, ponto_matriz_interpolada_central[0].y, ponto_matriz_interpolada_central[0].atenuacao = ponto.x,ponto.y,ponto.atenuacao
                       
                        ponto_matriz_interpolada_direita = [p for p in ResultadoFullthreshold.matriz_interpolada if p.x == (i * ind_max_inter_x) + ind_max_inter_x and p.y == j * ind_max_inter_y]
                        ponto_matriz_interpolada_direita[0].x,ponto_matriz_interpolada_direita[0].y, ponto_matriz_interpolada_direita[0].atenuacao = ponto_direita.x,ponto_direita.y,ponto_direita.atenuacao
                       
                        ponto_matriz_interpolada_baixo = [p for p in ResultadoFullthreshold.matriz_interpolada if p.x == i * ind_max_inter_x and p.y == (j * ind_max_inter_y) + ind_max_inter_y]
                        ponto_matriz_interpolada_baixo[0].x,ponto_matriz_interpolada_baixo[0].y, ponto_matriz_interpolada_baixo[0].atenuacao = ponto_abaixo.x,ponto_abaixo.y,ponto_abaixo.atenuacao
                       
                        ponto_matriz_interpolada_diagonal = [p for p in ResultadoFullthreshold.matriz_interpolada if p.x == (i * ind_max_inter_x) + ind_max_inter_x and p.y == (j * ind_max_inter_y) + ind_max_inter_y]
                        ponto_matriz_interpolada_diagonal[0].x, ponto_matriz_interpolada_diagonal[0].y, ponto_matriz_interpolada_diagonal[0].atenuacao = ponto_diagonal.x , ponto_diagonal.y,ponto_diagonal.atenuacao
        
      

    
    
    @staticmethod
    def mapa_pontos():
            # Criar uma imagem branca
        ResultadoFullthreshold.gerar_matriz_interpolada()
        imagem = Image.new("RGB", (960,540), "white")
        draw = ImageDraw.Draw(imagem)      
       

        
        
        

        # Carregar texturas (Certifique-se de que os arquivos existem!)
        texturas = []
        for i in range(1,11):
            caminho = f"campimetria/utils/images/bitmaps/{i}.bmp"
            if os.path.exists(caminho):
                texturas.append(Image.open(caminho))
          
            else:
      
                texturas.append(Image.new("RGB", (50, 50), (200,0 , 0)))  # Placeholder cinza

      

        # Preencher a imagem com as texturas
        for ponto in ResultadoFullthreshold.matriz_interpolada:
            if ponto.atenuacao <= -90:
               pass
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
            
            # Aplicar textura
            if textura:
                
                imagem.paste(textura, (ponto.x, ponto.y))

        # Salvar e exibir a imagem
        imagem.save("mapa_gerado.png")
        pygame.image.load("png","mapa_gerado").blit(pygame.display.get_surface(),(0,0))
        pygame.display.update()
    

    @staticmethod
    def desenha_legendas():
        # exame
        # duracao do exame
        # total de pontos
        # limiar foveal
        # colocar legenda
        # falso positivo
        # falso negativo

        perda_fixacao = 0

        perda_fixacao = (
            ((DadosExame.perda_de_fixacao / DadosExame.total_testes_mancha) * 100)
            if DadosExame.perda_de_fixacao > 0.0
            else 0
        )

        DadosExame.falso_negativo_respondidos_percentual = (
            DadosExame.falso_negativo_respondidos
            / DadosExame.total_testes_falsos_negativo
            * 100
            if DadosExame.falso_negativo_respondidos > 0
            else 0
        )
        DadosExame.falso_positivo_respondidos_percentual = (
            DadosExame.falso_positivo_respondidos
            / DadosExame.total_testes_falsos_positivo
            * 100
            if DadosExame.falso_positivo_respondidos > 0
            else 0
        )
        DadosExame.duracao_do_exame = (DadosExame.duracao_do_exame / 1000) / 60

        labels = [
            f"Exame: {DadosExame.exame_selecionado}",
            f"Duração (min): {DadosExame.duracao_do_exame:.2f}",
            f"Total de pontos: {DadosExame.total_de_pontos_testados}",
            f"Falso positivo: {int(DadosExame.falso_positivo_respondidos)} / {int(DadosExame.total_testes_falsos_positivo)} ({DadosExame.falso_positivo_respondidos_percentual:.2f}%)",
            f"Falso negativo: {DadosExame.falso_negativo_respondidos} / {DadosExame.total_testes_falsos_negativo} ({DadosExame.falso_negativo_respondidos_percentual:.2f}%)",
            f"Perda de fixacao: {int(DadosExame.perda_de_fixacao)} / {DadosExame.total_testes_mancha} ({perda_fixacao:.2f}%)",
        ]

        # Posição inicial para desenhar labels (quadrante direito)
        pos_x = 1920 * 3 // 4  # 75% da largura (centro do quadrante direito)
        pos_y = 270  # Começa no meio da tela
        espacamento = 100  # Espaço entre as labels
        fonte = pygame.font.Font(None, 30)
        color_label_info = (0, 0, 0)

        for i, texto in enumerate(labels):
            # Renderiza a label
            color_label_info = (0, 0, 0)
            if (
                i == 3
                and DadosExame.falso_positivo_respondidos_percentual > 33
                or i == 4
                and DadosExame.falso_negativo_respondidos_percentual > 33
                or i == 5
                and perda_fixacao > 33
            ):
                color_label_info = pygame.Color("red")

            texto_renderizado = fonte.render(texto, True, color_label_info)

            # Posiciona centralizado no quadrante direito
            pygame.display.get_surface().blit(
                texto_renderizado, (pos_x - 200, pos_y + i * espacamento)
            )

    @staticmethod
    def desenha_mapa_limiares():
        LARGURA, ALTURA = 1920, 1080  # Tela original
        nova_largura, nova_altura = 960, 540  # Nova tela

        pygame.draw.circle(pygame.display.get_surface(), (0, 0, 0), (480, 270), 469 / 2, 1)
        pygame.draw.line(
            pygame.display.get_surface(), (0, 0, 0), (480, 519), (480, 20), 1
        )
        pygame.draw.line(
            pygame.display.get_surface(), (0, 0, 0), (729, 270), (230, 270), 1
        )

        pontos_ajustados = DadosExame.matriz_pontos
        for ponto in pontos_ajustados:
            ponto.x = int(ponto.x * nova_largura / LARGURA)  # Reduzindo a coordenada X
            ponto.y = int(ponto.y * nova_altura / ALTURA)  # Reduzindo a coordenada Y

        for ponto in pontos_ajustados:
            fonte = pygame.font.Font(None, 20)
            label = fonte.render(f"{ponto.atenuacao}", True, (0, 0, 0))
            pygame.display.get_surface().blit(
                label, label.get_rect(center=(ponto.x, ponto.y))
            )  # Adicionar texto abaixo

    @staticmethod
    def exibir_resultados():
        pygame.font.init()

        pygame.display.get_surface().fill(pygame.Color("white"))
        ResultadoFullthreshold.desenha_legendas()
        ResultadoFullthreshold.desenha_mapa_limiares()

        pygame.display.flip()
