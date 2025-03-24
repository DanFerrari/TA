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

class FixacaoDiamante:
    @staticmethod
    def plotar_fixacao_diamante():
        Ponto(0, 6, 3, pygame.Color("yellow"), distancia=DadosExame.distancia_exame).plotarPonto()
        Ponto(0, -6, 3, pygame.Color("yellow"),distancia=DadosExame.distancia_exame).plotarPonto()
        Ponto(6, 0, 3, pygame.Color("yellow"),distancia=DadosExame.distancia_exame).plotarPonto()
        Ponto(-6, 0, 3, pygame.Color("yellow"),distancia=DadosExame.distancia_exame).plotarPonto()