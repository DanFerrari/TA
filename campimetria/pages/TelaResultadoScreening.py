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


class ResultadoScreening:
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
        
        
        minutos,segundos = divmod((DadosExame.duracao_do_exame / 1000),60)
        

        labels = [
            f"Exame: {DadosExame.exame_selecionado.upper()}",
            f"Duração (min): {int(minutos)}:{int(segundos)}",
            f"Total de pontos: {DadosExame.total_de_pontos_testados}",
            f"Falso positivo: {int(DadosExame.falso_positivo_respondidos)} / {int(DadosExame.total_testes_falsos_positivo)} ({DadosExame.falso_positivo_respondidos_percentual:.2f}%)",
            f"Falso negativo: {int(DadosExame.falso_negativo_respondidos)} / {DadosExame.total_testes_falsos_negativo} ({DadosExame.falso_negativo_respondidos_percentual:.2f}%)",
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
        CONFIG_FILE = "config.json"

        DEFAULT_CONFIG ={
            "distancia_paciente":200,
            "tamanho_estimulo":3,
            "exame_id":1
        }
        config = ResultadoScreening.carregar_config(CONFIG_FILE,DEFAULT_CONFIG)        
        config["exame_id"] = (DadosExame.exame_id + 1) if DadosExame.exame_id < 999 else 1
        config["distancia_paciente"] = DadosExame.distancia_paciente
        config["tamanho_estimulo"] = DadosExame.tamanho_estimulo
        
        ResultadoScreening.salvar_config(config,CONFIG_FILE)
        
        
        pygame.display.get_surface().fill(pygame.Color("white"))
        perda_fixacao = 0.0
        LARGURA, ALTURA = 1920, 1080  # Tela original
        nova_largura, nova_altura = 960, 540  # Nova tela

        # circulo do mapa de pontos
        pygame.draw.circle(pygame.display.get_surface(), (0, 0, 0), (480, 270), 250, 1)

        # circulo do mapa de limiar
        pygame.draw.circle(pygame.display.get_surface(), (0, 0, 0), (480, 810), 250, 1)

        # linhas da cruz mapa de pontos
        pygame.draw.line(
            pygame.display.get_surface(), (0, 0, 0), (480, 519), (480, 20), 1
        )
        pygame.draw.line(
            pygame.display.get_surface(), (0, 0, 0), (729, 270), (230, 270), 1
        )

        # linhas da cruz mapa de limiar
        pygame.draw.line(
            pygame.display.get_surface(), (0, 0, 0), (480, 1060), (480, 560), 1
        )
        pygame.draw.line(
            pygame.display.get_surface(), (0, 0, 0), (729, 810), (230, 810), 1
        )

        # legenda do mapa de pontos
        fonte = pygame.font.SysFont("Arial", 15)

        ponto_legenda_green = Ponto(0, 0, 3, pygame.Color("green"))
        ponto_legenda_green.x = 800
        ponto_legenda_green.y = 270
        ponto_legenda_green.plotarPonto()
        label_legenda_green = fonte.render(
            "Acima do limiar de referência", True, (0, 0, 0)
        )
        pygame.display.get_surface().blit(
            label_legenda_green, label_legenda_green.get_rect(center=(900, 270))
        )

        label_legenda_red = fonte.render(
            "Abaixo do limiar de referência", True, (0, 0, 0)
        )

        pygame.display.get_surface().blit(
            label_legenda_red, label_legenda_red.get_rect(center=(900, 310))
        )
        quadrado_legenda_vermelho = Ponto(0, 0, tamanhoPonto = 5,cor =  pygame.Color("red"),distancia = 200)
        quadrado_legenda_vermelho.raio_ponto = 10
        quadrado_legenda_vermelho.x = 800
        quadrado_legenda_vermelho.y = 310
        quadrado_legenda_vermelho.desenha_quadrado()

        pontos_ajustados = []
        for ponto in DadosExame.matriz_pontos:                    
            ponto = Ponto(ponto.xg,ponto.yg,tamanhoPonto = 5, cor = (0,0,0), distancia = 200)
            ponto.raio_ponto = 6
            ponto.pontoPix = 4        
            pontos_ajustados.append(ponto)
        for ponto in pontos_ajustados:
            ponto.x = int(ponto.x * nova_largura / LARGURA)  # Reduzindo a coordenada X
            ponto.y = int(ponto.y * nova_altura / ALTURA)  # Reduzindo a coordenada Y
            
            if ponto.response_received:
                ponto.cor = pygame.Color("green")
                ponto.plotarPonto()
            elif not ponto.response_received:
                ponto.cor = pygame.Color("red")                
                ponto.desenha_quadrado()

        for ponto in pontos_ajustados:
            if ponto.response_received:
                ponto.atenuacao = DadosExame.atenuacao_screening
            else:
                ponto.atenuacao = 0
            fonte = pygame.font.Font(None, 20)
            texto = fonte.render(f"{ponto.atenuacao}", True, (0, 0, 0))

            ponto.y += ALTURA // 2
            pygame.display.get_surface().blit(
                texto, texto.get_rect(center=(ponto.x, ponto.y))
            )

        ResultadoScreening.desenha_legendas()

        pygame.display.flip()
        visualizando = True

        while visualizando:
            for evento in pygame.event.get():
                if (
                    evento.type == pygame.QUIT
                    or evento.type == pygame.KEYDOWN
                    and evento.key == pygame.K_j
                ):
                    visualizando = False
                    DadosExame.reset()


if __name__ == "__main__":
    from cordenadas_30 import cordenadas_30
    pygame.init()
    pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    DadosExame.matriz_pontos = [Ponto(x,y,tamanhoPonto = 5,cor = (0,0,0), distancia = 250) for x,y in cordenadas_30]
    ResultadoScreening.desenha_pontos()