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
from core.color_filter import ColorFilter
from states.menu import MenuState
from states.tutorial import TutorialState
from states.primeiraFaseState import Fase1State

from cv.config import (
    BRIGHTNESS_LEVELS,
    DEFAULT_BRIGHTNESS_OBJECT,
    VOLUME_LEVELS,
    DEFAULT_VOLUME_OBJECT,
    GAME_SOUNDS,
    COLOR_MODES,
    DEFAULT_COLOR_MODE_OBJECT,
)


class Game:
    def __init__(self, game_controller=None):
        pygame.init()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.window_width, self.window_height = self.screen.get_size()

        self.game_surface = pygame.Surface((LARGURA, ALTURA)).convert_alpha()

        pygame.display.set_caption("A Vaca Fazendeira e os ETs")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_controller = game_controller

        default_opacity = BRIGHTNESS_LEVELS.get(DEFAULT_BRIGHTNESS_OBJECT, 0)
        self.brightness_overlay = BrightnessOverlay(LARGURA, ALTURA, default_opacity)

        # Audio
        default_volume = VOLUME_LEVELS.get(DEFAULT_VOLUME_OBJECT, 0.3)
        music_info = GAME_SOUNDS.get("background_music", {})
        self.audio_manager = AudioManager(
            music_info.get("path", ""),
            default_volume,
            music_info.get("base_volume", 0.02)
        )

        for name, info in GAME_SOUNDS.items():
            if name != "background_music":
                self.audio_manager.register_sound(
                    name, info["path"], info["base_volume"]
                )

        self.audio_manager.play_background_music(loops=-1)

        # Filtro de cor
        default_color_mode = COLOR_MODES.get(DEFAULT_COLOR_MODE_OBJECT, "color")
        self.color_filter = ColorFilter(LARGURA, ALTURA, default_color_mode)

        # States
        self.state_manager = StateManager()
        self.state_manager.add_state("cutscene1", Cutscene1(self))
        self.state_manager.add_state("cutscene2", Cutscene2(self))
        self.state_manager.add_state("cutscene3", Cutscene3(self))
        self.state_manager.add_state("cutscene4_tutorial", Cutscene4_Tutorial(self))
        self.state_manager.add_state("cutscene5_tutorial_pratico", Cutscene5_TutorialPratico(self))
        self.state_manager.add_state("cutscene6_inicio_missoes", Cutscene6_InicioMissoes(self))
        self.state_manager.add_state("fase1", Fase1State(self))

        self.state_manager.set_state("cutscene1")

    def run(self):
        while self.running:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    self.running = False

            self.state_manager.handle_events(events)
            self.state_manager.update()

            self.game_surface.fill(PRETO)
            self.state_manager.draw(self.game_surface)

            # Aplica brilho e filtro (no buffer!)
            self.brightness_overlay.draw(self.game_surface)
            self.color_filter.apply_filter_optimized(self.game_surface)

            scaled = pygame.transform.scale(
                self.game_surface,
                (self.window_width, self.window_height)
            )

            self.screen.blit(scaled, (0, 0))
            pygame.display.flip()
            self.clock.tick(FPS)

        self.audio_manager.cleanup()
        pygame.quit()
