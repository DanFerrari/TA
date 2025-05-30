import pygame, random, time, os, sys, math, json, copy
import numpy as np
import matplotlib.pyplot as plt


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
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "constants", "base"))
)

from dados import *
from Ponto import Ponto
from gerar_pdf import GerarPdf
from atenuacoes_base import atenuacoes_base
from atenuacao_daniel import atenuacao_daniel


class ResultadoFullthreshold:
    
    

    @staticmethod
    def gerar_pontos_mapa_textura():
        matriz = []
        for ponto in DadosExame.matriz_pontos:
            if DadosExame.programa_selecionado == Constantes.central10:
                ponto.xg = ponto.xg * 1.5
                ponto.yg = ponto.yg * 1.5
            ponto_novo = Ponto(
                ponto.xg, ponto.yg, tamanhoPonto=3, cor=(0, 0, 0), distancia=200
            )
            ponto_novo.raio_ponto = 6
            ponto_novo.pontoPix = 4
            ponto_novo.x = int(ponto_novo.x * 960 / 1920)
            ponto_novo.y = int(ponto_novo.y * 540 / 1080)
            ponto_novo.atenuacao = ponto.atenuacao
            matriz.append(ponto_novo)
        return matriz

    @staticmethod
    def gerar_pontos_mapa_limiar():
        matriz = []
        for ponto in DadosExame.matriz_pontos:
            if DadosExame.programa_selecionado == Constantes.central10:
                ponto.xg = ponto.xg * 1.5
                ponto.yg = ponto.yg * 1.5
            ponto_novo = Ponto(
                ponto.xg, ponto.yg, tamanhoPonto=3, cor=(0, 0, 0), distancia=200
            )
            ponto_novo.raio_ponto = 6
            ponto_novo.pontoPix = 4
            
            ponto_novo.x = int(ponto_novo.x * 960 / 1920)
            ponto_novo.y = int(ponto_novo.y * 540 / 1080)
            ponto_novo.atenuacao = ponto.atenuacao
            matriz.append(ponto_novo)
        return matriz

    mapa_cor = True
    mapa_cinza = True
    matriz_pontos_mapa_textura = None
    matriz_pontos_mapa_limiar = None
    textura_cache = []
    cache_texturas_cor = {}
    cache_texturas_cinza = {}

    @staticmethod
    def carregar_texturas():
        for i in range(1, 11):
            caminho = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    "utils",
                    "images",
                    "bitmaps",
                    f"{i}.bmp",
                )
            )
            if os.path.exists(caminho):
                ResultadoFullthreshold.textura_cache.append(
                    pygame.image.load(caminho).convert()
                )

    @staticmethod
    def inicializar_matrizes():
        ResultadoFullthreshold.matriz_pontos_mapa_textura = (
            ResultadoFullthreshold.gerar_pontos_mapa_textura()
        )
        ResultadoFullthreshold.matriz_pontos_mapa_limiar = (
            ResultadoFullthreshold.gerar_pontos_mapa_limiar()
        )

    @staticmethod
    def calcular_atenuacao_interpolada(x, y, kdtree, pontos, raio_fixo=15):
        """Interpola a atenuação suavizando a transição, mantendo valores fixos dentro de um raio"""
        dists, indices = kdtree.query((x, y), k=min(10, len(pontos)))

        if len(indices) == 0:
            return 0

        # Se o ponto está dentro do raio, usa a atenuação do ponto mais próximo
        if dists[0] < raio_fixo:
            return round(pontos[indices[0]].atenuacao, 1)

        # Fora do raio, faz interpolação com os vizinhos
        pesos = np.exp(-np.array(dists, dtype=np.float32) / 10)
        pesos /= np.sum(pesos)
        atenuacao_interpolada = np.dot(
            pesos, [pontos[idx].atenuacao for idx in indices]
        )

        return round(atenuacao_interpolada, 1)

    @staticmethod
    def mostrar_label_temporaria(carregado):
        """Mostra uma label temporária na tela e depois a apaga"""
        fonte = pygame.font.Font(None, 36)
        label = fonte.render("CARREGANDO MAPA...", True, (0, 0, 0), (255, 255, 255))
        label_rect = label.get_rect(center=(480, 540))

        if not carregado:
            # Desenha a label na tela
            pygame.display.get_surface().blit(label, label_rect)
            pygame.display.update()

        if carregado:
            pygame.draw.rect(
                pygame.display.get_surface(), (255, 255, 255), label_rect
            )  # Fundo preto (ajuste conforme necessário)
            pygame.display.update()

    @staticmethod
    def estrutura_legenda(texturas, surface):

        centro_x, centro_y = 480, 270
        largura, altura = 40, 30
        fonte = pygame.font.Font(None, 24)

        textura_rect = [
            (centro_x + 280, centro_y + 120, largura, altura),
            (centro_x + 280, centro_y + 90, largura, altura),
            (centro_x + 280, centro_y + 60, largura, altura),
            (centro_x + 280, centro_y + 30, largura, altura),
            (centro_x + 280, centro_y - 0, largura, altura),
            (centro_x + 280, centro_y - 30, largura, altura),
            (centro_x + 280, centro_y - 60, largura, altura),
            (centro_x + 280, centro_y - 90, largura, altura),
            (centro_x + 280, centro_y - 120, largura, altura),
            # (centro_x + 280, centro_y - 150, largura, altura),
        ]

        texto_medidas = [
            "0",
            "1 - 5",
            "6 - 10",
            "11 - 15",
            "16 - 20",
            "21 - 25",
            "26 - 30",
            "31 - 35",
            "36 - 40",
            # "41 - 50"
        ]

        if ResultadoFullthreshold.mapa_cor:
            for i, rect in enumerate(textura_rect):
                pygame.draw.rect(surface, texturas[i], textura_rect[i])
                surface.blit(
                    fonte.render(texto_medidas[i], True, (0, 0, 0)),
                    ((lambda: rect[0])() + 50, (lambda: rect[1])() + 7.5),
                )
        else:
            for k, rect in enumerate(textura_rect):
                surface.blit(
                    fonte.render(texto_medidas[k], True, (0, 0, 0)),
                    ((lambda: rect[0])() + 50, (lambda: rect[1])() + 7.5),
                )
                borda = (rect[0] - 1, rect[1] - 1, rect[2] + 2, rect[3] + 2)
                pygame.draw.rect(surface, pygame.Color("black"), borda, 2)

                for i in range(0, largura, 5):
                    for j in range(0, altura, 5):
                        pos_x = rect[0] + i
                        pos_y = rect[1] + j
                        surface.blit(texturas[k], (pos_x, pos_y))

    @staticmethod
    def gerar_legenda_pontos(surface):
        texturas = []
        for i in range(1, 10):
            caminho = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    "utils",
                    "images",
                    "bitmaps",
                    f"{i}.bmp",
                )
            )
            if os.path.exists(caminho):
                texturas.append(pygame.image.load(caminho).convert())
            else:
                print(f"caminho nao existe: {caminho}")
        ResultadoFullthreshold.estrutura_legenda(texturas, surface)

    @staticmethod
    def gerar_legenda_cores(surface):

        texturas = [
            (0, 0, 156),
            (0, 85, 204),
            (0, 131, 207),
            (2, 147, 166),
            (0, 145, 107),
            (0, 163, 87),
            (149, 201, 28),
            (252, 219, 0),
            (232, 129, 26),
            # (255, 0, 0)
        ]

        ResultadoFullthreshold.estrutura_legenda(texturas, surface)

    def gerar_legenda_tons_cinza(surface):

        texturas = [
            (0, 0, 0),
            (40, 40, 40),
            (65, 65, 65),
            (90, 90, 90),
            (115, 115, 115),
            (140, 140, 140),
            (165, 165, 165),
            (185, 185, 185),
            (225, 225, 225),
        ]

        ResultadoFullthreshold.estrutura_legenda(texturas, surface)

    @staticmethod
    def gerar_texturas_coloridas(atenuacao):
        """Mapeia atenuação para um gradiente de cores passando por vermelho, amarelo, verde e azul"""
        if atenuacao in ResultadoFullthreshold.cache_texturas_cor:
            return ResultadoFullthreshold.cache_texturas_cor[atenuacao]

        if atenuacao <= 0:
            cor = (0, 0, 156)
        elif atenuacao < 6:
            cor = (0, 85, 204)
        elif atenuacao < 11:
            cor = (0, 131, 207)
        elif atenuacao < 16:
            cor = (2, 147, 166)
        elif atenuacao < 21:
            cor = (0, 145, 107)
        elif atenuacao < 26:
            cor = (0, 163, 87)
        elif atenuacao < 31:
            cor = (149, 201, 28)
        elif atenuacao < 36:
            cor = (252, 219, 0)
        elif atenuacao < 41:
            cor = (232, 129, 26)
        # else:
        #     cor = (255, 0, 0)

        # Armazena no cache e retorna
        ResultadoFullthreshold.cache_texturas_cor[atenuacao] = cor
        return cor

    @staticmethod
    def gerar_texturas_pontos(atenuacao):
        if not ResultadoFullthreshold.textura_cache:
            ResultadoFullthreshold.carregar_texturas()

        if atenuacao <= 0:
            cor = ResultadoFullthreshold.textura_cache[0]
        elif atenuacao < 6:
            cor = ResultadoFullthreshold.textura_cache[1]
        elif atenuacao < 11:
            cor = ResultadoFullthreshold.textura_cache[2]
        elif atenuacao < 16:
            cor = ResultadoFullthreshold.textura_cache[3]
        elif atenuacao < 21:
            cor = ResultadoFullthreshold.textura_cache[4]
        elif atenuacao < 26:
            cor = ResultadoFullthreshold.textura_cache[5]
        elif atenuacao < 31:
            cor = ResultadoFullthreshold.textura_cache[6]
        elif atenuacao < 36:
            cor = ResultadoFullthreshold.textura_cache[7]
        elif atenuacao < 41:
            cor = ResultadoFullthreshold.textura_cache[8]
        # else:
        #     cor = ResultadoFullthreshold.textura_cache[9]
        return cor

    @staticmethod
    def gerar_texturas_cinza(atenuacao):
        """Mapeia a atenuação para tons de cinza e usa cache"""
        if atenuacao in ResultadoFullthreshold.cache_texturas_cinza:
            return ResultadoFullthreshold.cache_texturas_cinza[atenuacao]

        if atenuacao <= 0:
            cor = (0, 0, 0)
        elif atenuacao < 6:
            cor = (40, 40, 40)
        elif atenuacao < 11:
            cor = (65, 65, 65)
        elif atenuacao < 16:
            cor = (90, 90, 90)
        elif atenuacao < 21:
            cor = (115, 115, 115)
        elif atenuacao < 26:
            cor = (140, 140, 140)
        elif atenuacao < 31:
            cor = (165, 165, 165)
        elif atenuacao < 36:
            cor = (185, 185, 185)
        elif atenuacao < 41:
            cor = (225, 225, 225)
        # else:
        #     cor = (225,225,225)

        # Armazena no cache e retorna
        ResultadoFullthreshold.cache_texturas_cinza[atenuacao] = cor
        return cor

    @staticmethod
    def desenhar_mapa_texturas(firstload):
        """Desenha o mapa com otimização de desempenho"""

        buffer = pygame.Surface((960, 540))  # Usa um buffer para melhorar a performance
        buffer.fill((255, 255, 255))
        if not firstload:
            ResultadoFullthreshold.mostrar_label_temporaria(False)

        centro_x, centro_y = 960 // 2, 540 // 2
        raio = min(centro_x, centro_y) - 55
        kdtree = KDTree(
            [(p.x, p.y) for p in ResultadoFullthreshold.matriz_pontos_mapa_textura]
        )
        atenuacoes_cache = {}
        step = 5 if ResultadoFullthreshold.mapa_cor else 5
        pixels = []
        for x in range(0, 960, step):
            for y in range(0, 540, step):
                if (x - centro_x) ** 2 + (y - centro_y) ** 2 <= raio**2:
                    atenuacao_interpolada = atenuacoes_cache.get(
                        (x, y),
                        ResultadoFullthreshold.calcular_atenuacao_interpolada(
                            x,
                            y,
                            kdtree,
                            ResultadoFullthreshold.matriz_pontos_mapa_textura,
                        ),
                    )
                    atenuacoes_cache[(x, y)] = atenuacao_interpolada

                    if ResultadoFullthreshold.mapa_cor:
                        if ResultadoFullthreshold.mapa_cinza:
                            cor = ResultadoFullthreshold.gerar_texturas_cinza(
                                atenuacao_interpolada
                            )
                        else:
                            cor = ResultadoFullthreshold.gerar_texturas_coloridas(
                                atenuacao_interpolada
                            )
                        pixels.append((x, y, cor))
                    else:
                        cor = ResultadoFullthreshold.gerar_texturas_pontos(
                            atenuacao_interpolada
                        )
                        buffer.blit(cor, (x, y))
        for x, y, cor in pixels:
            pygame.draw.rect(buffer, cor, (x, y, step, step))
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

        ResultadoFullthreshold.gerar_legenda_textura(buffer)

        pygame.image.save(
            buffer,
            os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    "utils",
                    "images",
                    "temp",
                    f"mapa_pontos.png",
                )
            ),
        )
        pygame.display.get_surface().blit(buffer, (-200, 0))

        if not firstload:
            ResultadoFullthreshold.mostrar_label_temporaria(True)
        else:
            ResultadoFullthreshold.status_resultado(carregado=True)

    @staticmethod
    def gerar_legenda_textura(surface):

        if ResultadoFullthreshold.mapa_cor:
            if ResultadoFullthreshold.mapa_cinza:
                ResultadoFullthreshold.gerar_legenda_tons_cinza(surface)

            else:
                ResultadoFullthreshold.gerar_legenda_cores(surface)
        else:
            ResultadoFullthreshold.gerar_legenda_pontos(surface)

    @staticmethod
    def desenhar_mapa_limiares():
        largura = 1920 / 2  # Raio do círculo * 2
        altura = 1080 / 2  # Raio do círculo * 2
        surface = pygame.Surface((largura, altura))
        surface.fill((255, 255, 255))
        fonte = pygame.font.Font(None, 18)
        # Desenhar pontos e labels
        for ponto in ResultadoFullthreshold.matriz_pontos_mapa_limiar:

            ponto.plotarPonto(surface=surface)
            label = fonte.render(f"{int(ponto.atenuacao)}", True, (0, 0, 0))
            label_rect = label.get_rect(center=(ponto.x - 0.505, ponto.y + 12))
            surface.blit(label, label_rect)

        # circulo do mapa de limiar
        pygame.draw.circle(surface, (0, 0, 0), (480, altura / 2), 230, 1)

        # cruz do mapa
        pygame.draw.line(
            surface,
            (0, 0, 0),
            (480 + 230, altura / 2),
            (480 - 230, altura / 2),
            1,
        )
        pygame.draw.line(
            surface,
            (0, 0, 0),
            (480, altura / 2 + 230),
            (480, altura / 2 - 230),
            1,
        )
        pygame.image.save(
            surface,
            os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    "utils",
                    "images",
                    "temp",
                    f"mapa_limiares.png",
                )
            ),
        )
        pygame.display.get_surface().blit(surface, (-200, 540))

    @staticmethod
    def gerar_mapa_desvios_e_curva_de_bebie():
        indices_nulos = []
        if DadosExame.programa_selecionado == Constantes.central24 and DadosExame.olho == Constantes.olho_direito:
            from cordenadas_24OD import indices_nulos_24OD
            indices_nulos = indices_nulos_24OD
        elif DadosExame.programa_selecionado == Constantes.central24 and DadosExame.olho == Constantes.olho_esquerdo:
            from cordenadas_24OE import indices_nulos_24OE
            indices_nulos = indices_nuindices_nulos_24OE
       
     
    

        def verifica_faixa_etaria(faixa_etaria):
            match DadosExame.faixa_etaria:
                case 1:
                    from idade_0_20 import lista_valores

                    lista_base_atenuacao = lista_valores
                case 2:
                    from idade_21_30 import lista_valores

                    lista_base_atenuacao = lista_valores
                case 3:
                    from idade_31_40 import lista_valores

                    lista_base_atenuacao = lista_valores
                case 4:
                    from idade_41_50 import lista_valores

                    lista_base_atenuacao = lista_valores
                case 5:
                    from idade_51_60 import lista_valores

                    lista_base_atenuacao = lista_valores
                case 6:
                    from idade_61_70 import lista_valores

                    lista_base_atenuacao = lista_valores
                case 7:
                    from idade_71_80 import lista_valores

                    lista_base_atenuacao = lista_valores
                case 8:
                    from idade_81_90 import lista_valores

                    lista_base_atenuacao = lista_valores
                case 9:
                    from idade_90 import lista_valores

            return lista_valores

        def espelhar_vetor(vetor):
            lista_atenuacao = []
            for cordenada, atenuacao in vetor.items():
                lista_atenuacao.append(atenuacao)

            tamanhos_linhas = [4, 6, 8, 10, 10, 10, 10, 8, 6, 4]
            espelhado = []
            inicio = 0

            for tamanho in tamanhos_linhas:
                linha = lista_atenuacao[inicio : inicio + tamanho]
                espelhado.extend(linha[::-1])  # faz o espelhamento (slice reverso)
                inicio += tamanho
            for (cordenada, atenuacao), atenuacao_espelhada in zip(
                vetor.items(), espelhado
            ):
                vetor[cordenada] = atenuacao_espelhada
            return vetor

        def desenha_curva_bebie(desvio_total, desvio_paciente):
            tolerancia_positiva = [valor - 3 for valor in desvio_total]
            tolerancia_negativa = [valor + 3 for valor in desvio_total]
            
            
            if DadosExame.programa_selecionado == Constantes.central30:
                step_labels_x = 15
            elif DadosExame.programa_selecionado == Constantes.central24:
                step_labels_x = 13.25
            elif DadosExame.programa_selecionado == Constantes.central10:
                step_labels_x = 16.75
            
            
            quantidade_pontos = np.arange(
                1, len(desvio_total) + 1
            )  
            fig, ax = plt.subplots()
            ax.step(
                quantidade_pontos,
                tolerancia_positiva,
                where="mid",
                label="N + 3",
                color="blue",
            )
            ax.step(
                quantidade_pontos, desvio_total, where="mid", label="N", color="green"
            )
            ax.step(
                quantidade_pontos,
                tolerancia_negativa,
                where="mid",
                label="N - 3",
                color="red",
            )
            ax.step(quantidade_pontos, desvio_paciente, where="mid", color="black")

            # Set y-axis limits and steps
            ax.set_ylim(25, -10)  # Set the y-axis range from 25 to -10
            ax.set_yticks(np.arange(25, -10, -5))  # Set y-axis ticks with a step of -5
            ax.set_yticklabels(
                [str(i) for i in np.arange(25, -10, -5)]
            )  # Ensure labels are displayed
            ax.set_xlim(1, len(desvio_total) + 2)
            ax.set_xticks(
                np.arange(1, len(desvio_total) + 1, step_labels_x)
            )  # Adjusted to include point 76
            ax.set_xticklabels(
                [str(int(i)) for i in np.arange(1, len(desvio_total) + 1, step_labels_x)]
            )  # Ensure labels are displayed
            ax.plot(
                [quantidade_pontos[-1], quantidade_pontos[-1]],
                [tolerancia_positiva[-1], 30],
                color="black",
                linestyle="-",
            )

            ax.set_xlabel("[Pontos]")
            ax.set_ylabel("[dB]")
            ax.set_title("Curva de Bebie:")
            ax.legend()

            plt.savefig(
                os.path.abspath(
                    os.path.join(
                        os.path.dirname(__file__),
                        "..",
                        "utils",
                        "images",
                        "temp",
                        "bebie_curve.png",
                    )
                )
            )

        def desenha_mapa_desvio(nome_imagem, matriz_pontos):
            ponto_central = Ponto(0, 0, tamanhoPonto=3, cor=(0, 0, 0), distancia=200)
            ponto_central.x = int(ponto_central.x * 480 / 1920)
            ponto_central.y = int(ponto_central.y * 270 / 1080)

            # Define o tamanho da superfície com base no conteúdo
            largura = 240  # Raio do círculo * 2
            altura = 240  # Raio do círculo * 2
            surface = pygame.Surface((largura, altura))
            surface.fill((255, 255, 255))

            # Ajusta o ponto central para o novo tamanho da superfície
            ponto_central.x = largura // 2
            ponto_central.y = altura // 2

            # Desenha o círculo e as linhas centrais
            pygame.draw.circle(
                surface,
                (0, 0, 0),
                (ponto_central.x, ponto_central.y),
                largura // 2,
                1,
            )
            pygame.draw.line(
                surface,
                (0, 0, 0),
                (ponto_central.x + largura // 2, ponto_central.y),
                (ponto_central.x - largura // 2, ponto_central.y),
                1,
            )
            pygame.draw.line(
                surface,
                (0, 0, 0),
                (ponto_central.x, ponto_central.y + altura // 2),
                (ponto_central.x, ponto_central.y - altura // 2),
                1,
            )

            # Plota os pontos na superfície
            for ponto in matriz_pontos:
               
                if DadosExame.olho == Constantes.olho_direito and (
                    (ponto.xg == 15 and ponto.yg == 3)
                    or (ponto.xg == 15 and ponto.yg == -3)
                ):
                    continue
                if DadosExame.olho == Constantes.olho_esquerdo and (
                    (ponto.xg == -15 and ponto.yg == 3)
                    or (ponto.xg == -15 and ponto.yg == -3)
                ):
                    continue
                
                if DadosExame.programa_selecionado == Constantes.central10:
                        ponto.xg = ponto.xg * 3
                        ponto.yg = ponto.yg * 3
                        ponto_novo = Ponto(
                            ponto.xg, ponto.yg, tamanhoPonto=3, cor=(0, 0, 0), distancia=200
                        )
                        ponto_novo.raio_ponto = 6
                        ponto_novo.pontoPix = 4
                        ponto_novo.x = int(ponto_novo.x * 480 / 1920)
                        ponto_novo.y = int(ponto_novo.y * 270 / 1080)
                        ponto_novo.x -=  120
                        ponto_novo.y -= 15
                        ponto_novo.atenuacao = ponto.atenuacao
                        ponto_novo.plotaString(ponto.atenuacao, 20, surface=surface)
                    
                   
                else:
                    ponto.plotaString(ponto.atenuacao, 20, surface=surface)

            # Salva a imagem
            pygame.image.save(
                surface,
                os.path.abspath(
                    os.path.join(
                        os.path.dirname(__file__),
                        "..",
                        "utils",
                        "images",
                        "temp",
                        f"{nome_imagem}.png",
                    )
                ),
            )

        def calcula_MD():
            somatorio1 = 0.0
            somatorio2 = 0.0
            variancia = 4.0
            for cordenada, atenuacao in lista_base_atenuacao.items():
                x, y = cordenada
                for ponto in DadosExame.matriz_pontos:
                    if (x, y) == (ponto.xg, ponto.yg):
                        if (
                            DadosExame.olho == Constantes.olho_direito
                            and ponto.xg == 15
                            and ponto.yg == 3
                            or ponto.xg == 15
                            and ponto.yg == -3
                        ):
                            continue
                        elif (
                            DadosExame.olho == Constantes.olho_esquerdo
                            and ponto.xg == -15
                            and ponto.yg == 3
                            or ponto.xg == -15
                            and ponto.yg == -3
                        ):
                            continue

                        somatorio1 = somatorio1 + (
                            float(ponto.atenuacao) - float(atenuacao)
                        ) / (variancia * variancia)
                        somatorio2 = somatorio2 + (1.0 / (variancia * variancia))

            DadosExame.md = float(round((somatorio1 / somatorio2), 3))

        def calcula_PSD(matriz_desvio_total):
            tam = len(matriz_desvio_total)
            somatorio1 = 0.0
            somatorio2 = 0.0
            variancia = 4.0
            for i in range(tam - 3):
                somatorio1 = somatorio1 + (variancia * variancia)

            for ponto in matriz_desvio_total:
                if DadosExame.olho == Constantes.olho_direito and (
                    (ponto.xg == 15 and ponto.yg == 3)
                    or (ponto.xg == 15 and ponto.yg == -3)
                ):
                    continue
                if DadosExame.olho == Constantes.olho_esquerdo and (
                    (ponto.xg == -15 and ponto.yg == 3)
                    or (ponto.xg == -15 and ponto.yg == -3)
                ):
                    continue
                somatorio2 = somatorio2 + float(
                    pow(ponto.atenuacao - DadosExame.md, 2.0) / pow(variancia, 2.0)
                )

            somatorio1 = somatorio1 / float(tam - 2)
            somatorio2 = somatorio2 / float(tam - 3)
            psd = somatorio1 * somatorio2
            psd = float(math.sqrt(psd))
            DadosExame.psd = psd

        def calcula_desvio(matriz_desvio_total):
            setimo_valor = 0
            curva_paciente_filtrada = [ponto.atenuacao for ponto in matriz_desvio_total]
            curva_paciente_filtrada.sort(reverse=True)
           
            setimo_valor = curva_paciente_filtrada[9]
            for ponto in matriz_desvio_total:
                ponto_desvio_padrao = Ponto(ponto.xg, ponto.yg, 3, (0, 0, 0), 200)
                ponto_desvio_padrao.atenuacao = ponto.atenuacao - setimo_valor
                ponto_desvio_padrao.x = ponto.x
                ponto_desvio_padrao.y = ponto.y
                matriz_desvio_padrao.append(ponto_desvio_padrao)

        lista_base_atenuacao = verifica_faixa_etaria(DadosExame.faixa_etaria)
        lista_temp = {}
        if DadosExame.programa_selecionado == Constantes.central10:
            from cordenadas_10 import indices_base_atenuacao,cordenadas_10
            
            for cordenada,indice in zip(cordenadas_10,indices_base_atenuacao):
                lista_temp[cordenada] = lista_base_atenuacao[list(lista_base_atenuacao.keys())[indice]]
            lista_base_atenuacao = lista_temp
        else:        
            keys_to_remove = [list(lista_base_atenuacao.keys())[i] for i in indices_nulos]
            for key in keys_to_remove:
                lista_base_atenuacao.pop(key, None)
    

        

        
        
        
        if DadosExame.olho == Constantes.olho_esquerdo:
            lista_base_atenuacao = espelhar_vetor(lista_base_atenuacao)

        curva_base = [
            atenuacao for cordenada, atenuacao in lista_base_atenuacao.items()
        ]
        curva_paciente = []
        desvio_paciente = []
        desvio_total = []
        matriz_desvio_padrao = []
        matriz_desvio_total = []

        for cordenada, atenuacao in lista_base_atenuacao.items():
            x, y = cordenada
            for ponto in DadosExame.matriz_pontos:
                if (x, y) == (ponto.xg, ponto.yg):
                    if DadosExame.olho == Constantes.olho_direito and (
                        (ponto.xg == 15 and ponto.yg == 3)
                        or (ponto.xg == 15 and ponto.yg == -3)
                    ):
                        
                        ponto_desvio = Ponto(
                            ponto.xg,
                            ponto.yg,
                            tamanhoPonto=3,
                            cor=(0, 0, 0),
                            distancia=200,
                        )
                        ponto_desvio.x = int(ponto_desvio.x * 480 / 1920)
                        ponto_desvio.y = int(ponto_desvio.y * 270 / 1080)
                        ponto_desvio.atenuacao = -1
                        curva_paciente.append( ponto_desvio.atenuacao)
                        matriz_desvio_total.append(ponto_desvio)
                        continue
                    if DadosExame.olho == Constantes.olho_esquerdo and (
                        (ponto.xg == -15 and ponto.yg == 3)
                        or (ponto.xg == -15 and ponto.yg == -3)
                    ):
                        
                        ponto_desvio = Ponto(
                            ponto.xg,
                            ponto.yg,
                            tamanhoPonto=3,
                            cor=(0, 0, 0),
                            distancia=200,
                        )
                        ponto_desvio.x = int(ponto_desvio.x * 480 / 1920)
                        ponto_desvio.y = int(ponto_desvio.y * 270 / 1080)
                        ponto_desvio.atenuacao = -1
                        matriz_desvio_total.append( ponto_desvio)
                        continue

                    ponto_desvio = Ponto(
                        ponto.xg, ponto.yg, tamanhoPonto=3, cor=(0, 0, 0), distancia=200
                    )
                    curva_paciente.append(ponto.atenuacao)

                    ponto_desvio.x = int(ponto_desvio.x * 480 / 1920)
                    ponto_desvio.y = int(ponto_desvio.y * 270 / 1080)
                    ponto_desvio.atenuacao = ponto.atenuacao - atenuacao
                    matriz_desvio_total.append(ponto_desvio)

        for paciente_atenuacao, base_atenuacao in zip(curva_paciente, curva_base):
            desvio_paciente.append(-1 * (paciente_atenuacao - base_atenuacao))
            desvio_total.append(np.mean(curva_base) - base_atenuacao)

        desvios_por_ponto = [abs(p - b) for p, b in zip(curva_paciente, curva_base)]
        desvio_padrao_global = int(np.std(desvios_por_ponto))

        for ponto in matriz_desvio_total:
            ponto.x -= 120
            ponto.y -= 15

        calcula_desvio(matriz_desvio_total)
        calcula_MD()
        calcula_PSD(matriz_desvio_total)
        desenha_mapa_desvio("desvio_total", matriz_desvio_total)
        desenha_mapa_desvio("desvio_padrao", matriz_desvio_padrao)

        desvio_total.sort(reverse=False)
        desvio_paciente.sort(reverse=False)

            
        desvio_total[-2:] = [desvio_total[-3]] * 2
        


        # desvio_paciente[:3] = desvio_paciente[3:6]
        desenha_curva_bebie(desvio_total, desvio_paciente)
    
    @staticmethod
    def gera_imagem_barra_indicador_colorido(min,max,valor,nome):
        from termometro import gerar_barra_com_indicador
        valor_normalizado = ((valor - min) / (max - min)) * 100
        if valor_normalizado > 96:
            valor_normalizado = 96
        elif valor_normalizado < 4:
            valor_normalizado = 4
            
        gerar_barra_com_indicador(valor_normalizado,nome)
    
    @staticmethod
    def plota_barra_indicativa_psd_md_confiabilidade():
        
        caminho_indicador_md = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils", "images","temp","indicador_md.png"))
        caminho_indicador_psd = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils", "images","temp","indicador_psd.png"))
        caminho_indicador_conf = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils", "images","temp","indicador_confiabilidade.png"))
        
        

        
        
        ResultadoFullthreshold.gera_imagem_barra_indicador_colorido(0,100,DadosExame.confiabilidade,caminho_indicador_conf)
        ResultadoFullthreshold.gera_imagem_barra_indicador_colorido(0,-15,DadosExame.md,caminho_indicador_md)
        ResultadoFullthreshold.gera_imagem_barra_indicador_colorido(0,10,DadosExame.psd,caminho_indicador_psd)
        
       
        image_indicador_md = pygame.image.load(caminho_indicador_md)
        image_indicador_psd = pygame.image.load(caminho_indicador_psd)
        image_confiabilidade = pygame.image.load(caminho_indicador_conf)

        # Redimensiona as imagens
        image_indicador_md = pygame.transform.scale(image_indicador_md, (210, 25))  
        image_indicador_psd = pygame.transform.scale(image_indicador_psd, (210, 25)) 
        image_confiabilidade = pygame.transform.scale(image_confiabilidade, (210, 25)) 
        
        return image_indicador_md, image_indicador_psd,image_confiabilidade
        
 

    @staticmethod
    def desenha_legendas_exame():
        
        
        
        cor_legenda_normal = (9,92,12)
        cor_legenda_leve = (161,156,14)
        cor_legenda_moderado = (179,108,8)
        cor_legenda_severo = (166,6,6)
        
        def render_texto_colorido(fonte, texto, cor_restante, cor_primeira=(0, 0, 0), largura_max=850):
            """
            Renderiza um texto com tudo que estiver antes de ':' em preto
            e o restante em uma cor definida.
            Faz quebra de linha se ultrapassar a largura máxima.
            """

            if ':' in texto:
                parte1, parte2 = texto.split(':', 1)
                parte1 += ':'
                parte2 = parte2.strip()
            else:
                parte1 = texto
                parte2 = ""

            linhas = []
            espaco = fonte.size(" ")[0]

            # Começa com a parte1
            rendered = fonte.render(parte1, True, cor_primeira)
            linha_atual = [rendered]
            largura_linha = rendered.get_width()

            if parte2:
                palavras = parte2.split()
                for palavra in palavras:
                    word_render = fonte.render(palavra, True, cor_restante)
                    word_width = word_render.get_width()

                    if largura_linha + espaco + word_width > largura_max:
                        # Salva a linha atual e começa uma nova
                        linhas.append(linha_atual)
                        linha_atual = [word_render]
                        largura_linha = word_width
                    else:
                        linha_atual.append(word_render)
                        largura_linha += espaco + word_width

            if linha_atual:
                linhas.append(linha_atual)

            # Calcula tamanho total da surface
            altura_linha = fonte.get_height()
            altura_total = altura_linha * len(linhas)
            largura_surface = largura_max

            surface_final = pygame.Surface((largura_surface, altura_total), pygame.SRCALPHA)

            # Blitando linhas
            y = 0
            for linha in linhas:
                x = 0
                for palavra in linha:
                    surface_final.blit(palavra, (x, y))
                    x += palavra.get_width() + espaco
                y += altura_linha

            return surface_final

        DadosExame.perda_de_fixacao_percentual = 0
        faixa_etaria = {
            1: "0 - 20",
            2: "21 - 30",
            3: "31 - 40",
            4: "41 - 50",
            5: "51 - 60",
            6: "61 - 70",
            7: "71 - 80",
            8: "81 - 90",
            9: "ACIMA 90",
        }
        faixa_md_chosen = 0
        faixa_md = [            
            "Normal ou alteração mínima",
            "Perda leve",
            "Perda moderada, ponto de atenção",
            "Perda severa",
            "Acima da média",
        ]
        faixa_psd_chosen = 0
        faixa_psd = [
            "Campo visual normal ou muito próximo do normal",
            "Leve irregularidade.",
            "Alterações moderadas",
            "Alterações graves / escotomas evidentes",
        ]
        estimulo = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}


        if DadosExame.md >= -2.0:
            faixa_md_chosen = 0
        if DadosExame.md >= -6.0 and DadosExame.md < -2.0:
            faixa_md_chosen = 1
        if DadosExame.md >= -10.0 and DadosExame.md < -6.0:
            faixa_md_chosen = 2
        if DadosExame.md < -10.0:
            faixa_md_chosen = 3
        if DadosExame.md > 0:
            faixa_md_chosen = 4

        if DadosExame.psd <= 2.0:
            faixa_psd_chosen = 0
        if DadosExame.psd <=3.0 and DadosExame.psd > 2.0:
            faixa_psd_chosen = 1
        if DadosExame.psd <=5.0 and DadosExame.psd > 3.0:
            faixa_psd_chosen = 2
        if DadosExame.psd > 5.0:
            faixa_psd_chosen = 3
            
        DadosExame.resultado_md = faixa_md[faixa_md_chosen]
        DadosExame.resultado_psd = faixa_psd[faixa_psd_chosen]

        def verifica_confiabilidade():
            bom, ruim, muito_ruim = 0, 0, 0

            if DadosExame.falso_positivo_respondidos_percentual <= 15:
                bom += 1
            if (
                DadosExame.falso_positivo_respondidos_percentual > 15
                and DadosExame.falso_positivo_respondidos_percentual <= 33
            ):
                ruim += 1
            elif DadosExame.falso_positivo_respondidos_percentual > 33:
                muito_ruim += 1

            if DadosExame.falso_negativo_respondidos_percentual <= 15:
                bom += 1
            if (
                DadosExame.falso_negativo_respondidos_percentual > 15
                and DadosExame.falso_negativo_respondidos_percentual <= 33
            ):
                ruim += 1
            elif DadosExame.falso_negativo_respondidos_percentual > 33:
                muito_ruim += 1

            if DadosExame.perda_de_fixacao_percentual <= 10:
                bom += 1
            if (
                DadosExame.perda_de_fixacao_percentual > 10
                and DadosExame.perda_de_fixacao_percentual <= 20
            ):
                ruim += 1
            elif DadosExame.perda_de_fixacao_percentual > 20:
                muito_ruim += 1

            # if bom == 3:
            #     DadosExame.confiabilidade = Constantes.confiavel
            # if ruim > 0 and muito_ruim < 2:
            #     DadosExame.confiabilidade = Constantes.questionavel
            # if muito_ruim == 2 or ruim == 3 or ruim == 2 and muito_ruim == 1:
            #     DadosExame.confiabilidade = Constantes.ruim
            # if muito_ruim == 3:
            #     DadosExame.confiabilidade = Constantes.nao_confiavel
            def confiabilidade_invertida():
                def pontuar(valor, lim_bom, lim_ruim):
                    if valor <= lim_bom:
                        return 0  # bom
                    elif valor <= lim_ruim:
                        return 50  # ruim
                    else:
                        return 100  # muito ruim

                pontos = []
                muito_ruim_flag = False

                # Calcula os pontos individuais
                for valor, lim_bom, lim_ruim in [
                    (DadosExame.falso_positivo_respondidos_percentual, 15, 33),
                    (DadosExame.falso_negativo_respondidos_percentual, 15, 33),
                    (DadosExame.perda_de_fixacao_percentual, 10, 20),
                ]:
                    p = pontuar(valor, lim_bom, lim_ruim)
                    pontos.append(p)
                    if p == 100:
                        muito_ruim_flag = True

                media = sum(pontos) / len(pontos)

                # Aumenta o peso da média se houver algum valor muito ruim
                if muito_ruim_flag:
                    media = media * 2.5  # aumenta a média em 25%
                    media = min(media, 100)  # limita a 100

                return round(media, 2)

            DadosExame.confiabilidade = confiabilidade_invertida()

            

        def gerar_resultado_final(faixa_psd,faixa_md,faixa_md_chosen,faixa_psd_chosen):         

            if DadosExame.confiabilidade == Constantes.nao_confiavel:
                interpretacao = "Resultado comprometido pela baixa confiabilidade."
            else:
                
                if (faixa_md_chosen == 0 or faixa_md_chosen == 4) and faixa_psd_chosen == 0:
                    interpretacao = "Campo visual dentro dos padrões de normalidade."
                elif (faixa_md_chosen != 0 or faixa_md_chosen != 4) and faixa_psd_chosen == 0:
                    interpretacao = f"Alteração difusa: {faixa_md[faixa_md_chosen]}."
                elif (faixa_md_chosen == 0 or faixa_md_chosen == 4) and faixa_psd_chosen != 0:
                    interpretacao = f"Presença de defeitos localizados: {faixa_psd[faixa_psd_chosen]}."
                else:
                    interpretacao = f"Alterações difusas e localizadas, MD: {faixa_md[faixa_md_chosen]}, PSD :{faixa_psd[faixa_psd_chosen]}."

            DadosExame.resultado_exame = interpretacao
            return interpretacao
        
        
        DadosExame.perda_de_fixacao_percentual = (
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
        verifica_confiabilidade()

        minutos, segundos = divmod((DadosExame.duracao_do_exame / 1000), 60)
        labels = [
            f"ID exame: {DadosExame.exame_id}",
            f"Programa:{DadosExame.programa_selecionado}",
            f"Falso positivo: {int(DadosExame.falso_positivo_respondidos)} / {int(DadosExame.total_testes_falsos_positivo)} ({DadosExame.falso_positivo_respondidos_percentual:.2f}%)",
            
            f"Olho: {DadosExame.olho}",
            f"Tamanho do estimulo: {estimulo.get(DadosExame.tamanho_estimulo)}",
            f"Falso negativo: {int(DadosExame.falso_negativo_respondidos)} / {int(DadosExame.total_testes_falsos_negativo)} ({DadosExame.falso_negativo_respondidos_percentual:.2f}%)",
            
            f"Exame: {DadosExame.exame_selecionado.upper()}",
            f"Duração (min): {int(minutos):02d}:{int(segundos):02d}",
            f"Perda de fixacao: {int(DadosExame.perda_de_fixacao)} / {int(DadosExame.total_testes_mancha)} ({DadosExame.perda_de_fixacao_percentual:.2f}%)",
            
            f"Faixa etária: {faixa_etaria.get(DadosExame.faixa_etaria)}",           
            f"Total de pontos: {DadosExame.total_de_pontos_testados}",
            f"Limiar Foveal: {int(DadosExame.LimiarFoveal)} (dB)",
        ]
        labels_valores = [ 
            f"MD:{DadosExame.md:.2f}", #f"MD:{DadosExame.md:.2f}  ({faixa_md[faixa_md_chosen]})",           
            f"Confiabilidade:{int(100 - DadosExame.confiabilidade)}%",        
            f"PSD:{DadosExame.psd:.2f}", #f"PSD:{DadosExame.psd:.2f}  ({faixa_psd[faixa_psd_chosen]})",
            # f"RESULTADO: {(gerar_resultado_final(faixa_psd,faixa_md,faixa_md_chosen,faixa_psd_chosen)).upper()}"
            ]

        # Configuração para desenhar labels em colunas de 3 com 4 linhas
        colunas = 3
        linhas = 4
        espacamento_x = 280  # Espaço entre colunas
        espacamento_y = 50  # Espaço entre linhas
        pos_x_inicial = 1020  # Posição inicial da primeira coluna
        pos_y_inicial = 50  # Posição inicial da primeira linha
        
        cor_resultado = (0,0,0)
        if (faixa_md_chosen == 0 or faixa_md_chosen == 4) and faixa_psd_chosen == 0:
            cor_resultado = cor_legenda_normal
        if (faixa_md_chosen != 0 and faixa_md_chosen != 4) or faixa_psd_chosen != 0:
            cor_resultado = cor_legenda_moderado
        if faixa_md_chosen == 3 or faixa_psd_chosen == 3:
            cor_resultado = cor_legenda_severo
            
        espacamento_x_valores = 450
        espacamento_y_valores = 80
        pos_x_inicial_valores = 1300  #1020
        pos_y_inicial_valores = 300
        fonte = pygame.font.Font(None, 28)
        image_md,image_psd,image_conf = ResultadoFullthreshold.plota_barra_indicativa_psd_md_confiabilidade()
        for i,texto in enumerate(labels_valores):
            coluna = i % 1
            linha = i // 1
            image = fonte.render("",True,(0,0,0))
            color_label_info = (0,0,0)
            
            if i == 0:
                # match faixa_md_chosen:
                #     case 0 | 4:  # Handles both cases 0 and 4
                #         color_label_info = cor_legenda_normal
                #     case 1:
                #         color_label_info = cor_legenda_leve
                #     case 2:
                #         color_label_info = cor_legenda_moderado
                #     case 3:
                #         color_label_info = cor_legenda_severo
                image = image_md
                

            if i == 1:
                # if DadosExame.confiabilidade == Constantes.confiavel:
                #     color_label_info = cor_legenda_normal
                # if DadosExame.confiabilidade == Constantes.questionavel:
                #     color_label_info = cor_legenda_leve
                # if DadosExame.confiabilidade == Constantes.ruim:
                #     color_label_info = cor_legenda_moderado
                # if DadosExame.confiabilidade == Constantes.nao_confiavel:
                #     color_label_info = cor_legenda_severo
                
                image = image_conf
            if i == 2:
                # match faixa_psd_chosen:
                #     case 0:
                #         color_label_info = cor_legenda_normal
                #     case 1:
                #         color_label_info = cor_legenda_leve
                #     case 2:
                #         color_label_info = cor_legenda_moderado
                #     case 3:
                #         color_label_info = cor_legenda_severo
                image = image_psd
            # if i == 3:
            #     color_label_info = cor_resultado
            
            pos_x = pos_x_inicial_valores + coluna * espacamento_x_valores
            pos_y = pos_y_inicial_valores + linha * espacamento_y_valores

            # Renderiza a label

            texto_renderizado = render_texto_colorido(fonte,texto.upper(),color_label_info)
            pygame.display.get_surface().blit(image, (pos_x , pos_y + 20))
            pygame.display.get_surface().blit(texto_renderizado, (pos_x, pos_y))
           

        fonte = pygame.font.Font(None, 26)
        for i, texto in enumerate(labels):
            # Calcula a posição da coluna e linha
            coluna = i % colunas
            linha = i // colunas

            # Define a cor do texto
            color_label_info = (0, 0, 0)
            if i == 2:
                if DadosExame.falso_positivo_respondidos_percentual <= 15:
                    color_label_info = (0, 0, 0)
                if (
                    DadosExame.falso_positivo_respondidos_percentual > 15
                    and DadosExame.falso_positivo_respondidos_percentual <= 20
                ):
                    color_label_info = cor_legenda_moderado
                elif DadosExame.falso_positivo_respondidos_percentual > 20:
                    color_label_info = cor_legenda_severo
            
            
            if i == 5:
                if DadosExame.falso_negativo_respondidos_percentual <= 15:
                    color_label_info = (0, 0, 0)
                if (
                    DadosExame.falso_negativo_respondidos_percentual > 15
                    and DadosExame.falso_negativo_respondidos_percentual <= 30
                ):
                    color_label_info = cor_legenda_moderado
                elif DadosExame.falso_negativo_respondidos_percentual > 30:
                    color_label_info = cor_legenda_severo

            if i == 8:
                if DadosExame.perda_de_fixacao_percentual <= 20:
                    color_label_info = (0, 0, 0)
                if (
                    DadosExame.perda_de_fixacao_percentual > 20
                    and DadosExame.perda_de_fixacao_percentual <= 30
                ):
                    color_label_info = cor_legenda_moderado
                elif DadosExame.perda_de_fixacao_percentual > 30:
                    color_label_info = cor_legenda_severo

           
            # Calcula a posição para desenhar
            pos_x = pos_x_inicial + coluna * espacamento_x
            pos_y = pos_y_inicial + linha * espacamento_y
            texto_renderizado = render_texto_colorido(fonte,texto.upper(),color_label_info)
            # Desenha a label na tela
            pygame.display.get_surface().blit(texto_renderizado, (pos_x, pos_y))

    @staticmethod
    def desenha_aviso_pdf():
        imagem = pygame.image.load(
            os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    "utils",
                    "images",
                    "warning_icon.png",
                )
            )
        )
        imagem = pygame.transform.scale(imagem, (59, 59))

        imagem_pos = (730, 950)
        x,y = imagem_pos
        fonte = pygame.font.Font(None, 38)
        texto_info_esc = fonte.render("ESC para voltar ao menu", True, (0, 0, 0))
        texto_info_esc_pos = (x + 80, y + 5)
        texto_info_entra = fonte.render("ENTRA para gerar o PDF", True, (0, 0, 0))
        texto_info_entra_pos = (x + 80, y + 35)
        pygame.display.get_surface().blit(texto_info_esc, texto_info_esc_pos)
        pygame.display.get_surface().blit(texto_info_entra, texto_info_entra_pos)
        pygame.display.get_surface().blit(imagem, imagem_pos)

    @staticmethod
    def status_resultado(carregado):
        """Mostra uma label temporária na tela e depois a apaga"""

        fonte = pygame.font.Font(None, 78)
        label = fonte.render("CARREGANDO MAPA...", True, (0, 0, 0), (255, 255, 255))
        label_rect = label.get_rect(center=(960, 540))

        if not carregado:
            # Desenha a label na tela
            pygame.display.get_surface().fill((255, 255, 255))
            pygame.display.get_surface().blit(label, label_rect)
            pygame.display.update()

        if carregado:
            pygame.draw.rect(
                pygame.display.get_surface(), (255, 255, 255), label_rect
            )  # Fundo preto (ajuste conforme necessário)
            pygame.display.update()

    @staticmethod
    def carregar_config(CONFIG_FILE, DEFAULT_CONFIG):
        """Lê as variáveis do arquivo JSON ou usa valores padrão."""
        if os.path.exists(
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", CONFIG_FILE))
        ):
            with open(
                os.path.abspath(
                    os.path.join(os.path.dirname(__file__), "..", CONFIG_FILE)
                ),
                "r",
            ) as f:
                return json.load(f)
        else:
            return DEFAULT_CONFIG

    @staticmethod
    def salvar_config(config, CONFIG_FILE):
        """Salva as variáveis no arquivo JSON."""
        with open(
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", CONFIG_FILE)),
            "w",
        ) as f:
            json.dump(config, f, indent=4)

    @staticmethod
    def plota_mapas():

        rect_mapas_desvio = pygame.Rect(0, 0, 912, 492)
        rect_mapas_desvio.center = (1920 / 2 + 200, 1080 / 2)

        image_desvio_padrao = pygame.image.load(
            os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    "utils",
                    "images",
                    "temp",
                    "desvio_padrao.png",
                )
            )
        )
        image_desvio_total = pygame.image.load(
            os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    "utils",
                    "images",
                    "temp",
                    "desvio_total.png",
                )
            )
        )
        image_bebie = pygame.image.load(
            os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    "utils",
                    "images",
                    "temp",
                    "bebie_curve.png",
                )
            )
        )
        x, y = rect_mapas_desvio.center

        rect_desvio_padrao = image_desvio_padrao.get_rect(center=(x - 300, y - 200))
        rect_desvio_total = image_desvio_total.get_rect(center=(x - 300, y + 200))
        rect_bebie = image_bebie.get_rect(center=(1450, 1080 / 2 + 250))

        fonte_legenda = pygame.font.Font(None, 30)
        legenda_desvio_padrao = fonte_legenda.render("Desvio padrão", True, (0, 0, 0))
        legenda_desvio_total = fonte_legenda.render("Desvio total", True, (0, 0, 0))

        legenda_desvio_padrao_pos = legenda_desvio_padrao.get_rect(
            center=(x - 300, y - 200 - 130)
        )
        legenda_desvio_total_pos = legenda_desvio_total.get_rect(
            center=(x - 300, y + 200 - 130)
        )

        pygame.display.get_surface().blit(image_desvio_padrao, rect_desvio_padrao)
        pygame.display.get_surface().blit(image_desvio_total, rect_desvio_total)
        pygame.display.get_surface().blit(image_bebie, rect_bebie)

        pygame.display.get_surface().blit(
            legenda_desvio_total, legenda_desvio_total_pos
        )
        pygame.display.get_surface().blit(
            legenda_desvio_padrao, legenda_desvio_padrao_pos
        )

    @staticmethod
    def exibir_resultados():
        ResultadoFullthreshold.status_resultado(carregado=False)
        ResultadoFullthreshold.gerar_mapa_desvios_e_curva_de_bebie()
        CONFIG_FILE = "config.json"

        DEFAULT_CONFIG = {
            "distancia_paciente": 200,
            "tamanho_estimulo": 3,
            "exame_id": 1,
            "background":120,
            "max_intensity": 255,
            "brightness":90,
            "contrast":50,
            "resolution-w":1920,
            "resolution-h":1080,
            "atenuacao":25,
        }
        config = ResultadoFullthreshold.carregar_config(CONFIG_FILE, DEFAULT_CONFIG)

        

        ResultadoFullthreshold.inicializar_matrizes()
        pygame.font.init()
        tempo_inicial = pygame.time.get_ticks()
        ResultadoFullthreshold.desenhar_mapa_texturas(firstload=True)
        tempo_final = pygame.time.get_ticks() - tempo_inicial
        ResultadoFullthreshold.desenhar_mapa_limiares()
        ResultadoFullthreshold.plota_mapas()
        ResultadoFullthreshold.desenha_legendas_exame()
        ResultadoFullthreshold.desenha_aviso_pdf()

        pygame.display.flip()
        visualizando = True              

        while visualizando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    visualizando = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:  # Mover para cima
                        ResultadoFullthreshold.mapa_cor = True
                        ResultadoFullthreshold.mapa_cinza = True
                        ResultadoFullthreshold.desenhar_mapa_texturas(firstload=False)
                        ResultadoFullthreshold.plota_mapas()
                        pygame.display.update()
                    elif event.key == pygame.K_g:  # Mover para baixo
                        ResultadoFullthreshold.mapa_cor = True
                        ResultadoFullthreshold.mapa_cinza = False
                        ResultadoFullthreshold.desenhar_mapa_texturas(firstload=False)
                        ResultadoFullthreshold.plota_mapas()
                        pygame.display.update()
                    elif event.key == pygame.K_0:
                        ResultadoFullthreshold.mapa_cor = False
                        ResultadoFullthreshold.desenhar_mapa_texturas(firstload=False)
                        ResultadoFullthreshold.plota_mapas()
                        pygame.display.update()
                    elif event.key == pygame.K_j:  # Tecla ESC para sair
                        visualizando = False
                        config["exame_id"] = (
                            (DadosExame.exame_id + 1)
                            if DadosExame.exame_id < 999
                            else 1
                        )  
                        config["distancia_paciente"] = DadosExame.distancia_paciente
                        config["tamanho_estimulo"] = DadosExame.tamanho_estimulo
                        ResultadoFullthreshold.salvar_config(config, CONFIG_FILE)
                        DadosExame.reset()                        

                    elif event.key == pygame.K_e:                                
                    
                        pdf = GerarPdf()
                        pdf.verifica_e_monta_pendrive()
                        caminho_pdf = f"/media/eyetec/EXAMES/relatorio-id-exame-{DadosExame.exame_id}.pdf"
                        caminho_pendrive = f"/media/eyetec/EXAMES/"
                      
                        if os.path.exists(caminho_pendrive):
                            pdf.gerar_relatorio(caminho_pdf)
                            fonte = pygame.font.Font(None, 45)
                            text_info_pdf = fonte.render(
                                "GERANDO PDF...", True, (0, 0, 0)
                            )
                            text_info_pdf_pos = text_info_pdf.get_rect()
                            text_info_pdf_pos.center = (1920 // 2, 1080 // 2)
                            pygame.display.get_surface().blit(
                                text_info_pdf, text_info_pdf_pos
                            )
                            pygame.display.update()
                            pygame.time.delay(7000)
                            if os.path.exists(caminho_pdf):
                                rect_dash = text_info_pdf.get_rect()
                                rect_dash.center = text_info_pdf_pos.center
                                pygame.draw.rect(
                                    pygame.display.get_surface(),
                                    pygame.Color("white"),
                                    rect_dash,
                                )
                                pygame.display.update()
                                text_info_pdf = fonte.render(
                                    "PDF GERADO!", True, (0, 0, 0)
                                )
                                pygame.display.update()
                                pygame.time.delay(3000)
                                pygame.draw.rect(
                                    pygame.display.get_surface(),
                                    pygame.Color("white"),
                                    rect_dash,
                                )
                                pygame.display.update()
                                
                            else:
                                fonte = pygame.font.Font(None, 45)
                                text_info_pdf = fonte.render(
                                    "ERRO AO GERAR PDF,TENTE NOVAMENTE!",
                                    True,
                                    (0, 0, 0),
                                )
                                text_info_pdf_pos = text_info_pdf.get_rect()
                                text_info_pdf_pos.center = (1920 // 2, 1080 // 2)
                                pygame.display.get_surface().blit(
                                    text_info_pdf, text_info_pdf_pos
                                )
                                pygame.display.update()
                                pygame.time.delay(5000)
                                rect_dash = text_info_pdf.get_rect()
                                rect_dash.center = text_info_pdf_pos.center
                                pygame.draw.rect(
                                    pygame.display.get_surface(),
                                    pygame.Color("white"),
                                    rect_dash,
                                )
                                pygame.display.update()
                        else:
                            fonte = pygame.font.Font(None, 45)
                            text_info_pdf = fonte.render(
                                "ERRO AO GERAR PDF, PENDRIVE NAO RECONHECIDO!",
                                True,
                                (0, 0, 0),
                            )
                            text_info_pdf_pos = text_info_pdf.get_rect()
                            text_info_pdf_pos.center = (1920 // 2, 1080 // 2)
                            pygame.display.get_surface().blit(
                                text_info_pdf, text_info_pdf_pos
                            )
                            pygame.display.update()
                            pygame.time.delay(5000)
                            rect_dash = text_info_pdf.get_rect()
                            rect_dash.center = text_info_pdf_pos.center
                            pygame.draw.rect(
                                pygame.display.get_surface(),
                                pygame.Color("white"),
                                rect_dash,
                            )
                            pygame.display.update()

        DadosExame.reset()


if __name__ == "__main__":
    from cordenadas_24OD import cordenadas_24OD
    from cordenadas_10 import cordenadas_10
    from converte_atenuacao_txt import read_file_to_list
    from termometro import gerar_barra_com_indicador
    atenuacoes = read_file_to_list(
        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), "..", "atenuacao_teste", "exame.txt"
            )
        ),
        7,
    )
    DadosExame.faixa_etaria = 4


    DadosExame.perda_de_fixacao = 1
    DadosExame.total_testes_mancha = 5
    DadosExame.falso_positivo_respondidos = 1
    DadosExame.falso_negativo_respondidos = 5
    DadosExame.total_testes_falsos_positivo = 10
    DadosExame.total_testes_falsos_negativo = 10

    DadosExame.exame_selecionado = Constantes.fullthreshold
    DadosExame.programa_selecionado = Constantes.central24
    DadosExame.olho = Constantes.olho_direito

    pygame.init()
    pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    pygame.display.get_surface().fill((255, 255, 255))
    pygame.display.update()
    
    for (x, y), atenuacao in zip(cordenadas_24OD, atenuacoes):
        ponto = Ponto(x, y, 3, (0, 0, 0), 200)
        ponto.atenuacao = atenuacao
        DadosExame.matriz_pontos.append(ponto)

    ResultadoFullthreshold.exibir_resultados()
