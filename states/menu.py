import pygame
from config import *

class MenuState:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font("assets/fonts/vcr.ttf", 80)

        self.botoes = {
            "iniciar": self.font.render("Iniciar Jogo", True, BRANCO),
            "tutorial": self.font.render("Tutorial", True, BRANCO),
            "sair": self.font.render("Sair", True, BRANCO)
        }
        self.rects = {}
        centro_x = LARGURA // 2
        centro_y = ALTURA // 2

        espacamento = 100
        for i, (nome, texto) in enumerate(self.botoes.items()):
            rect = texto.get_rect(center=(centro_x, centro_y + i * espacamento))
            self.rects[nome] = rect

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for nome, rect in self.rects.items():
                    if rect.collidepoint(mouse_pos):
                        if nome == "iniciar":
                            print("Iniciar jogo")
                            self.game.state_manager.set_state("fase1")
                        elif nome == "tutorial":
                            print("Abrir tutorial")
                            self.game.state_manager.set_state("tutorial")
                        elif nome == "sair":
                            print("Saindo...")
                            self.game.running = False

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(PRETO)

        for nome, texto in self.botoes.items():
            rect = self.rects[nome]
            screen.blit(texto, rect)

        mouse_pos = pygame.mouse.get_pos()
        for nome, rect in self.rects.items():
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, VERMELHO, rect, 3)