import pygame, random, time, os, sys, math
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


class ResultadoScreening:
    @staticmethod
    def desenha_legendas():
         #exame 
        #duracao do exame
        #total de pontos
        #limiar foveal
        #colocar legenda
        #falso positivo
        #falso negativo
        
        perda_fixacao = 0
        perda_fixacao = (
            (DadosExame.perda_de_fixacao / DadosExame.total_testes_mancha) * 100
            if perda_fixacao > 0.0
            else 0
        )
        
        DadosExame.falso_negativo_respondidos_percentual = DadosExame.falso_negativo_respondidos / DadosExame.total_testes_falsos_negativo * 100 if DadosExame.falso_negativo_respondidos > 0 else 0
        DadosExame.falso_positivo_respondidos_percentual = DadosExame.falso_positivo_respondidos / DadosExame.total_testes_falsos_positivo  * 100 if DadosExame.falso_positivo_respondidos > 0 else 0
        DadosExame.duracao_do_exame = (DadosExame.duracao_do_exame / 1000) / 60
        
        labels = [f"Exame: {DadosExame.exame_selecionado}", f"Duracao do exame:{DadosExame.duracao_do_exame}", f"Total de pontos:76", f"Falso positivo:{DadosExame.falso_positivo_respondidos} / {DadosExame.total_testes_falsos_positivo} ({DadosExame.falso_positivo_respondidos_percentual}%)", f"Falso negativo:{DadosExame.falso_negativo_respondidos} / {DadosExame.total_testes_falsos_negativo} ({DadosExame.falso_negativo_respondidos_percentual}%)", f"Perda de fixacao:{int(DadosExame.perda_de_fixacao)} / {DadosExame.total_testes_mancha} ({perda_fixacao}%)"]

        

        # Posição inicial para desenhar labels (quadrante direito)
        pos_x = 1920 * 3 // 4  # 75% da largura (centro do quadrante direito)
        pos_y = 25  # Começa no meio da tela
        espacamento = 150  # Espaço entre as labels
        fonte = pygame.font.Font(None, 30)
        for i, texto in enumerate(labels):
            # Renderiza a label
            texto_renderizado = fonte.render(texto, True, (0,0,0))

            # Posiciona centralizado no quadrante direito
            pygame.display.get_surface().blit(texto_renderizado, (pos_x - texto_renderizado.get_width() // 2, pos_y + i * espacamento))


        



      
        
    @staticmethod
    def desenha_pontos():
        pygame.display.get_surface().fill(pygame.Color("white"))
        perda_fixacao = 0.0
        LARGURA, ALTURA = 1920, 1080  # Tela original
        nova_largura, nova_altura = 960, 540  # Nova tela
        pygame.draw.rect(pygame.display.get_surface(), pygame.Color("black"), (0, 0, 960, 540), 1, 0)
        pygame.draw.rect(pygame.display.get_surface(), pygame.Color("black"), (0,540, 960, 540), 1, 0)
        pygame.draw.rect(pygame.display.get_surface(), pygame.Color("black"), (960, 0, 960, 540), 1, 0)
        pygame.draw.rect(pygame.display.get_surface(), pygame.Color("black"), (960, 540, 960, 540), 1, 0)
        
        pontos_ajustados = DadosExame.matriz_pontos
        for ponto in pontos_ajustados:                       
            ponto.x = int(ponto.x * nova_largura / LARGURA)  # Reduzindo a coordenada X
            ponto.y = int(ponto.y * nova_altura / ALTURA)  # Reduzindo a coordenada Y
            if ponto.response_received:
                ponto.cor = pygame.Color("green")
                ponto.plotarPonto()
            elif not ponto.response_received:
                ponto.cor = pygame.Color("red")
                ponto.plotarPonto()
                
                
        for ponto in pontos_ajustados:
            if ponto.response_received:
                ponto.atenuacao = 25
            else:
                ponto.atenuacao = 0
            fonte = pygame.font.Font(None, 20)
            texto = fonte.render(f"{ponto.atenuacao}", True, (0,0,0))  
            
            
            ponto.y += ALTURA//2  
            pygame.display.get_surface().blit(texto, (ponto.x,ponto.y))



        ResultadoScreening.desenha_legendas()

       
        pygame.display.flip()
        visualizando = True
        while visualizando:
            for evento in pygame.event.get():
                if (
                    evento.type == pygame.QUIT
                    or evento.type == pygame.KEYDOWN
                    and evento.key == pygame.K_ESCAPE
                ):
                    visualizando = False
        