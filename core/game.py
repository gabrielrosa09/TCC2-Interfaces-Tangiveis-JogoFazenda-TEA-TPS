import pygame
from config import *
from core.state_manager import StateManager
from states.cutscene1 import Cutscene1
from states.cutscene2 import Cutscene2
from states.cutscene3 import Cutscene3
from states.cutscene4_tutorial import Cutscene4_Tutorial
from states.cutscene5_tutorial_pratico import Cutscene5_TutorialPratico
from states.cutscene6_inicio_missoes import Cutscene6_InicioMissoes
from core.brightness_overlay import BrightnessOverlay
from core.audio_manager import AudioManager
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
        pygame.display.set_caption("A Vaca Fazendeira e os ETs")
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

        # Adiciona todas as cutscenes
        self.state_manager.add_state("cutscene1", Cutscene1(self))
        self.state_manager.add_state("cutscene2", Cutscene2(self))
        self.state_manager.add_state("cutscene3", Cutscene3(self))
        self.state_manager.add_state("cutscene4_tutorial", Cutscene4_Tutorial(self))
        self.state_manager.add_state("cutscene5_tutorial_pratico", Cutscene5_TutorialPratico(self))
        self.state_manager.add_state("cutscene6_inicio_missoes", Cutscene6_InicioMissoes(self))
        self.state_manager.add_state("fase1", Fase1State(self))

        # Começa pela primeira cutscene
        self.state_manager.set_state("cutscene1")

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
