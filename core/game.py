import pygame
from config import *
from core.state_manager import StateManager
from core.brightness_overlay import BrightnessOverlay
from core.audio_manager import AudioManager
from states.menu import MenuState
from states.tutorial import TutorialState
from states.primeiraFaseState import Fase1State
from cv.config import (
    BRIGHTNESS_LEVELS,
    DEFAULT_BRIGHTNESS_OBJECT,
    VOLUME_LEVELS,
    DEFAULT_VOLUME_OBJECT,
    BACKGROUND_MUSIC_PATH,
)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Meu Jogo de Gestos")
        self.clock = pygame.time.Clock()
        self.running = True

        # Inicializar o overlay de brilho com o valor padrão
        default_opacity = BRIGHTNESS_LEVELS.get(DEFAULT_BRIGHTNESS_OBJECT, 0)
        self.brightness_overlay = BrightnessOverlay(LARGURA, ALTURA, default_opacity)

        # Inicializar o gerenciador de áudio com o volume padrão
        default_volume = VOLUME_LEVELS.get(DEFAULT_VOLUME_OBJECT, 1.0)
        self.audio_manager = AudioManager(BACKGROUND_MUSIC_PATH, default_volume)
        
        # Iniciar a música de fundo em loop
        self.audio_manager.play_background_music(loops=-1)

        self.state_manager = StateManager()
        self.state_manager.add_state("menu", MenuState(self))
        self.state_manager.add_state("tutorial", TutorialState(self))
        self.state_manager.add_state("fase1", Fase1State(self))

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

            # Desenhar o overlay de brilho por cima de tudo
            self.brightness_overlay.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

        # Limpar recursos de áudio antes de encerrar
        self.audio_manager.cleanup()
        pygame.quit()
