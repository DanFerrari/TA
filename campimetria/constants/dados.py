class Constantes():
    dbMin = 0  
    dbMax = 40  
    bigdelta = 3  
    smalldelta = 2  
    screening = "screening"
    fullthreshold = "fullthreshold"
    olho_direito = "OD"
    olho_esquerdo = "OE"
    
class Colors():

    BACKGROUND = (122, 122, 122)
    ERASE_INTENSITY = 122
    DEFAULT = (53, 43, 54)
    
    
    
class DadosExame():
    olho = ""
    exame_selecionado = ""
    atenuacao_screening = 0
    gContIgual = 0
    gFlutuacao = False  # Ajuste conforme necessário
    LimQuad = False  # Ajuste conforme necessário
    LF = False
    ThrRel = False
    gExame = [] 
    LimiarFoveal = 0
    posicao_mancha_cega = (0,0)
    total_pontos_definidos = 0
    
    @staticmethod
    def reset():
        DadosExame.olho = ""
        DadosExame.exame_selecionado = ""
        DadosExame.atenuacao_screening = 0
        DadosExame.gContIgual = 0
        DadosExame.gFlutuacao = False
        DadosExame.LimQuad = False
        DadosExame.LF = False
        DadosExame.ThrRel = False
        DadosExame.gExame = []
        DadosExame.LimiarFoveal = 0
        DadosExame.posicao_mancha_cega = 0,0
    





    
    
    