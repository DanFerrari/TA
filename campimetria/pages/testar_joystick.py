import pygame,os,sys,importlib
import OPi.GPIO as GPIO

PIN_ENTRADA = "PD22"




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



    
if 'config_screen' not in globals():
    config_screen = importlib.import_module("pages.config_screen")
    globals()['config_screen'] = config_screen
else:
    config_screen = globals()['config_screen']
    

class TestarJoystick:
    def __init__(self, game):
        self.game = game
        self.desenhar_botao = False
        self.font = pygame.font.Font(None, 48)
        self.cor_fundo = game.cor_fundo
        self.cor_texto = game.cor_texto 




    def handle_events(self, events):
        self.desenhar_botao = False
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:  # Confirma a seleção
                    self.desenhar_botao = True                    
                elif event.key == pygame.K_j:
                    self.game.change_screen(config_screen.ConfigScreen(self.game))
        if GPIO.input(PIN_ENTRADA) == GPIO.HIGH:
              self.desenhar_botao = True

    def update(self):
        pass

    def draw(self, surface):
        
        surface.fill(self.cor_fundo)
        label_text = self.font.render("APERTE O JOYSTICK PARA TESTAR, CASO APARECA O PONTO AZUL O JOYSTICK ESTÁ FUNCIONANDO", True, self.cor_texto)
        surface.blit(label_text, (self.game.width // 2 - label_text.get_width() // 2, int(self.game.height * 0.2)))
        if self.desenhar_botao:
            pygame.draw.circle(surface, (0, 0, 255), (self.game.width // 2, self.game.height // 2), 100)
        pygame.display.update()
        pygame.time.delay(150)
 
        

        
        
      