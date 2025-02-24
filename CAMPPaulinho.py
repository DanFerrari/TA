import pygame
import time
import math

def attenuate_intensity(current_intensity, db_step, min_db=-2):
    """
    Atenua a intensidade (0 a 255) reduzindo-a em 'db_step' decibéis, com um limite mínimo definido por min_db.
    """
    min_intensity = int(255 * (10 ** (min_db / 20)))  # Calcula o valor mínimo permitido
    new_intensity = int(current_intensity * (10 ** (-db_step / 20)))
    return max(new_intensity, min_intensity)  # Garante que não passe do limite

def amplify_intensity(current_intensity, db_step):
    """
    Amplifica a intensidade (0 a 255) aumentando-a em 'db_step' decibéis.
    """
    new_intensity = int(current_intensity * (10 ** (db_step / 20)))
    return min(new_intensity, 255)  # Mantém o máximo em 255

def intensity_to_db(intensity, max_intensity=255):
    """
    Converte a intensidade (0 a 255) para dB, considerando 255 como 0 dB.
    Se intensity for 0, retorna -infinito.
    """
    if intensity > 0:
        return 20 * math.log10(intensity / max_intensity)
    return float('-inf')

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
screen_dim = min(info.current_w, info.current_h)
screen = pygame.display.set_mode((screen_dim, screen_dim))
pygame.display.set_caption("Experimento de Limiar Visual")

# --- Contagem regressiva de 3 segundos ---
countdown_seconds = 3
start_countdown = time.time()
while True:
    elapsed = time.time() - start_countdown
    remaining = countdown_seconds - elapsed
    if remaining <= 0:
        break
    countdown_value = math.ceil(remaining)
    screen.fill(BACKGROUND_COLOR)
    text = font.render(str(countdown_value), True, (255, 255, 255))  # Texto em branco
    text_rect = text.get_rect(center=(screen_dim // 2, screen_dim // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(100)

# Após a contagem, limpe a tela e a fila de eventos para evitar entradas antecipadas
screen.fill(BACKGROUND_COLOR)
pygame.display.flip()
pygame.event.clear()

# Parâmetros visuais e do estímulo
stimulus_radius = 10
stimulus_x, stimulus_y = screen_dim // 2, screen_dim // 2
stimulus_duration = 0.2     # Estímulo exibido por 200ms
stimulus_onset_delay = 0.5  # Atraso de 500ms antes da apresentação do ponto

# Janela de resposta
max_response_time = 2.0  # 2 segundos para resposta

clock = pygame.time.Clock()
init_intensity_db = background_db / 2
# Parâmetros do procedimento
current_intensity = int(255 * (10 ** (init_intensity_db / 20)))  # Intensidade inicial
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

while running:
    # Limpa a tela para iniciar o teste
    screen.fill(BACKGROUND_COLOR)
    pygame.display.flip()
    
    trial_counter += 1
    trial_start_time = time.time()
    stimulus_onset_time = trial_start_time + stimulus_onset_delay
    stimulus_end_time = stimulus_onset_time + stimulus_duration
    response_deadline = trial_start_time + max_response_time
    response_received = False
    stimulus_presented = False  # Flag para indicar se o estímulo já foi apresentado

    # Exibe a intensidade atual em dB
    current_db = intensity_to_db(current_intensity)
    print(f"Teste {trial_counter}: Intensidade = {current_intensity} ({current_db:.2f} dB)")

    # Loop para exibir o estímulo e capturar a resposta
    while time.time() < response_deadline:
        current_time = time.time()
        if stimulus_onset_time <= current_time < stimulus_end_time:
            # Apresenta o estímulo e define o flag
            if not stimulus_presented:
                stimulus_presented = True
            screen.fill(BACKGROUND_COLOR)
            pygame.draw.circle(screen, (current_intensity, current_intensity, current_intensity),
                               (stimulus_x, stimulus_y), stimulus_radius)
            pygame.display.flip()
        else:
            screen.fill(BACKGROUND_COLOR)
            pygame.display.flip()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if stimulus_presented:
                    response_received = True
                else:
                    print("Entrada antecipada! Aguarde a apresentação do ponto.")
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
        new_intensity = attenuate_intensity(current_intensity, db_decrement, min_db=min_db_limit)
    else:
        new_intensity = amplify_intensity(current_intensity, db_increment)
    
    print(f"Atualizando intensidade de {current_intensity} para {new_intensity}\n")
    current_intensity = new_intensity

    # Intervalo entre testes (1 segundo)
    pygame.time.wait(1000)

pygame.quit()