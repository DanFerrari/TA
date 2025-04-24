import pygame
import time



class Autenticacao():
    def __init__(self):
       
        self.fonte = pygame.font.Font(None, 80)
        self.senha_secreta = ["p", "f1", "f2", "f3", "f4","p"]
        self.entrada_usuario = []
        self.modo_autenticado = False
        self.mostrar_erro = False
        self.tempo_erro = 0
        self.clock = pygame.time.Clock()


    def desenhar_tela_login(self):
        pygame.display.get_surface().fill((30, 30, 30))
        texto = self.fonte.render("Digite a senha:", True, (255, 255, 255))
        pygame.display.get_surface().blit(texto, (600, 300))

        senha_oculta = "*" * len(self.entrada_usuario)
        senha_render = self.fonte.render(senha_oculta, True, (200, 200, 255))
        pygame.display.get_surface().blit(senha_render, (600,380))

        if self.mostrar_erro:
            pygame.display.get_surface().fill((100, 0, 0))
            texto = self.fonte.render("ACESSO NEGADO", True, (255, 255, 255))
            pygame.display.get_surface().blit(texto, (750, 500))
            pygame.display.flip()
            pygame.time.delay(2000)


        pygame.display.flip()


    def desenhar_tela_protegida(self):
        pygame.display.get_surface().fill((0, 100, 0))
        texto = self.fonte.render("ACESSO PERMITIDO", True, (255, 255, 255))
        pygame.display.get_surface().blit(texto, (750, 500))
        pygame.display.flip()


    def verificar_senha(self):
        rodando = True

        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_j:
                    self.modo_autenticado = False
                    rodando = False

                elif (
                    evento.type == pygame.KEYDOWN
                    and not self.modo_autenticado
                    and not self.mostrar_erro
                ):
                    tecla = pygame.key.name(evento.key)
                    self.entrada_usuario.append(tecla)

                    if len(self.entrada_usuario) == len(self.senha_secreta):
                        if self.entrada_usuario == self.senha_secreta:
                            self.modo_autenticado = True
                        else:
                            self.mostrar_erro = True
                            self.tempo_erro = pygame.time.get_ticks()
                    pygame.display.update()
                

            # Mostrar pygame.display.get_surface() correta
            if self.modo_autenticado:
                self.desenhar_tela_protegida()
                pygame.display.flip()
                pygame.time.delay(3000)
                rodando = False
            else:
                self.desenhar_tela_login()
                pygame.display.flip()
                

            if self.mostrar_erro:
                rodando = False
            # Limpar

            self.clock.tick(30)
            

        return self.modo_autenticado
