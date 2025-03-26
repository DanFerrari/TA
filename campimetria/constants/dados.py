import pygame







class Constantes:
    dbMin = 0
    dbMax = 40
    bigdelta = 6
    smalldelta = 3
    screening = "screening"
    fullthreshold = "fullthreshold"
    olho_direito = "OD"
    olho_esquerdo = "OE"


class Colors:

    BACKGROUND = (120, 120, 120)
    ERASE_INTENSITY = 120
    DEFAULT = (53, 43, 54)
    WHITE = (255,255,255)
    SOFT_GREEN = (0,200,0)
    GREEN = (0,255,0)
    BLACK = (0,0,0)
    SOFT_BLACK = (20,20,20)
    MEDIUM_BLACK = (50,50,50)
    GRAY = (122,122,122)
    

class Fonts:    
    pass



class DadosExame:
    #  faixa_etaria =>  1:"0 - 20", 2:"21 - 30", 3:"31 - 40", 4:"41 - 50", 5:"51 - 60", 6:"61 - 70", 7:"71 - 80"
    exame_id = 0
    faixa_etaria = 0
    distancia_paciente = 200
    tamanho_estimulo = 3
    olho = ""
    exame_selecionado = ""
    atenuacao_screening = 0
    duracao_do_exame = 0
    gContIgual = 0
    gFlutuacao = False  # Ajuste conforme necessário
    LimQuad = False  # Ajuste conforme necessário
    LF = False
    ThrRel = False
    gExame = []
    LimiarFoveal = 0
    total_pontos_definidos = 0
    matriz_pontos = []
    total_de_pontos_testados = 0
    posicao_mancha_cega = (0, 0)
    perda_de_fixacao = 0.0
    total_testes_mancha = 0    
    falso_positivo_respondidos = 0.0
    falso_negativo_respondidos = 0.0
    total_testes_falsos_positivo = 0
    total_testes_falsos_negativo = 0
    falso_negativo_respondidos_percentual = 0.0
    falso_positivo_respondidos_percentual = 0.0
    
    

    @staticmethod
    def reset():
        DadosExame.faixa_etaria = 0
        DadosExame.olho = ""
        DadosExame.exame_selecionado = ""
        DadosExame.atenuacao_screening = 0
        DadosExame.duracao_do_exame = 0
        DadosExame.gContIgual = 0
        DadosExame.gFlutuacao = False 
        DadosExame.LimQuad = False 
        DadosExame.LF = False
        DadosExame.ThrRel = False
        DadosExame.gExame = []
        DadosExame.LimiarFoveal = 0
        DadosExame.total_pontos_definidos = 0
        DadosExame.matriz_pontos = []
        DadosExame.total_de_pontos_testados = 0
        DadosExame.posicao_mancha_cega = (0, 0)
        DadosExame.perda_de_fixacao = 0.0
        DadosExame.total_testes_mancha = 0    
        DadosExame.falso_positivo_respondidos = 0.0
        DadosExame.falso_negativo_respondidos = 0.0
        DadosExame.total_testes_falsos_positivo = 0
        DadosExame.total_testes_falsos_negativo = 0
        DadosExame.falso_negativo_respondidos_percentual = 0.0
        DadosExame.falso_positivo_respondidos_percentual = 0.0
        
        
