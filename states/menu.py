import pygame
from config import *

class MenuState:
    def __init__(self, game):
        self.game = game

        self.botoes = {
            "iniciar": pygame.image.load("assets/images/botao_iniciar.png"),
            "tutorial": pygame.image.load("assets/images/botao_tutorial.png"),
            "sair": pygame.image.load("assets/images/botao_sair.png")
        }

        for nome in self.botoes:
            self.botoes[nome] = pygame.transform.scale(self.botoes[nome], (300, 100))

        self.rects = {}
        centro_x = LARGURA // 2
        centro_y = ALTURA // 2
        espacamento = 150

        for i, (nome, img) in enumerate(self.botoes.items()):
            rect = img.get_rect(center=(centro_x, centro_y + i * espacamento))
            self.rects[nome] = rect

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for nome, rect in self.rects.items():
                    if rect.collidepoint(mouse_pos):
                        if nome == "iniciar":
                            print("Iniciar jogo")
                        elif nome == "tutorial":
                            print("Abrir tutorial")
                        elif nome == "sair":
                            print("Saindo...")
                            self.game.running = False

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(PRETO)

        for nome, img in self.botoes.items():
            rect = self.rects[nome]
            screen.blit(img, rect)

        mouse_pos = pygame.mouse.get_pos()
        for nome, rect in self.rects.items():
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, VERMELHO, rect, 3)
