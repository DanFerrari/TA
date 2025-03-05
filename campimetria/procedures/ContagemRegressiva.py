import pygame
import time
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "constants")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "pages")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "procedures")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "strategies")))
from dados import Colors

class ContagemRegressiva():
    @staticmethod
    def iniciar_contagem(start_time):
        """
        Exibe uma contagem regressiva de 3 segundos na tela.

        Args:
            surface: A tela do pygame onde o texto será desenhado.
            fonte: Objeto pygame.font.Font para renderizar o texto.
            posicao: Tupla (x, y) indicando onde exibir o texto na tela.
        """

        for i in range(start_time, 0, -1):
            pygame.display.get_surface().fill(Colors.BACKGROUND)  # Limpa a tela (preto)
            texto = pygame.font.Font(None, 150).render(
                str(i), True, (255, 255, 255)
            )  # Texto branco
            pygame.display.get_surface().blit(texto, (1920 / 2 - 37, 1080 / 2 - 37))
            pygame.display.update()
            time.sleep(1)  # Aguarda 1 segundo