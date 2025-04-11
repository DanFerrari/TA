import pygame, random, time, os, sys, math,json


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


class ResultadoScreening:
    @staticmethod
    def desenha_legendas():

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
        
 
        estimulo = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}

     
            
     

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

            if bom == 3:
                DadosExame.confiabilidade = Constantes.confiavel
            if ruim > 0 and muito_ruim < 2:
                DadosExame.confiabilidade = Constantes.questionavel
            if muito_ruim == 2 or ruim == 3 or ruim == 2 and muito_ruim == 1:
                DadosExame.confiabilidade = Constantes.ruim
            if muito_ruim == 3:
                DadosExame.confiabilidade = Constantes.nao_confiavel
            

        def gerar_resultado_final():         

            if DadosExame.confiabilidade == Constantes.nao_confiavel:
                interpretacao = "Resultado comprometido pela baixa confiabilidade."
            else:
                if DadosExame.porcentagem_respondidos_screening >= 90:
                    interpretacao = f"Paciente com visão normal, pontos respondidos: {int(DadosExame.porcentagem_respondidos_screening)}%"
                elif DadosExame.porcentagem_respondidos_screening < 90 and DadosExame.porcentagem_respondidos_screening >= 80:
                    interpretacao = f"Paciente com leve perda, pontos respondidos: {int(DadosExame.porcentagem_respondidos_screening)}%"
                elif DadosExame.porcentagem_respondidos_screening < 80:
                    interpretacao = f"Paciente com severa perda, ponto de atenção, pontos respondidos: {int(DadosExame.porcentagem_respondidos_screening)}%"
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
            f"Central 30°",
            f"Falso positivo: {int(DadosExame.falso_positivo_respondidos)} / {int(DadosExame.total_testes_falsos_positivo)} ({DadosExame.falso_positivo_respondidos_percentual:.2f}%)",
            
            f"Olho: {DadosExame.olho}",
            f"Tamanho do estimulo: {estimulo.get(DadosExame.tamanho_estimulo)}",
            f"Falso negativo: {int(DadosExame.falso_negativo_respondidos)} / {int(DadosExame.total_testes_falsos_negativo)} ({DadosExame.falso_negativo_respondidos_percentual:.2f}%)",
            
            f"Exame: {DadosExame.exame_selecionado.upper()}",
            f"Duração (min): {int(minutos)}:{int(segundos)}",
            f"Perda de fixacao: {int(DadosExame.perda_de_fixacao)} / {int(DadosExame.total_testes_mancha)} ({DadosExame.perda_de_fixacao_percentual:.2f}%)",
            
            f"Atenuacao:{DadosExame.atenuacao_screening}",           
            f"Total de pontos: {DadosExame.total_de_pontos_testados}",

        ]
        labels_valores = [          
            f"Confiabilidade:{DadosExame.confiabilidade}",       
            
            f"RESULTADO: {(gerar_resultado_final()).upper()}"]

        # Configuração para desenhar labels em colunas de 3 com 4 linhas
        colunas = 3
        linhas = 4
        espacamento_x = 280  # Espaço entre colunas
        espacamento_y = 50  # Espaço entre linhas
        pos_x_inicial = 1020  # Posição inicial da primeira coluna
        pos_y_inicial = 50  # Posição inicial da primeira linha
        
        cor_resultado = (0,0,0)
       
            
        espacamento_x_valores = 450
        espacamento_y_valores = 50
        pos_x_inicial_valores = 1020
        pos_y_inicial_valores = 300
        fonte = pygame.font.Font(None, 28)
        
        for i,texto in enumerate(labels_valores):
            coluna = i % 1
            linha = i // 1
            
           

            if i == 0:
                if DadosExame.confiabilidade == Constantes.confiavel:
                    color_label_info = cor_legenda_normal
                if DadosExame.confiabilidade == Constantes.questionavel:
                    color_label_info = cor_legenda_leve
                if DadosExame.confiabilidade == Constantes.ruim:
                    color_label_info = cor_legenda_moderado
                if DadosExame.confiabilidade == Constantes.nao_confiavel:
                    color_label_info = cor_legenda_severo
         
            if i == 1:
                color_label_info = cor_resultado
            
            pos_x = pos_x_inicial_valores + coluna * espacamento_x_valores
            pos_y = pos_y_inicial_valores + linha * espacamento_y_valores

            # Renderiza a label

            texto_renderizado = render_texto_colorido(fonte,texto.upper(),color_label_info)
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
    def desenha_pontos():

        
        surface = pygame.Surface((1920/2,1080/2))
        surface.fill((255,255,255))
        surface_limiar = pygame.Surface((1920/2,1080/2))
        surface_limiar.fill((255,255,255))
        
        perda_fixacao = 0.0
        LARGURA, ALTURA = 1920, 1080  # Tela original
        nova_largura, nova_altura = 960, 540  # Nova tela

        # circulo do mapa de pontos
        pygame.draw.circle(surface, (0, 0, 0), (480, 270), 250, 1)

        # circulo do mapa de limiar
        pygame.draw.circle(surface_limiar, (0, 0, 0), (480, 270), 250, 1)

        # linhas da cruz mapa de pontos
        pygame.draw.line(
            surface, (0, 0, 0), (480, 519), (480, 20), 1
        )
        pygame.draw.line(
            surface, (0, 0, 0), (729, 270), (230, 270), 1
        )

        # linhas da cruz mapa de limiar
        pygame.draw.line(
           surface_limiar, (0, 0, 0), (480, 519), (480, 20), 1
        )
        pygame.draw.line(
           surface_limiar, (0, 0, 0), (729, 270), (230, 270), 1
        )

        # legenda do mapa de pontos
        fonte = pygame.font.SysFont("Arial", 15)

        ponto_legenda_green = Ponto(0, 0, 5, pygame.Color("green"),distancia=200)
        ponto_legenda_green.raio_ponto = 6
        ponto_legenda_green.pontoPix = 6
        ponto_legenda_green.x = 800
        ponto_legenda_green.y = 270
        ponto_legenda_green.plotarPonto(surface)
        label_legenda_green = fonte.render(
            "Acima do limiar", True, (0, 0, 0)
        )
        surface.blit(
            label_legenda_green, label_legenda_green.get_rect(center=(900, 270))
        )

        label_legenda_red = fonte.render(
            "Abaixo do limiar", True, (0, 0, 0)
        )

        surface.blit(
            label_legenda_red, label_legenda_red.get_rect(center=(900, 310))
        )
        quadrado_legenda_vermelho = Ponto(0, 0, tamanhoPonto = 5,cor =  pygame.Color("red"),distancia = 200)
        quadrado_legenda_vermelho.raio_ponto = 10
        quadrado_legenda_vermelho.x = 800
        quadrado_legenda_vermelho.y = 310
        quadrado_legenda_vermelho.desenha_x(surface)
        
        respondidos,nao_respondidos = 0,0
        for ponto in DadosExame.matriz_pontos:                    
            ponto_novo = Ponto(ponto.xg,ponto.yg,tamanhoPonto = 5, cor = (0,0,0), distancia = 200)
            ponto.raio_ponto = 6
            
            ponto.pontoPix = 4   
            ponto.x = ponto_novo.x
            ponto.y = ponto_novo.y
            ponto.x = int(ponto.x * nova_largura / LARGURA)  # Reduzindo a coordenada X
            ponto.y = int(ponto.y * nova_altura / ALTURA)  # Reduzindo a coordenada Y
            
            if ponto.response_received:
                respondidos+=1
                ponto.atenuacao = DadosExame.atenuacao_screening
                ponto.cor = pygame.Color("green")
                ponto.plotarPonto(surface)
            elif not ponto.response_received:
                nao_respondidos+=1
                ponto.cor = pygame.Color("red")                
                ponto.desenha_x(surface)
                ponto.atenuacao = 0
          
            ponto.plotaString(ponto.atenuacao,20,surface_limiar) 
        
        DadosExame.porcentagem_respondidos_screening = (respondidos/DadosExame.total_de_pontos_testados) * 100
            

        pygame.image.save(surface,os.path.abspath(os.path.join(os.path.dirname(__file__),"..","utils","images","temp","mapa_pontos.png")))
        pygame.image.save(surface_limiar,os.path.abspath(os.path.join(os.path.dirname(__file__),"..","utils","images","temp","mapa_limiares.png")))
        
        pygame.display.get_surface().blit(surface,(-200, 0))  
        pygame.display.get_surface().blit(surface_limiar, (-200, 540))
          
          

        
    def exibir_resultados():
        pygame.display.get_surface().fill((255,255,255))
        ResultadoScreening.desenha_pontos()    
        ResultadoScreening.desenha_legendas()
        ResultadoScreening.desenha_aviso_pdf()
        pygame.display.flip()
        visualizando = True
        while visualizando:
            CONFIG_FILE = "config.json"

            DEFAULT_CONFIG ={
                "distancia_paciente":200,
                "tamanho_estimulo":3,
                "exame_id":1
            }
            config = ResultadoScreening.carregar_config(CONFIG_FILE,DEFAULT_CONFIG) 
            DadosExame.exame_id = config["exame_id"]       
          
            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_j:
                        visualizando = False
                        DadosExame.reset()
                        config["exame_id"] = (DadosExame.exame_id + 1) if DadosExame.exame_id < 999 else 1
                        config["distancia_paciente"] = DadosExame.distancia_paciente
                        config["tamanho_estimulo"] = DadosExame.tamanho_estimulo
                        ResultadoScreening.salvar_config(config,CONFIG_FILE)
                        
                    if evento.key == pygame.K_e:
                        config["exame_id"] = (
                            (DadosExame.exame_id + 1)
                            if DadosExame.exame_id < 999
                            else 1
                        )
                        config["distancia_paciente"] = DadosExame.distancia_paciente
                        config["tamanho_estimulo"] = DadosExame.tamanho_estimulo
                        ResultadoScreening.salvar_config(config, CONFIG_FILE)
                        pdf = GerarPdf()
                        # pdf.verifica_e_monta_pendrive()
                        # caminho_pdf = f"/media/eyetec/EXAMES/relatorio-id-exame-{DadosExame.exame_id}.pdf"
                        # caminho_pendrive = f"/media/eyetec/EXAMES/"
                        caminho_pendrive = os.path.abspath(
                            os.path.join(
                                os.path.dirname(__file__), "..", "utils", "pdfs"
                            )
                        )
                        caminho_pdf = os.path.abspath(
                            os.path.join(
                                os.path.dirname(__file__),
                                "..",
                                "utils",
                                "pdfs",
                                f"relatorio-id-exame-{DadosExame.exame_id}.pdf",
                            )
                        )
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
                                visualizando = False
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
                            
                            
                        
                        
                    


if __name__ == "__main__":
    from cordenadas_30 import cordenadas_30
    pygame.init()
    pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    DadosExame.matriz_pontos = [Ponto(x,y,tamanhoPonto = 5,cor = (0,0,0), distancia = 250) for x,y in cordenadas_30]
    for i,ponto in enumerate(DadosExame.matriz_pontos):
        if i % 2 == 0:
            ponto.response_received = True
        
      
            
    DadosExame.atenuacao_screening = 25
    DadosExame.total_de_pontos_testados = 76
    DadosExame.exame_selecionado = Constantes.screening
        
    ResultadoScreening.exibir_resultados()