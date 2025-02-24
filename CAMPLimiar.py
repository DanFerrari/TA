import pygame
import time
import math
from Ponto import Ponto


def fixacao_diamante():
    Ponto(0,6,2,pygame.Color("yellow")).plotarPonto()
    Ponto(0,-6,2,pygame.Color("yellow")).plotarPonto()    
    Ponto(6,0,2,pygame.Color("yellow")).plotarPonto()    
    Ponto(-6,0,2,pygame.Color("yellow")).plotarPonto()    



def db_para_intensidade(db):
    dB = max(0,min(35,db))
    brilho = 255 * (1 - dB / 35)
    return int(brilho)

def calcular_limiar_foveal():
    UV=0
    AT=0
    UNV=0
    NC=0
    Delta = 0
    viu = 0 
    Dbig = 3
    Dsmall = 2
    limiarok = False
    status = ''
    limiar = 0.1
    primeiro = True
    tempoExposicao = 200
    tamanhoPonto = 3
    sairAplicacao = False
    fixacao_diamante()
    limiarok = False
    
    
    while limiarok == False and sairAplicacao == False:
        
        ponto_limiar = Ponto(0,0,1.5,(db_para_intensidade(AT),db_para_intensidade(AT),db_para_intensidade(AT)))
        status = ''
        primeiro = True
        AT = 25
        while status != '=' and sairAplicacao == False:
            
            ponto_limiar = Ponto(0,0,1.5,(db_para_intensidade(AT),db_para_intensidade(AT),db_para_intensidade(AT))).testaPonto() 
            
                                            
            if ponto_limiar.:
                viu = 2
            else:   
                viu = 1
                
            
            match viu:
                case 1:
                    if AT <= 0:
                        AT = -1 
                        status = '='                            
                        continue
                                            
                    UNV = AT 
                    if primeiro == True:
                        primeiro = False
                        NC = 0
                        UV = 0
                        Delta = Dbig
                        AT = AT - Delta
                        status = '+'
                        continue
                    if status == '-':
                        NC += 1
                        Delta = Dsmall
                        if NC >= 2:
                            status = '='
                            AT = (UV + UNV) / 2
                            continue
                        else:            
                            AT = AT - Delta
                            status = '+'
                            continue
                    else:
                        AT = AT - Delta        
                        status = '+'
                        continue
                        
                    
                case 2:
                    UV = AT
                    if primeiro == True:
                        primeiro = False
                        NC = 0
                        UNV = 35
                        Delta = Dbig
                        AT = AT + Delta
                        status = '-'
                        continue
                        
                    if status == '+':
                        NC =+ 1
                        Delta = Dsmall
                        
                        if NC >= 2:
                            status = '='
                            AT = (UV + UNV) / 2
                            continue
                            
                        else:
                            AT = AT + Delta
                            status = '-' 
                            continue
                            
                                

                    else:
                        AT = AT + Delta
                        status = '-'
                        continue
                        
            
                    
            if AT > 40:
                AT = 35    
        
        
        limiar = AT
        labelIntensidade.setStyleSheet("QLabel { color : black; font-size: 38px; }")
        limiarok = True
        labelLimiarFoveal.setText(f"Limiar Foveal= {limiar}")


