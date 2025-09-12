import pygame
from config import *

class Fase1State:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font("assets/fonts/vcr.ttf", 60)

        try:
            self.background_image = pygame.image.load("assets/images/fazenda.png").convert()
            self.background_image = pygame.transform.scale(self.background_image, (LARGURA, ALTURA))
        except pygame.error as e:
            print(f"Erro ao carregar a imagem de fundo: {e}")
            self.background_image = None

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.game.state_manager.set_state("menu")

    def update(self):
        pass

    def draw(self, screen):
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        else:
            screen.fill(PRETO)
