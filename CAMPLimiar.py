import pygame
import time
import math


areaTrabalhoX = 1000
areaTrabalhoY = 1000

# variáveis para conversão de coordenadas
resolucaoX = 0.25
#resolucaoY = 0.242
resolucaoY = 0.25
# variáveis para controle de cores        
tomDeCinzaArea = 120
tomDeCinzaCena = 100
# variáveis para controle de posição 
sairAplicacao = False
distanciaPacienteTela = 200

# Parâmetros do fundo
background_db = -4.0  # atenuação da iluminação de fundo em dB
background_intensity = int(255 * (10 ** (background_db / 20)))
BACKGROUND_COLOR = (background_intensity, background_intensity, background_intensity)

# Inicializa o Pygame
pygame.init()
pygame.font.init()  # Inicializa o módulo de fontes

# Define uma fonte para o cronômetro (tamanho 100, por exemplo)
font = pygame.font.SysFont(None, 100)

# Obtém informações da tela e define a janela com aspecto 1:1 (quadrada)
info = pygame.display.Info()
screen_dim = max(info.current_w, info.current_h)
screen = pygame.display.set_mode((screen_dim, screen_dim), pygame.FULLSCREEN)
pygame.display.set_caption("Experimento de Limiar Visual")
screen_width = screen.get_width()
screen_height = screen.get_height()

# --- Contagem regressiva de 3 segundos ---
countdown_seconds = 3
start_countdown = time.time()

class Ponto():
    def __init__(self,xg, yg, tamanhoPonto, cor, db):      
        self.xg = xg
        self.yg = yg
        self.tamanhoPonto = tamanhoPonto
        self.cor = cor
        self.db = db
        self.resolucaoX = 0.246
        self.resolucaoY = 0.250
        self.x = 0
        self.y = 0
      
     
    
    def plotarPonto(self):          
        # Cálculo correto do deslocamento angular
        xrad = math.radians(abs(self.xg))
        xmm = distanciaPacienteTela * math.tan(xrad)
        
        yrad = math.radians(abs(self.yg))
        ymm = distanciaPacienteTela * math.tan(yrad)

        # Converte para pixels
        self.x = xmm / self.resolucaoX
        self.y = ymm / self.resolucaoY

        # Ajusta posição com base nos quadrantes
        if self.xg < 0:
            self.x = -self.x
        if self.yg < 0:
            self.y = -self.y
        
        # Ajusta para o centro da tela
        self.x = round(self.x + screen_width / 2)
        self.y = round(self.y + screen_height / 2)

        # Desenha o ponto
        pygame.draw.circle(screen, self.cor, (self.x, self.y), self.tamanhoPonto)
        pygame.display.flip()

        
    def apagarPonto(self):
        pygame.draw.circle(screen, BACKGROUND_COLOR, (self.x, self.y), self.tamanhoPonto)
        pygame.display.update((self.x - self.tamanhoPonto, self.y - self.tamanhoPonto, 
                           self.tamanhoPonto * 2, self.tamanhoPonto * 2))
        
        
class fixacaoDiamante():
    def __init__(self):
        Ponto(6,0,8,pygame.Color("yellow"),0).plotarPonto()
        Ponto(0,6,8,pygame.Color("yellow"),0).plotarPonto()
        Ponto(-6,0,8,pygame.Color("yellow"),0).plotarPonto()
        Ponto(0,-6,8,pygame.Color("yellow"),0).plotarPonto()
        
        
        

def attenuate_intensity(atenuacao, db_step, min_db=-2):
    """
    Atenua a intensidade (0 a 255) reduzindo-a em 'db_step' decibéis, com um limite mínimo definido por min_db.
    """
    min_intensity = int(255 * (10 ** (min_db / 20)))  # Calcula o valor mínimo permitido
    new_intensity = int(atenuacao * (10 ** (-db_step / 20)))
    return max(new_intensity, min_intensity)  # Garante que não passe do limite

def amplify_intensity(atenuacao, db_step):
    """
    Amplifica a intensidade (0 a 255) aumentando-a em 'db_step' decibéis.
    """
    new_intensity = int(atenuacao * (10 ** (db_step / 20)))
    return min(new_intensity, 255)  # Mantém o máximo em 255

def intensity_to_db(intensity, max_intensity=255):
    """
    Converte a intensidade (0 a 255) para dB, considerando 255 como 0 dB.
    Se intensity for 0, retorna -infinito.
    """
    if intensity > 0:
        return 20 * math.log10(intensity / max_intensity)
    return float('-inf')

while True:
    elapsed = time.time() - start_countdown
    remaining = countdown_seconds - elapsed
    if remaining <= 0:
        break
    countdown_value = math.ceil(remaining)
    screen.fill(BACKGROUND_COLOR)
    text = font.render(str(countdown_value), True, (255, 255, 255))  # Texto em branco
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(100)

# Após a contagem, limpe a tela
screen.fill(BACKGROUND_COLOR)
pygame.display.flip()

# Parâmetros visuais e do estímulo
BLACK = (0, 0, 0)
tamanho_estimulo = 3
tempoExposicao = 0.2  # Estímulo exibido por 200ms
ultimo_visto = 0
atenuacao = 0
ultimo_naovisto = 0
numero_cruzamentos = 0
delta = 0
estimuloVisto = 0
incrementoMaior = 3
incrementoMenor = 2
limiarEncontrada = False
status = ''
limiar = 0.1
primeiro = True
tempo_resposta_paciente = 2.0
clock = pygame.time.Clock()

intensidade_inicial = background_db/2
# Parâmetros do procedimento
atenuacao = int(255 * (10 ** (intensidade_inicial / 20)))  # Intensidade inicial
db_decrement = 0.10            # Atenuação se o estímulo for visto
db_increment = 0.07            # Amplificação se o estímulo não for visto
min_db_limit = background_db   # Limite máximo de atenuação

trial_counter = 0
last_direction = None         # Armazena a resposta do teste anterior: 'seen' ou 'not_seen'
reversal_count = 0
last_seen_db = None           # Último valor visto em dB
last_not_seen_db = None       # Último valor não visto em dB

running = True
print("Iniciando o experimento...")
fixacaoDiamante()


while running and not limiarEncontrada:
    # Limpa a tela para iniciar o teste
    
    #pygame.display.flip()
  
    trial_counter += 1
    trial_start_time = pygame.time.get_ticks()
    stimulus_end_time = trial_start_time + int(tempoExposicao * 1000)
    response_deadline = trial_start_time + int(tempo_resposta_paciente * 1000)
    response_received = False
    pontoLimiar = Ponto(0,0,10,(atenuacao,atenuacao,atenuacao),20)
   
    # Exibe a intensidade atual em dB
    current_db = intensity_to_db(atenuacao)
    print(f"Teste {trial_counter}: Intensidade = {atenuacao} ({current_db:.2f} dB)")
    while status != '=' and running:      
        # Loop para exibir o estímulo e capturar a resposta
        while pygame.time.get_ticks() < response_deadline:
            current_time = pygame.time.get_ticks()
            if current_time < stimulus_end_time:
                    
                pontoLimiar.cor = (atenuacao,atenuacao,atenuacao)
                pontoLimiar.plotarPonto()
                #pygame.display.flip()
            else:
                pontoLimiar.apagarPonto()
                #pygame.display.flip()
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                    break    
        
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    response_received = True
                    break
            
            if response_received:
                break
            clock.tick(60)
        
        # Define o resultado deste teste
        if response_received:
            result = 'seen'
            last_seen_db = current_db  # Armazena o último valor visto
            print(f"Teste {trial_counter}: O usuário VIU o estímulo.")
        else:
            result = 'not_seen'
            last_not_seen_db = current_db  # Armazena o último valor não visto
            print(f"Teste {trial_counter}: O usuário NÃO viu o estímulo.")
        
        # Verifica reversão (cruzamento de resposta)
        if last_direction is not None and result != last_direction:
            reversal_count += 1
            print(f"** Reversão {reversal_count} detectada no teste {trial_counter}.")
            
            if reversal_count == 3:
                # Calcula a média entre os últimos valores de estímulo visto e não visto
                if last_seen_db is not None and last_not_seen_db is not None:
                    threshold_db = (last_seen_db + last_not_seen_db) / 2
                    print(f"\n>>> Limiar detectado no teste {trial_counter}: {threshold_db:.2f} dB <<<")
                else:
                    print("\n>>> Erro: Não há dados suficientes para calcular o limiar. <<<")
                running = False
                break
        
        last_direction = result

        # Atualiza a intensidade para o próximo teste
        if result == 'seen':
            new_intensity = attenuate_intensity(atenuacao, db_decrement, min_db=min_db_limit)
        else:
            new_intensity = amplify_intensity(atenuacao, db_increment)
        
        print(f"Atualizando intensidade de {atenuacao} para {new_intensity}\n")
        atenuacao = new_intensity

        # Intervalo entre testes (1 segundo)
        pygame.time.wait(1000)

pygame.quit()


pygame.time.wait(1000)