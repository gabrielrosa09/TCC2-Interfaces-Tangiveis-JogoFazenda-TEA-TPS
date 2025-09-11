import pygame
from config import *
from core.state_manager import StateManager
from states.menu import MenuState
from states.tutorial import TutorialState

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Meu Jogo de Gestos")
        self.clock = pygame.time.Clock()
        self.running = True

        self.state_manager = StateManager()
        self.state_manager.add_state("menu", MenuState(self))
        self.state_manager.add_state("tutorial", TutorialState(self))

        self.state_manager.set_state("menu")

    def run(self):
        while self.running:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    self.running = False

            self.state_manager.handle_events(events)
            self.state_manager.update()
            self.screen.fill(PRETO)
            self.state_manager.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
