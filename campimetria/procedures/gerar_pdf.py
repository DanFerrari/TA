from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import pygame, os, sys, math



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
from TelaResultadoFullThreshold import ResultadoFullthreshold
from dados import *

def capturar_parte_tela(x, y, largura, altura, nome_arquivo="parte_tela.png"):
    tela = pygame.display.get_surface()  # Obtém a tela atual
    recorte = pygame.Surface((largura, altura))  # Cria uma superfície do tamanho desejado
    recorte.blit(tela, (0, 0), (x, y, largura, altura))  # Copia a parte da tela desejada
    pygame.image.save(recorte, nome_arquivo)  # Salva como imagem


def gerar_relatorio(nome_arquivo_pdf, nome_arquivo_imagem):
    c = canvas.Canvas(nome_arquivo_pdf, pagesize=A4)
    largura, altura = A4  # Tamanho da página (595x842 pontos)
    faixa_etaria = {1:"0 - 20", 2:"21 - 30", 3:"31 - 40", 4:"41 - 50", 5:"51 - 60", 6:"61 - 70", 7:"71 - 80"}

    # Adicionar título
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, altura - 50, "Relatório do Jogo")

    # Adicionar resultados
    c.setFont("Helvetica", 10)
    y_pos = altura - 100
    DadosExame.exame_selecionado = "SCREENING"
    DadosExame.faixa_etaria = 1
    DadosExame.olho = "DIREITO"
    
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y_pos, f"EXAME:")
    c.drawString(250, y_pos, f"OLHO:")
    c.drawString(50, y_pos -50, f"FAIXA-ETÁRIA:")
    c.drawString(250, y_pos -50, f"TAMANHO ESTIMULO:")
    c.drawString(350, y_pos -50, f"TAMANHO ESTIMULO:")

    # Redimensionar e adicionar a imagem no PDF
    nova_largura = 400  # Defina o tamanho desejado
    nova_altura = int(nova_largura * (540 / 960))  # Mantém a proporção original
    x_pos = 220 # Centraliza na página
    y_pos = 100  # Posição vertical na página

    c.drawImage(nome_arquivo_imagem, x_pos, y_pos, width=nova_largura, height=nova_altura)

    c.save()  # Salvar o PDF




if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    screen.fill((255,255,255))
    from atenuacoes_personalizadas import atenuacoes_personalizadas
    from cordenadas_30 import cordenadas_30
    from Ponto import Ponto
    DadosExame.matriz_pontos = [Ponto(x,y,tamanhoPonto = 3,cor = (0,0,0), distancia = 100) for x,y in cordenadas_30]
    for ponto in DadosExame.matriz_pontos:
        ponto.atenuacao = atenuacoes_personalizadas.get((ponto.xg,ponto.yg))
    ResultadoFullthreshold.exibir_resultados()
    pygame.display.update()

    # Caminho para salvar a imagem
    caminho_imagem = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils", "images","temp","parte_tela.png"))
    capturar_parte_tela(0, 0, 960, 540, caminho_imagem)

    # Caminho para salvar o PDF
    caminho_pdf = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils", "pdfs", "relatorio.pdf"))
    gerar_relatorio(caminho_pdf, caminho_imagem)