import pygame
import random
import sys
import os
import OPi.GPIO as GPIO

PIN_ENTRADA = "PD22"

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
from ManchaCega import TesteLimiarManchaCega


from ContagemRegressiva import ContagemRegressiva
from dados import *
from TelaResultadoScreening import ResultadoScreening
from fixacao_central import FixacaoCentral
from MenuPausa import MenuPausa
from strategy_screen import StrategyScreen

from cordenadas_mcdir import cordenadas_mcdir
from cordenadas_mcesq import cordenadas_mcesq


class Screening:

    def __init__(self, game):
        self.game = game
        
        
        self.cordenadas = []
        if DadosExame.programa_selecionado == Constantes.central30:
            from cordenadas_30 import cordenadas_30
            self.cordenadas = cordenadas_30
        elif DadosExame.programa_selecionado == Constantes.central24 and DadosExame.olho == Constantes.olho_direito:
            from cordenadas_24OD import cordenadas_24OD
            self.cordenadas = cordenadas_24OD
        elif DadosExame.programa_selecionado == Constantes.central24 and DadosExame.olho == Constantes.olho_esquerdo:
            from cordenadas_24OE import cordenadas_24OE
            self.cordenadas = cordenadas_24OE
        elif DadosExame.programa_selecionado == Constantes.central75 and DadosExame.olho == Constantes.olho_direito:
            from cordenadas_ESTOD import cordenadas_ESTOD
            self.cordenadas = cordenadas_ESTOD
        elif DadosExame.programa_selecionado == Constantes.central75 and DadosExame.olho == Constantes.olho_esquerdo:
            from cordenadas_ESTOE import cordenadas_ESTOE
            self.cordenadas = cordenadas_ESTOE
        elif DadosExame.programa_selecionado == Constantes.central75 and DadosExame.olho == Constantes.binocular:
            from cordenadas_ESTBIN import cordenadas_ESTBIN
            self.cordenadas = cordenadas_ESTBIN
        

        self.pontos = self.criar_pontos()
        self.indice_atual = 0
        self.menu = MenuPausa()
        self.voltar_ao_menu_inicial = False

        self.estado = "inicio"
        self.teste_fixacao = True
        self.aviso_inicial_respondido: bool = None

        self.mancha_cega = TesteLimiarManchaCega()
        self.indice_atual = 0
        self.matriz_mancha_cega = (
            cordenadas_mcdir
            if DadosExame.olho == Constantes.olho_direito
            else cordenadas_mcesq
        )

        random.shuffle(self.matriz_mancha_cega)
        self.total_pontos_mancha = len(self.matriz_mancha_cega)
        self.delay_entre_pontos = 100
        self.reiniciar = False

        random.shuffle(self.pontos)
        self.tempo_resposta = 2.0
        self.tempos = []
        self.pontos_vistos = []
        self.testemancha = 0
        self.testenegativo = 0
        self.testepositivo = 0

        self.total_pontos_exame = len(self.pontos)
        print(self.total_pontos_exame)

        self.tempo_inicial_exame = 0
        self.tempo_final_exame = 0
        self.tempo_decorrido_exame = 0
        self.tempo_pausado = 0
        self.tecla_pause_pressionada = False
        self.tecla_menu_pressionada = False

    def media_de_tempo_de_resposta_paciente(self, tempos):
        tempo_medio = sum(tempos) / len(tempos)
        if tempo_medio < 1.0:
            tempo_medio = 1.0
        if tempo_medio > 2.0:
            tempo_medio = 2.0
        return tempo_medio

    def criar_pontos(self):
        return [Ponto(x, y, tamanhoPonto = DadosExame.tamanho_estimulo, cor =  (255, 255, 255), distancia = DadosExame.distancia_paciente) for x, y in self.cordenadas]

    def testa_mancha_cega(self, ponto):
        x, y = ponto
        teste = Ponto(x, y, tamanhoPonto = DadosExame.tamanho_estimulo, cor = (255,255,255), distancia = DadosExame.distancia_paciente)
        continua = self.verifica_testa_ponto(
            teste.testaPonto(
                0.2, 2, menu_pressionado=self.verifica_tecla_pressionada_menu()
            )
        )
        if not continua:
            return
        if teste.response_received:
            return 1
        else:
            return 0

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j: 
                    print("entrei no for")
                    self.menu.usuario = "OPERADOR"
                    tempo_inicial = pygame.time.get_ticks()
                    while self.menu.selecionando:
                        self.menu.handle_event()
                        self.menu.draw()
                        self.menu.update()
                    self.menu.selecionando = True
                    tempo_final = pygame.time.get_ticks()
                    tempo_decorrido = tempo_final - tempo_inicial
                    self.tempo_pausado += tempo_decorrido
                    if self.menu.sair:
                        self.voltar_ao_menu_inicial = True

    def update(self):
        print(f"indice atual: {self.indice_atual}")
        pygame.display.update()
        if self.voltar_ao_menu_inicial:
            from select_eye_screen import SelectEyeScreen
            self.game.change_screen(SelectEyeScreen(self.game))

    def verifica_tecla_pressionada_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    return True
                else:
                    return False

    def verifica_testa_ponto(self, testaponto):
        menu_pause = testaponto
        if menu_pause:
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_j}))
            return False
        else:
            return True

    def draw(self, surface):
        print(DadosExame.olho)
        if self.menu.sair:
            return

        if self.estado == "inicio":
            self.aviso_inicial_respondido = ContagemRegressiva.iniciar_contagem(5)
            if self.aviso_inicial_respondido == False:
                self.voltar_ao_menu_inicial = True
            else:
                if DadosExame.programa_selecionado == Constantes.central75 and DadosExame.olho == Constantes.binocular:
                    self.estado = "exame"
                    self.teste_fixacao = False
                else: 
                    self.estado = "encontrando_mancha"
                self.tempo_inicial_exame = pygame.time.get_ticks()

        elif self.estado == "encontrando_mancha":
            if self.indice_atual < self.total_pontos_mancha:
                ponto = self.matriz_mancha_cega[self.indice_atual]
                x, y = ponto
                cor_ponto = Ponto.db_para_intensidade(0)
                teste = Ponto(x, y, tamanhoPonto = DadosExame.tamanho_estimulo,cor =  cor_ponto, distancia = DadosExame.distancia_paciente)
                continua = self.verifica_testa_ponto(
                    teste.testaPonto(
                        0.2, 2, menu_pressionado=self.verifica_tecla_pressionada_menu()
                    )
                )
                if not continua:
                    return

                if not teste.response_received:
                    self.mancha_cega.pontos_naorespondidos.append((teste.xg, teste.yg))
                self.indice_atual += 1

            if self.indice_atual == self.total_pontos_mancha:
                self.indice_atual = 0
                if len(self.mancha_cega.pontos_naorespondidos) == 0:
                    self.mancha_cega.verifica_mensagem()
                    if self.mancha_cega.reiniciar:
                        self.mancha_cega.pontos_naorespondidos = []
                        self.mancha_cega.reiniciar = False
                        voltando = ContagemRegressiva.iniciar_contagem(
                            5, fixacao="central"
                        )
                        if voltando == False:
                            self.voltar_ao_menu_inicial = True
                            return
                    else:
                        self.mancha_cega.encontrou_mancha = False
                        voltando = ContagemRegressiva.iniciar_contagem(
                            5, fixacao="central"
                        )
                        if voltando == False:
                            self.voltar_ao_menu_inicial = True
                            return
                else:
                    self.resultado = self.mancha_cega.calculo_centro_de_massa()
                    self.mancha_cega.encontrou_mancha = True
                    DadosExame.posicao_mancha_cega = self.resultado

            if self.mancha_cega.encontrou_mancha != None:
                if self.mancha_cega.encontrou_mancha:
                    self.teste_fixacao = True
                elif self.mancha_cega.encontrou_mancha == False:
                    self.teste_fixacao = False
                self.estado = "exame"

        elif self.estado == "exame":

            if self.indice_atual < self.total_pontos_exame:

                self.pontos[self.indice_atual].cor = self.pontos[
                    self.indice_atual
                ].db_para_intensidade(DadosExame.atenuacao_screening)
                
                continua = self.verifica_testa_ponto(
                    self.pontos[self.indice_atual].testaPonto(
                        0.2,
                        self.tempo_resposta,
                        menu_pressionado=self.verifica_tecla_pressionada_menu(),
                    )
                )
                if not continua:
                    return
                
                if self.pontos[self.indice_atual].response_received:
                    self.pontos_vistos.append(self.pontos[self.indice_atual])
                    self.pontos[self.indice_atual].limiar_encontrado = True
                    self.tempos.append(self.pontos[self.indice_atual].tempo_resposta)
                self.testemancha += 1
                self.testenegativo += 1
                self.testepositivo += 1
                if self.testemancha == 10 and self.teste_fixacao:
                    print("testando mancha cega...")
                    DadosExame.perda_de_fixacao += self.testa_mancha_cega(
                        DadosExame.posicao_mancha_cega
                    )
                    self.testemancha = 0
                    DadosExame.total_testes_mancha += 1

                if self.testepositivo == 15 and len(self.pontos_vistos) > 1:
                    print("testando falso positivo...")
                    ponto_teste_positivo = Ponto(self.pontos_vistos[-1].xg,self.pontos_vistos[-1].yg,self.pontos_vistos[-1].tamanhoPonto,Colors.BACKGROUND ,self.pontos_vistos[-1].distanciaPacienteTela)
                                                          
                    continua = self.verifica_testa_ponto(
                        ponto_teste_positivo.testaPonto(
                            0.2,
                            self.tempo_resposta,
                            menu_pressionado=self.verifica_tecla_pressionada_menu(),
                        )
                    )
                    if not continua:
                        return
                    DadosExame.total_testes_falsos_positivo += 1
                    if ponto_teste_positivo.response_received:
                        DadosExame.falso_positivo_respondidos += 1
                    self.testepositivo = 0
                if self.testenegativo == 12 and len(self.pontos_vistos) > 1:
                    print("testando falso negativo...")
                    ponto_teste_negativo = Ponto(self.pontos_vistos[-1].xg,self.pontos_vistos[-1].yg,self.pontos_vistos[-1].tamanhoPonto,Ponto.db_para_intensidade((DadosExame.atenuacao_screening - 9) if DadosExame.atenuacao_screening >= 9 else 0),self.pontos_vistos[-1].distanciaPacienteTela)
                    
                    
                    continua = self.verifica_testa_ponto(
                        ponto_teste_negativo.testaPonto(
                            0.2,
                            self.tempo_resposta,
                            menu_pressionado=self.verifica_tecla_pressionada_menu(),
                        )
                    )
                    if not continua:
                        return
                    DadosExame.total_testes_falsos_negativo += 1
                    if not ponto_teste_negativo.response_received:
                        DadosExame.falso_negativo_respondidos += 1
                    self.testenegativo = 0

                if len(self.tempos) == 5:
                    self.tempo_resposta = self.media_de_tempo_de_resposta_paciente(
                        self.tempos
                    )
                    self.tempos = []

                self.indice_atual += 1
                DadosExame.total_de_pontos_testados += 1

            if self.indice_atual == self.total_pontos_exame:
                self.tempo_final_exame = pygame.time.get_ticks()
                self.tempo_decorrido_exame = (
                    self.tempo_final_exame
                    - self.tempo_inicial_exame
                    - self.tempo_pausado
                )
                DadosExame.duracao_do_exame = self.tempo_decorrido_exame

                DadosExame.matriz_pontos = self.pontos
                self.estado = "resultado"

        elif self.estado == "resultado":
            ResultadoScreening.exibir_resultados()
            self.game.change_screen(StrategyScreen(self.game))
