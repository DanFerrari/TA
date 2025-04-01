import pygame, random, time, os, sys, math,json
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
from gerar_pdf import GerarPdf



class ResultadoFullthreshold:
    
    

    
    @staticmethod
    def gerar_pontos_mapa_textura():
        matriz = []
        for ponto in DadosExame.matriz_pontos:
            ponto_novo = Ponto(ponto.xg,ponto.yg,tamanhoPonto = 3, cor = (0,0,0), distancia = 200)
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
            ponto_novo = Ponto(ponto.xg,ponto.yg,tamanhoPonto = 3, cor = (0,0,0), distancia = 200)
            ponto_novo.raio_ponto = 6
            ponto_novo.pontoPix = 4  
            ponto_novo.x = int(ponto_novo.x * 960 / 1920)
            ponto_novo.y = int(ponto_novo.y * 540 / 1080)
            ponto_novo.y += 540 
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
            caminho = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils', 'images', 'bitmaps', f"{i}.bmp"))
            if os.path.exists(caminho):
                ResultadoFullthreshold.textura_cache.append(pygame.image.load(caminho).convert())


    @staticmethod
    def inicializar_matrizes():
        ResultadoFullthreshold.matriz_pontos_mapa_textura = ResultadoFullthreshold.gerar_pontos_mapa_textura()
        ResultadoFullthreshold.matriz_pontos_mapa_limiar = ResultadoFullthreshold.gerar_pontos_mapa_limiar()
    
    

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
        atenuacao_interpolada = np.dot(pesos, [pontos[idx].atenuacao for idx in indices])

        return round(atenuacao_interpolada, 1)

    
    
    @staticmethod
    def mostrar_label_temporaria(carregado):
        """Mostra uma label temporária na tela e depois a apaga"""
        fonte = pygame.font.Font(None, 36)
        label = fonte.render("CARREGANDO MAPA...", True, (0, 0, 0),(255,255,255))  
        label_rect = label.get_rect(center=(480,540))

        if not carregado:
            # Desenha a label na tela
            pygame.display.get_surface().blit(label, label_rect)
            pygame.display.update()

        if carregado:
            pygame.draw.rect(pygame.display.get_surface(), (255, 255, 255), label_rect)  # Fundo preto (ajuste conforme necessário)
            pygame.display.update()
        
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
        texturas = []
        for i in range(1, 10):
            caminho = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils', 'images', 'bitmaps',f"{i}.bmp"))
            if os.path.exists(caminho):
                texturas.append(pygame.image.load(caminho).convert())
            else:
                print(f"caminho nao existe: {caminho}")       
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
                    # (255, 0, 0)
                    ]

        ResultadoFullthreshold.estrutura_legenda(texturas)
    
    
    def gerar_legenda_tons_cinza():
        
        texturas = [          
            (0,0,0),
            (25,25,25),
            (50,50,50),
            (75,75,75),
            (100,100,100),
            (125,125,125),
            (150,150,150),
            (170,170,170),
            (210,210,210),        
            # (225,225,225)
        ]
        
        
        ResultadoFullthreshold.estrutura_legenda(texturas)
       
       
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
            cor = (0,0,0)
        elif atenuacao < 6:
            cor = (25,25,25)
        elif atenuacao < 11:
            cor = (50,50,50)
        elif atenuacao < 16:
            cor = (75,75,75)
        elif atenuacao < 21:
            cor = (100,100,100)
        elif atenuacao < 26:
            cor = (125,125,125)
        elif atenuacao < 31:
            cor = (150,150,150)
        elif atenuacao < 36:
            cor = (170,170,170)
        elif atenuacao < 41:
            cor = (210,210,210)
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
        kdtree = KDTree([(p.x, p.y) for p in ResultadoFullthreshold.matriz_pontos_mapa_textura])
        atenuacoes_cache = {}
        step = 5 if ResultadoFullthreshold.mapa_cor else 5
        pixels = []
        for x in range(0, 960, step):
            for y in range(0, 540, step):
                if (x - centro_x) ** 2 + (y - centro_y) ** 2 <= raio**2:
                    atenuacao_interpolada = atenuacoes_cache.get(
                        (x, y),
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
                        pixels.append((x,y,cor))
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
        pygame.display.get_surface().blit(buffer, (0, 0))
        ResultadoFullthreshold.gerar_legenda_textura()
        if not firstload:
            ResultadoFullthreshold.mostrar_label_temporaria(True)
        else:
            ResultadoFullthreshold.status_resultado( carregado = True)
   

    @staticmethod
    def gerar_legenda_textura():
       
        if ResultadoFullthreshold.mapa_cor:
            if ResultadoFullthreshold.mapa_cinza:
                ResultadoFullthreshold.gerar_legenda_tons_cinza()
               
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
            label = fonte.render(f"{int(ponto.atenuacao)}", True, (0, 0, 0))
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
        
        minutos,segundos = divmod((DadosExame.duracao_do_exame / 1000),60)
        labels = [
            f"Exame: {DadosExame.exame_selecionado.upper()}",
            f"Olho: {DadosExame.olho}",
            f"Duração (min): {int(minutos)}:{int(segundos)}",
            f"Total de pontos: {DadosExame.total_de_pontos_testados}",
            f"Falso positivo: {int(DadosExame.falso_positivo_respondidos)} / {int(DadosExame.total_testes_falsos_positivo)} ({DadosExame.falso_positivo_respondidos_percentual:.2f}%)",
            f"Falso negativo: {int(DadosExame.falso_negativo_respondidos)} / {int(DadosExame.total_testes_falsos_negativo)} ({DadosExame.falso_negativo_respondidos_percentual:.2f}%)",
            f"Perda de fixacao: {int(DadosExame.perda_de_fixacao)} / {int(DadosExame.total_testes_mancha)} ({perda_fixacao:.2f}%)",
            f"Limiar Foveal:{int(DadosExame.LimiarFoveal)}(dB)",
            
        ]

        # Posição inicial para desenhar labels (quadrante direito)
        pos_x = 1165  # 75% da largura (centro do quadrante direito)
        pos_y = 92  # Começa no meio da tela
        espacamento = 50  # Espaço entre as labels
        fonte = pygame.font.Font(None, 30)
        color_label_info = (0, 0, 0)

        for i, texto in enumerate(labels):
            # Renderiza a label
            color_label_info = (0, 0, 0)
            if (
                i == 4
                and DadosExame.falso_positivo_respondidos_percentual > 33
                or i == 5
                and DadosExame.falso_negativo_respondidos_percentual > 33
                or i == 6
                and perda_fixacao > 33
            ):
                color_label_info = pygame.Color("red")

            texto_renderizado = fonte.render(texto, True, color_label_info)

            # Posiciona centralizado no quadrante direito
            pygame.display.get_surface().blit(
                texto_renderizado, (pos_x, pos_y + i * espacamento)
            )
            
    @staticmethod
    def desenha_elementos_botao_pdf():
        imagem = pygame.image.load(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils", "images","warning_icon.png")))
        imagem = pygame.transform.scale(imagem, (59, 59))  
        imagem_pos = (1165,795)
        
        fonte = pygame.font.Font(None, 32)
        texto_info_esc = fonte.render("ESC para voltar ao menu",True,(0,0,0))
        texto_info_esc_pos = (1256,800)
        texto_info_entra= fonte.render("ENTRA para gerar o PDF",True,(0,0,0))
        texto_info_entra_pos = (1256,830)
        pygame.display.get_surface().blit(texto_info_esc,texto_info_esc_pos)
        pygame.display.get_surface().blit(texto_info_entra,texto_info_entra_pos)
        pygame.display.get_surface().blit(imagem,imagem_pos)
        
        rect_buton_pdf = pygame.Rect(1165,966,492,81)
        pygame.draw.rect(pygame.display.get_surface(),(209,41,41),rect_buton_pdf,border_radius=15)
        pygame.draw.rect(pygame.display.get_surface(),(255,247,28),rect_buton_pdf,5,border_radius=15)
        button_pdf_text = fonte.render("Gerar PDF",True,(255,255,255))
        button_pdf_text_pos = button_pdf_text.get_rect()
        button_pdf_text_pos.center = rect_buton_pdf.center
        pygame.display.get_surface().blit(button_pdf_text,button_pdf_text_pos)
         

    @staticmethod
    def status_resultado(carregado):
        """Mostra uma label temporária na tela e depois a apaga"""
        
        fonte = pygame.font.Font(None, 78)
        label = fonte.render("CARREGANDO MAPA...", True, (0, 0, 0),(255,255,255))  
        label_rect = label.get_rect(center=(960,540))

        if not carregado:
            # Desenha a label na tela
            pygame.display.get_surface().fill((255,255,255))
            pygame.display.get_surface().blit(label, label_rect)
            pygame.display.update()

        if  carregado:
            pygame.draw.rect(pygame.display.get_surface(), (255, 255, 255), label_rect)  # Fundo preto (ajuste conforme necessário)
            pygame.display.update()




     
    @staticmethod
    def carregar_config(CONFIG_FILE,DEFAULT_CONFIG):
        """Lê as variáveis do arquivo JSON ou usa valores padrão."""
        if os.path.exists(os.path.abspath(os.path.join(os.path.dirname(__file__), "..",CONFIG_FILE))):
            with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "..",CONFIG_FILE)), "r") as f:
                return json.load(f)
        else:
            return DEFAULT_CONFIG
    @staticmethod
    def salvar_config(config,CONFIG_FILE):
        """Salva as variáveis no arquivo JSON."""
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "..",CONFIG_FILE)), "w") as f:
            json.dump(config, f, indent=4)




    @staticmethod
    def exibir_resultados():
        CONFIG_FILE = "config.json"

        DEFAULT_CONFIG ={
            "distancia_paciente":200,
            "tamanho_estimulo":3,
            "exame_id":1
        }
        config = ResultadoFullthreshold.carregar_config(CONFIG_FILE,DEFAULT_CONFIG)      

        DadosExame.exame_id = config["exame_id"]

        
        
        
        
        
        ResultadoFullthreshold.inicializar_matrizes()
        pygame.font.init()
        ResultadoFullthreshold.status_resultado(carregado=False)      
        tempo_inicial = pygame.time.get_ticks()
        ResultadoFullthreshold.desenhar_mapa_texturas(firstload=True)
        tempo_final = pygame.time.get_ticks() - tempo_inicial       
        ResultadoFullthreshold.desenhar_mapa_limiares()
        ResultadoFullthreshold.desenha_legendas_exame()
        print(tempo_final / 1000)
        ResultadoFullthreshold.desenha_elementos_botao_pdf()
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
                        pygame.display.update()
                    elif event.key == pygame.K_g:  # Mover para baixo
                        ResultadoFullthreshold.mapa_cor = True
                        ResultadoFullthreshold.mapa_cinza = False
                        ResultadoFullthreshold.desenhar_mapa_texturas(firstload=False)
                        pygame.display.update()
                    elif event.key == pygame.K_0:
                        ResultadoFullthreshold.mapa_cor = False                        
                        ResultadoFullthreshold.desenhar_mapa_texturas(firstload=False)
                        pygame.display.update()
                    elif event.key == pygame.K_j:  # Tecla ESC para sair
                        visualizando = False
                        DadosExame.reset()
                        config["exame_id"] = (DadosExame.exame_id + 1) if DadosExame.exame_id < 999 else 1
                        config["distancia_paciente"] = DadosExame.distancia_paciente
                        config["tamanho_estimulo"] = DadosExame.tamanho_estimulo
                        ResultadoFullthreshold.salvar_config(config,CONFIG_FILE)
                        
                    elif event.key == pygame.K_e:
                        config["exame_id"] = (DadosExame.exame_id + 1) if DadosExame.exame_id < 999 else 1
                        config["distancia_paciente"] = DadosExame.distancia_paciente
                        config["tamanho_estimulo"] = DadosExame.tamanho_estimulo                        
                        ResultadoFullthreshold.salvar_config(config,CONFIG_FILE)
                        pdf = GerarPdf()
                        
                        caminho_pdf = f"/media/orangepi/EXAMES/relatorio-id-exame-{DadosExame.exame_id}.pdf"
                        caminho_pendrive = f"/media/orangepi/EXAMES/"
                        if os.path.exists(caminho_pendrive):
                            pdf.gerar_relatorio(caminho_pdf)
                            fonte = pygame.font.Font(None, 45)
                            text_info_pdf = fonte.render("PDF GERADO! RETORNANDO AO MENU...",True,(0,0,0))                          
                            text_info_pdf_pos = text_info_pdf.get_rect()
                            text_info_pdf_pos.center = (1920//2,1080//2)
                            pygame.display.get_surface().blit(text_info_pdf,text_info_pdf_pos)
                            pygame.display.update()
                            visualizando = False
                            pygame.time.delay(5000)
                        else:
                            fonte = pygame.font.Font(None, 45)
                            text_info_pdf = fonte.render("ERRO AO GERAR PDF, VERIFIQUE SEU PENDRIVE!",True,(0,0,0))                          
                            text_info_pdf_pos = text_info_pdf.get_rect()
                            text_info_pdf_pos.center = (1920//2,1080//2)
                            pygame.display.get_surface().blit(text_info_pdf,text_info_pdf_pos)
                            pygame.display.update()
                            pygame.time.delay(5000)
                            rect_dash = text_info_pdf.get_rect()
                            rect_dash.center = text_info_pdf_pos.center
                            pygame.draw.rect(pygame.display.get_surface(),pygame.Color("white"),rect_dash)
                            pygame.display.update()
                        
                

        DadosExame.reset()



if __name__ == "__main__":
    from cordenadas_30 import cordenadas_30
    from atenuacoes_personalizadas import atenuacoes_personalizadas
    pygame.init()
    pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    DadosExame.matriz_pontos = [Ponto(x,y,tamanhoPonto = 3,cor = (0,0,0), distancia = 100) for x,y in cordenadas_30]
    for ponto in DadosExame.matriz_pontos:
        ponto.atenuacao = atenuacoes_personalizadas.get((ponto.xg,ponto.yg))
    ResultadoFullthreshold.exibir_resultados()