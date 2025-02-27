from Ponto import Ponto
from ManchaCega import TesteLimiarManchaCega
import pygame
import time
import math
import random


# Inicializa o Pygame


coordinates_30 = [
    (-9, -27),
    (-3, -27),
    (3, -27),
    (9, -27),
    (-15, -21),
    (-9, -21),
    (-3, -21),
    (3, -21),
    (9, -21),
    (15, -21),
    (-21, -15),
    (-15, -15),
    (-9, -15),
    (-3, -15),
    (3, -15),
    (9, -15),
    (15, -15),
    (21, -15),
    (-27, -9),
    (-21, -9),
    (-15, -9),
    (-9, -9),
    (-3, -9),
    (3, -9),
    (9, -9),
    (15, -9),
    (21, -9),
    (27, -9),
    (-27, -3),
    (-21, -3),
    (-15, -3),
    (-9, -3),
    (-3, -3),
    (3, -3),
    (9, -3),
    (15, -3),
    (21, -3),
    (27, -3),
    (-27, 3),
    (-21, 3),
    (-15, 3),
    (-9, 3),
    (-3, 3),
    (3, 3),
    (9, 3),
    (15, 3),
    (21, 3),
    (27, 3),
    (-27, 9),
    (-21, 9),
    (-15, 9),
    (-9, 9),
    (-3, 9),
    (3, 9),
    (9, 9),
    (15, 9),
    (21, 9),
    (27, 9),
    (-21, 15),
    (-15, 15),
    (-9, 15),
    (-3, 15),
    (3, 15),
    (9, 15),
    (15, 15),
    (21, 15),
    (-15, 21),
    (-9, 21),
    (-3, 21),
    (3, 21),
    (9, 21),
    (15, 21),
    (3, 27),
    (9, 27),
    (-3, 27),
    (-9, 27),
]


def media_de_tempo_de_resposta_paciente(tempos):
    tempo_medio = sum(tempos) / len(tempos)
    if tempo_medio < 1.0:
        tempo_medio = 1.0
    if tempo_medio > 2.0:
        tempo_medio = 2.0
    return tempo_medio
    


def criar_pontos():
    return [Ponto(x, y, 3, (255, 255, 255)) for x, y in coordinates_30]


def exame_screening():
    pontos = criar_pontos()
    random.shuffle(pontos)
    tempo_resposta = 2.0
    tempos = []
    for ponto in pontos:
        ponto.cor = ponto.db_para_intensidade(25)
        pygame.time.delay(100)  # Aguarda 100 ms para cada ponto
        ponto.testaPonto(0.2, tempo_resposta)
        ponto.limiar_encontrado = True
        tempos.append(ponto.tempo_resposta)
        print(f"tempo_resposta no screening: {ponto.tempo_resposta}")
        if len(tempos) == 5:
            tempo_resposta = media_de_tempo_de_resposta_paciente(tempos)
            tempos = []

    for ponto in pontos:
        if ponto.response_received:
            ponto.cor = pygame.Color("green")
            ponto.plotarPonto()
        elif not ponto.response_received:
            ponto.cor = pygame.Color("red")
            ponto.plotarPonto()
    pygame.time.delay(15000)  # Aguarda 5 segundos para reiniciar o loop


def main():
    running = True
    sair = True
    teste_fixacao = True

    while running or sair:

        pygame.display.get_surface().fill((120, 120, 120))
        pygame.display.update()
        Ponto(0, 0, 3, pygame.Color("yellow")).plotarPonto()
        # Captura eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Fecha ao clicar no botão de fechar
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Fecha ao pressionar ESC
                    running = False

        pygame.time.delay(2000)  # Aguarda 1 segundo para reiniciar o loop
        # resultado_mancha_cega = TesteLimiarManchaCega().teste_mancha_cega("OD")
        # if resultado_mancha_cega == True:
        #     break
        # elif resultado_mancha_cega == False:
        #     teste_fixacao = False
            
      
        exame_screening()

        pygame.time.delay(30000)  # Aguarda 1 segundo para reiniciar o loop
        pygame.display.flip()
        running = False


pygame.init()
tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT or (
            evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE
        ):
            rodando = False

    pygame.display.flip()
    main()
    # exame_screening()
    rodando = False


pygame.quit()
