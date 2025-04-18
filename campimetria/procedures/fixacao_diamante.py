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
        Ponto(0, 6, 3, Colors.YELLOW_SIGHT, distancia=DadosExame.distancia_paciente).plotarPonto()
        Ponto(0, -6, 3,  Colors.YELLOW_SIGHT,distancia=DadosExame.distancia_paciente).plotarPonto()
        Ponto(6, 0, 3,  Colors.YELLOW_SIGHT,distancia=DadosExame.distancia_paciente).plotarPonto()
        Ponto(-6, 0, 3,  Colors.YELLOW_SIGHT,distancia=DadosExame.distancia_paciente).plotarPonto()
        
        
        
