class Constantes:
    dbMin = 0
    dbMax = 40
    bigdelta = 3
    smalldelta = 2
    screening = "screening"
    fullthreshold = "fullthreshold"
    olho_direito = "OD"
    olho_esquerdo = "OE"


class Colors:

    BACKGROUND = (155, 155, 155)
    ERASE_INTENSITY = 155
    DEFAULT = (53, 43, 54)


class DadosExame:

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
    
    posicao_mancha_cega = (0, 0)
    perda_de_fixacao = 0.0
    total_testes_mancha = 0
    
    falso_positivo_respondidos = 0.0
    falso_negativo_respondidos = 0.0
    total_testes_falsos_positivo = 0
    total_testes_falsos_negativo = 0
    falso_negativo_respondidos_percentual = falso_negativo_respondidos /  total_testes_falsos_negativo * 100
    falso_positivo_respondidos_percentual = falso_positivo_respondidos / total_testes_falsos_positivo * 100
    
    

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
        DadosExame.posicao_mancha_cega = 0, 0
        DadosExame.total_pontos_definidos = 0
        DadosExame.matriz_pontos = []
        DadosExame.perda_de_fixacao = 0.0
        DadosExame.total_testes_mancha = 0
        DadosExame.falso_positivo = 0
        DadosExame.falso_negativo = 0
        DadosExame.duracao_do_exame = 0
        
