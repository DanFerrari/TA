import os, pygame, sys,math,random

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
from Ponto import Ponto
from cordenadas_30 import cordenadas_30

class DesenhoAreaExame:

    @staticmethod
    def distancia(p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    # Função para calcular o círculo mínimo que contém dois pontos
    @staticmethod
    def circulo_de_dois_pontos(p1, p2):
        centro = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
        raio = DesenhoAreaExame.distancia(p1, p2) / 2
        return centro, raio

    # Função para calcular o círculo mínimo que contém três pontos
    @staticmethod
    def circulo_de_tres_pontos(p1, p2, p3):
        A = 2 * (p2[0] - p1[0])
        B = 2 * (p2[1] - p1[1])
        C = 2 * (p3[0] - p1[0])
        D = 2 * (p3[1] - p1[1])
        E = (p2[0] ** 2 - p1[0] ** 2) + (p2[1] ** 2 - p1[1] ** 2)
        F = (p3[0] ** 2 - p1[0] ** 2) + (p3[1] ** 2 - p1[1] ** 2)

        det = A * D - B * C
        if abs(det) < 1e-9:  # Se os pontos forem colineares
            return DesenhoAreaExame.circulo_de_dois_pontos(p1, p2)

        cx = (E * D - B * F) / det
        cy = (A * F - E * C) / det
        centro = (cx, cy)
        raio = DesenhoAreaExame.distancia(centro, p1)
        return centro, raio

    # Algoritmo de Welzl para encontrar o menor círculo que cobre todos os pontos
    @staticmethod
    def encontrar_circulo_minimo(pontos):
        def welzl(P, R):
            if len(P) == 0 or len(R) == 3:
                if len(R) == 0:
                    return ((0, 0), 0)
                elif len(R) == 1:
                    return (R[0], 0)
                elif len(R) == 2:
                    return DesenhoAreaExame.circulo_de_dois_pontos(R[0], R[1])
                elif len(R) == 3:
                    return DesenhoAreaExame.circulo_de_tres_pontos(R[0], R[1], R[2])

            p = P[-1]  # Pegamos o último ponto SEM remover
            novo_centro, novo_raio = welzl(P[:-1], R)  # Chamamos a recursão sem o último ponto

            if DesenhoAreaExame.distancia(p, novo_centro) <= novo_raio:
                return novo_centro, novo_raio

            return welzl(P[:-1], R + [p])

        if not pontos:
            return ((0, 0), 0)  # Retorna um círculo inválido se não houver pontos

        pontos_copia = pontos[:]
        random.shuffle(pontos_copia)
        return welzl(pontos_copia, [])

    @staticmethod
    def desenhar():
        matriz_pontos = []
        matriz_circle = []
        
        for x, y in cordenadas_30:
            ponto_novo = Ponto(
                x,
                y,
                tamanhoPonto=DadosExame.tamanho_estimulo,                
                cor=(255, 255, 255),
                distancia=DadosExame.distancia_paciente,
                
            )
            
            matriz_pontos.append(ponto_novo)
            matriz_circle.append((ponto_novo.x,ponto_novo.y))
        centro, raio = DesenhoAreaExame.encontrar_circulo_minimo(matriz_circle)
        raio += matriz_pontos[0].raio_ponto * 4
        
        


        rect = pygame.Rect(int(centro[0] - raio), int(centro[1] - raio), int(raio * 2), int(raio * 2))

        # Desenha os 4 semicirculos
        pygame.draw.arc(pygame.display.get_surface(), (255, 0, 0), rect, math.radians(60), math.radians(120), 1)  # Cima
        pygame.draw.arc(pygame.display.get_surface(), (255,0,0), rect, math.radians(240), math.radians(300), 1)  # Baixo
        pygame.draw.arc(pygame.display.get_surface(), (255,0, 0), rect, math.radians(150), math.radians(210), 1)  # Esquerda
        pygame.draw.arc(pygame.display.get_surface(), (255,0, 0), rect, math.radians(330), math.radians(30), 1)  # Direita
        
                    

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    DadosExame.distancia_paciente = 200
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
                    pygame.draw.circle
                    matriz_pontos = []
                    matriz_circle = []
                    
                    for x, y in cordenadas_30:
                        ponto_novo = Ponto(
                            x,
                            y,
                            tamanhoPonto=tamanho_estimulo,
                            distancia=DadosExame.distancia_paciente,
                            cor=(255, 255, 255),
                            
                        )
                        matriz_pontos.append(ponto_novo)
                        matriz_circle.append((ponto_novo.x,ponto_novo.y))
                    centro, raio = encontrar_circulo_minimo(matriz_circle)
                    raio += matriz_pontos[0].raio_ponto * 4
                    
                    

                    for ponto in matriz_pontos:
                        ponto.plotarPonto()
                    #pygame.draw.circle(pygame.display.get_surface(), (255, 0, 0), (int(centro[0]), int(centro[1])), int(raio), 2)
                    rect = pygame.Rect(int(centro[0] - raio), int(centro[1] - raio), int(raio * 2), int(raio * 2))

                    # Desenha os 4 semicirculos
                    pygame.draw.arc(pygame.display.get_surface(), (0, 255, 0), rect, math.radians(60), math.radians(120), 1)  # Cima
                    pygame.draw.arc(pygame.display.get_surface(), (255,0, 0), rect, math.radians(240), math.radians(300), 1)  # Baixo
                    pygame.draw.arc(pygame.display.get_surface(), (0,255, 0), rect, math.radians(150), math.radians(210), 1)  # Esquerda
                    pygame.draw.arc(pygame.display.get_surface(), (0,255, 0), rect, math.radians(330), math.radians(30), 1)  # Direita
                    
                    
                    
                    print(f"centro: {centro}, raio:{raio}")
                    pygame.display.flip()
