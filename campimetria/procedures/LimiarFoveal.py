import pygame
import time
import math
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "constants")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "pages")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "procedures")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "strategies")))


from Ponto import Ponto
from colors import Colors





def fixacao_diamante():
    Ponto(0, 6, 3, pygame.Color("yellow")).plotarPonto()
    Ponto(0, -6, 3, pygame.Color("yellow")).plotarPonto()
    Ponto(6, 0, 3, pygame.Color("yellow")).plotarPonto()
    Ponto(-6, 0, 3, pygame.Color("yellow")).plotarPonto()


def db_para_intensidade(db, db_min=40, db_max=0, i_min=Colors.ERASE_INTENSITY, i_max=255):
    """Converte dB para intensidade de cor (escala logarítmica)."""
    norm_db = (db - db_min) / (db_max - db_min)  # Normaliza dB entre 0 e 1

    intensity = i_min + (i_max - i_min) * ((10 ** (norm_db) - 1) / (10**1 - 1))

    if intensity > 255:
        intensity = 255
    elif intensity < i_min:
        intensity = i_min

    return int(round(intensity))
    # return 110 + (255 - 110) * ((10**(db / 40) - 1) / (10**(1) - 1))


def contagem_regressiva():
    """
    Exibe uma contagem regressiva de 3 segundos na tela.

    Args:
        surface: A tela do pygame onde o texto será desenhado.
        fonte: Objeto pygame.font.Font para renderizar o texto.
        posicao: Tupla (x, y) indicando onde exibir o texto na tela.
    """

    for i in range(3, 0, -1):
        pygame.display.get_surface().fill(Colors.BACKGROUND)  # Limpa a tela (preto)
        texto = pygame.font.Font(None, 150).render(
            str(i), True, (255, 255, 255)
        )  # Texto branco
        pygame.display.get_surface().blit(texto, (1920 / 2 - 37, 1080 / 2 - 37))
        pygame.display.update()
        time.sleep(1)  # Aguarda 1 segundo


def tela_resultado(db):
    PRETO = (0, 0, 0)
    BRANCO = (255, 255, 255)
    AZUL = (50, 150, 255)
    AZUL_ESCURO = (30, 100, 200)

    # Fonte para exibição
    fonte = pygame.font.Font(None, 50)
    fonte_botao = pygame.font.Font(None, 40)

    # Número grande de exemplo
    numero_grande = db

    # Configuração do botão OK
    botao_rect = pygame.Rect(1920 // 2 - 50, 1080 // 2 + 50, 100, 50)
    esperando_clique = True
    while esperando_clique:
        screen.fill((0, 0, 0))  # Fundo preto

        # Renderiza o texto
        texto = fonte.render(f"Resultado: {numero_grande}", True, BRANCO)
        rect_texto = texto.get_rect(center=(1920 // 2, 1080 // 2 - 50))
        screen.blit(texto, rect_texto)

        # Desenha o botão OK
        pygame.draw.rect(screen, AZUL, botao_rect, border_radius=10)
        texto_botao = fonte_botao.render("OK", True, BRANCO)
        rect_texto_botao = texto_botao.get_rect(center=botao_rect.center)
        screen.blit(texto_botao, rect_texto_botao)

        pygame.display.flip()  # Atualiza a tela

        # Captura eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                esperando_clique = False  # Sai do loop ao fechar a janela
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_rect.collidepoint(evento.pos):
                    esperando_clique = False  # Fecha a tela quando clica no botão


def calcular_limiar_foveal():
    contagem_regressiva()
    screen.fill(Colors.BACKGROUND)
    pygame.display.update()
    UV = 0
    AT = 0
    UNV = 0
    NC = 0
    Delta = 0
    viu = 0
    Dbig = 3
    Dsmall = 2
    limiarok = False
    status = ""
    limiar = 0
    primeiro = True
    tempoExposicao = 0.2
    tempoRespostaPaciente = 2.0
    tamanhoPonto = 3
    sairAplicacao = False
    fixacao_diamante()
    limiarok = False

    ponto_limiar = Ponto(
        0,
        0,
        tamanhoPonto,
        (
            db_para_intensidade(AT),
            db_para_intensidade(AT),
            db_para_intensidade(AT),
        ),
    )
    

    while limiarok == False and sairAplicacao == False:
        primeiro = True
        AT = 25
        while status != "=" and sairAplicacao == False:
            ponto_limiar.response_received = False
            ponto_limiar.cor = (
                db_para_intensidade(AT),
                db_para_intensidade(AT),
                db_para_intensidade(AT),
            )

            ponto_limiar.testaPonto(tempoExposicao, tempoRespostaPaciente)

            print(
                f"AT: {AT}, viu: {"Yes" if ponto_limiar.response_received else "No"}, intensidade: {db_para_intensidade(AT)}"
            )
            if ponto_limiar.response_received:
                viu = 2
            else:
                viu = 1
            pygame.time.delay(500)
            match viu:
                case 1:
                    if AT <= 0:
                        AT = -1
                        status = "="
                        continue

                    UNV = AT
                    if primeiro == True:
                        primeiro = False
                        NC = 0
                        UV = 0
                        Delta = Dbig
                        AT = AT - Delta
                        status = "+"
                        continue
                    if status == "-":
                        NC += 1
                        Delta = Dsmall
                        if NC >= 2:
                            status = "="
                            AT = (UV + UNV) / 2
                            continue
                        else:
                            AT = AT - Delta
                            status = "+"
                            continue
                    else:
                        AT = AT - Delta
                        status = "+"
                        continue

                case 2:
                    UV = AT
                    if primeiro == True:
                        primeiro = False
                        NC = 0
                        UNV = 35
                        Delta = Dbig
                        AT = AT + Delta
                        status = "-"
                        continue

                    if status == "+":
                        NC = +1
                        Delta = Dsmall

                        if NC >= 2:
                            status = "="
                            AT = (UV + UNV) / 2
                            continue

                        else:
                            AT = AT + Delta
                            status = "-"
                            continue

                    else:
                        AT = AT + Delta
                        status = "-"
                        continue

            if AT > 40:
                AT = 35

        limiar = AT
        print(f"Limiar Foveal: {limiar} dB")
        limiarok = True
        ponto_limiar.db = limiar
        tela_resultado(limiar)


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    info = pygame.display.Info()
    screen_dim = min(info.current_w, info.current_h)
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Teste de Estímulo")   
    screen.fill(Colors.BACKGROUND)
    pygame.display.flip()
    pygame.event.clear()

    calcular_limiar_foveal()

    pygame.quit()
