import pygame
import random
import sys
import os

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

from Ponto import Ponto
from cordenadas_mcdir import cordenadas_mcdir
from cordenadas_mcesq import cordenadas_mcesq
from dados import *
from fixacao_central import FixacaoCentral

pygame.font.init()
fonte_titulo = pygame.font.Font(None,64)
fonte_subtitulo = pygame.font.Font(None,48)
fonte_button = pygame.font.Font(None, 40)
cor_titulo = (209,41,41)
cor_texto = (0, 0, 0)
cor_texto_botao = (255,255,255)
cor_alerta = (255,255,255)
cor_botao = (133, 137, 131)
cor_botao_hover = (255, 247, 28)
cor_botao_selecao = (45,167,8 )  
botao_selecionado = 1
largura, altura = 1744, 925
x, y = (1920 - largura) // 2, (
    1080 - altura
) // 2  # Centro da tela
rect_fundo = pygame.Rect(x, y, largura, altura)


def desenhar_botao(texto, rect, selecionado):
    this_x, this_y, this_largura, this_altura = rect
    cor_atual = cor_botao_selecao if selecionado else cor_botao
    pygame.draw.rect(
        pygame.display.get_surface(),
        cor_atual,
        (this_x, this_y, this_largura, this_altura),
        border_radius=15,
    )
    

    # Se for o botão selecionado, desenha uma borda ao redor
    if selecionado:
        pygame.draw.rect(
            pygame.display.get_surface(),
            cor_botao_hover,
            (this_x - 2, this_y - 2, this_largura + 4, this_altura + 4),
            2,
            border_radius=15,
        )
        
    texto_renderizado = fonte_button.render(texto, True, cor_texto_botao)
    texto_rect = texto_renderizado.get_rect(center=(this_x + this_largura // 2, this_y + this_altura // 2))
    pygame.display.get_surface().blit(texto_renderizado, texto_rect)
    pygame.display.update()
    return pygame.Rect(this_x, this_y, this_largura, this_altura)  # Retorna a área do botão


def mostrar_alerta(botao_reiniciar_estado, botao_continuar_estado):
    
    pygame.draw.rect(
        pygame.display.get_surface(),
        cor_alerta,
      rect_fundo ,
        border_radius=25,
    )

    titulo = fonte_titulo.render("MANCHA CEGA NÃO ENCONTRADA",True,cor_titulo)
    titulo_pos = titulo.get_rect()
    titulo_pos.center = rect_fundo.center
    titulo_pos.y -= 224
    pygame.display.get_surface().blit(titulo, titulo_pos)
    
    
    sub_titulo = fonte_subtitulo.render("Caso opte por continuar os testes de perda de fixação não serão feitos",True,cor_texto)
    sub_titulo_pos = sub_titulo.get_rect()
    
    sub_titulo_pos.center = rect_fundo.center
    sub_titulo_pos.y -= 49
    pygame.display.get_surface().blit(sub_titulo,sub_titulo_pos)
    
    
    rect_botao_reiniciar = pygame.Rect(0,0,529,105)
    rect_botao_continuar = pygame.Rect(0,0,529,105)
    rect_botao_reiniciar.center = rect_fundo.center
    rect_botao_continuar.center = rect_fundo.center
    rect_botao_reiniciar.x -= 350
    rect_botao_continuar.x += 350
    rect_botao_continuar.y += 105
    rect_botao_reiniciar.y += 105
    
    # Desenha os botões com a seleção destacada  
    botao_reiniciar = desenhar_botao(
        "REINCIAR", rect_botao_reiniciar, botao_reiniciar_estado
    )
    botao_continuar = desenhar_botao(
        "CONTINUAR", rect_botao_continuar, botao_continuar_estado
    )
    pygame.display.update()
    return (
        botao_reiniciar,
        botao_continuar,
    )  # Retorna os retângulos dos botões para referência


class TesteLimiarManchaCega:

    def __init__(self):
        self.encontrou_mancha = None
        self.resultado = None
        self.indice_atual = 0
        self.pontos_naorespondidos = []
        self.matriz_mancha_cega = (
            cordenadas_mcdir
            if DadosExame.olho == Constantes().olho_direito
            else cordenadas_mcesq
        )
        random.shuffle(self.matriz_mancha_cega)
        self.total_pontos = len(self.matriz_mancha_cega)
        self.delay_entre_pontos = 100
        self.reiniciar = False

    def verifica_mensagem(self):
        rodando = True
        mostrar_mensagem = True
        botao_reiniciar = None
        botao_continuar = None
        pygame.display.get_surface().fill(Colors.BACKGROUND)
        pygame.display.update()
        botao_selecionado = 0
        botao_reiniciar, botao_continuar = mostrar_alerta(True, False)
        while rodando:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    rodando = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_j:
                        pygame.quit()
                    if event.key == pygame.K_LEFT:
                        mostrar_alerta(
                            botao_reiniciar_estado=True, botao_continuar_estado=False
                        )
                        botao_selecionado = 0
                    elif event.key == pygame.K_RIGHT:
                        mostrar_alerta(
                            botao_reiniciar_estado=False, botao_continuar_estado=True
                        )
                        botao_selecionado = 1
                    elif event.key == pygame.K_e and mostrar_mensagem:
                        if botao_selecionado == 0:
                            rodando = False  
                            pygame.display.get_surface().fill(Colors.BACKGROUND)
                            FixacaoCentral.plotar_fixacao_central()
                            self.reiniciar = True
                            return
                        elif botao_selecionado == 1:
                            rodando = False  
                            pygame.display.get_surface().fill(Colors.BACKGROUND)
                            FixacaoCentral.plotar_fixacao_central()
                            self.reiniciar = False
                            return
                        mostrar_mensagem = False  # Fecha a notificação

    def calculo_centro_de_massa(self):
        somaMx = 0
        somaMy = 0
        icont = 0
        if len(self.pontos_naorespondidos) == 0:
            return False
        for i in range(len(self.pontos_naorespondidos)):
            for pontoNaoRespondido in self.pontos_naorespondidos:
                x, y = pontoNaoRespondido
                somaMx += x
                somaMy += y
                icont += 1
                print(f"SOMAM {somaMx} SOMAMY: {somaMy} ICONT:{icont}")

        xcm = round(somaMx / icont)
        ycm = round(somaMy / icont)
        print(f"XCM1: {xcm}, YCM1: {ycm}")
        return xcm, ycm

    def teste_mancha_cega(self):        

        if self.indice_atual < self.total_pontos:

            ponto = self.matriz_mancha_cega[self.indice_atual]
            x, y = ponto
            cor_ponto = Ponto.db_para_intensidade(0)
            teste = Ponto(x, y, 3, cor_ponto)
            teste.testaPonto(0.2, 2)
            if not teste.response_received:
                self.pontos_naorespondidos.append((teste.xg, teste.yg))
            self.indice_atual += 1

        if self.indice_atual == self.total_pontos:

            if len(self.pontos_naorespondidos) == 0:
                self.verifica_mensagem()
                if self.reiniciar:
                    self.indice_atual = 0
                    self.pontos_naorespondidos = []
                    self.reiniciar = False
                else:
                    self.encontrou_mancha = False
            else:
                self.resultado = self.calculo_centro_de_massa()
                self.encontrou_mancha = True
                DadosExame.posicao_mancha_cega = self.resultado


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    testando = True
    mensagem = TesteLimiarManchaCega()
    
    while testando:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    rodando = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_j:
                        pygame.quit()
        mensagem.verifica_mensagem()
    
    pygame.quit()