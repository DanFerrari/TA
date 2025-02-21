import pygame
import time
import math

def attenuate_intensity(current_intensity, db_step, min_db=-6.50):
    """
    Atenua a intensidade (0 a 255) reduzindo-a em 'db_step' decibéis, com um limite mínimo de -45 dB.
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

# Inicializa o Pygame
pygame.init()

# Obtém informações da tela e define a janela com aspecto 1:1 (quadrada)
info = pygame.display.Info()
screen_dim = min(info.current_w, info.current_h)
screen = pygame.display.set_mode((screen_dim, screen_dim))
pygame.display.set_caption("Experimento de Limiar Visual")

# Parâmetros visuais e do estímulo
BLACK = (120, 120, 120)
stimulus_radius = 10
stimulus_x, stimulus_y = screen_dim // 2, screen_dim // 2
stimulus_duration = 0.2  # Estímulo exibido por 500ms

# Janela de resposta
max_response_time = 2.0  # 2 segundos para resposta

clock = pygame.time.Clock()

# Parâmetros do procedimento
current_intensity = 255       # Intensidade inicial (0 dB)
db_decrement = 3        # Atenuação de 4 dB se o estímulo for visto
db_increment = 2            # Amplificação de 2 dB se o estímulo não for visto
min_db_limit = -6.50  # Limite máximo de atenuação (-45 dB)

trial_counter = 0
last_direction = None         # Armazena a resposta do teste anterior: 'seen' ou 'not_seen'
reversal_count = 0
threshold_intensity = None    # Será definido no quinto cruzamento

running = True
print("Iniciando o experimento...")
while running:
    # Limpa a tela para iniciar o teste
    screen.fill(BLACK)
    pygame.display.flip()
    
    trial_counter += 1
    trial_start_time = time.time()
    stimulus_end_time = trial_start_time + stimulus_duration
    response_deadline = trial_start_time + max_response_time
    response_received = False

    # Exibe a intensidade atual em dB
    current_db = intensity_to_db(current_intensity)
    print(f"Teste {trial_counter}: Intensidade = {current_intensity} ({current_db:.2f} dB)")

    # Loop para exibir o estímulo e capturar a resposta
    while time.time() < response_deadline:
        current_time = time.time()
        if current_time < stimulus_end_time:
            screen.fill(BLACK)
            pygame.draw.circle(screen, (current_intensity, current_intensity, current_intensity,current_intensity),
                               (stimulus_x, stimulus_y), stimulus_radius)
            pygame.display.flip()
        else:
            screen.fill(BLACK)
            pygame.display.flip()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                response_received = True
                break
        
        if response_received:
            break
        
        clock.tick(55)
    
    # Define o resultado deste teste
    if response_received:
        result = 'seen'
        print(f"Teste {trial_counter}: O usuário VIU o estímulo.")
    else:
        result = 'not_seen'
        print(f"Teste {trial_counter}: O usuário NÃO viu o estímulo.")
    
    # Verifica reversão (cruzamento de resposta)
    if last_direction is not None and result != last_direction:
        reversal_count += 1
        print(f"** Reversão {reversal_count} detectada no teste {trial_counter}.")
        if reversal_count == 2:
            threshold_intensity = current_intensity
            threshold_db = intensity_to_db(threshold_intensity)
            print(f"\n>>> Limiar detectado no teste {trial_counter}: Intensidade = {threshold_intensity} ({threshold_db:.2f} dB) <<<")
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

    # Intervalo entre testes (500ms)
    pygame.time.wait(1000)

pygame.quit()