import pygame
import os
import sys
import OPi.GPIO as GPIO
import time
import subprocess
import signal
import json


GPIO.setwarnings(False)
GPIO.setmode(GPIO.SUNXI)

PIN_ENTRADA = "PD22"
GPIO.setup(PIN_ENTRADA, GPIO.IN)


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
from pages.select_eye_screen import SelectEyeScreen
from pages.index import Index


class Campimetria:

    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        self.screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.NOFRAME)
        self.width, self.height = self.screen.get_size()
        pygame.display.set_caption("Seleção de Estratégia")
        self.clock = pygame.time.Clock()
        self.running = True
        self.FLAG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__),"utils","temp","xscreensaver_was_running.flag"))
        self.ATIVA_SCREENSAVER = os.path.abspath(os.path.join(os.path.dirname(__file__),"scripts","ativa_xscreensaver.sh"))
        
        self.cor_fundo = (20, 20, 20)
        self.cor_botao = (122, 122, 122)
        self.cor_botao_hover = (255, 255, 255)
        self.cor_texto = (255, 255, 255)
        self.font_main = pygame.font.Font(None, int(self.height * 0.07))

        self.current_screen = Index(self)
        self.CONFIG_FILE = "config.json"

       
        
        self.config = self.carregar_config()
        self.set_brightness(self.config["brightness"])
        self.set_contrast(self.config["contrast"])
        DadosExame.tamanho_estimulo = self.config["tamanho_estimulo"]
        DadosExame.distancia_paciente = self.config["distancia_paciente"]
        DadosExame.exame_id = self.config["exame_id"]
        print(os.path.abspath(os.path.join(os.path.dirname(__file__),"config.json")))



    def carregar_config(self):
        """Lê as variáveis do arquivo JSON ou usa valores padrão."""
        self.DEFAULT_CONFIG ={
            "distancia_paciente": 200,
            "tamanho_estimulo": 3,
            "exame_id": 1,
            "background":120,
            "max_intensity": 255,
            "brightness":90,
            "contrast":50,
            "resolution-w":1920,
            "resolution-h":1080,
            "atenuacao":25,
        }
        if os.path.exists(os.path.abspath(os.path.join(os.path.dirname(__file__),"config.json"))):
            with open(os.path.abspath(os.path.join(os.path.dirname(__file__),"config.json")), "r") as f:
                return json.load(f)
        else:
            return self.DEFAULT_CONFIG
        
    def salvar_config(self,config):
        """Salva as variáveis no arquivo JSON."""
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__),self.CONFIG_FILE)), "w") as f:
            json.dump(config, f, indent=4)
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
    def is_xscreensaver_running(self):
        try:
            subprocess.check_output(["pidof", "xscreensaver"])
            return True
        except subprocess.CalledProcessError:
            return False

    def stop_xscreensaver(self):
        os.system("killall xscreensaver")

    def start_xscreensaver(self):       
        subprocess.Popen([self.ATIVA_SCREENSAVER])

    def save_flag(self):
        with open(self.FLAG_FILE, "w") as f:
            f.write("running")

    def clear_flag(self):
        if os.path.exists(self.FLAG_FILE):
            os.remove(self.FLAG_FILE)

    def was_running_before(self):
        return os.path.exists(self.FLAG_FILE)


if __name__ == "__main__":

    game = Campimetria()
    if game.is_xscreensaver_running():
        print("xscreensaver está rodando. Parando e salvando estado...")
        game.save_flag()
        game.stop_xscreensaver()
    else:
        print("xscreensaver não está rodando.")
        game.clear_flag()

    # Simula execução do app
    try:
        game.run()
    finally:
        caminho = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "lib", "mainTA.py")
        )        
        if game.was_running_before():
            print("xscreensaver estava rodando antes. Reiniciando...")
            game.start_xscreensaver()
            game.clear_flag()
        else:
            print("xscreensaver não estava rodando antes. Nada a fazer.")
        os.execvp("python", ["python", caminho])


    
