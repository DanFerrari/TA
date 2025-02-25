import pygame
import time
import math
from Ponto import Ponto


def fixacao_diamante():
    Ponto(0, 6, 2, pygame.Color("yellow")).plotarPonto()
    Ponto(0, -6, 2, pygame.Color("yellow")).plotarPonto()
    Ponto(6, 0, 2, pygame.Color("yellow")).plotarPonto()
    Ponto(-6, 0, 2, pygame.Color("yellow")).plotarPonto()

def db_para_intensidade(db, db_min=35, db_max=0, i_min=122, i_max=255):
    """ Converte dB para intensidade de cor (escala logarítmica). """
    norm_db = (db - db_min) / (db_max - db_min)  # Normaliza dB entre 0 e 1
    intensity = i_min + (i_max - i_min) * ((10**(norm_db) - 1) / (10**1 - 1))
    return int(round(intensity))


def calcular_limiar_foveal():
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
            #ponto_limiar.cor = (db_para_intensidade(AT),db_para_intensidade(AT),db_para_intensidade(AT))            
            #ponto_limiar.testaPonto(tempoExposicao,tempoRespostaPaciente)
            ponto_limiar.cor = pygame.Color("yellow")
            ponto_limiar.plotarPonto()
            print(f"AT: {AT}, viu: {"Yes" if ponto_limiar.response_received else "No"}, current_db: {ponto_limiar.current_db:.2f} dB")
            if ponto_limiar.response_received:
                viu = 2
            else:
                viu = 1
            pygame.time.delay(400)
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
        #limiarok = True
    
    

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    info = pygame.display.Info()
    screen_dim = min(info.current_w, info.current_h)
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Teste de Estímulo")
    background_db = -4.0
    background_intensity = int(255 * (10 ** (background_db / 20)))
    BACKGROUND_COLOR = (
        122,
        122,
        122,    
    )
    screen.fill(BACKGROUND_COLOR)
    pygame.display.flip()
    pygame.event.clear()
    
    calcular_limiar_foveal()  

    pygame.quit()
