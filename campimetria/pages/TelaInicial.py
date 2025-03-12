import pygame
import os, sys
import numpy as np

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

from CAMPScreening import Screening
from dados import *
from CAMPFullThreshold import FullThreshold
from Ponto import Ponto
from cordenadas_30 import cordenadas_30
from fixacao_central import FixacaoCentral

# Inicializa o pygame
pygame.init()

# Configurações da tela (FULLSCREEN)
tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
LARGURA, ALTURA = tela.get_size()
pygame.display.set_caption("Seleção de Estratégia")

# Fonte e cores estilizadas
fonte = pygame.font.Font(None, int(ALTURA * 0.07))  # Fonte escalável
cor_fundo = (0, 0, 0)
cor_botao = (122, 122, 122)
cor_botao_hover = (255, 255, 255)
cor_borda_selecao = (255, 215, 0)  # Dourado para destacar o botão selecionado
cor_texto = (255, 255, 255)


# Índice do botão selecionado (0 = "Estratégia 1", 1 = "Estratégia 2")
botao_selecionado = 0


# Funções para cada botão
def selecionar_olho():
    fonte_titulo = pygame.font.Font(None, int(ALTURA * 0.08))
    fonte_opcoes = pygame.font.Font(None, int(ALTURA * 0.06))
    fonte_numero = pygame.font.Font(None, int(ALTURA * 0.07))
    fonte_botao = pygame.font.Font(None, int(ALTURA * 0.06))
    cor_fundo = (20, 20, 20)
    cor_texto = (255, 255, 255)
    cor_texto_fade = (100, 100, 100)  # Cor mais fraca para opção não selecionada
    cor_caixa = (50, 50, 50)
    cor_caixa_selecao = (70, 70, 70)  # Branco para destacar a caixa de seleção
    cor_botao = (0, 200, 0)  # Verde
    cor_botao_hover = (0, 255, 0)  # Verde mais brilhante para hover
    cor_font_olho = (255, 255, 255)  # Branco
    # Opções do topo
    opcoes = ["Olho Esquerdo", "Olho Direito"]
    opcao_selecionada = 0  # 0 = Esquerda, 1 = Direita

    # Controle da seleção
    selecao_atual = "opcoes"  # Pode ser "opcoes", "numero" ou "botao"

    # Caixa numérica
    numero = 25
    NUMERO_MIN = 0
    NUMERO_MAX = 40

    rodando = True
    while rodando:
        tela.fill(cor_fundo)  # Fundo da tela
        DadosExame.olho = Constantes.olho_direito
        # Renderiza as opções do topo
        pos_y_opcoes = ALTURA * 0.2

        if selecao_atual == "opcoes":
            cor_font_olho = (255, 255, 255)
        else:
            cor_font_olho = (0, 255, 0)

        texto_esquerda = fonte_opcoes.render(
            opcoes[0], True, cor_font_olho if opcao_selecionada == 0 else cor_texto_fade
        )
        texto_direita = fonte_opcoes.render(
            opcoes[1], True, cor_font_olho if opcao_selecionada == 1 else cor_texto_fade
        )
        # Desenha uma borda para o texto à esquerda, se selecionado

        tela.blit(
            texto_esquerda,
            (LARGURA * 0.25 - texto_esquerda.get_width() // 2, pos_y_opcoes),
        )
        tela.blit(
            texto_direita,
            (LARGURA * 0.75 - texto_direita.get_width() // 2, pos_y_opcoes),
        )

        # Renderiza a caixa numérica
        if DadosExame.exame_selecionado == Constantes.screening:
            cor_caixa_atual = (
                cor_caixa_selecao if selecao_atual == "numero" else cor_caixa
            )
            pos_y_numero = ALTURA * 0.4
            pygame.draw.rect(
                tela,
                cor_caixa_atual,
                (LARGURA // 2 - 100, pos_y_numero, 200, 100),
                border_radius=10,
            )
            texto_numero = fonte_numero.render(str(numero), True, cor_texto)
            tela.blit(
                texto_numero,
                (LARGURA // 2 - texto_numero.get_width() // 2, pos_y_numero + 25),
            )
            if selecao_atual == "numero":
                pygame.draw.rect(
                    tela,
                    (255, 255, 255),  # Cor da borda (branca)
                    (LARGURA // 2 - 100, pos_y_numero, 200, 100),
                    5,  # Espessura da borda
                    border_radius=10,  # Mesma curvatura que a caixa
                )

        # Renderiza o botão "Iniciar Exame"
        pos_y_botao = ALTURA * 0.6
        cor_botao_atual = cor_botao_hover if selecao_atual == "botao" else cor_botao
        pygame.draw.rect(
            tela,
            cor_botao_atual,
            (LARGURA // 2 - 150, pos_y_botao, 300, 80),
            border_radius=10,
        )
        texto_botao = fonte_botao.render("Iniciar Exame", True, cor_fundo)
        tela.blit(
            texto_botao, (LARGURA // 2 - texto_botao.get_width() // 2, pos_y_botao + 20)
        )
        if selecao_atual == "botao":
            pygame.draw.rect(
                tela,
                (255, 255, 255),  # Cor da borda (branca)
                (LARGURA // 2 - 150, pos_y_botao, 300, 80),
                5,  # Espessura da borda
                border_radius=10,  # Mesma curvatura que o botão
            )

        # Captura eventos do teclado
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Tecla ESC para sair
                    rodando = False

                # Alterna entre seleção de opções, número e botão
                elif event.key == pygame.K_UP:
                    if selecao_atual == "numero":
                        selecao_atual = "opcoes"
                    elif selecao_atual == "botao":
                        if DadosExame.exame_selecionado == Constantes.screening:
                            selecao_atual = "numero"
                        else:
                            selecao_atual = "opcoes"
                elif event.key == pygame.K_DOWN:
                    if selecao_atual == "opcoes":
                        if DadosExame.exame_selecionado == Constantes.screening:
                            selecao_atual = "numero"
                        else:
                            selecao_atual = "botao"
                    elif selecao_atual == "numero":
                        selecao_atual = "botao"

                # Navegação dentro da seleção ativa
                elif selecao_atual == "opcoes":
                    if event.key == pygame.K_LEFT:
                        opcao_selecionada = 0
                        DadosExame.olho = Constantes.olho_esquerdo
                    elif event.key == pygame.K_RIGHT:
                        opcao_selecionada = 1
                        DadosExame.olho = Constantes.olho_direito

                elif selecao_atual == "numero":
                    if event.key == pygame.K_LEFT and numero > NUMERO_MIN:
                        numero -= 1
                    elif event.key == pygame.K_RIGHT and numero < NUMERO_MAX:
                        numero += 1

                elif selecao_atual == "botao":
                    if event.key == pygame.K_RETURN:

                        if DadosExame.exame_selecionado == Constantes.screening:
                            exame = Screening()
                            DadosExame.atenuacao_screening = numero
                            exame.iniciar_screening()
                            rodando = False
                        elif DadosExame.exame_selecionado == Constantes.fullthreshold:
                            exame = FullThreshold()
                            exame.main()
                            rodando = False
                        else:
                            print("Exame não implementado!")

        pygame.display.flip()  # Atualiza a tela


# Função para desenhar um botão centralizado
def desenhar_botao(texto, y, largura, altura, selecionado):
    x = (LARGURA - largura) // 2  # Centraliza o botão horizontalmente
    cor_atual = cor_botao_hover if selecionado else cor_botao
    texto_renderizado = fonte.render(texto, True, cor_atual)
    texto_rect = texto_renderizado.get_rect(center=(x + largura // 2, y + altura // 2))
    tela.blit(texto_renderizado, texto_rect)
    return pygame.Rect(x, y, largura, altura)  # Retorna a área do botão


# Loop principal
rodando = True
while rodando:

    DadosExame.matriz_pontos = [
        Ponto(x, y, 3, (255, 255, 255)) for x, y in cordenadas_30
    ]
    from TelaResultadoFullThreshold import ResultadoFullthreshold

    ResultadoFullthreshold.exibir_resultados()

    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    rodando = False

    tela.fill(cor_fundo)  # Preenche o fundo

    # Renderiza a label no topo da tela
    label_texto = fonte.render("Selecione a estratégia", True, cor_texto)
    tela.blit(label_texto, (LARGURA // 2 - label_texto.get_width() // 2, ALTURA * 0.2))

    # Dimensões dos botões proporcionais à tela
    largura_botao = int(LARGURA * 0.3)
    altura_botao = int(ALTURA * 0.1)
    espacamento = int(ALTURA * 0.15)

    # Desenha os botões com destaque no botão selecionado
    botao1 = desenhar_botao(
        "Screnning", ALTURA * 0.4, largura_botao, altura_botao, botao_selecionado == 0
    )
    botao2 = desenhar_botao(
        "Fulltheshold",
        ALTURA * 0.4 + espacamento,
        largura_botao,
        altura_botao,
        botao_selecionado == 1,
    )

    # Captura eventos do teclado
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:  # Mover para cima
                botao_selecionado = 0  # Seleciona "Estratégia 1"
            elif event.key == pygame.K_DOWN:  # Mover para baixo
                botao_selecionado = 1  # Seleciona "Estratégia 2"
            elif event.key == pygame.K_RETURN:  # Tecla ENTER para confirmar
                if botao_selecionado == 0:
                    DadosExame.exame_selecionado = Constantes.screening
                    selecionar_olho()
                elif botao_selecionado == 1:
                    DadosExame.exame_selecionado = Constantes.fullthreshold
                    selecionar_olho()
            elif event.key == pygame.K_ESCAPE:  # Tecla ESC para sair
                rodando = False

    pygame.display.flip()  # Atualiza a tela

pygame.quit()
