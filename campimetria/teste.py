import os, pygame, sys

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


from constants.dados import *
from procedures.Ponto import Ponto
from constants.cordenadas_30 import cordenadas_30


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    DadosExame.distancia_paciente = 600
    tamanho_estimulo = 3
    while True:
        screen.fill((0, 0, 100))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    pygame.quit() 
                elif event.key == pygame.K_RIGHT:
                    DadosExame.distancia_paciente += 10
                    print(DadosExame.distancia_paciente)
                elif event.key == pygame.K_LEFT:
                    DadosExame.distancia_paciente -= 10
                    print(DadosExame.distancia_paciente)

                elif event.key == pygame.K_UP:
                    if tamanho_estimulo < 5:
                        tamanho_estimulo += 1
                        print(tamanho_estimulo)

                elif event.key == pygame.K_DOWN:
                    if tamanho_estimulo > 0:
                        tamanho_estimulo -= 1
                        print(tamanho_estimulo)
                elif event.key == pygame.K_e:

                    matriz_pontos = []
                    for x, y in cordenadas_30:
                        ponto_novo = Ponto(
                            x,
                            y,
                            tamanhoPonto=tamanho_estimulo,
                            distancia=DadosExame.distancia_paciente,
                            cor=(255, 255, 255),
                            
                        )
                        matriz_pontos.append(ponto_novo)

                    for ponto in matriz_pontos:
                        ponto.plotarPonto()
                    pygame.display.update()
