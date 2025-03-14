import sys, os, random, pygame

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
from cordenadas_30 import cordenadas_30
from ContagemRegressiva import ContagemRegressiva
from LimiarFoveal import CalcularLimiar
from TelaResultadoFullThreshold import ResultadoFullthreshold
from ManchaCega import TesteLimiarManchaCega
from fixacao_central import FixacaoCentral


class FullThreshold:

    def __init__(self):
        pass

    def criar_pontos(self):
        return [Ponto(x, y, 3, (255, 255, 255)) for x, y in cordenadas_30]

    def teste_fullthreshold(self, paciente_viu: int, ponto) -> int:
        resp = 0

        if paciente_viu == 1:
            if ponto.atenuacao == 0:
                ponto.atenuacao = -1
                ponto.status = "="
                resp = 1
            else:
                ponto.ultima_atenuacao_nao_vista = ponto.atenuacao
                if ponto.primeira_visualizacao:
                    ponto.primeira_visualizacao = False
                    ponto.ultima_atenuacao_vista = Constantes.dbMin
                    ponto.numero_cruzamentos = 0
                    ponto.delta = Constantes.bigdelta
                    ponto.atenuacao -= ponto.delta
                    if ponto.atenuacao <= 0:
                        ponto.atenuacao = 0
                    ponto.status = "+"
                elif ponto.status == "-":
                    ponto.numero_cruzamentos += 1
                    ponto.delta = Constantes.smalldelta
                    if ponto.numero_cruzamentos >= 2:
                        ponto.status = "="
                        ponto.atenuacao = (
                            ponto.ultima_atenuacao_nao_vista
                            + ponto.ultima_atenuacao_vista
                        ) / 2
                        resp = 1
                    else:
                        ponto.atenuacao -= ponto.delta
                        if ponto.atenuacao <= 0:
                            ponto.atenuacao = 0
                        ponto.status = "+"
                else:
                    ponto.atenuacao -= ponto.delta
                    if ponto.atenuacao <= 0:
                        ponto.atenuacao = 0
                    ponto.status = "+"

        elif paciente_viu == 2:
            ponto.ultima_atenuacao_vista = ponto.atenuacao
            if ponto.primeira_visualizacao:
                ponto.primeira_visualizacao = False
                ponto.numero_cruzamentos = 0
                ponto.ultima_atenuacao_nao_vista = Constantes.dbMax
                ponto.delta = Constantes.bigdelta
                ponto.atenuacao += ponto.delta
                if ponto.atenuacao >= 40:
                    ponto.atenuacao = 40
                ponto.status = "-"
            elif ponto.status == "+":
                ponto.numero_cruzamentos += 1
                ponto.delta = Constantes.smalldelta
                if ponto.numero_cruzamentos >= 2:
                    ponto.status = "="
                    ponto.atenuacao = (
                        ponto.ultima_atenuacao_nao_vista + ponto.ultima_atenuacao_vista
                    ) / 2
                    resp = 1
                else:
                    ponto.atenuacao += ponto.delta
                    if ponto.atenuacao >= 40:
                        ponto.atenuacao = 40
                    ponto.status = "-"
            else:
                ponto.atenuacao += ponto.delta
                if ponto.atenuacao >= 40:
                    ponto.atenuacao = 40
                ponto.status = "-"

        #     if Dados.gFlutuacao and not Dados.DadosExame.LF and Dados.gExame[idPto].SF and not Dados.LimQuad:
        #         setLimiarFlutuacao(matExame, idPto)

        # if resp == 1 and not Dados.DadosExame.LF and not Dados.DadosExame.ThrRel and not Dados.LimQuad:
        #     VerifyFalseNegative()

        return resp

    def testa_mancha_cega(self, ponto):
        x, y = ponto
        teste = Ponto(x, y, 3, Ponto.db_para_intensidade(0))
        teste.testaPonto(0.2, 2.0)
        if teste.response_received:
            return 1.0
        else:
            return 0.0

    def media_de_tempo_de_resposta_paciente(self, tempos):
        tempo_medio = sum(tempos) / len(tempos)
        if tempo_medio < 1.0:
            tempo_medio = 1.0
        if tempo_medio > 2.0:
            tempo_medio = 2.0
        return tempo_medio

    def main(self):
        CalcularLimiar.iniciar_teste_limiar_foveal()
        testando_mancha = True
        pygame.display.get_surface().fill(Colors.BACKGROUND)
        pontos = self.criar_pontos()
        tempo_resposta = 2.0
        tempos = []
        mancha_cega = False
        teste_de_fixacao = True
        perda_de_fixacao = 0.0
        testemancha = 0
        testes_realizados = 0

        while testando_mancha:
            verfica_mancha = TesteLimiarManchaCega.teste_mancha_cega(DadosExame.olho)
            if mancha_cega == True:
                ContagemRegressiva().iniciar_contagem(5)
                continue
            elif mancha_cega == False:
                teste_fixacao = False
                testando_mancha = False
        pygame.display.get_surface().fill(Colors.BACKGROUND)
        FixacaoCentral.plotar_fixacao_central()
        while not all(
            ponto.status == "=" for ponto in pontos
        ):  # Enquanto nem todos estiverem ativados
            random.shuffle(pontos)  # Embaralha a lista antes de testar
            for ponto in pontos:
                if not ponto.status == "=":  # Apenas testa se ainda não foi ativado
                    ponto.cor = Ponto.db_para_intensidade(ponto.atenuacao)
                    ponto.testaPonto(0.2, tempo_resposta)
                    if ponto.response_received:
                        paciente_viu = 2
                    else:
                        paciente_viu = 1

                    self.teste_fullthreshold(paciente_viu=paciente_viu, ponto=ponto)
                    tempos.append(ponto.tempo_resposta)
                    testemancha += 1

                    if testemancha == 100 and teste_de_fixacao:
                        perda_de_fixacao += self.testa_mancha_cega(
                            DadosExame.posicao_mancha_cega
                        )
                        testemancha = 0
                        testes_realizados += 1
                    if len(tempos) == 5:
                        tempo_resposta = self.media_de_tempo_de_resposta_paciente(
                            tempos
                        )
                        tempos = []
                    print(
                        f"Ponto: ({ponto.x}, {ponto.y}), Atenuacao: {ponto.atenuacao}, Cor: {ponto.cor}"
                    )
                    print(
                        f"Ponto definidos: {DadosExame.total_pontos_definidos} Mancha: {testemancha}"
                    )
        DadosExame.matriz_pontos = pontos

        visualizando = True
        pygame.display.get_surface().fill(Colors.BACKGROUND)
        fonte_label = pygame.font.Font(None, 30)
        perda_de_fixacao = (
            ((perda_de_fixacao / testes_realizados) * 100)
            if perda_de_fixacao > 0.0
            else 0
        )
        texto_label = fonte_label.render(
            f"Perda de fixacao: {perda_de_fixacao}%", True, (255, 255, 255)
        )
        pygame.display.get_surface().blit(
            texto_label,
            (
                pygame.display.get_surface().get_width()
                - texto_label.get_width()
                - 250,
                pygame.display.get_surface().get_height()
                - texto_label.get_height()
                - 150,
            ),
        )
        ResultadoFullthreshold.exibir_resultados()
        while visualizando:
            for evento in pygame.event.get():
                if (
                    evento.type == pygame.QUIT
                    or evento.type == pygame.KEYDOWN
                    and evento.key == pygame.K_j
                ):
                    visualizando = False
