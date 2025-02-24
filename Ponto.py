import pygame
import time
import math


class Ponto():
    def __init__(self,xg, yg, tamanhoPonto, cor):      
        self.xg = xg
        self.yg = yg
        self.tamanhoPonto = tamanhoPonto
        self.cor = cor
        self.db = 0
        self.resolucaoX = 0.246875
        self.resolucaoY = 0.250
        self.resolucao_video = 0.2484375
        self.x = 0
        self.y = 0
        self.response_received = False
        self.current_db = 0
        self.tempo_resposta = 0
        self.clock = pygame.time.Clock()
        self.distanciaPacienteTela = 200
        self.screen_width = 1920
        self.screen_height = 1080
        self.surface = pygame.display.get_surface()
        self.background_db = -4.0 
        self.BACKGROUND_COLOR = self.surface.get_at((0,0))
        xrad = math.radians((self.xg))
        xmm = self.distanciaPacienteTela * math.tan(xrad)
        yrad = math.radians((self.yg))
        ymm = self.distanciaPacienteTela * math.tan(yrad)
        self.pontoPix = tamanhoPonto / self.resolucao_video

        # Converte para pixels
        self.x = xmm / self.resolucaoX
        self.y = ymm / self.resolucaoY

        # Ajusta posição com base nos quadrantes
        # if self.xg < 0:
        #     self.x = -self.x
        # if self.yg < 0:
        #     self.y = -self.y
        
        # Ajusta para o centro da tela
        self.x = round(self.x + self.screen_width / 2 )
        self.y = round(self.y + self.screen_height / 2 )  
        
    def intensity_to_db(self,intensity, max_intensity=255):
        """
        Converte a intensidade (0 a 255) para dB, considerando 255 como 0 dB.
        Se intensity for 0, retorna -infinito.
        """
        if intensity > 0:
            return 20 * math.log10(intensity / max_intensity)
        return float('-inf')
    
    def plotarPonto(self):
        
        pygame.draw.circle(self.surface , self.cor,(self.x,self.y),self.pontoPix)
        pygame.display.update()
        
      
    def desenhaQuadrado(self):
        rect_size = self.pontoPix * 2
        rect_x = self.x + self.pontoPix
        rect_y = self.y + self.pontoPix
        pygame.draw.rect(self.surface, self.cor, (rect_x, rect_y, rect_size, rect_size))
        pygame.display.update((rect_x, rect_y, rect_size, rect_size))
    
    def testaPonto(self, tempo_exposicao,tempo_resposta_paciente):            
                
                
        trial_start_time = pygame.time.get_ticks()
        stimulus_end_time = trial_start_time + int(tempo_exposicao * 1000)
        response_deadline = trial_start_time + int(tempo_resposta_paciente * 1000)
        self.response_received = False
        init_intensity_db = self.background_db / 2
        # Parâmetros do procedimento
        current_intensity = int(255 * (10 ** (init_intensity_db / 20))) 
        self.current_db = self.intensity_to_db(current_intensity)
      
        
        while pygame.time.get_ticks() < response_deadline:
            current_time = pygame.time.get_ticks()
            if current_time < stimulus_end_time:
                    
                pygame.draw.circle(self.surface , self.cor, (self.x, self.y), self.pontoPix)
                pygame.display.update()
              
            else:
                self.apagarPonto()                  
            
        
            for event in pygame.event.get():                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.tempo_resposta = pygame.time.get_ticks() - trial_start_time
                    self.response_received = True                    
                    break
                if event.type ==pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
            
            if self.response_received:
                break
            self.clock.tick(60)

        
    def apagarPonto(self):
        pygame.draw.circle(self.surface , self.BACKGROUND_COLOR, (self.x, self.y), self.pontoPix)
        pygame.display.update()
        