import pygame,os,sys,json,subprocess,re

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

from dados import *  # Supondo que esses módulos estejam configurados
from Ponto import Ponto

class Config:
    def __init__(self,game):
        self.game = game
        self.estimulo = 5
      
        self.modo = "info"
        
        self.atenuacao = 0
      
        
        self.CONFIG_FILE = "config.json"

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
        self.config = self.carregar_config()
        self.set_brightness(self.config["brightness"])
        self.set_contrast(self.config["contrast"])
        self.brightness = (self.config["brightness"])
        self.contrast = (self.config["contrast"])
        self.background = self.config["background"]
        self.max_intensity = self.config["max_intensity"]

        
        

    def carregar_config(self):
        """Lê as variáveis do arquivo JSON ou usa valores padrão."""
        if os.path.exists(os.path.abspath(os.path.join(os.path.dirname(__file__), "..",self.CONFIG_FILE))):
            with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "..",self.CONFIG_FILE)), "r") as f:
                return json.load(f)
        else:
            return self.DEFAULT_CONFIG
    def salvar_config(self,config):
        """Salva as variáveis no arquivo JSON."""
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "..",self.CONFIG_FILE)), "w") as f:
            json.dump(config, f, indent=4)
        
        
    def handle_events(self,events):
        
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if self.modo == "info":
                        self.modo = "fundo"
                    elif self.modo == "fundo":
                        self.modo = "estimulo"
                    elif self.modo == "estimulo":
                        self.modo = "fundo_preto"
                    elif self.modo == "fundo_preto":
                        self.modo = "info"
                if event.key == pygame.K_e:                    
                    
                    self.config["background"] = self.background
                    self.config["max_intensity"] = self.max_intensity
                   
                    
                    Colors.ERASE_INTENSITY = self.background
                    Colors.BACKGROUND = (self.background,self.background,self.background)
                    self.salvar_config(self.config)   
                    from strategy_screen import StrategyScreen                 
                    self.game.change_screen(StrategyScreen(self.game))
                if event.key == pygame.K_j: 
                    from strategy_screen import StrategyScreen
                    self.game.change_screen(StrategyScreen(self.game))
                if event.key == pygame.K_RIGHT:
                    
                    if self.background < 255:
                        self.background += 1   
                        Colors.ERASE_INTENSITY = self.background
                        Colors.BACKGROUND = (self.background,self.background,self.background)   
                    
                if event.key == pygame.K_LEFT:
                   
                    if self.background > 0:
                        self.background -= 1                
                        Colors.ERASE_INTENSITY = self.background
                        Colors.BACKGROUND = (self.background,self.background,self.background)
                 
                if event.key == pygame.K_l:   
                    if self.estimulo < 5:
                        self.estimulo += 1                 
                    
                   
                if event.key == pygame.K_k:
                    if self.estimulo > 0:
                        self.estimulo -= 1
                    
                        
                if event.key == pygame.K_DOWN:
                    if self.max_intensity < 255:
                        self.max_intensity += 1
                       
                if event.key == pygame.K_UP:         
                    if self.max_intensity > 0:
                        self.max_intensity -= 1                    
                        
                if event.key == pygame.K_F1:
                  
                    if self.atenuacao != 40:
                        self.atenuacao += 1
                    self.ponto_calibracao.cor = Ponto.db_para_intensidade(self.atenuacao)
                if event.key == pygame.K_F2:
                 
                    if self.atenuacao != 0:
                        self.atenuacao -= 1
                    self.ponto_calibracao.cor = Ponto.db_para_intensidade(self.atenuacao)
                                    
                    
    def update(self):
        pygame.display.update()
    
    def draw(self,surface):
        
        font = pygame.font.SysFont(None, 36)
        self.ponto_calibracao = Ponto(0,0,self.estimulo,Ponto.db_para_intensidade(self.atenuacao),200)
        
        fundo = font.render(f"Fundo: {self.background}", True, (26, 45, 254))
        brilho = font.render(f"Brilho: {self.brightness}", True, (26, 45, 254))
        contraste = font.render(f"Contraste: {self.contrast}", True, (26, 45, 254))
        estimulo = font.render(f"Estimulo: {self.estimulo}", True, (26, 45, 254))
        resolutionW = self.config["resolution-w"]
        resolutionH = self.config["resolution-h"]
        resolution = font.render(f"Resolucao:{resolutionW} x {resolutionH}",True,(26, 45, 254))
        atenuacao_estimulo = font.render(f"Atenuacao do estimulo:{self.atenuacao}",True,(26, 45, 254))
        intensidade_maxima = font.render(f"Intensidade maxima:{self.max_intensity}",True,(26, 45, 254))
        if self.modo == "info":
            surface.fill(Colors.BACKGROUND)
            self.ponto_calibracao.plotarPonto()
            surface.blit(fundo, (80, 100))
            surface.blit(atenuacao_estimulo, (80, 150))
            surface.blit(estimulo, (80, 200))  
            surface.blit(contraste, (80, 250))            
            surface.blit(brilho,(80,300))          
            surface.blit(resolution,(80,350))   
            surface.blit(intensidade_maxima,(80,400))    
        elif self.modo == "fundo":
            surface.fill(Colors.BACKGROUND)
        elif self.modo == "estimulo":
            surface.fill((0,0,0))
            square_size = 300
            square_color = Ponto.db_para_intensidade(self.ponto_calibracao.atenuacao)
            square_x = (surface.get_width() - square_size) // 2
            square_y = (surface.get_height() - square_size) // 2
            pygame.draw.rect(surface, square_color, (square_x, square_y, square_size, square_size))
            
            
            estimulo = font.render(f"Estimulo: {self.estimulo}", True, (50, 50, 50))
            surface.blit(estimulo, (80, 200)) 
        elif self.modo == "fundo_preto":
            surface.fill((0,0,0))
        
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
            
            
if __name__ == "__main__":
    visualizando = True
    pygame.init()
    pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    config = Config()
    while visualizando:
        config.handle_events(pygame.event.get())
        config.update()
        config.draw(pygame.display.get_surface())