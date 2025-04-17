from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors  # Importa cores
import pygame, os, sys, math
import subprocess



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


 
    def verifica_e_monta_pendrive(self):
        caminho_verifica = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "scripts","monta_pendrive.sh")
    )
        subprocess.run(['bash',caminho_verifica])
   
        
    def gerar_relatorio(self,nome_arquivo_pdf):
        c = canvas.Canvas(nome_arquivo_pdf, pagesize=A4)
        largura, altura = A4  # Tamanho da página (595x842 pontos)
        faixa_etaria = {1:"0-20", 2:"21-30", 3:"31-40", 4:"41-50", 5:"51-60", 6:"61-70", 7:"71-80"}
        estimulo = {1:"I",2:"II",3:"III",4:"IV",5:"V"}
        caminho_indicador_md = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils", "images","temp","indicador_md.png"))
        caminho_indicador_psd = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils", "images","temp","indicador_psd.png"))
        caminho_indicador_conf = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils", "images","temp","indicador_confiabilidade.png"))
        
        perda_fixacao = 0

        perda_fixacao = (
            ((DadosExame.perda_de_fixacao / DadosExame.total_testes_mancha) * 100)
            if DadosExame.perda_de_fixacao > 0.0
            else 0
        )

        
        minutos,segundos = divmod((DadosExame.duracao_do_exame / 1000),60)
         
        
        
        
      
        c.setFont("Helvetica-Bold", 10)
        c.drawString(26,altura - 38, f"ID exame:{DadosExame.exame_id}")
        c.drawString(26, altura - 85, f"Olho:{DadosExame.olho}")  
        c.drawString(26, altura - 131, f"Exame: {(DadosExame.exame_selecionado).upper()}")  
        c.drawString(226, altura - 38, f"Programa:{DadosExame.programa_selecionado}")
        c.drawString(226, altura - 85, f"Tamanho Estímulo:{estimulo.get(DadosExame.tamanho_estimulo)}")
        c.drawString(413, altura - 38, f"Falso positivo: {int(DadosExame.falso_positivo_respondidos)} / {int(DadosExame.total_testes_falsos_positivo)} ({DadosExame.falso_positivo_respondidos_percentual:.2f}%)")
        c.drawString(226, altura - 131, f"Duração (min): {int(minutos):02d}:{int(segundos):02d}")
        c.drawString(413, altura - 85, f"Falso negativo: {int(DadosExame.falso_negativo_respondidos)} / {int(DadosExame.total_testes_falsos_negativo)} ({DadosExame.falso_negativo_respondidos_percentual:.2f}%)")
        c.drawString(413, altura -131, f"Perda de fixacao: {int(DadosExame.perda_de_fixacao)} / {int(DadosExame.total_testes_mancha)} ({perda_fixacao:.2f}%)")
        c.drawString(226, altura - 176, f"Total de pontos: {DadosExame.total_de_pontos_testados}")
        if DadosExame.exame_selecionado == Constantes.fullthreshold:
            c.drawString(413, altura - 176, f"Limiar Foveal(dB):{DadosExame.LimiarFoveal}")  
            c.drawString(26, altura - 176, f"Faixa etária: {faixa_etaria.get(DadosExame.faixa_etaria)}") 
            nova_largura = 400  
            nova_altura = int(nova_largura * (540 / 960))
            x_pos = 220 
            y_pos = 100  
                # Caminho para salvar a imagem
            caminho_imagem_pontos = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils", "images","temp","mapa_pontos.png"))
         
            caminho_imagem_limiares = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils", "images","temp","mapa_limiares.png"))
         
            caminho_imagem_logo = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils", "images","logo_branco.png"))
            
            caminho_imagem_curva_bebie = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils", "images","temp","bebie_curve.png"))
            caminho_image_desvio_padrao = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils", "images","temp","desvio_padrao.png"))
            caminho_image_desvio_total = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils", "images","temp","desvio_total.png"))
            
            c.drawImage(caminho_imagem_pontos, largura / 2 - nova_altura + 150,390, width=nova_largura, height=nova_altura)
            c.drawImage(caminho_imagem_limiares, largura / 2 - nova_altura -150,390, width=nova_largura, height=nova_altura)
            c.drawImage(caminho_imagem_logo, 0,-26, width=156, height=110)
            
            c.drawImage(caminho_image_desvio_padrao, 180, altura - 540 - 110, width=100, height=100)
            c.drawImage(caminho_image_desvio_total,20 , altura - 540 - 110, width=100, height=100)
            c.drawImage(caminho_imagem_curva_bebie, 300, altura - 540 - 180, width= 320, height=240)
            c.drawImage(caminho_indicador_md,20,145, width=105, height=12.5)
            c.drawImage(caminho_indicador_psd,20,105, width=105, height=12.5)
            c.drawImage(caminho_indicador_conf,20,65, width=105, height=12.5)
            
            c.drawString(38, altura - 540, "Desvio Total")
            c.drawString(195, altura -540, "Desvio Padrão")
            c.setFont("Helvetica-Bold", 10)
            c.drawString(20,160,(f"MD: {DadosExame.md:.2f} ").upper())
            c.drawString(20,120,(f"PSD: {DadosExame.psd:.2f}").upper())
            c.drawString(20,80,(f"CONFIABILIDADE: {DadosExame.confiabilidade}").upper())
            # c.drawString(5,70,(f"RESULTADO: {DadosExame.resultado_exame}").upper())
         
        elif DadosExame.exame_selecionado == Constantes.screening:
            c.drawString(26, altura - 176, f"Atenuação (dB):{DadosExame.atenuacao_screening}")
            nova_largura = 400  
            nova_altura = int(nova_largura * (540 / 960))
            x_pos = 220 
            y_pos = 100  
                

            caminho_imagem_pontos = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils", "images","temp","mapa_pontos.png"))
            caminho_imagem_limiares = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils", "images","temp","mapa_limiares.png"))

            caminho_imagem_logo = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils", "images","logo_branco.png"))
            
            c.drawImage(caminho_imagem_logo, 0,-26, width=156, height=110)
            c.drawImage(caminho_imagem_pontos, largura / 2 - nova_altura,420, width=nova_largura, height=nova_altura)
            c.drawImage(caminho_imagem_limiares, largura / 2 - nova_altura,150, width=nova_largura, height=nova_altura) 
            c.drawImage(caminho_indicador_conf,20,145, width=105, height=12.5) 
            c.setFont("Helvetica-Bold", 10)
            c.drawString(20,160,(f"CONFIABILIDADE: {DadosExame.confiabilidade}").upper())
            
            # c.drawString(5,70,(f"RESULTADO: {DadosExame.resultado_exame}").upper())

        

        
       
        
        
        
        
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
        with open(nome_arquivo_pdf, 'rb+') as f:
            f.flush()
            os.fsync(f.fileno())
        subprocess.run(["sync"])
        
        pasta = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils", "images","temp"))

        # for arquivo in os.listdir(pasta):
        #     caminho_arquivo = os.path.join(pasta, arquivo)
        #     if os.path.isfile(caminho_arquivo):
        #         os.remove(caminho_arquivo)  




if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    screen.fill((255,255,255))
    from atenuacao_daniel import atenuacao_daniel
    from cordenadas_30 import cordenadas_30
    from Ponto import Ponto
    DadosExame.exame_selecionado = Constantes.screening
    DadosExame.atenuacao_screening = 25
    DadosExame.matriz_pontos = [Ponto(x,y,tamanhoPonto = 3,cor = (0,0,0), distancia = 100) for x,y in cordenadas_30]
    for i,ponto in enumerate(DadosExame.matriz_pontos):
        ponto.atenuacao = atenuacao_daniel.get((ponto.xg,ponto.yg))
        if i > 30:
            ponto.response_received = True
    from TelaResultadoFullThreshold import ResultadoFullthreshold


    pygame.display.update()
    DadosExame.resultado_psd ="Campo visual normal ou muito próximo do normal" 
    DadosExame.resultado_md = 'Perda moderada, ponto de atenção',
    DadosExame.resultado_exame = f"Alterações difusas e localizadas, MD: {DadosExame.resultado_md},\n PSD :{DadosExame.resultado_psd}."

    caminho_pdf = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils", "pdfs", f"relatorio-id-exame-{DadosExame.exame_id}.pdf"))
    pdf = GerarPdf()
    pdf.gerar_relatorio(caminho_pdf)