import pygame
from config import *


class Fase1State:
    def __init__(self, game):
        self.game = game

        try:
            self.font = pygame.font.Font("assets/fonts/MinecraftStandard.otf", 6)
            self.result_font = pygame.font.Font("assets/fonts/MinecraftStandard.otf", 6)
        except:
            self.font = pygame.font.SysFont("arial", 30)
            self.result_font = pygame.font.SysFont("arial", 60)

        self.text_color = (89, 86, 82)
        self.dialog_text = ("Muuu! Olha só o que temos disponível hoje, que sorte! "
                            "Uma Nave E, uma OU e uma NÃO. Está sem sol "
                            "mas o vento tá muuuito forte!")

        # --- Armazenamento de Imagens e Retângulos ---
        self.images = {}
        self.rects = {}

        # --- Animação da vaca ---
        self.cow_frames = []
        self.current_cow_frame = 0
        self.cow_animation_speed = 120  # ms entre frames
        self.last_cow_update = pygame.time.get_ticks()

        # --- TYPEWRITER (texto sendo escrito) ---
        self.full_dialog_text = self.dialog_text  # texto completo
        self.shown_chars = 0  # quantidade de caracteres visíveis
        self.text_speed = 20  # chars por segundo
        self.last_text_update = pygame.time.get_ticks()
        self.typewriter_started = False

        # Carrega tudo e define as posições
        self._load_assets()
        self._load_cow_animation()
        self._setup_layout()

    # -------------------------------------------------------------------------
    # SISTEMA DE CARREGAMENTO DE IMAGENS
    # -------------------------------------------------------------------------

    def _load_sprite(self, path, scale_factor=1.0, size_override=None):
        try:
            img = pygame.image.load(path).convert_alpha()

            if size_override:
                return pygame.transform.scale(img, size_override)

            if scale_factor != 1.0:
                w = int(img.get_width() * scale_factor)
                h = int(img.get_height() * scale_factor)
                img = pygame.transform.scale(img, (w, h))

            return img
        except pygame.error as e:
            print(f"Erro ao carregar {path}: {e}")
            return None

    def _load_cow_animation(self):
        """Carrega todos os frames da vaquinha animada."""
        for i in range(30):  # coloque o número exato de frames
            path = f"assets/images/final_images/vaca_noite_comVento_LOOP/vaca_noite_comVento_-_frame_{i:02}.png"
            frame = self._load_sprite(path)
            if frame:
                self.cow_frames.append(frame)

        if not self.cow_frames:
            print("Nenhum frame da vaquinha foi carregado!")

    def _load_assets(self):
        bg_img = pygame.image.load("assets/images/final_images/fundo_noite.png").convert()
        self.images['background'] = pygame.transform.scale(bg_img, (LARGURA, ALTURA))

        self.images['dialog_box'] = self._load_sprite("assets/images/final_images/caixa_Dialogo.png")
        self.images['panel'] = self._load_sprite("assets/images/final_images/painel_noite_comVento.png")
        self.images['fase_demo_noite'] = self._load_sprite("assets/images/final_images/fase_demo_noite.png")

        self.images['display_0'] = self._load_sprite("assets/images/final_images/val_inf_Display_1.png")
        self.images['display_1'] = self._load_sprite("assets/images/final_images/val_sup_Display_0.png")

    # -------------------------------------------------------------------------
    # POSICIONAMENTO DOS ELEMENTOS
    # -------------------------------------------------------------------------

    def _setup_layout(self):
        if self.images.get('dialog_box'):
            r = self.images['dialog_box'].get_rect()
            r.topleft = (0, 0)
            self.rects['dialog_box'] = r

            padding_x = 8
            padding_y = 5
            self.rects['text_area'] = pygame.Rect(
                r.x + padding_x,
                r.y + padding_y,
                r.width - (padding_x * 2),
                r.height - (padding_y * 2)
            )

        if self.images.get('panel'):
            r = self.images['panel'].get_rect()
            r.topleft = (0, 0)
            self.rects['panel'] = r

        if self.images.get('fase_demo_noite'):
            r = self.images['fase_demo_noite'].get_rect()
            r.topleft = (0, 0)
            self.rects['fase_demo_noite'] = r

        # --- VAQUINHA ANIMADA (usa os frames)
        if self.cow_frames and 'panel' in self.rects:
            r = self.cow_frames[0].get_rect()
            r.center = self.rects['panel'].center
            r.y += 0
            r.x += 0
            self.rects['cow'] = r

        if self.images.get('display_0'):
            r = self.images['display_0'].get_rect()
            r.topleft = (0, 0)
            self.rects['display_0'] = r

        if self.images.get('display_1'):
            r = self.images['display_1'].get_rect()
            r.x = 0
            r.y = 0
            self.rects['display_1'] = r

    # -------------------------------------------------------------------------
    # EVENTOS / UPDATE
    # -------------------------------------------------------------------------

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.game.state_manager.set_state("menu")

    def update(self):
        # Atualiza animação da vaca
        now = pygame.time.get_ticks()
        if now - self.last_cow_update > self.cow_animation_speed:
            self.last_cow_update = now
            self.current_cow_frame = (self.current_cow_frame + 1) % len(self.cow_frames)

        elapsed = now - self.last_text_update
        chars_to_add = int(elapsed / (1000 / self.text_speed))

        if chars_to_add > 0:
            self.shown_chars = min(len(self.full_dialog_text), self.shown_chars + chars_to_add)
            self.last_text_update = now

    # -------------------------------------------------------------------------
    # DESENHO NA TELA
    # -------------------------------------------------------------------------

    def draw(self, screen):
        if self.images.get('background'):
            screen.blit(self.images['background'], (0, 0))
        else:
            screen.fill((0, 0, 0))

        if not self.typewriter_started:
            self.last_text_update = pygame.time.get_ticks()
            self.shown_chars = 0
            self.typewriter_started = True

        if 'dialog_box' in self.rects:
            screen.blit(self.images['dialog_box'], self.rects['dialog_box'])

            partial_text = self.full_dialog_text[:self.shown_chars]

            self.draw_text_justified(
                screen,
                partial_text,
                self.font,
                self.text_color,
                self.rects['text_area']
            )

        if 'panel' in self.rects:
            screen.blit(self.images['panel'], self.rects['panel'])

        if 'fase_demo_noite' in self.rects:
            screen.blit(self.images['fase_demo_noite'], self.rects['fase_demo_noite'])

        # --- DESENHA A VAQUINHA ANIMADA ---
        if self.cow_frames:
            frame = self.cow_frames[self.current_cow_frame]
            screen.blit(frame, self.rects['cow'])

        if 'display_0' in self.rects:
            screen.blit(self.images['display_0'], self.rects['display_0'])

        if 'display_1' in self.rects:
            screen.blit(self.images['display_1'], self.rects['display_1'])

        self._draw_phase_zone_info(screen)

    # -------------------------------------------------------------------------
    # (O RESTANTE DO SEU CÓDIGO PERMANECE IGUAL, SEM ALTERAÇÕES)
    # -------------------------------------------------------------------------

    def draw_text_justified(self, surface, text, font, color, rect, line_spacing=1):
        words = text.split()
        space_w, _ = font.size(" ")
        lines = []
        current_line = []
        current_w = 0

        for word in words:
            word_w = font.size(word)[0]

            if current_w + word_w <= rect.width:
                current_line.append(word)
                current_w += word_w + space_w
            else:
                lines.append(current_line)
                current_line = [word]
                current_w = word_w + space_w

        if current_line:
            lines.append(current_line)

        y = rect.y
        for i, line_words in enumerate(lines):
            if i == len(lines) - 1 or len(line_words) == 1:
                line_surf = font.render(" ".join(line_words), True, color)
                surface.blit(line_surf, (rect.x, y))
            else:
                total_w = sum(font.size(w)[0] for w in line_words)
                num_spaces = len(line_words) - 1
                extra_space = (rect.width - total_w) / num_spaces if num_spaces > 0 else 0

                x = rect.x
                for word in line_words:
                    surf = font.render(word, True, color)
                    surface.blit(surf, (x, y))
                    x += surf.get_width() + extra_space

            y += font.get_linesize() + line_spacing

    def _draw_phase_zone_info(self, screen):
        # (não modificado – seu código original aqui)
        if not hasattr(self.game, 'game_controller') or not self.game.game_controller: return
        gc = self.game.game_controller
        if not hasattr(gc, 'camera') or not gc.camera: return
        camera = gc.camera
        if not hasattr(camera, 'action_handler') or not camera.action_handler: return

        action_handler = camera.action_handler
        phase_manager = action_handler.get_phase_manager()
        zone_manager = camera.zone_manager

        if not phase_manager or not zone_manager: return

        if action_handler.current_phase_id != 1:
            action_handler.set_current_phase(1)

        phase_info = phase_manager.get_current_phase_info()
        if not phase_info: return

        zones_by_name = {z["name"]: z for z in phase_info.get("zones", [])}
        zone_objects = zone_manager.get_all_zone_objects()
        validation_results = phase_manager.get_validation_results()
        show_results = phase_manager.should_show_results()

        phase_zones = ["INPUT1", "INPUT2", "GATE1", "GATE2"]

        VERDE = (0, 255, 0)
        VERMELHO = (255, 0, 0)
        PRETO_COR = (0, 0, 0)
        BRANCO_COR = (255, 255, 255)

        for zone_name in phase_zones:
            zone_config = zones_by_name.get(zone_name)
            if not zone_config: continue

            if zone_objects.get(zone_name):
                marker_pos = phase_manager.get_zone_marker_position(zone_config)
                if marker_pos:
                    m_rect = pygame.Rect(0, 0, 300, 300)
                    m_rect.center = marker_pos
                    pygame.draw.rect(screen, PRETO_COR, m_rect)

            if show_results and zone_name in validation_results:
                val = validation_results[zone_name]
                if val is not None:
                    res_pos = phase_manager.get_zone_result_position(zone_config)
                    if res_pos:
                        txt_col = VERDE if val == 1 else VERMELHO
                        txt_surf = self.result_font.render(str(val), True, txt_col)
                        txt_rect = txt_surf.get_rect(center=res_pos)

                        bg_rect = txt_rect.inflate(20, 20)
                        pygame.draw.rect(screen, PRETO_COR, bg_rect)
                        pygame.draw.rect(screen, BRANCO_COR, bg_rect, 2)
                        screen.blit(txt_surf, txt_rect)
