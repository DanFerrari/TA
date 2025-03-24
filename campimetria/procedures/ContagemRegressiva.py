import pygame
import time
import os
import sys

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
from dados import Colors
from fixacao_central import FixacaoCentral
from fixacao_diamante import FixacaoDiamante
from area_exame_desenho import DesenhoAreaExame


class ContagemRegressiva:
    @staticmethod
    def iniciar_contagem(start_time, fixacao = "central"):

        pygame.display.get_surface().fill(Colors.BACKGROUND)

        iniciar_exame = False
        if fixacao == "central":
            FixacaoCentral.plotar_fixacao_central()
        elif fixacao == "diamante":
            FixacaoDiamante.plotar_fixacao_diamante()
        font = pygame.font.Font(None, 42)
        text = font.render(
            "Posicione corretamente o paciente na distância recomendada, apoie bem o queixo e a testa!",
            1,
            (255, 255, 255),
        )
        textpos = text.get_rect(centerx=960, centery=540 - 400)
        pygame.display.get_surface().blit(text, textpos)

        font = pygame.font.Font(None, 42)
        text2 = font.render(
            "Aperte ENTRA para continuar o exame ou aperte ESC para voltar",
            1,
            (255, 255, 255),
        )
        textpos2 = text2.get_rect(centerx=960, centery=540 - 300)
        pygame.display.get_surface().blit(text2, textpos2)

        DesenhoAreaExame.desenhar()
        pygame.display.update()
        while not iniciar_exame:
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        iniciar_exame = True
                    if event.key == pygame.K_j:
                        return False

        for i in range(start_time, -1, -1):
            pygame.display.get_surface().fill(Colors.BACKGROUND)  # Limpa a tela (preto)
            if fixacao == "central":
                FixacaoCentral.plotar_fixacao_central()
            elif fixacao == "diamante":
                FixacaoDiamante.plotar_fixacao_diamante()
            texto = pygame.font.Font(None, 150).render(
                str(i), True, (255, 255, 255)
            )  # Texto branco
            if not i == 0:
                pygame.display.get_surface().blit(texto, (1920 / 2 - 37, 100))
            time.sleep(1)  # Aguarda 1 segundo
            pygame.display.update()
        return True

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    ContagemRegressiva.iniciar_contagem(5)
    pygame.quit()
