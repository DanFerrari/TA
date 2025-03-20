import sys, os, random, pygame
import OPi.GPIO as GPIO

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
from cordenadas_30 import cordenadas_30
from ContagemRegressiva import ContagemRegressiva
from LimiarFoveal import CalcularLimiar
from TelaResultadoFullThreshold import ResultadoFullthreshold
from ManchaCega import TesteLimiarManchaCega
from fixacao_central import FixacaoCentral
from MenuPausa import MenuPausa


class FullThreshold:

    def __init__(self,game):
        self.game = game
        self.pontos = self.criar_pontos()
        self.indice_atual = 0
        self.UV = 0
        self.AT = 20
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
            3,
            (
                self.db_para_intensidade(self.AT),
                self.db_para_intensidade(self.AT),
                self.db_para_intensidade(self.AT),
            ),
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
            if DadosExame.olho == Contantes.olho_direito
            else cordenadas_mcesq
        )
        random.shuffle(self.matriz_mancha_cega)
        self.total_pontos_mancha = len(self.matriz_mancha_cega)
        self.delay_entre_pontos = 100
        self.reiniciar = False
        
        self.tempo_pausa = 0
        self.cronometrar = False
        
        random.shuffle(self.pontos)
        self.tempo_resposta = 2.0
        self.tempos = []
        self.pontos_vistos = []
        self.testemancha = 0
        self.testenegativo = 0
        self.testepositivo = 0

        self.total_pontos_exame = len(self.pontos)
        self.pontos_fechados = 0
        self.perda_de_fixacao = 0
        
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
        if ponto.status == "=":
            self.pontos_fechados += 1
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


    def update(self):
        print(f"indice atual: {self.indice_atual}")
        pygame.display.update()
        if self.voltar_ao_menu_inicial:
            self.game.change_screen(StrategyScreen(self.game))
        
        if self.cronometrar:
            tempo_inicial = self.tempo_pausa
            tempo_atual = pygame.time.get_ticks()
            tempo_decorrido = tempo_atual - tempo_inicial
            
            if tempo_decorrido > 2500:
                self.cronometrar = False
                self.pausa_paciente(reiniciar=True)
                print("entrei no menu")
                self.menu.usuario = "paciente"
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
              
    


    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:  # Volta para o menu ou sai
                    print("entrei no for")
                    self.menu.usuario = "operador"
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
          
                        
        if GPIO.input(PIN_ENTRADA) == GPIO.HIGH:
            if self.cronometrar:
                return
            self.cronometrar = True
            self.pausa_paciente(reiniciar = False)
        elif GPIO.input(PIN_ENTRADA) == GPIO.LOW:        
            self.cronometrar = False
            self.pausa_paciente(reiniciar=True)




    def pausa_paciente(self,reiniciar):
        if reiniciar:
            self.tempo_pausa = 0
            self.cronometrar = False
        else:
            self.tempo_pausa = pygame.time.get_ticks()
            
            



    def draw(self, surface):
        if self.menu.sair:
            return
        if self.estado == "inicio":
            self.aviso_inicial_respondido = ContagemRegressiva.iniciar_contagem(5)
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
                
        
        
        elif self.estado == "mancha_cega":
            if self.indice_atual < self.total_pontos_mancha:
                ponto = self.matriz_mancha_cega[self.indice_atual]
                x, y = ponto
                cor_ponto = Ponto.db_para_intensidade(0)
                teste = Ponto(x, y, 3, cor_ponto)
                teste.testaPonto(0.2, 2)
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
            if self.total_pontos_exame < self.pontos_fechados:
                random.shuffle(self.pontos)  # Embaralha a lista antes de testar
                ponto = self.pontos[self.indice_atual]
                if not ponto.status == "=":  # Apenas testa se ainda não foi ativado
                    ponto.cor = Ponto.db_para_intensidade(ponto.atenuacao)
                    ponto.testaPonto(0.2, self.tempo_resposta)
                    if ponto.response_received:
                        paciente_viu = 2
                    else:
                        paciente_viu = 1

                    self.teste_fullthreshold(paciente_viu=paciente_viu, ponto=ponto)
                    self.tempos.append(ponto.tempo_resposta)
                    self.testemancha += 1

                    if self.testemancha == 100 and self.teste_fixacao:
                        self.perda_de_fixacao += self.testa_mancha_cega(
                            DadosExame.posicao_mancha_cega
                        )
                        self.testemancha = 0
                        self.testes_realizados += 1
                    if len(self.tempos) == 5:
                        self.tempo_resposta = self.media_de_tempo_de_resposta_paciente(
                            self.tempos
                        )
                        self.tempos = []
                    print(
                        f"Ponto: ({ponto.x}, {ponto.y}), Atenuacao: {ponto.atenuacao}, Cor: {ponto.cor}"
                    )
                    print(
                        f"Ponto definidos: {DadosExame.total_pontos_definidos} Mancha: {self.testemancha}"
                    )
                    if self.indice_atual < 76:
                        self.indice_atual += 1
                    else:
                        self.indice_atual = 0
            
            else:
                DadosExame.matriz_pontos = self.pontos

            
                DadosExame.perda_de_fixacao = (
                    ((self.perda_de_fixacao / self.testes_realizados) * 100)
                    if self.perda_de_fixacao > 0.0
                    else 0
                )
                self.estado = "resultado"
            
           
        elif self.estado == "resultado":
            ResultadoFullthreshold.exibir_resultados()
            self.voltar_ao_menu_inicial = True
            
        
                        
    def db_para_intensidade(self,db, db_min=40, db_max=0, i_min=Colors.ERASE_INTENSITY, i_max=255):
        """Converte dB para intensidade de cor (escala logarítmica)."""
        norm_db = (db - db_min) / (db_max - db_min)  # Normaliza dB entre 0 e 1

        intensity = i_min + (i_max - i_min) * ((10 ** (norm_db) - 1) / (10**1 - 1))

        if intensity > 255:
            intensity = 255
        elif intensity < i_min:
            intensity = i_min

        return int(round(intensity))
        # return 110 + (255 - 110) * ((10**(db / 40) - 1) / (10**(1) - 1))

    def iniciar_teste_limiar_foveal(self):        
        
        if self.limiar_status != "=":
            self.ponto_limiar.response_received = False
            self.ponto_limiar.cor = (
                self.db_para_intensidade(self.AT),
                self.db_para_intensidade(self.AT),
                self.db_para_intensidade(self.AT),
            )

            self.ponto_limiar.testaPonto(0.2, 2.0)

            
            if self.ponto_limiar.response_received:
                self.viu = 2
            else:
                self.viu = 1
            pygame.time.delay(500)
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
                        self.UNV = 35
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
                self.AT = 35
        else:
            self.limiar = self.AT
            DadosExame.limiar_foveal = self.limiar
            print(f"Limiar Foveal: {self.limiar} dB")
            self.limiarok = True  
                             
