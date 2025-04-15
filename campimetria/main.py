import pygame
import os
import sys
import OPi.GPIO as GPIO
import time
import subprocess
import json


GPIO.setwarnings(False)
GPIO.setmode(GPIO.SUNXI)

PIN_ENTRADA = "PD22"
# GPIO.setup(PIN_ENTRADA, GPIO.IN)


# Adiciona os caminhos (suas pastas de constantes, páginas, procedimentos, etc.)
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


from constants.dados import *
from pages.strategy_screen import StrategyScreen



class Campimetria:

    def __init__(self):
        pygame.init()
        # Configura a tela em FULLSCREEN e captura dimensões
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width, self.height = self.screen.get_size()
        pygame.display.set_caption("Seleção de Estratégia")
        self.clock = pygame.time.Clock()
        self.running = True

        # Definições de cores e fontes
        self.cor_fundo = (20, 20, 20)
        self.cor_botao = (122, 122, 122)
        self.cor_botao_hover = (255, 255, 255)
        self.cor_texto = (255, 255, 255)
        self.font_main = pygame.font.Font(None, int(self.height * 0.07))

        # Estado inicial: tela de seleção de estratégia
        self.current_screen = StrategyScreen(self)
        self.CONFIG_FILE = "config.json"

        self.DEFAULT_CONFIG ={
            "distancia_paciente": 200,
            "tamanho_estimulo": 3,
            "exame_id": 1,
            "background":120,
            "brightness":90,
            "contrast":50,
            "resolution-w":1920,
            "resolution-h":1080
        }
        self.config = self.carregar_config()
        self.set_brightness(self.config["brightness"])
        self.set_contrast(self.config["contrast"])
        DadosExame.tamanho_estimulo = self.config["tamanho_estimulo"]
        DadosExame.distancia_paciente = self.config["distancia_paciente"]
        DadosExame.exame_id = self.config["exame_id"]




    def carregar_config(self):
        """Lê as variáveis do arquivo JSON ou usa valores padrão."""
        if os.path.exists(os.path.abspath(os.path.join(os.path.dirname(__file__), "..",self.CONFIG_FILE))):
            with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "..",self.CONFIG_FILE)), "r") as f:
                return json.load(f)
        else:
            return self.DEFAULT_CONFIG
    def get_brightness(self): return self.get_vcp_value("10")
    def set_brightness(self,val): self.set_vcp_value("10", val)

    def get_contrast(self): return self.get_vcp_value("12")
    def set_contrast(self,val): self.set_vcp_value("12", val)
    
    def get_vcp_value(self,code):
        try:
            output = subprocess.check_output(["ddcutil", "getvcp", code], text=True)
            match = re.search(r'current value = (\d+)', output)
            if match:
                return int(match.group(1))
        except Exception as e:
            print(f"Erro ao obter VCP {code}:", e)
        return 50

    def set_vcp_value(self,code, value):
        value = max(0, min(value, 100))  # clampa entre 0 e 100
        try:
            subprocess.run(["ddcutil", "setvcp", code, str(value)])
        except Exception as e:
            print(f"Erro ao definir VCP {code}:", e)
    def get_screen_settings(self):
        """Obtém as configurações atuais de tempo de espera da tela"""
        try:
            output = subprocess.check_output("xset q", shell=True, text=True)
            for line in output.split("\n"):
                if "timeout" in line:
                    return line.strip()
        except Exception as e:
            print(f"Erro ao obter configurações: {e}")
        return None

    def disable_screen_sleep(self):
        """Desativa o descanso de tela e modo de espera"""
        os.system("xset s off")  # Desativa proteção de tela
        os.system("xset -dpms")  # Desativa gerenciamento de energia

    def enable_screen_sleep(self):
        """Ativa o descanso de tela e modo de espera"""
        os.system("xset s on")  # Ativa proteção de tela
        os.system("xset +dpms")  # Ativa gerenciamento de energia

    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            # Delegamos o tratamento de eventos, atualização e desenho para a tela ativa
            self.current_screen.handle_events(events)
            self.current_screen.update()
            self.current_screen.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def change_screen(self, new_screen):
        self.current_screen = new_screen


if __name__ == "__main__":

    game = Campimetria()
    # Obtém as configurações atuais antes de desativar
    original_settings = game.get_screen_settings()
    # Desativa o stand-by e descanso de tela
    game.disable_screen_sleep()
    print("Stand-by e descanso de tela desativados!")

    game.run()
    caminho = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "lib", "mainTA.py")
    )
    # Após o app fechar, restaura a configuração anterior
    if original_settings and "timeout: 0" not in original_settings:
        game.enable_screen_sleep()
        print("Configurações restauradas!")
    else:
        print("Stand-by já estava desativado, mantendo assim.")
    os.execvp("python", ["python", caminho])
