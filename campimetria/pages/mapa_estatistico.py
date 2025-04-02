from PIL import Image, ImageDraw, ImageFont
import numpy as np

class Mapa2d:
    def __init__(self, tamanho_imagem, dados_exame, limiares):
        self.tamanho_imagem = tamanho_imagem
        self.dados_exame = dados_exame
        self.limiares = limiares
        self.matriz_original = np.full((10, 10), None)  # Exemplo de matriz vazia

    def desenhar_mapa(self):
        pass  # Método abstrato a ser sobrescrito

class MapaEstatistico(Mapa2d):
    def __init__(self, tamanho_imagem, vetor_desvio, dados_exame, limiares, dictionary):
        super().__init__(tamanho_imagem, dados_exame, limiares)
        self.dictionary = dictionary
        self.vetor_desvio = vetor_desvio
        self.indices_estatisticos = []
        self.inicializar_matriz_original(vetor_desvio)
        self.carregar_estatistica()

    def desenhar_mapa(self):
        img = Image.new("RGB", self.tamanho_imagem, "white")
        draw = ImageDraw.Draw(img)
        
        for i in range(len(self.matriz_original)):
            for j in range(len(self.matriz_original[i])):
                if self.matriz_original[i][j] is not None:
                    x = j * (self.tamanho_imagem[0] // len(self.matriz_original))
                    y = i * (self.tamanho_imagem[1] // len(self.matriz_original[0]))
                    draw.rectangle([x, y, x+10, y+10], fill="black")

        return img

    def desenhar_legenda(self, tamanho_legenda):
        legenda = Image.new("RGB", tamanho_legenda, "white")
        draw = ImageDraw.Draw(legenda)
        draw.text((10, 10), "< 5%", fill="black")
        draw.text((10, 30), "< 2%", fill="black")
        draw.text((10, 50), "< 1%", fill="black")
        draw.text((10, 70), "< 0.5%", fill="black")
        return legenda

    def inicializar_matriz_original(self, vetor_desvio):
        count = 0
        for i in range(len(self.matriz_original)):
            for j in range(len(self.matriz_original[i])):
                if count < len(vetor_desvio):
                    self.matriz_original[i][j] = vetor_desvio[count]
                count += 1

    def carregar_estatistica(self):
        arquivo_estatistica = "base_30.txt"  # Exemplo fixo, pode variar conforme a idade
        with open(arquivo_estatistica, "r") as f:
            linhas = [int(linha.strip()) for linha in f.readlines()]

        self.indices_estatisticos = [
            [linhas[i], linhas[i+76], linhas[i+152], linhas[i+228]]
            for i in range(76)
        ]

# Criando um exemplo de uso
mapa = MapaEstatistico((500, 500), [1, 2, 3, 4, 5], "dados", ["limiar1"], "dic")
mapa_img = mapa.desenhar_mapa()
mapa_img.show()
