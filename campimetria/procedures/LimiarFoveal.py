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
from dados import *








def db_para_intensidade(db, db_min=40, db_max=0, i_min=Colors.ERASE_INTENSITY, i_max=Colors.MAX_INTENSITY):
    """Converte dB para intensidade de cor (escala logarítmica)."""
    norm_db = (db - db_min) / (db_max - db_min)  # Normaliza dB entre 0 e 1

    intensity = i_min + (i_max - i_min) * ((10 ** (norm_db) - 1) / (10**1 - 1))

    if intensity > 255:
        intensity = 255
    elif intensity < i_min:
        intensity = i_min

    return int(round(intensity))
    # return 110 + (255 - 110) * ((10**(db / 40) - 1) / (10**(1) - 1))





class CalcularLimiar():
    
    def iniciar_teste_limiar_foveal():
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
            DadosExame.limiar_foveal = limiar
            print(f"Limiar Foveal: {limiar} dB")
            limiarok = True  
     
        



