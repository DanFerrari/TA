import pygame
import time
import math
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "constants")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "pages")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "procedures")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "strategies")))

from Ponto import Ponto

class TestaLimiar():
    
    def __init__(self, ponto:Ponto):
        self.ponto = ponto
        self.self.UV = 0
        self.AT = 0
        self.UNV = 0
        self.NC = 0
        self.Delta = 0
        self.viu = 0
        self.Dbig = 3
        self.Dsmall = 2
        self.limiarok = False
        self.status = ""
        self.limiar = 0
        self.primeiro = True
        self.limiarok = False
   
    
    def calcular_limiar_foveal(self):  
        
        
            if self.self.status == "=":
                self.ponto.limiar_encontrado = True
                return
            if self.ponto.response_received:
                self.viu = 2
            else:
                self.viu = 1
            pygame.time.delay(500)
            match self.viu:
                case 1:
                    if self.AT <= 0:
                        self.AT = -1
                        self.status = "="
                        #break

                    self.UNV = self.AT
                    if self.primeiro == True:
                        self.primeiro = False
                        self.NC = 0
                        self.UV = 0
                        self.Delta = self.Dbig
                        self.AT = self.AT - self.Delta
                        self.status = "+"
                        #break
                    if self.status == "-":
                        self.NC += 1
                        self.Delta = self.Dsmall
                        if self.NC >= 2:
                            self.status = "="
                            self.AT = (self.UV + self.UNV) / 2
                            #break
                        else:
                            self.AT = self.AT - self.Delta
                            self.status = "+"
                            #break
                    else:
                        self.AT = self.AT - self.Delta
                        self.status = "+"
                        #break

                case 2:
                    self.UV = self.AT
                    if self.primeiro == True:
                        self.primeiro = False
                        self.NC = 0
                        self.UNV = 35
                        self.Delta = self.Dbig
                        self.AT = self.AT + self.Delta
                        self.status = "-"
                        #break

                    if self.status == "+":
                        self.NC = +1
                        self.Delta = self.Dsmall

                        if self.NC >= 2:
                            self.status = "="
                            self.AT = (self.UV + self.UNV) / 2
                            #break

                        else:
                            self.AT = self.AT + self.Delta
                            self.status = "-"
                            #break

                    else:
                        self.AT = self.AT + self.Delta
                        self.status = "-"
                        #break

            if self.AT > 40:
                self.AT = 35

            self.limiar = self.AT

            self.limiarok = True
            self.ponto.db = self.limiar
 