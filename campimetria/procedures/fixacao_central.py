import pygame,os,sys


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
from dados import *

class FixacaoCentral:
    @staticmethod   
    def plotar_fixacao_central():
        Ponto(0, 0, 3, pygame.Color("yellow"),DadosExame.distancia_paciente).plotarPonto()