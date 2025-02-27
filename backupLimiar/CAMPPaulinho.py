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

def run_trial(screen, point_coords, current_intensity, attenuation_db, 
              stimulus_exposure_time, max_keyboard_wait, background_color, 
              stimulus_radius=10, stimulus_onset_delay=0.5, amplification_db=0.07, 
              min_db_limit=-4.0):
    """
    Executa um teste único de apresentação do estímulo e captura a resposta do usuário.
    
    Parâmetros:
        screen: superfície do Pygame onde o estímulo será desenhado.
        point_coords: tupla (x, y) com as coordenadas do ponto a ser testado.
        current_intensity: intensidade atual (0 a 255) do estímulo.
        attenuation_db: valor de atenuação (dB) a ser aplicado se o estímulo for visto.
        stimulus_exposure_time: tempo de exposição do estímulo (em segundos).
        max_keyboard_wait: tempo máximo para aguardar a resposta do teclado (em segundos).
        background_color: cor de fundo da tela (tupla RGB).
        stimulus_radius: raio do estímulo (padrão=10).
        stimulus_onset_delay: atraso (em segundos) antes de apresentar o estímulo (padrão=0.5).
        amplification_db: valor de amplificação (dB) a ser aplicado se o estímulo não for visto (padrão=0.07).
        min_db_limit: limite mínimo de atenuação em dB (padrão=-4.0).
    
    Retorna:
        result: 'seen' se o usuário respondeu durante a apresentação do estímulo; 'not_seen' caso contrário.
        new_intensity: nova intensidade atualizada de acordo com a resposta.
        response_time: tempo (em segundos) decorrido entre o início da apresentação do estímulo e a resposta do usuário;
                       se não houver resposta, retorna None.
    """
    trial_start_time = time.time()
    stimulus_onset_time = trial_start_time + stimulus_onset_delay
    stimulus_end_time = stimulus_onset_time + stimulus_exposure_time
    response_deadline = trial_start_time + max_keyboard_wait
    
    response_received = False
    stimulus_presented = False  # Flag para indicar se o estímulo já foi apresentado
    response_time = None        # Tempo de resposta (em segundos)
    
    clock = pygame.time.Clock()
    
    while time.time() < response_deadline:
        current_time = time.time()
        # Exibe o estímulo somente após o atraso definido e enquanto estiver dentro do tempo de exposição
        if stimulus_onset_time <= current_time < stimulus_end_time:
            if not stimulus_presented:
                stimulus_presented = True
            screen.fill(background_color)
            pygame.draw.circle(screen, (current_intensity, current_intensity, current_intensity),
                               point_coords, stimulus_radius)
            pygame.display.flip()
        else:
            screen.fill(background_color)
            pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None, current_intensity, None
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if stimulus_presented:
                    response_received = True
                    # Calcula o tempo de resposta a partir do início da apresentação do estímulo
                    response_time = current_time - stimulus_onset_time
                else:
                    print("Entrada antecipada! Aguarde a apresentação do ponto.")
                break
        
        if response_received:
            break
        clock.tick(200)
    
    if response_received:
        result = 'seen'
        print("O usuário VIU o estímulo.")
        new_intensity = attenuate_intensity(current_intensity, attenuation_db, min_db_limit)
    else:
        result = 'not_seen'
        print("O usuário NÃO viu o estímulo.")
        new_intensity = amplify_intensity(current_intensity, amplification_db)
    
    return result, new_intensity, response_time

# Exemplo de uso:
if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    info = pygame.display.Info()
    screen_dim = min(info.current_w, info.current_h)
    screen = pygame.display.set_mode((screen_dim, screen_dim))
    pygame.display.set_caption("Teste de Estímulo")
    
    background_db = -4.0
    background_intensity = int(255 * (10 ** (background_db / 20)))
    BACKGROUND_COLOR = (background_intensity, background_intensity, background_intensity)
    
    current_intensity = int(255 * (10 ** ((background_db/2) / 20)))  # Intensidade inicial
    
    # Parâmetros do teste
    point_coords = (screen_dim // 2, screen_dim // 2)
    attenuation_db = 0.10           # dB a ser usado se o estímulo for visto
    stimulus_exposure_time = 0.2      # 200 ms de exposição
    max_keyboard_wait = 2.0         # 2 segundos para resposta
    
    # Limpa a tela e a fila de eventos antes do teste
    screen.fill(BACKGROUND_COLOR)
    pygame.display.flip()
    pygame.event.clear()
    
    # Executa o teste e recebe o resultado, a nova intensidade e o tempo de resposta
    result, updated_intensity, rt = run_trial(screen, point_coords, current_intensity, attenuation_db,
                                              stimulus_exposure_time, max_keyboard_wait, BACKGROUND_COLOR)
    print(f"Resultado do teste: {result}")
    print(f"Nova intensidade: {updated_intensity}")
    if rt is not None:
        print(f"Tempo de resposta: {rt:.3f} segundos")
    else:
        print("Sem resposta do usuário.")
    
    pygame.quit()
