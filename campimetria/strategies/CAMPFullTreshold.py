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
from constantes_exame import Constantes




class Dados:
    gContIgual = 0
    gFlutuacao = False  # Ajuste conforme necessário
    LimQuad = False  # Ajuste conforme necessário
    class DadosExame:
        LF = False
        ThrRel = False
    gExame = []  # Lista simulando exames (deve ser inicializada corretamente)

def setLimiarFlutuacao(matExame, idPto):
    """Função simulada para ajuste de limiar de flutuação"""
    pass

def VerifyFalseNegative():
    """Função simulada para verificar falso negativo"""
    pass

class TMatExame:
    def __init__(self):
        self.Atenuacao = 0
        self.Status = ''
        self.UltAtenNaoVista = 0
        self.UltAtenVista = 0
        self.NCruzou = 0
        self.primeiro = True
        self.Delta = 0

def FullThreshold(paciente_viu: int,ponto:Ponto) -> int:
    resp = 0

    if paciente_viu == 1:
        if ponto.atenuacao == 0:
            ponto.atenuacao = -1
            ponto.status = '='
            resp = 1
        else:
            ponto.ultima_atenuacao_nao_vista = ponto.atenuacao
            if ponto.primeira_visualizacao:
                ponto.primeira_visualizacao = False
                ponto.ultima_atenuacao_vista = Constantes.Constantes.dbMin
                ponto.numero_cruzamentos = 0
                ponto.delta = Constantes.Constantes.bigdelta
                ponto.atenuacao -= ponto.delta
                if ponto.atenuacao <= 0:
                    ponto.atenuacao = 0
                ponto.status = '+'
            elif ponto.status == '-':
                ponto.numero_cruzamentos += 1
                ponto.delta = Constantes.Constantes.smalldelta
                if ponto.numero_cruzamentos >= 2:
                    ponto.status = '='
                    ponto.atenuacao = (ponto.ultima_atenuacao_nao_vista + ponto.ultima_atenuacao_vista) / 2
                    resp = 1
                else:
                    ponto.atenuacao -= ponto.delta
                    if ponto.atenuacao <= 0:
                        ponto.atenuacao = 0
                    ponto.status = '+'
            else:
                ponto.atenuacao -= ponto.delta
                if ponto.atenuacao <= 0:
                    ponto.atenuacao = 0
                ponto.status = '+'

    elif paciente_viu == 2:
        ponto.ultima_atenuacao_vista = ponto.atenuacao
        if ponto.primeira_visualizacao:
            ponto.primeira_visualizacao = False
            ponto.numero_cruzamentos = 0
            ponto.ultima_atenuacao_nao_vista = Constantes.Constantes.dbMax
            ponto.delta = Constantes.Constantes.bigdelta
            ponto.atenuacao += ponto.delta
            if ponto.atenuacao >= 40:
                ponto.atenuacao = 40
            ponto.status = '-'
        elif ponto.status == '+':
            ponto.numero_cruzamentos += 1
            ponto.delta = Constantes.Constantes.smalldelta
            if ponto.numero_cruzamentos >= 2:
                ponto.status = '='
                ponto.atenuacao = (ponto.ultima_atenuacao_nao_vista + ponto.ultima_atenuacao_vista) / 2
                resp = 1
            else:
                ponto.atenuacao += ponto.delta
                if ponto.atenuacao >= 40:
                    ponto.atenuacao = 40
                ponto.status = '-'
        else:
            ponto.atenuacao += ponto.delta
            if ponto.atenuacao >= 40:
                ponto.atenuacao = 40
            ponto.status = '-'

    if ponto.status == '=':
        Dados.gContIgual += 1
        if Dados.gFlutuacao and not Dados.DadosExame.LF and Dados.gExame[idPto].SF and not Dados.LimQuad:
            setLimiarFlutuacao(matExame, idPto)

    if resp == 1 and not Dados.DadosExame.LF and not Dados.DadosExame.ThrRel and not Dados.LimQuad:
        VerifyFalseNegative()

    return resp
