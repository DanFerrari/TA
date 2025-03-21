import pygame
from dados import DadosExame, Constantes
from CAMPScreening import Screening
from CAMPFullThreshold import FullThreshold
from strategy_screen import StrategyScreen



class SelectEyeScreen:
    def __init__(self, game):
        self.game = game
        self.width, self.height = game.width, game.height

        # Fontes utilizadas na tela
        self.fonte = pygame.font.Font(None, 40)
        self.fonte_numero = pygame.font.Font(None, 80)

        
        # Cores e configurações visuais
        self.cor_texto = (255, 255, 255)
        self.cor_texto_fade = (100, 100, 100)
        self.cor_caixa = (50, 50, 50)
        self.cor_caixa_selecao = (70, 70, 70)
        self.cor_botao = (70, 70, 70)
        self.cor_botao_hover = (45,167,8)
        self.cor_font_olho = (255, 255, 255)
        self.cor_fundo = game.cor_fundo
        self.cor_padrao_botao =  (100,100,100)
        self.cor_padrao_botao_fade = (70, 70, 70)
        self.cor_selecao = (255,247,28)
        

        # Opções de olho
        self.opcoes = ["OLHO ESQUERDO", "OLHO DIREITO"]
        self.opcao_selecionada = 0

        # Controle de qual item está selecionado:
        # Pode ser "opcoes", "numero" ou "botao"
        self.selecao_atual = "opcoes"
        
        # Caixa numérica (para exame screening)
        self.numero = 25
        self.NUMERO_MIN = 0
        self.NUMERO_MAX = 40
        self.faixa_etaria = {1:"0 - 20", 2:"21 - 30", 3:"31 - 40", 4:"41 - 50", 5:"51 - 60", 6:"61 - 70", 7:"71 - 80"}
        self.escolha_faixa = 1

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:  # Volta para o menu ou sai
                    self.game.change_screen(StrategyScreen(self.game))
                elif event.key == pygame.K_x:
                    if self.selecao_atual == "numero":
                        self.selecao_atual = "opcoes"
                    elif self.selecao_atual == "botao":                       
                        self.selecao_atual = "numero"
                     
                elif event.key == pygame.K_e:
                    if self.selecao_atual == "opcoes":                        
                        self.selecao_atual = "numero"                       
                    elif self.selecao_atual == "numero":
                        self.selecao_atual = "botao"
                    elif self.selecao_atual == "botao":
                        # Ao confirmar no botão, inicia o exame conforme a estratégia selecionada
                        if DadosExame.exame_selecionado == Constantes.screening:
                            if self.opcao_selecionada == 0:
                                DadosExame.olho = Constantes.olho_esquerdo
                            else:
                                DadosExame.olho = Constantes.olho_direito
                            DadosExame.atenuacao_screening = self.numero                           
                            self.game.change_screen(Screening(self.game))
                            
                        elif DadosExame.exame_selecionado == Constantes.fullthreshold:
                            if self.opcao_selecionada == 0:
                                DadosExame.olho = Constantes.olho_esquerdo
                            else:
                                DadosExame.olho = Constantes.olho_direito
                            DadosExame.faixa_etaria = self.escolha_faixa
                            self.game.change_screen(FullThreshold(self.game))
                         
                        else:
                            print("Exame não implementado!")
                elif self.selecao_atual == "opcoes":
                    if event.key == pygame.K_LEFT:
                        self.opcao_selecionada = 0
                        DadosExame.olho = Constantes.olho_esquerdo
                    elif event.key == pygame.K_RIGHT:
                        self.opcao_selecionada = 1
                        DadosExame.olho = Constantes.olho_direito
                elif self.selecao_atual == "numero":
                    if event.key == pygame.K_LEFT and self.numero > self.NUMERO_MIN:
                        self.numero -= 1
                        if self.escolha_faixa > 1:
                            self.escolha_faixa -= 1
                        
                    elif event.key == pygame.K_RIGHT and self.numero < self.NUMERO_MAX:
                        self.numero += 1
                        if self.escolha_faixa < 7:
                            self.escolha_faixa += 1
                        

    def update(self):
        # Atualizações de animações ou lógicas adicionais podem ser inseridas aqui
        pass

    def draw(self, surface):
        surface.fill(self.cor_fundo)
        # Garante um valor default para teste (pode ser removido se necessário)
        DadosExame.olho = Constantes.olho_direito
        
        # Renderiza as opções de olho no topo
        pos_y_opcoes = self.height * 0.2
        if self.selecao_atual == "opcoes":
            self.cor_padrao_botao = (76, 76, 76)
        else:
            self.cor_padrao_botao = (45,167,8)
            
        
        texto_esquerda = self.fonte.render(
            self.opcoes[0],
            True,
            self.cor_font_olho
        )
        texto_direita = self.fonte.render(
            self.opcoes[1],
            True,
            self.cor_font_olho
        )
        rect_esquerda = pygame.Rect(self.width * 0.25 - 265, pos_y_opcoes - 35, 530, 100)
        rect_direita = pygame.Rect(self.width * 0.75 - 265, pos_y_opcoes - 35, 530, 100)
        
        pygame.draw.rect(surface,self.cor_padrao_botao if self.opcao_selecionada == 0 else self.cor_padrao_botao_fade, rect_esquerda, border_radius=15)
        pygame.draw.rect(surface,self.cor_padrao_botao if self.opcao_selecionada == 1 else self.cor_padrao_botao_fade, rect_direita, border_radius=15)
        if self.selecao_atual == "opcoes":
            if self.opcao_selecionada == 0:
                pygame.draw.rect(surface, self.cor_selecao, rect_esquerda, 5, border_radius=15)
            else:
                pygame.draw.rect(surface, self.cor_selecao, rect_direita, 5, border_radius=15)
        
        
        
        
        surface.blit(texto_esquerda, (self.width * 0.25 - texto_esquerda.get_width() // 2, pos_y_opcoes))
        surface.blit(texto_direita, (self.width * 0.75 - texto_direita.get_width() // 2, pos_y_opcoes))
        
        
        # Renderiza a caixa numérica (se o exame selecionado for Screening)
        if DadosExame.exame_selecionado == Constantes.screening:          
            cor_caixa_atual = self.cor_caixa_selecao if self.selecao_atual == "numero" else self.cor_caixa
            pos_y_numero = self.height * 0.4
            rect_box = pygame.Rect(self.width // 2 - 75, pos_y_numero, 150, 130)
            pygame.draw.rect(surface, cor_caixa_atual, rect_box, border_radius=10)
            
            texto_numero = self.fonte_numero.render(str(self.numero), True, self.cor_texto)
            texto_numero_pos = texto_numero.get_rect(center=((self.width // 2 -75) + 150//2, pos_y_numero + 65))
            surface.blit(texto_numero, texto_numero_pos)
            
            label_atenuacao_texto = self.fonte.render("ATENUACAO", True, self.cor_texto)
            label_atenuacao_pos = label_atenuacao_texto.get_rect(center=(self.width // 2 , pos_y_numero -50))
            surface.blit(label_atenuacao_texto, label_atenuacao_pos)
            
            if self.selecao_atual == "numero":
                pygame.draw.rect(surface, self.cor_selecao, rect_box, 5, border_radius=10)
    
        if DadosExame.exame_selecionado == Constantes.fullthreshold:          
            cor_caixa_atual = self.cor_caixa_selecao if self.selecao_atual == "numero" else self.cor_caixa
            pos_y_numero = self.height * 0.4
            rect_box = pygame.Rect(self.width // 2 - 150, pos_y_numero, 300, 130)
            pygame.draw.rect(surface, cor_caixa_atual, rect_box, border_radius=10)
            
            texto_numero = self.fonte_numero.render(self.faixa_etaria.get(self.escolha_faixa), True, self.cor_texto)
            texto_numero_pos = texto_numero.get_rect(center=((self.width // 2 -150) + 300//2, pos_y_numero + 65))
            surface.blit(texto_numero, texto_numero_pos)
            
            label_atenuacao_texto = self.fonte.render("FAIXA ETARIA", True, self.cor_texto)
            label_atenuacao_pos = label_atenuacao_texto.get_rect(center=(self.width // 2 , pos_y_numero -50))
            surface.blit(label_atenuacao_texto, label_atenuacao_pos)
            
            if self.selecao_atual == "numero":
                pygame.draw.rect(surface, self.cor_selecao, rect_box, 5, border_radius=10)       
                
                
                
        
        #caixa selecao distancia do paciente
        cor_caixa_distancia = self.cor_caixa_selecao if self.selecao_atual == "distancia" else self.cor_caixa
        pos_y_distancia = self.height * 0.4
        rect_box_distancia = pygame.Rect(self.width // 2 - 150 -400, pos_y_distancia, 300, 130)
        pygame.draw.rect(surface, cor_caixa_distancia, rect_box_distancia, border_radius=10)

        texto_distancia = self.fonte_numero.render("20 CM", True, self.cor_texto)
        texto_distancia_pos = texto_distancia.get_rect(center=((self.width // 2 ) -400 , pos_y_distancia + 65))

        surface.blit(texto_distancia, texto_distancia_pos)

        label_distancia_texto = self.fonte.render("DISTANCIA PACIENTE", True, self.cor_texto)
        label_distancia_pos = label_distancia_texto.get_rect(center=((self.width // 2) - 400 , pos_y_distancia -50))
        surface.blit(label_distancia_texto, label_distancia_pos)

        if self.selecao_atual == "distancia":
            pygame.draw.rect(surface, self.cor_selecao, rect_box_distancia, 5, border_radius=10)  
            
            
            
        #caixa selecao tamanho estimulo
        
        cor_caixa_estimulo = self.cor_caixa_selecao if self.selecao_atual == "estimulo" else self.cor_caixa
        pos_y_estimulo = self.height * 0.4
        rect_box_estimulo = pygame.Rect(self.width // 2 - 150 +400, pos_y_estimulo, 300, 130)
        pygame.draw.rect(surface, cor_caixa_estimulo, rect_box_estimulo, border_radius=10)
        texto_estimulo = self.fonte_numero.render("III", True, self.cor_texto)
        texto_estimulo_pos = texto_estimulo.get_rect(center=((self.width // 2 ) +400 , pos_y_estimulo + 65))
        surface.blit(texto_estimulo, texto_estimulo_pos)
        label_estimulo_texto = self.fonte.render("TAMANHO ESTIMULO", True, self.cor_texto)
        label_estimulo_pos = label_estimulo_texto.get_rect(center=((self.width // 2) + 400 , pos_y_estimulo -50))
        surface.blit(label_estimulo_texto, label_estimulo_pos)
        if self.selecao_atual == "estimulo":
            pygame.draw.rect(surface, self.cor_selecao, rect_box_estimulo, 5, border_radius=10)      
            
                         
                
                
                
                
                
                
                
                
        
        # Renderiza o botão "Iniciar Exame"
        pos_y_botao = self.height * 0.70
        cor_botao_atual = self.cor_botao_hover if self.selecao_atual == "botao" else self.cor_botao
        rect_botao = pygame.Rect(self.width // 2 - 750, pos_y_botao, 1500, 170)
        pygame.draw.rect(surface, cor_botao_atual, rect_botao, border_radius=10)
        texto_botao = self.fonte.render("INICIAR EXAME", True, (255,255,255))
        texto_botao_pos = texto_botao.get_rect(center=((self.width // 2 ) , pos_y_botao + 85))  
        surface.blit(texto_botao, texto_botao_pos)
        if self.selecao_atual == "botao":
            pygame.draw.rect(surface, self.cor_selecao, rect_botao, 5, border_radius=10)
    
        
        
