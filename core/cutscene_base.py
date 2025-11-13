import pygame
from config import *
import numpy as np

class CutsceneBase:
    def __init__(self, game, text, next_state, background=None, typing_speed=40, fade_duration=1000):

        self.game = game
        self.text = text
        self.next_state = next_state
        self.background = background
        self.font = pygame.font.Font("assets/fonts/vcr.ttf", 32)
        self.typing_speed = typing_speed
        self.fade_duration = fade_duration

        self.displayed_text = ""
        self.char_index = 0
        self.last_update = pygame.time.get_ticks()

        self.fade_alpha = 255
        self.fading_in = True
        self.fading_out = False
        self.fade_start = pygame.time.get_ticks()

        self.margin = 100
        self.line_spacing = 45

        self.type_sound = self.generate_soft_plim()

    def generate_soft_plim(self):
        try:
            pygame.mixer.init(frequency=44100, channels=2)
            sample_rate = 44100
            duration = 0.05
            frequency = 400

            t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
            fade = np.linspace(1.0, 0.0, len(t))
            wave = (np.sin(2 * np.pi * frequency * t) * fade * 0.3).astype(np.float32)

            stereo_wave = np.column_stack((wave, wave))

            sound = pygame.sndarray.make_sound((stereo_wave * 32767).astype(np.int16))
            sound.set_volume(0.1)
            return sound
        except Exception as e:
            print(f"[Aviso] Erro ao gerar som de digitação sintético: {e}")
            return None

    def wrap_text(self, text, max_width):
        # Remove quebras e cria quebras automáticas antes de falas
        text = text.replace("\n", " ")

        for personagem in ["Vaca fazendeira:", "ETs:", "Narrador:"]:
            text = text.replace(personagem, f"\n{personagem}")

        # Remove quebra no início se existir
        if text.startswith("\n"):
            text = text[1:]

        lines = []
        for paragraph in text.split("\n"):
            words = paragraph.strip().split(" ")
            current_line = ""

            for word in words:
                test_line = current_line + word + " "
                if self.font.size(test_line)[0] < max_width - 2 * self.margin:
                    current_line = test_line
                else:
                    lines.append(current_line.strip())
                    current_line = word + " "
            if current_line:
                lines.append(current_line.strip())
        return lines

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN or e.type == pygame.MOUSEBUTTONDOWN:

                if self.char_index < len(self.text):
                    self.displayed_text = self.text
                    self.char_index = len(self.text)

                elif not self.fading_out:
                    self.fading_out = True
                    self.fade_start = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()

        if self.fading_in:
            elapsed = now - self.fade_start
            self.fade_alpha = max(255 - int((elapsed / self.fade_duration) * 255), 0)
            if self.fade_alpha <= 0:
                self.fade_alpha = 0
                self.fading_in = False

        if not self.fading_in and self.char_index < len(self.text):
            if now - self.last_update > self.typing_speed:
                self.displayed_text += self.text[self.char_index]
                self.char_index += 1
                self.last_update = now
                if self.type_sound:
                    self.type_sound.play()

        if self.fading_out:
            elapsed = now - self.fade_start
            self.fade_alpha = min(int((elapsed / self.fade_duration) * 255), 255)
            if self.fade_alpha >= 255:
                self.game.state_manager.set_state(self.next_state)

    def draw(self, screen):
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(PRETO)

        personagens_cores = {
            "Vaca fazendeira": (255, 200, 100),  # amarelado
            "ETs": (100, 200, 255),  # azul-claro
            "Narrador": (200, 200, 200)
        }

        wrapped_lines = self.wrap_text(self.displayed_text, LARGURA)
        y = int(ALTURA * 0.7)

        fala_atual = None  # mantém quem está falando

        for line in wrapped_lines:
            # Detecta início de nova fala
            for personagem, cor in personagens_cores.items():
                if line.startswith(personagem + ":"):
                    fala_atual = personagem
                    break

            # Define a cor com base na fala atual
            if fala_atual and fala_atual in personagens_cores:
                color = personagens_cores[fala_atual]
            else:
                color = BRANCO

            surface = self.font.render(line, True, color)
            rect = surface.get_rect(center=(LARGURA // 2, y))
            screen.blit(surface, rect)
            y += self.line_spacing

        # Texto "pressione qualquer tecla"
        if self.char_index >= len(self.text) and not self.fading_out:
            tip = self.font.render("(Pressione qualquer tecla para continuar)", True, CINZA)
            tip_rect = tip.get_rect(center=(LARGURA // 2, ALTURA - 50))
            screen.blit(tip, tip_rect)

        # Efeito fade
        if self.fade_alpha > 0:
            fade_surface = pygame.Surface((LARGURA, ALTURA))
            fade_surface.fill(PRETO)
            fade_surface.set_alpha(self.fade_alpha)
            screen.blit(fade_surface, (0, 0))

