from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors  # Importa cores
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

from dados import *



class GerarPdf():
    
    def salvar_icone_com_fundo_branco(self,arquivo_entrada, arquivo_saida):

        icone = pygame.image.load(arquivo_entrada).convert_alpha()    
        largura, altura = icone.get_size()
        surface = pygame.Surface((largura, altura))
        surface.fill((255, 255, 255))  # Fundo branco
        surface.blit(icone, (0, 0))  # Desenha o ícone    
        pygame.image.save(surface, arquivo_saida)  # Salva o novo ícone



    def capturar_parte_tela(self,x, y, largura, altura, nome_arquivo):
        tela = pygame.display.get_surface()  # Obtém a tela atual
        recorte = pygame.Surface((largura, altura))  # Cria uma superfície do tamanho desejado
        recorte.blit(tela, (0, 0), (x, y, largura, altura))  # Copia a parte da tela desejada
        pygame.image.save(recorte, nome_arquivo)  # Salva como imagem
        
    def gerar_relatorio(self,nome_arquivo_pdf):
        c = canvas.Canvas(nome_arquivo_pdf, pagesize=A4)
        largura, altura = A4  # Tamanho da página (595x842 pontos)
        faixa_etaria = {1:"0-20", 2:"21-30", 3:"31-40", 4:"41-50", 5:"51-60", 6:"61-70", 7:"71-80"}
        estimulo = {1:"I",2:"II",3:"III",4:"IV",5:"V"}
        DadosExame.exame_selecionado = Constantes.fullthreshold
        #DadosExame.exame_selecionado = Constantes.screening
        DadosExame.faixa_etaria = 1
        DadosExame.olho = "DIREITO"
        DadosExame.perda_de_fixacao = 5.0
        DadosExame.total_testes_mancha = 10
        
        perda_fixacao = 0

        perda_fixacao = (
            ((DadosExame.perda_de_fixacao / DadosExame.total_testes_mancha) * 100)
            if DadosExame.perda_de_fixacao > 0.0
            else 0
        )

        
        minutos,segundos = divmod((DadosExame.duracao_do_exame / 1000),60)
        
        c.setFont("Helvetica-Bold", 10)
        c.drawString(26,altura - 38, f"Central 30°")
        c.drawString(226, altura - 38, f"Exame: {(DadosExame.exame_selecionado).upper()}")  
        c.drawString(26, altura - 85, f"ID exame:{DadosExame.exame_id}")
        c.drawString(226, altura - 85, f"Olho:{DadosExame.olho}")  
        c.drawString(413, altura - 85, f"Tamanho Estímulo:{estimulo.get(DadosExame.tamanho_estimulo)}")
        c.drawString(26, altura - 131, f"Falso positivo: {int(DadosExame.falso_positivo_respondidos)} / {int(DadosExame.total_testes_falsos_positivo)} ({DadosExame.falso_positivo_respondidos_percentual:.2f}%)")
        c.drawString(226, altura - 131, f"Duração (min): {int(minutos)}:{int(segundos)}")
        c.drawString(413, altura -131, f"Falso negativo: {DadosExame.falso_negativo_respondidos} / {DadosExame.total_testes_falsos_negativo} ({DadosExame.falso_negativo_respondidos_percentual:.2f}%)")
        c.drawString(26, altura - 176, f"Perda de fixacao: {int(DadosExame.perda_de_fixacao)} / {DadosExame.total_testes_mancha} ({perda_fixacao:.2f}%)")
        c.drawString(226, altura - 176, f"Total de pontos: {DadosExame.total_de_pontos_testados}")
        if DadosExame.exame_selecionado == Constantes.fullthreshold:
            c.drawString(413, altura - 176, f"Limiar Foveal(db):{DadosExame.LimiarFoveal}")  
            c.drawString(413, altura - 38, f"Faixa etária: {faixa_etaria.get(DadosExame.faixa_etaria)}")  
        elif DadosExame.exame_selecionado == Constantes.screening:
            c.drawString(413, altura - 38, f"Atenuação:{DadosExame.atenuacao_screening}")  

        
        nova_largura = 400  
        nova_altura = int(nova_largura * (540 / 960))
        x_pos = 220 
        y_pos = 100  
            # Caminho para salvar a imagem
        caminho_imagem_pontos = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils", "images","temp","mapa_pontos.png"))
        self.capturar_parte_tela(0, 0, 960, 540, caminho_imagem_pontos)
        caminho_imagem_limiares = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils", "images","temp","mapa_limiares.png"))
        self.capturar_parte_tela(0, 540, 960, 540, caminho_imagem_limiares)
        caminho_imagem_logo = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils", "images","logo_branco.png"))
        


        
        c.drawImage(caminho_imagem_pontos, largura / 2 - nova_altura,379, width=nova_largura, height=nova_altura)
        c.drawImage(caminho_imagem_limiares, largura / 2 - nova_altura,109, width=nova_largura, height=nova_altura)
        c.drawImage(caminho_imagem_logo, 0,-26, width=156, height=110)
        
        
        
        
        
        # Adicionando uma label para o campo de texto
        c.setFont("Helvetica-Bold", 12)
        c.drawString(160,38,"Paciente:")
        c.drawString(377, 38, "Medico:")
        
        c.acroForm.textfield(
            name="nome_paciente",
            x=160, y=16,  # Posição do campo (X, Y)
            width=180, height=20,  # Largura e altura do campo
            borderColor=colors.black,  # Cor da borda (preto)
            fillColor=None,  # Sem preenchimento de fundo
            textColor=colors.black, # Cor do texto (preto)
            fontName="Helvetica",
            fontSize=12
        )
        c.acroForm.textfield(
            name="nome_medico",
            x=377, y=16,  # Posição do campo (X, Y)
            width=180, height=20,  # Largura e altura do campo
            borderColor=colors.black,  # Cor da borda (preto)
            fillColor=None,  # Sem preenchimento de fundo
            textColor=colors.black, # Cor do texto (preto)
            fontName="Helvetica",
            fontSize=12
        )

        
        c.save() 
        
        pasta = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils", "images","temp"))

        for arquivo in os.listdir(pasta):
            caminho_arquivo = os.path.join(pasta, arquivo)
            if os.path.isfile(caminho_arquivo):
                os.remove(caminho_arquivo)  




if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    screen.fill((255,255,255))
    from atenuacoes_personalizadas import atenuacoes_personalizadas
    from cordenadas_30 import cordenadas_30
    from Ponto import Ponto
    DadosExame.atenuacao_screening = 25
    DadosExame.matriz_pontos = [Ponto(x,y,tamanhoPonto = 3,cor = (0,0,0), distancia = 100) for x,y in cordenadas_30]
    for i,ponto in enumerate(DadosExame.matriz_pontos):
        ponto.atenuacao = atenuacoes_personalizadas.get((ponto.xg,ponto.yg))
        if i > 30:
            ponto.response_received = True
    from TelaResultadoFullThreshold import ResultadoFullthreshold
    #ResultadoScreening.desenha_pontos()
    ResultadoFullthreshold.exibir_resultados()
    pygame.display.update()
    
    caminho_pdf = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils", "pdfs", f"relatorio-id-exame-{DadosExame.exame_id}.pdf"))
    pdf = GerarPdf()
    pdf.gerar_relatorio(caminho_pdf)