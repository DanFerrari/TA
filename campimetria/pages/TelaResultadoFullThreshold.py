import pygame, random, time, os, sys, math
from PIL import Image, ImageDraw
import numpy as np
from scipy.spatial import KDTree


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

class ResultadoFullthreshold:
    
    @staticmethod
    def desenhar_mapa():
        # Cria os pontos a partir das coordenadas
        DadosExame.matriz_pontos = [Ponto(xg, yg, 3, (0, 0, 0)) for xg, yg in cordenadas_30]
        
        # Extraímos as coordenadas para referência
        pontos = [(p.x, p.y) for p in DadosExame.matriz_pontos]
        xs = [p[0] for p in pontos]
        ys = [p[1] for p in pontos]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        
        # Define a resolução da imagem base
        base_width, base_height = 960, 540
        base_img = Image.new("RGBA", (base_width, base_height), "white")
        
        # Carrega as texturas
        texturas = []
        for i in range(1, 11):
            caminho = f"campimetria/utils/images/bitmaps/{i}.bmp"
            if os.path.exists(caminho):
                texturas.append(Image.open(caminho))
            else:
                print(f"⚠️ Aviso: {caminho} não encontrado!")
                texturas.append(Image.new("RGB", (50, 50), (200, 200, 200)))
        
        # Aqui, definimos o tamanho base da célula.
        # Se os pontos centrais estão a 3 de distância e os demais a 6, escolha um tamanho que minimize lacunas.
        cell_width = cell_height = 7  # Ajuste conforme necessário
        
        cells = []  # Armazenará informações de cada célula
        
        # Redimensiona as coordenadas dos pontos para a resolução da imagem base
        for ponto in DadosExame.matriz_pontos:
            ponto.x = int(ponto.x * base_width / 1920)   # Exemplo de escala para X
            ponto.y = int(ponto.y * base_height / 1080)    # Exemplo de escala para Y
        
        # Calcula o centro dos pontos para centralizar o desenho na imagem base
        soma_x = sum(ponto.x for ponto in DadosExame.matriz_pontos)
        soma_y = sum(ponto.y for ponto in DadosExame.matriz_pontos)
        num_pontos = len(DadosExame.matriz_pontos)
        centro_grade_x = soma_x // num_pontos
        centro_grade_y = soma_y // num_pontos
        offset_x = (base_width // 2) - centro_grade_x
        offset_y = (base_height // 2) - centro_grade_y
        
        # Desenha as células e armazena suas informações
        for ponto in DadosExame.matriz_pontos:
            # Seleciona a textura conforme a atenuação
            if ponto.atenuacao <= -90:
                textura = None
            elif ponto.atenuacao <= 0:
                textura = texturas[0]
            elif ponto.atenuacao < 6:
                textura = texturas[1]
            elif ponto.atenuacao < 11:
                textura = texturas[2]
            elif ponto.atenuacao < 16:
                textura = texturas[3]
            elif ponto.atenuacao < 21:
                textura = texturas[4]
            elif ponto.atenuacao < 26:
                textura = texturas[5]
            elif ponto.atenuacao < 31:
                textura = texturas[6]
            elif ponto.atenuacao < 36:
                textura = texturas[7]
            elif ponto.atenuacao < 41:
                textura = texturas[8]
            else:
                textura = texturas[9]
            
            # Calcula a posição onde a célula será desenhada (com centralização e offset)
            cell_x = int(ponto.x) - (cell_width // 2) + offset_x
            cell_y = int(ponto.y) - (cell_height // 2) + offset_y
            
            # Cria a célula e preenche com tiling da textura, se definida
            cell_img = Image.new("RGB", (cell_width, cell_height), "white")
            if textura is not None:
                for i_pos in range(0, cell_width, textura.width):
                    for j_pos in range(0, cell_height, textura.height):
                        cell_img.paste(textura, (i_pos, j_pos))
            
            base_img.paste(cell_img, (cell_x, cell_y))
            
            cells.append({
                'center': (int(ponto.x) + offset_x, int(ponto.y) + offset_y),
                'top_left': (cell_x, cell_y),
                'texture': textura,
                'cell_width': cell_width,
                'cell_height': cell_height
            })
        
        # Cria a máscara circular centrada na imagem base
        diameter = min(base_width, base_height)
        mask = Image.new("L", (base_width, base_height), 0)
        draw = ImageDraw.Draw(mask)
        circ_left = (base_width - diameter) // 2
        circ_top  = (base_height - diameter) // 2
        circ_right = circ_left + diameter
        circ_bottom = circ_top + diameter
        draw.ellipse((circ_left, circ_top, circ_right, circ_bottom), fill=255)
        
        # Aplica a máscara e recorta para obter somente a área circular
        circular_img = Image.new("RGBA", (base_width, base_height))
        circular_img.paste(base_img, (0, 0), mask)
        circular_img = circular_img.crop((circ_left, circ_top, circ_right, circ_bottom))
        
        # Ajusta as coordenadas das células para o novo sistema (após o crop)
        for cell in cells:
            cell['center'] = (cell['center'][0] - circ_left, cell['center'][1] - circ_top)
            cell['top_left'] = (cell['top_left'][0] - circ_left, cell['top_left'][1] - circ_top)
        
        # Preenche os "buracos" (pixels com fundo branco) com a textura da célula mais próxima
        final_img = ResultadoFullthreshold.preencher_lacunas(circular_img, cells)
        
        # Desenha uma cruz central (linha vertical e horizontal no centro)
        draw_final = ImageDraw.Draw(final_img)
        w, h = final_img.size
        center = (w // 2, h // 2)
        line_color = (0, 0, 0, 255)  # Cor preta com opacidade total
        line_width = 1  # Espessura da linha
        
        # Linha vertical: do topo ao fundo, no centro
        draw_final.line([(center[0], 0), (center[0], h)], fill=line_color, width=line_width)
        # Linha horizontal: do lado esquerdo ao direito, no centro
        draw_final.line([(0, center[1]), (w, center[1])], fill=line_color, width=line_width)
        
        final_img.save("mapa_gerado.png")
        final_img.show()
        
    @staticmethod
    def preencher_lacunas(circular_img, cells):
        """
        Preenche os pixels vazios (fundo branco) com a textura da célula cujo centro é o mais próximo.
        """
        circular_np = np.array(circular_img)
        H, W = circular_np.shape[:2]
        
        # Identifica pixels com fundo branco (assumindo [255,255,255,255])
        white_mask = np.all(circular_np[:, :, :3] == 255, axis=-1)
        
        # Cria o KDTree com os centros das células
        cell_centers = np.array([cell['center'] for cell in cells])
        tree = KDTree(cell_centers)
        
        # Cria um grid com as coordenadas de cada pixel
        grid_y, grid_x = np.indices((H, W))
        
        # Coleta as coordenadas dos pixels vazios
        vazio_coords = np.column_stack((grid_x[white_mask], grid_y[white_mask]))
        
        # Para cada pixel vazio, consulta o vizinho mais próximo
        if vazio_coords.shape[0] > 0:
            dist, indices = tree.query(vazio_coords)
        else:
            return circular_img  # Se não houver pixels vazios, retorna a imagem original
        
        # Preenche os pixels vazios com a textura da célula mais próxima
        for (x, y), idx in zip(vazio_coords, indices):
            cell = cells[idx]
            textura = cell['texture']
            if textura is None:
                continue
            tex_np = np.array(textura.convert("RGBA"))
            tex_w, tex_h = textura.size
            # Calcula a posição relativa dentro da célula (para tiling)
            cell_top_left = cell['top_left']
            local_x = (x - cell_top_left[0]) % tex_w
            local_y = (y - cell_top_left[1]) % tex_h
            circular_np[y, x] = tex_np[local_y, local_x]
        
        return Image.fromarray(circular_np)
            
    @staticmethod
    def exibir_resultados():
        pygame.font.init()

        fonte = pygame.font.Font(None, 24)

        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # Desenhar pontos e labels
        for ponto in DadosExame.matriz_pontos:
            ponto.cor = pygame.Color("blue")
            ponto.plotarPonto()
            label = fonte.render(f"{ponto.atenuacao}", True, (255, 255, 255))
            pygame.display.get_surface().blit(
                label, (ponto.x - 10, ponto.y + 10)
            )  # Adicionar texto abaixo
        pygame.display.get_surface().fill(Colors.BACKGROUND)
        
        pygame.display.flip()
