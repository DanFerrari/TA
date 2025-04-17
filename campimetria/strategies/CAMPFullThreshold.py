import sys, os, random, pygame
import OPi.GPIO as GPIO
import numpy as np
PIN_ENTRADA = 'PD22'

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
from ContagemRegressiva import ContagemRegressiva
from LimiarFoveal import CalcularLimiar
from TelaResultadoFullThreshold import ResultadoFullthreshold
from ManchaCega import TesteLimiarManchaCega
from fixacao_central import FixacaoCentral
from MenuPausa import MenuPausa
from cordenadas_mcdir import cordenadas_mcdir
from cordenadas_mcesq import cordenadas_mcesq
from strategy_screen import StrategyScreen



class FullThreshold:

    def __init__(self,game):
        
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
        elif DadosExame.programa_selecionado == Constantes.central10:
            from cordenadas_10 import cordenadas_10
            self.cordenadas = cordenadas_10
        
    
        
        self.game = game
        self.pontos = []
        self.indice_atual = 0
        self.UV = 0
        self.AT = 25
        self.UNV = 0
        self.NC = 0
        self.Delta = 0
        self.viu = 0
        self.Dbig = 3
        self.Dsmall = 2
        self.limiarok = False
        self.limiar_status = ""
        self.limiar = 0
        self.primeiro = True
        self.ponto_limiar = Ponto(
            0,
            0,
            tamanhoPonto = DadosExame.tamanho_estimulo,
            cor = (
                self.db_para_intensidade(self.AT),
                self.db_para_intensidade(self.AT),
                self.db_para_intensidade(self.AT),
            ),
            distancia =  DadosExame.distancia_paciente
        )
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
        

        
        
        self.tempo_resposta = 2
        self.tempos = []
        self.pontos_vistos = []
        self.testemancha = 0
        self.testenegativo = 0
        self.testepositivo = 0

        self.total_pontos_exame = 0
        self.pontos_fechados = []
        self.total_pontos_fechados = 0
        self.perda_de_fixacao = 0
        self.tempo_pausado = 0     
        
        
        self.ponto_NE = Ponto(-9,9,DadosExame.tamanho_estimulo,(0,0,0),DadosExame.distancia_paciente)        
        self.ponto_NO = Ponto(9,9,DadosExame.tamanho_estimulo,(0,0,0),DadosExame.distancia_paciente)
        self.ponto_SE = Ponto(9,-9,DadosExame.tamanho_estimulo,(0,0,0),DadosExame.distancia_paciente)
        self.ponto_SO = Ponto(-9,-9,DadosExame.tamanho_estimulo,(0,0,0),DadosExame.distancia_paciente)   
        self.ponto_quad = [self.ponto_NE,self.ponto_NO,self.ponto_SE,self.ponto_SO]
        random.shuffle(self.ponto_quad)
        
        
        
        self.tecla_menu_pressionada = False
        self.tecla_pause_pressionada = False
        self.primeira_varredura = True
        self.pontos_primeira_varredura = []
        self.cordenadas_primeira_varredura = [(3,3),(9,3),(3,9),(9,9),(15,3),(15,9),(15,15),(9,15),(3,15)]
        
    
    def criar_pontos(self):        
        for x,y in self.cordenadas:
            ponto = Ponto(x, y,tamanhoPonto = DadosExame.tamanho_estimulo, cor = (255, 255, 255), distancia = DadosExame.distancia_paciente)
            if x < 0 and y > 0:
                ponto.atenuacao = self.ponto_NO.atenuacao               
        
            elif x > 0 and y > 0:
                ponto.atenuacao = self.ponto_NE.atenuacao
        
            elif x < 0 and y < 0:
                ponto.atenuacao = self.ponto_SO.atenuacao
        
            else:
                ponto.atenuacao = self.ponto_SE.atenuacao
            
            if abs(ponto.xg) == 3 and  abs(ponto.yg) == 3:
                ponto.atenuacao -= 2
            elif (abs(ponto.xg) == 9 and  abs(ponto.yg) == 3 or abs(ponto.xg) == 15 and  abs(ponto.yg) == 3 or abs(ponto.xg) == 21 and  abs(ponto.yg) == 3  or abs(ponto.xg) == 3 and  abs(ponto.yg) == 9 or abs(ponto.xg) == 9 and  abs(ponto.yg) == 9 or abs(ponto.xg) == 15 and  abs(ponto.yg) == 9 or abs(ponto.xg) == 21 and  abs(ponto.yg) == 9  or abs(ponto.xg) == 3 and  abs(ponto.yg) == 15 or abs(ponto.xg) == 9 and  abs(ponto.yg) == 15 or abs(ponto.xg) == 15 and  abs(ponto.yg) == 15 or abs(ponto.xg) == 3 and  abs(ponto.yg) == 21 or abs(ponto.xg) == 9 and  abs(ponto.yg) == 21) :
                ponto.atenuacao -= 4
            elif (abs(ponto.xg) == 27 and  abs(ponto.yg) == 3 or abs(ponto.xg) == 27 and  abs(ponto.yg) == 9 or abs(ponto.xg) == 21 and  abs(ponto.yg) == 15 or abs(ponto.xg) == 15 and  abs(ponto.yg) == 21 or abs(ponto.xg) == 9 and  abs(ponto.yg) == 27 or abs(ponto.xg) == 3 and  abs(ponto.yg) == 27):
                ponto.atenuacao -= 6
            if (abs(ponto.xg),abs(ponto.yg)) in self.cordenadas_primeira_varredura:
                self.pontos_primeira_varredura.append(ponto)
                
            
            
            self.pontos.append(ponto)
        self.total_pontos_exame = len(self.pontos)
        random.shuffle(self.pontos)

        
    

    def teste_fullthreshold(self, paciente_viu: int, ponto) -> int:
        resp = 0

        if paciente_viu == 1:
            if ponto.atenuacao == 0:
                ponto.atenuacao = -1
                ponto.status = "="
                resp = 1
                return resp
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
                resp = 0
                return resp
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
                    return resp
                else:
                    ponto.atenuacao -= ponto.delta
                    if ponto.atenuacao <= 0:
                        ponto.atenuacao = 0
                    ponto.status = "+"
                    resp = 0 
                    return resp
            ponto.atenuacao -= ponto.delta
            if ponto.atenuacao <= 0:
                ponto.atenuacao = 0
            ponto.status = "+"
            resp = 0
            return resp    

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
                resp = 0
                return resp
            elif ponto.status == "+":
                ponto.numero_cruzamentos += 1
                ponto.delta = Constantes.smalldelta
                if ponto.numero_cruzamentos >= 2:
                    ponto.status = "="
                    ponto.atenuacao = (
                        ponto.ultima_atenuacao_nao_vista + ponto.ultima_atenuacao_vista
                    ) / 2
                    resp = 1
                    return resp
                else:
                    ponto.atenuacao += ponto.delta
                    if ponto.atenuacao >= 40:
                        ponto.atenuacao = 40
                    ponto.status = "-"
                    resp = 0
                    return resp
            
            ponto.atenuacao += ponto.delta
            if ponto.atenuacao >= 40:
                ponto.atenuacao = 40
            ponto.status = "-"
            resp = 0
            return resp

        #     if Dados.gFlutuacao and not Dados.DadosExame.LF and Dados.gExame[idPto].SF and not Dados.LimQuad:
        #         setLimiarFlutuacao(matExame, idPto)

        # if resp == 1 and not Dados.DadosExame.LF and not Dados.DadosExame.ThrRel and not Dados.LimQuad:
        #     VerifyFalseNegative()
        
        return resp

    def testa_mancha_cega(self, ponto):
        x, y = ponto
        teste = Ponto(x, y, tamanhoPonto = DadosExame.tamanho_estimulo, cor = Ponto.db_para_intensidade(0), distancia = DadosExame.distancia_paciente)
        continua = self.verifica_testa_ponto(teste.testaPonto(0.2, 2, menu_pressionado = self.verifica_tecla_pressionada_menu()))
        if not continua:
            return
        if teste.response_received:
            return 1
        else:
            return 0

    def media_de_tempo_de_resposta_paciente(self, tempos):
        tempo_medio = sum(tempos) / len(tempos)
        if tempo_medio < 1.0:
            tempo_medio = 1.0
        if tempo_medio > 2.0:
            tempo_medio = 2.0
        return tempo_medio


    def update(self):
        self.menu.fixacao = "diamante" if self.estado == "limiar_foveal"  else "central"
        print(f"indice atual: {self.indice_atual} estado: {self.estado} pontos encontrados: {len(self.pontos_fechados)},  total de pontos: {self.total_pontos_exame}, limiar foveal: {DadosExame.LimiarFoveal}")
        print(f"pontoNO:{self.ponto_NO.atenuacao}  pontoNE:{self.ponto_NE.atenuacao} pontoSO: {self.ponto_SO.atenuacao} pontoSE:{self.ponto_SE.atenuacao}")
        pygame.display.update()
        if self.voltar_ao_menu_inicial:
            from select_eye_screen import SelectEyeScreen
            self.game.change_screen(SelectEyeScreen(self.game))
            
    def handle_events(self, events):
        self.menu.fixacao = "diamante" if self.estado == "limiar_foveal" else "central"
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
                        
    def verifica_tecla_pressionada_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j: 
                    return True
                else:
                    return False
    
    
        
    def verifica_testa_ponto(self,testaponto):
        menu_pause = testaponto
        if menu_pause:      
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_j}))                 
            return False
        
        else:
            return True
        
        
    def draw(self, surface):
        if self.menu.sair:
            return
     
        if self.estado == "inicio":
            self.aviso_inicial_respondido = ContagemRegressiva.iniciar_contagem(5,fixacao = "diamante")
            if self.aviso_inicial_respondido == False:
                self.voltar_ao_menu_inicial = True               
            else:
                self.estado = "limiar_foveal"
                self.tempo_inicial_exame = pygame.time.get_ticks()
           
        
        elif self.estado == "limiar_foveal":            
            self.iniciar_teste_limiar_foveal()
            if self.limiarok:
                self.estado = "mancha_cega"
                self.indice_atual = 0
                surface.fill(Colors.BACKGROUND)
                FixacaoCentral.plotar_fixacao_central()
                
                
        
        
        elif self.estado == "mancha_cega":
            if self.indice_atual < self.total_pontos_mancha:
                ponto = self.matriz_mancha_cega[self.indice_atual]
                x, y = ponto
                cor_ponto = Ponto.db_para_intensidade(0)
                teste = Ponto(x, y, tamanhoPonto = DadosExame.tamanho_estimulo, cor = cor_ponto, distancia = DadosExame.distancia_paciente)
                continua = self.verifica_testa_ponto(teste.testaPonto(0.2, self.tempo_resposta, menu_pressionado = self.verifica_tecla_pressionada_menu()))
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
                        voltando = ContagemRegressiva.iniciar_contagem(5)
                        if voltando == False:
                            self.voltar_ao_menu_inicial = True
                            return
                    else:
                        self.mancha_cega.encontrou_mancha = False
                        voltando = ContagemRegressiva.iniciar_contagem(5,fixacao = "central")
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
                self.estado = "quadrante"
                self.indice_atual = 0
        
        
        elif self.estado == "quadrante":
            self.testa_quadrante() 
            
        elif self.estado == "exame":
            
            
            if self.primeira_varredura:
                ponto = self.pontos_primeira_varredura[self.indice_atual]
                ponto.cor = Ponto.db_para_intensidade(ponto.atenuacao)
                continua = self.verifica_testa_ponto(ponto.testaPonto(0.2, self.tempo_resposta, menu_pressionado = self.verifica_tecla_pressionada_menu()))
                if not continua:
                    return            
                if ponto.response_received:
                    self.pontos_vistos.append(ponto)
                    self.tempos.append(ponto.tempo_resposta)

                    paciente_viu = 2
                else:
                    paciente_viu = 1
                if self.teste_fullthreshold(paciente_viu=paciente_viu, ponto=ponto) == 1:
                    self.total_pontos_fechados += 1                        
                    self.pontos_fechados.append(self.pontos.pop(self.indice_atual))
                self.indice_atual += 1
                if self.indice_atual == 35:
                    self.indice_atual = 0 
                    self.primeira_varredura = False
                
            self.indice_atual += 1
            if self.indice_atual >= len(self.pontos):
                self.indice_atual = 0
                
            if self.total_pontos_fechados  <  self.total_pontos_exame:
                ponto = self.pontos[self.indice_atual]
                if not ponto.status == "=":  # Apenas testa se ainda não foi ativado
                    self.testemancha += 1
                    self.testenegativo +=1
                    self.testepositivo += 1
                    ponto.cor = Ponto.db_para_intensidade(ponto.atenuacao)
                    continua = self.verifica_testa_ponto(ponto.testaPonto(0.2, self.tempo_resposta, menu_pressionado = self.verifica_tecla_pressionada_menu()))
                    if not continua:
                        return            
                    if ponto.response_received:
                        self.pontos_vistos.append(ponto)
                        self.tempos.append(ponto.tempo_resposta)

                        paciente_viu = 2
                    else:
                        paciente_viu = 1

                    if self.teste_fullthreshold(paciente_viu=paciente_viu, ponto=ponto) == 1:
                        self.total_pontos_fechados += 1                        
                        self.pontos_fechados.append(self.pontos.pop(self.indice_atual))
                        
                    
                        
                    if self.testemancha == 35 and self.teste_fixacao:
                        print("testando mancha cega...")
                        self.perda_de_fixacao += self.testa_mancha_cega(
                            DadosExame.posicao_mancha_cega
                        )
                        self.testemancha = 0
                        DadosExame.total_testes_mancha += 1
            
                    if len(self.tempos) == 2:
                        self.tempo_resposta = self.media_de_tempo_de_resposta_paciente(
                            self.tempos
                        )
                        self.tempos = []
                        
                    
                    if self.testepositivo == 40 and len(self.pontos_vistos) > 0:
                        print("testando falso positivo...")
                        ponto_teste_positivo = Ponto(self.pontos_vistos[-1].xg,self.pontos_vistos[-1].yg,self.pontos_vistos[-1].tamanhoPonto,Colors.BACKGROUND ,self.pontos_vistos[-1].distanciaPacienteTela)

                        continua = self.verifica_testa_ponto(ponto_teste_positivo.testaPonto(0.2, self.tempo_resposta, menu_pressionado = self.verifica_tecla_pressionada_menu()))
                        if not continua:
                            return          
                        DadosExame.total_testes_falsos_positivo += 1
                        if ponto_teste_positivo.response_received:
                            DadosExame.falso_positivo_respondidos += 1
                        self.testepositivo = 0
                    
                    
                    if self.testenegativo == 45 and len(self.pontos_vistos) > 0:
                        print("testando falso negativo...")
                        ponto_teste_negativo = Ponto(self.pontos_vistos[-1].xg,self.pontos_vistos[-1].yg,self.pontos_vistos[-1].tamanhoPonto,Ponto.db_para_intensidade((self.pontos_vistos[-1].atenuacao - 9) if self.pontos_vistos[-1].atenuacao >= 9 else 0),self.pontos_vistos[-1].distanciaPacienteTela)
                        
                        continua = self.verifica_testa_ponto(ponto_teste_negativo.testaPonto(0.2, self.tempo_resposta, menu_pressionado = self.verifica_tecla_pressionada_menu()))
                        if not continua:
                            return  
                        DadosExame.total_testes_falsos_negativo += 1
                        if not ponto_teste_negativo.response_received:
                            DadosExame.falso_negativo_respondidos += 1
                        self.testenegativo = 0
                    
                        
                    
                   
                                 
                    print(
                        f"Ponto: ({ponto.x}, {ponto.y}), Atenuacao: {ponto.atenuacao}, Cor: {ponto.cor}"
                    )
                   
                    DadosExame.total_de_pontos_testados += 1

            
            if self.total_pontos_exame == len(self.pontos_fechados): 
                self.tempo_final_exame = pygame.time.get_ticks()
                self.tempo_decorrido_exame = self.tempo_final_exame - self.tempo_inicial_exame
                DadosExame.duracao_do_exame = self.tempo_decorrido_exame
                DadosExame.matriz_pontos = self.pontos_fechados          
            
                self.estado = "resultado"
           
        elif self.estado == "resultado":
            ResultadoFullthreshold.exibir_resultados()
            self.game.change_screen(StrategyScreen(self.game))
            
        
                        
    def db_para_intensidade(self,db, db_min=Constantes.dbMax, db_max=0, i_min=Colors.ERASE_INTENSITY, i_max=255):
        """Converte dB para intensidade de cor (escala logarítmica)."""
        norm_db = (db - db_min) / (db_max - db_min)  # Normaliza dB entre 0 e 1

        intensity = i_min + (i_max - i_min) * ((10 ** (norm_db) - 1) / (10**1 - 1))

        if intensity > 255:
            intensity = 255
        elif intensity < i_min:
            intensity = i_min

        #return int(round(intensity))
        return (intensity)

        
        
    def iniciar_teste_limiar_foveal(self):        
        
        if self.limiar_status != "=":
            self.ponto_limiar.response_received = False
            self.ponto_limiar.cor = (
                self.db_para_intensidade(self.AT),
                self.db_para_intensidade(self.AT),
                self.db_para_intensidade(self.AT),
            )

            continua = self.verifica_testa_ponto(self.ponto_limiar.testaPonto(0.2, 2, menu_pressionado = self.verifica_tecla_pressionada_menu()))
            if not continua:
                return
            
            if self.ponto_limiar.response_received:
                self.viu = 2
            else:
                self.viu = 1

            match self.viu:
                case 1:
                    if self.AT <= 0:
                        self.AT = -1
                        self.limiar_status = "="
                        return

                    self.UNV = self.AT
                    if self.primeiro == True:
                        self.primeiro = False
                        self.NC = 0
                        self.UV = 0
                        self.Delta = self.Dbig
                        self.AT = self.AT - self.Delta
                        self.limiar_status = "+"
                        return
                    if self.limiar_status == "-":
                        self.NC += 1
                        self.Delta = self.Dsmall
                        if self.NC >= 2:
                            self.limiar_status = "="
                            self.AT = (self.UV + self.UNV) / 2
                            return
                        else:
                            self.AT = self.AT - self.Delta
                            self.limiar_status = "+"
                            return
                    else:
                        self.AT = self.AT - self.Delta
                        self.limiar_status = "+"
                        return

                case 2:
                    self.UV = self.AT
                    if self.primeiro == True:
                        self.primeiro = False
                        self.NC = 0
                        self.UNV = Constantes.dbMax
                        self.Delta = self.Dbig
                        self.AT = self.AT + self.Delta
                        self.limiar_status = "-"
                        return

                    if self.limiar_status == "+":
                        self.NC = +1
                        self.Delta = self.Dsmall

                        if self.NC >= 2:
                            self.limiar_status = "="
                            self.AT = (self.UV + self.UNV) / 2
                            return

                        else:
                            self.AT = self.AT + self.Delta
                            self.limiar_status = "-"
                            return

                    else:
                        self.AT = self.AT + self.Delta
                        self.limiar_status = "-"
                        return

            if self.AT > 40:
                self.AT = Constantes.dbMax
        else:
            self.limiar = self.AT
            DadosExame.LimiarFoveal = self.limiar
            for ponto in self.ponto_quad:
                ponto.atenuacao = self.limiar - 12
           
            self.limiarok = True  
            self.UV = 0
            self.AT = 25
            #self.AT = 30
            self.UNV = 0
            self.NC = 0
            self.Delta = 0
            self.viu = 0
            self.Dbig = 6
            self.Dsmall = 3
            self.limiar_status = ""
            self.limiar = 0
            self.primeiro = True
            
            



    def testa_quadrante(self):

        if  not all(ponto.status == "=" for ponto in self.ponto_quad):
            self.indice_atual += 1
            if self.indice_atual == 4:
                self.indice_atual = 0
            if self.ponto_quad[self.indice_atual].status == "=":
                return
            self.ponto_quad[self.indice_atual].response_received = False
            self.ponto_quad[self.indice_atual].cor = (
                self.db_para_intensidade(self.ponto_quad[self.indice_atual].atenuacao),
                self.db_para_intensidade(self.ponto_quad[self.indice_atual].atenuacao),
                self.db_para_intensidade(self.ponto_quad[self.indice_atual].atenuacao),
            )

            continua = self.verifica_testa_ponto(self.ponto_quad[self.indice_atual].testaPonto(0.2, self.tempo_resposta, menu_pressionado = self.verifica_tecla_pressionada_menu()))
            if not continua:
                return
            
            if self.ponto_quad[self.indice_atual].response_received:
                self.viu = 2
            else:
                self.viu = 1
           
            match self.viu:
                case 1:
                    if self.ponto_quad[self.indice_atual].atenuacao <= 0:
                        self.ponto_quad[self.indice_atual].atenuacao = -1
                        self.ponto_quad[self.indice_atual].status = "="
                        return

                    self.ponto_quad[self.indice_atual].ultima_atenuacao_nao_vista = self.ponto_quad[self.indice_atual].atenuacao
                    if self.ponto_quad[self.indice_atual].primeira_visualizacao == True:
                        self.ponto_quad[self.indice_atual].primeira_visualizacao = False
                        self.ponto_quad[self.indice_atual].numero_cruzamentos = 0
                        self.ponto_quad[self.indice_atual].ultima_atenuacao_vista = 0
                        self.ponto_quad[self.indice_atual].delta = self.Dbig
                        self.ponto_quad[self.indice_atual].atenuacao = self.ponto_quad[self.indice_atual].atenuacao - self.ponto_quad[self.indice_atual].delta
                        self.ponto_quad[self.indice_atual].status = "+"
                        return
                    if self.ponto_quad[self.indice_atual].status == "-":
                        self.ponto_quad[self.indice_atual].numero_cruzamentos += 1
                        self.ponto_quad[self.indice_atual].delta = self.Dsmall
                        if self.ponto_quad[self.indice_atual].numero_cruzamentos >= 1:
                            self.ponto_quad[self.indice_atual].status = "="
                            self.ponto_quad[self.indice_atual].atenuacao = (self.ponto_quad[self.indice_atual].ultima_atenuacao_vista + self.ponto_quad[self.indice_atual].ultima_atenuacao_nao_vista) / 2
                            return
                        else:
                            self.ponto_quad[self.indice_atual].atenuacao = self.ponto_quad[self.indice_atual].atenuacao - self.ponto_quad[self.indice_atual].delta
                            self.ponto_quad[self.indice_atual].status = "+"
                            return
                    else:
                        self.ponto_quad[self.indice_atual].atenuacao = self.ponto_quad[self.indice_atual].atenuacao - self.ponto_quad[self.indice_atual].delta
                        self.ponto_quad[self.indice_atual].status = "+"
                        return

                case 2:
                    self.ponto_quad[self.indice_atual].ultima_atenuacao_vista = self.ponto_quad[self.indice_atual].atenuacao
                    if self.ponto_quad[self.indice_atual].primeira_visualizacao == True:
                        self.ponto_quad[self.indice_atual].primeira_visualizacao = False
                        self.ponto_quad[self.indice_atual].numero_cruzamentos = 0
                        self.ponto_quad[self.indice_atual].ultima_atenuacao_nao_vista = Constantes.dbMax
                        self.ponto_quad[self.indice_atual].delta = self.Dbig
                        self.ponto_quad[self.indice_atual].atenuacao = self.ponto_quad[self.indice_atual].atenuacao + self.ponto_quad[self.indice_atual].delta
                        self.ponto_quad[self.indice_atual].status = "-"
                        return

                    if self.ponto_quad[self.indice_atual].status == "+":
                        self.ponto_quad[self.indice_atual].numero_cruzamentos = +1
                        self.ponto_quad[self.indice_atual].delta = self.Dsmall

                        if self.ponto_quad[self.indice_atual].numero_cruzamentos >= 1:
                            self.ponto_quad[self.indice_atual].status = "="
                            self.ponto_quad[self.indice_atual].atenuacao = (self.ponto_quad[self.indice_atual].ultima_atenuacao_vista + self.ponto_quad[self.indice_atual].ultima_atenuacao_nao_vista) / 2
                            return

                        else:
                            self.ponto_quad[self.indice_atual].atenuacao = self.ponto_quad[self.indice_atual].atenuacao + self.ponto_quad[self.indice_atual].delta
                            self.ponto_quad[self.indice_atual].status = "-"
                            return

                    else:
                        self.ponto_quad[self.indice_atual].atenuacao = self.ponto_quad[self.indice_atual].atenuacao + self.ponto_quad[self.indice_atual].delta
                        self.ponto_quad[self.indice_atual].status = "-"
                        return

            if self.ponto_quad[self.indice_atual].atenuacao > 40:
                self.ponto_quad[self.indice_atual].atenuacao = Constantes.dbMax
        else:       
            for ponto in self.ponto_quad:
                if ponto == self.ponto_NE:                    
                    self.ponto_NE.atenuacao = ponto.atenuacao  
                    
                
                if ponto == self.ponto_SO:                    
                    self.ponto_SO.atenuacao = ponto.atenuacao   
                    
                if ponto == self.ponto_SE:                    
                    self.ponto_SE.atenuacao = ponto.atenuacao    
                    
                if ponto == self.ponto_NO:                    
                    self.ponto_NO.atenuacao = ponto.atenuacao       
                    
                    
            self.criar_pontos()
            self.indice_atual = 0         
            self.estado = "exame"

            
                
