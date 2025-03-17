import pygame
import os
import sys
import numpy as np
import OPi.GPIO as GPIO

# Adiciona os caminhos (suas pastas de constantes, páginas, procedimentos, etc.)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "constants")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "pages")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "procedures")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "strategies")))


from constants.dados import *
from pages.strategy_screen import StrategyScreen

BOTAO_PINO = 98

GPIO.setmode(GPIO)
GPIO.setup(BOTAO_PINO,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)


def testeGPIO():
    try:
        while True:
            estado = GPIO.input(BOTAO_PINO)  # Lê o pino
            if estado == GPIO.HIGH:
                print("Botão pressionado!")
            else:
                print("Botão solto!")
            pygame.time.delay(100)  # Pequeno delay para evitar leituras muito rápidas
    except KeyboardInterrupt:
        print("\nEncerrando...")
        GPIO.cleanup()  # Libera os pinos ao sair


class Campimetria:
    

    
    def __init__(self):
        pygame.init()
        # Configura a tela em FULLSCREEN e captura dimensões
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width, self.height = self.screen.get_size()
        pygame.display.set_caption("Seleção de Estratégia")
        self.clock = pygame.time.Clock()
        self.running = True

        # Definições de cores e fontes
        self.cor_fundo = (20, 20, 20)
        self.cor_botao = (122, 122, 122)
        self.cor_botao_hover = (255, 255, 255)
        self.cor_texto = (255, 255, 255)
        self.font_main = pygame.font.Font(None, int(self.height * 0.07))
        
        # Estado inicial: tela de seleção de estratégia
        self.current_screen = StrategyScreen(self)

    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            # Delegamos o tratamento de eventos, atualização e desenho para a tela ativa
            self.current_screen.handle_events(events)
            self.current_screen.update()
            self.current_screen.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def change_screen(self, new_screen):
        self.current_screen = new_screen
        

    

if __name__ == "__main__":
    testeGPIO()

    # game = Campimetria()
    # game.run()    
    # caminho = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', "lib","mainTA.py"))
    # os.execvp("python", ["python", caminho])
        