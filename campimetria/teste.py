import pygame
import os
import sys


# Adiciona os caminhos (suas pastas de constantes, páginas, procedimentos, etc.)
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




from dados import *


if __name__ == "__main__":
    pygame.init()    
    pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    ContagemRegressiva
