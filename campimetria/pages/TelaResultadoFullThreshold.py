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
        """Determina o tamanho da célula baseado na distribuição dos pontos, evitando lacunas e garantindo cobertura uniforme"""
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
        """Interpola a atenuação dentro da célula suavizando a transição para as vizinhas"""
        dists, indices = kdtree.query((x, y), k=min(5, len(pontos)))

        if len(indices) == 0:
            return 0

        pesos = np.exp(-np.array(dists) / 10)
        pesos /= pesos.sum()

        atenuacao_interpolada = sum(
            pesos[i] * pontos[indices[i]].atenuacao for i in range(len(indices))
        )
        return atenuacao_interpolada

    @staticmethod
    def desenhar_mapa():
        """Desenha o mapa com otimização de desempenho"""
        pygame.init()
        screen = pygame.display.get_surface()
        screen.fill(pygame.Color("white"))
        buffer = pygame.Surface((960, 540))  # Usa um buffer para melhorar a performance
        buffer.fill((255, 255, 255))

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
        step = 2  # Reduz a granularidade para melhorar a performance

        for x in range(0, 960, step):
            for y in range(0, 540, step):
                if (x - centro_x) ** 2 + (y - centro_y) ** 2 <= raio**2:
                    if (x, y) in atenuacoes_cache:
                        atenuacao_interpolada = atenuacoes_cache[(x, y)]
                    else:
                        atenuacao_interpolada = (
                            ResultadoFullthreshold.calcular_atenuacao_interpolada(
                                x, y, kdtree, DadosExame.matriz_pontos
                            )
                        )
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

                    pygame.draw.rect(
                        buffer, cor, (x, y, step, step)
                    )  # Desenha blocos em vez de pixels individuais

        pygame.draw.line(
            buffer,
            (0, 0, 0),
            (centro_x, centro_y - raio),
            (centro_x, centro_y + raio),
            2,
        )
        pygame.draw.line(
            buffer,
            (0, 0, 0),
            (centro_x - raio, centro_y),
            (centro_x + raio, centro_y),
            2,
        )

        screen.blit(buffer, (0, 0))  # Atualiza a tela com o buffer

    @staticmethod
    def desenhar_mapa_limiares():
        fonte = pygame.font.Font(None, 24)
        # Desenhar pontos e labels
        for ponto in DadosExame.matriz_pontos:
            ponto.y += 540
            ponto.cor = pygame.Color("black")
            ponto.plotarPonto()
            label = fonte.render(f"{ponto.atenuacao}", True, (0, 0, 0))
            label_rect = label.get_rect(center=(ponto.x - 0.505, ponto.y + 15))
            pygame.display.get_surface().blit(label, label_rect)
        # circulo do mapa de limiar
        pygame.draw.circle(pygame.display.get_surface(), (0, 0, 0), (480, 810), 250, 1)





    @staticmethod
    def desenha_legendas():

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
    def exibir_resultados():
        pygame.font.init()

        ResultadoFullthreshold.desenhar_mapa()
        ResultadoFullthreshold.desenhar_mapa_limiares()
        ResultadoFullthreshold.desenha_legendas()
        
        DadosExame.reset()
        
        pygame.display.flip()
