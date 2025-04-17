import pygame

def gerar_barra_com_indicador(valor, nome_arquivo="barra_com_indicador.png"):
    # Parâmetros da barra
    bar_width = 400
    bar_height = 30
    border_radius = 15
    padding = 10  # Espaço extra ao redor da barra

    # Tamanho da imagem
    largura = bar_width + 2 * padding
    altura = bar_height + 2 * padding
    surface = pygame.Surface((largura, altura))
    surface.fill((255, 255, 255))

    # Faixas de cor (invertido: vermelho até verde)
    faixas = [
        (81, 100, (255, 0, 0)),     # Vermelho
        (61, 80, (255, 140, 0)),    # Laranja
        (41, 60, (255, 255, 0)),    # Amarelo
        (21, 40, (144, 238, 144)),  # Verde claro
        (0, 20, (0, 128, 0)),       # Verde escuro
    ]

    # Posição da barra
    bar_x = padding
    bar_y = padding

    # Desenha a barra invertida
    faixa_largura = bar_width // len(faixas)
    for i, faixa in enumerate(faixas):
        color = faixa[2]
        rect_x = bar_x + i * faixa_largura
        if i == 0:
            pygame.draw.rect(surface, color, (rect_x, bar_y, faixa_largura, bar_height),
                             border_top_left_radius=border_radius,
                             border_bottom_left_radius=border_radius)
        elif i == len(faixas) - 1:
            pygame.draw.rect(surface, color, (rect_x, bar_y, faixa_largura, bar_height),
                             border_top_right_radius=border_radius,
                             border_bottom_right_radius=border_radius)
        else:
            pygame.draw.rect(surface, color, (rect_x, bar_y, faixa_largura, bar_height))

    # Inverte o valor (já que a barra vai de 100 a 0)
    valor_invertido = 100 - valor
    pos = bar_x + int((valor_invertido / 100) * bar_width)

    # Linha indicadora
    pygame.draw.line(surface, (0, 0, 0), (pos, bar_y - 10), (pos, bar_y + bar_height + 10), 10)

    # Salva a imagem
    pygame.image.save(surface, nome_arquivo)
