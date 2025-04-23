import os,sys
import pygame
import fitz  # PyMuPDF

# Simula o caminho de um pendrive
CAMINHO_PENDRIVE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils", "pdfs")) # Altere se necessário

pygame.init()
tela = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
pygame.display.set_caption("Visualizador de PDF")

fonte = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()

# Cores
COR_BG = (30, 30, 30)
COR_TEXTO = (255, 255, 255)
COR_HOVER = (70, 70, 200)

def listar_pdfs(caminho_base):
    pdfs = []
    for raiz, dirs, arquivos in os.walk(caminho_base):
        for arquivo in arquivos:
            if arquivo.lower().endswith(".pdf"):
                pdfs.append(os.path.join(raiz, arquivo))
    return pdfs

def renderizar_texto(texto, cor):
    return fonte.render(texto, True, cor)

def carregar_pagina_pdf(caminho_pdf, numero_pagina=0):
    doc = fitz.open(caminho_pdf)
    if numero_pagina >= len(doc):
        return None
    pagina = doc.load_page(numero_pagina)
    pix = pagina.get_pixmap()
    superficie = pygame.image.frombuffer(pix.samples, (pix.width, pix.height), "RGB")
    return superficie

def mostrar_lista_pdfs(lista_pdfs):
    tela.fill(COR_BG)
    y = 50
    pos_mouse = pygame.mouse.get_pos()
    opcoes = []

    for i, caminho in enumerate(lista_pdfs):
        nome = os.path.basename(caminho)
        texto = renderizar_texto(nome, COR_TEXTO)
        rect = texto.get_rect(topleft=(50, y))

        if rect.collidepoint(pos_mouse):
            pygame.draw.rect(tela, COR_HOVER, rect)
        tela.blit(texto, rect)
        opcoes.append((rect, caminho))
        y += 40

    pygame.display.flip()
    return opcoes

def mostrar_pagina_pdf(superficie):
    tela.fill(COR_BG)
    largura, altura = superficie.get_size()
    superficie_zoom = pygame.transform.scale(superficie, (int(largura * 1.1), int(altura * 1.1)))  # Aplicar zoom
    tela.blit(superficie_zoom, (0, 0))  # Exibir a página na tela
    pygame.display.flip()

def main():
    lista_pdfs = listar_pdfs(CAMINHO_PENDRIVE)
    pagina_pdf = None
    modo_visualizacao = "lista"
    pdf_atual = ""
    pagina_atual = 0

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and modo_visualizacao == "lista":
                pos = pygame.mouse.get_pos()
                for rect, caminho in opcoes:
                    if rect.collidepoint(pos):
                        superficie = carregar_pagina_pdf(caminho)
                        if superficie:
                            pagina_pdf = superficie
                            modo_visualizacao = "visualizar"
                            pdf_atual = caminho
                            pagina_atual = 0

            elif evento.type == pygame.KEYDOWN and modo_visualizacao == "visualizar":
                if evento.key == pygame.K_ESCAPE:
                    modo_visualizacao = "lista"
                elif evento.key == pygame.K_RIGHT:
                    pagina_atual += 1
                    nova_pagina = carregar_pagina_pdf(pdf_atual, pagina_atual)
                    if nova_pagina:
                        pagina_pdf = nova_pagina
                elif evento.key == pygame.K_LEFT and pagina_atual > 0:
                    pagina_atual -= 1
                    pagina_pdf = carregar_pagina_pdf(pdf_atual, pagina_atual)

        if modo_visualizacao == "lista":
            opcoes = mostrar_lista_pdfs(lista_pdfs)
        elif modo_visualizacao == "visualizar" and pagina_pdf:
            mostrar_pagina_pdf(pagina_pdf)

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
