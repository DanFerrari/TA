import pygame, random, time, os, sys, math
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
from atenuacoes_personalizadas import atenuacoes_personalizadas


class ResultadoFullthreshold:


    
    @staticmethod
    def gerar_pontos_mapa_textura():
        matriz = []
        for ponto in DadosExame.matriz_pontos:
            ponto_novo = Ponto(0,0,1,(0,0,0))
            if (ponto.xg, ponto.yg) in atenuacoes_personalizadas:
                ponto_novo.atenuacao = atenuacoes_personalizadas[(ponto.xg, ponto.yg)]

            ponto_novo.x = int(ponto.x * 960 / 1920)
            ponto_novo.y = int(ponto.y * 540 / 1080)
            matriz.append(ponto_novo)
        return matriz
    @staticmethod
    def gerar_pontos_mapa_limiar():
        matriz = []
        for ponto in DadosExame.matriz_pontos:
            ponto_novo = Ponto(0,0,0.5,(0,0,0))
            if (ponto.xg, ponto.yg) in atenuacoes_personalizadas:
                ponto_novo.atenuacao = atenuacoes_personalizadas[(ponto.xg, ponto.yg)]
            ponto_novo.x = int(ponto.x * 960 / 1920)
            ponto_novo.y = int(ponto.y * 540 / 1080)
            ponto_novo.y += 540 
            matriz.append(ponto_novo)
        return matriz
    
    
    
    mapa_cor = True
    mapa_cinza = True        
    matriz_pontos_mapa_textura = None
    matriz_pontos_mapa_limiar = None

    @staticmethod
    def inicializar_matrizes():
        ResultadoFullthreshold.matriz_pontos_mapa_textura = ResultadoFullthreshold.gerar_pontos_mapa_textura()
        ResultadoFullthreshold.matriz_pontos_mapa_limiar = ResultadoFullthreshold.gerar_pontos_mapa_limiar()
    
    

    @staticmethod
    def calcular_atenuacao_interpolada(x, y, kdtree, pontos):
        """Interpola a atenuação dentro da célula suavizando a transição para as vizinhas"""
        dists, indices = kdtree.query((x, y), k=min(10, len(pontos)))

        if len(indices) == 0:
            return 0

        pesos = np.exp(-np.array(dists) / 10)

        pesos /= pesos.sum()

        atenuacao_interpolada = sum(
            pesos[i] * pontos[indices[i]].atenuacao for i in range(len(indices))
        )
        atenuacao_interpolada = round(atenuacao_interpolada, 1)
        return atenuacao_interpolada

    
    
    
    @staticmethod
    def estrutura_legenda(texturas):       

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
            (centro_x + 280, centro_y - 150, largura, altura),
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
                    "41 - 50"
                    ]

        if ResultadoFullthreshold.mapa_cor:
            for i,rect in enumerate(textura_rect):                
                pygame.draw.rect(pygame.display.get_surface(), texturas[i], textura_rect[i])
                pygame.display.get_surface().blit(fonte.render(texto_medidas[i],True,(0,0,0)), ( (lambda: rect[0])() + 50, (lambda:rect[1])() + 7.5) )
        else:
            for k,rect in enumerate(textura_rect):
                pygame.display.get_surface().blit(fonte.render(texto_medidas[k],True,(0,0,0)), ( (lambda: rect[0])() + 50, (lambda:rect[1])() + 7.5) )
                borda = (rect[0] - 1 , rect[1] - 1, rect[2] + 2, rect[3] + 2)
                pygame.draw.rect(pygame.display.get_surface(), pygame.Color("black"), borda, 2)
                    
                for i in range(0,largura,5):
                    for j in range(0,altura,5):
                        pos_x = rect[0] + i
                        pos_y = rect[1] + j
                        pygame.display.get_surface().blit(texturas[k], (pos_x,pos_y))       

    @staticmethod
    def gerar_legenda_pontos():
        texturas = [pygame.image.load(f"campimetria/utils/images/bitmaps/{i}.bmp").convert() for i in range(1,11)]        
        ResultadoFullthreshold.estrutura_legenda(texturas)


    @staticmethod
    def gerar_legenda_cores():
        
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
                    (255, 0, 0)
                    ]

        ResultadoFullthreshold.estrutura_legenda(texturas)
    
    
    def gerar_legenda_tons_cinza():
        texturas = []
        for i in range(0, 10):
            texturas.append((25 * i, 25 * i, 25 * i))
        ResultadoFullthreshold.estrutura_legenda(texturas)
       
       
    @staticmethod
    def gerar_texturas_coloridas(atenuacao):
        """Mapeia atenuação para um gradiente de cores passando por vermelho, amarelo, verde e azul"""
        if atenuacao <= 0:
            vermelho = 0
            verde = 0
            azul = 156
        elif atenuacao < 6:
            vermelho = 0
            verde = 85
            azul = 204
        elif atenuacao < 11:
            vermelho = 0
            verde = 131
            azul = 207
        elif atenuacao < 16:
            vermelho = 2
            verde = 147
            azul = 166
        elif atenuacao < 21:
            vermelho = 0
            verde = 145
            azul = 107
        elif atenuacao < 26:
            vermelho = 0
            verde = 163
            azul = 87
        elif atenuacao < 31:
            vermelho = 149
            verde = 201
            azul = 28
        elif atenuacao < 36:
            vermelho = 252
            verde = 219
            azul = 0
        elif atenuacao < 41:
            vermelho = 232
            verde = 129
            azul = 26
        elif atenuacao < 50:
            vermelho = 255
            verde = 0
            azul = 0

        return (vermelho, verde, azul)
        
    @staticmethod
    def gerar_texturas_pontos(atenuacao):
        texturas = []
        for i in range(1, 11):
            caminho = f"campimetria/utils/images/bitmaps/{i}.bmp"
            texturas.append(pygame.image.load(caminho).convert())
           

        if atenuacao <= 0:
            cor = texturas[0]
        elif atenuacao < 6:
            cor = texturas[1]
        elif atenuacao < 11:
            cor = texturas[2]
        elif atenuacao < 16:
            cor = texturas[3]
        elif atenuacao < 21:
            cor = texturas[4]
        elif atenuacao < 26:
            cor = texturas[5]
        elif atenuacao < 31:
            cor = texturas[6]
        elif atenuacao < 36:
            cor = texturas[7]
        elif atenuacao < 41:
            cor = texturas[8]
        elif atenuacao < 50:
            cor = texturas[9]

        return cor

    @staticmethod
    def gerar_texturas_cinza(atenuacao):
        texturas = []
        for i in range(0, 10):
            texturas.append((25 * i, 25 * i, 25 * i))

        if atenuacao <= 0:
            cor = texturas[0]
        elif atenuacao < 6:
            cor = texturas[1]
        elif atenuacao < 11:
            cor = texturas[2]
        elif atenuacao < 16:
            cor = texturas[3]
        elif atenuacao < 21:
            cor = texturas[4]
        elif atenuacao < 26:
            cor = texturas[5]
        elif atenuacao < 31:
            cor = texturas[6]
        elif atenuacao < 36:
            cor = texturas[7]
        elif atenuacao < 41:
            cor = texturas[8]
        else:
            cor = texturas[9]

        return cor

    @staticmethod
    def desenhar_mapa_texturas():
        """Desenha o mapa com otimização de desempenho"""
       
        
        buffer = pygame.Surface((960, 540))  # Usa um buffer para melhorar a performance
        buffer.fill((255, 255, 255))
        
        
        centro_x, centro_y = 960 // 2, 540 // 2
        raio = min(centro_x, centro_y) - 55
        kdtree = KDTree([(p.x, p.y) for p in ResultadoFullthreshold.matriz_pontos_mapa_textura])
        atenuacoes_cache = {}
        step = 2 if ResultadoFullthreshold.mapa_cor else 5

        for x in range(0, 960, step):
            for y in range(0, 540, step):
                if (x - centro_x) ** 2 + (y - centro_y) ** 2 <= raio**2:
                    if (x, y) in atenuacoes_cache:
                        atenuacao_interpolada = atenuacoes_cache[(x, y)]
                    else:
                        atenuacao_interpolada = (
                            ResultadoFullthreshold.calcular_atenuacao_interpolada(
                                x, y, kdtree, ResultadoFullthreshold.matriz_pontos_mapa_textura
                            )
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
                        pygame.draw.rect(
                            buffer, cor, (x, y, step, step)
                        )  # Desenha blocos em vez de pixels individuais
                    else:
                        cor = ResultadoFullthreshold.gerar_texturas_pontos(
                            atenuacao_interpolada
                        )
                        buffer.blit(cor, (x, y))

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
        pygame.display.get_surface().blit(buffer, (0, 0))
        ResultadoFullthreshold.gerar_legenda_textura()
   

    @staticmethod
    def gerar_legenda_textura():
       
        if ResultadoFullthreshold.mapa_cor:
            if ResultadoFullthreshold.mapa_cinza:
                ResultadoFullthreshold.gerar_legenda_tons_cinza()
                pygame.display.update()
            else:
                ResultadoFullthreshold.gerar_legenda_cores()
        else:
            ResultadoFullthreshold.gerar_legenda_pontos()
                    


    @staticmethod
    def desenhar_mapa_limiares():
        fonte = pygame.font.Font(None, 18)
        # Desenhar pontos e labels
        for ponto in ResultadoFullthreshold.matriz_pontos_mapa_limiar:            
            ponto.plotarPonto()
            label = fonte.render(f"{ponto.atenuacao}", True, (0, 0, 0))
            label_rect = label.get_rect(center=(ponto.x - 0.505, ponto.y + 12))
            pygame.display.get_surface().blit(label, label_rect)
        
        # circulo do mapa de limiar
        pygame.draw.circle(pygame.display.get_surface(), (0, 0, 0), (480, 810), 230, 1)
        
        #cruz do mapa
        pygame.draw.line(
            pygame.display.get_surface(),
            (0, 0, 0),
            (480 + 230, 810),
            (480 - 230, 810),
            1,
        )
        pygame.draw.line(
            pygame.display.get_surface(),
            (0, 0, 0),
            (480, 810 + 230),
            (480, 810 - 230),
            1,
        )

    @staticmethod
    def desenha_legendas_exame():

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
        ResultadoFullthreshold.inicializar_matrizes()
        pygame.font.init()
        pygame.display.get_surface().fill((255,255,255))
        pygame.display.update()
        tempo_inicial = pygame.time.get_ticks()
        ResultadoFullthreshold.desenhar_mapa_texturas()
        tempo_final = pygame.time.get_ticks() - tempo_inicial       
        ResultadoFullthreshold.desenhar_mapa_limiares()
        ResultadoFullthreshold.desenha_legendas_exame()
        pygame.display.update()
        visualizando = True
        while visualizando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    visualizando = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:  # Mover para cima
                        ResultadoFullthreshold.mapa_cor = True
                        ResultadoFullthreshold.mapa_cinza = True
                        ResultadoFullthreshold.desenhar_mapa_texturas()
                        pygame.display.update()
                    elif event.key == pygame.K_DOWN:  # Mover para baixo
                        ResultadoFullthreshold.mapa_cor = True
                        ResultadoFullthreshold.mapa_cinza = False
                        ResultadoFullthreshold.desenhar_mapa_texturas()
                        pygame.display.update()
                    elif event.key == pygame.K_RIGHT:
                        ResultadoFullthreshold.mapa_cor = False                        
                        ResultadoFullthreshold.desenhar_mapa_texturas()
                        pygame.display.update()
                    elif event.key == pygame.K_ESCAPE:  # Tecla ESC para sair
                        visualizando = False    
                        pygame.quit()   
                

        DadosExame.reset()

