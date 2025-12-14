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

        # Carregar todos os displays de valores (INPUT1 e INPUT2)
        self.images['val_inf_display_0'] = self._load_sprite("assets/images/final_images/val_inf_Display_0.png")
        self.images['val_inf_display_1'] = self._load_sprite("assets/images/final_images/val_inf_Display_1.png")
        self.images['val_inf_display_vazio'] = self._load_sprite("assets/images/final_images/val_inf_Display_Vazio.png")
        
        self.images['val_sup_display_0'] = self._load_sprite("assets/images/final_images/val_sup_Display_0.png")
        self.images['val_sup_display_1'] = self._load_sprite("assets/images/final_images/val_sup_Display_1.png")
        self.images['val_sup_display_vazio'] = self._load_sprite("assets/images/final_images/val_sup_Display_Vazio.png")
        
        # Carregar displays das portas lógicas (GATE1 e GATE2)
        self.images['portaLog_display_0'] = self._load_sprite("assets/images/final_images/portaLog_Display_0.png")
        self.images['portaLog_display_1'] = self._load_sprite("assets/images/final_images/portaLog_Display_1.png")
        self.images['portaLog_display_vazio'] = self._load_sprite("assets/images/final_images/portaLog_Display_Vazio.png")
        
        self.images['portaNot_display_0'] = self._load_sprite("assets/images/final_images/portaNot_Display_0.png")
        self.images['portaNot_display_1'] = self._load_sprite("assets/images/final_images/portaNot_Display_1.png")
        self.images['portaNot_display_vazio'] = self._load_sprite("assets/images/final_images/portaNot_Display_Vazio.png")

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
        
        # INPUT1 (superior) - val_sup
        if self.images.get('val_sup_display_vazio'):
            r = self.images['val_sup_display_vazio'].get_rect()
            self.rects['INPUT1_display'] = r
        
        # INPUT2 (inferior) - val_inf
        if self.images.get('val_inf_display_vazio'):
            r = self.images['val_inf_display_vazio'].get_rect()
            self.rects['INPUT2_display'] = r
        
        # GATE1 (porta AND) - portaLog
        if self.images.get('portaLog_display_vazio'):
            r = self.images['portaLog_display_vazio'].get_rect()
            self.rects['GATE1_display'] = r
        
        # GATE2 (porta NOT) - portaNot
        if self.images.get('portaNot_display_vazio'):
            r = self.images['portaNot_display_vazio'].get_rect()
            self.rects['GATE2_display'] = r

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

        action_handler = self._get_action_handler()
        
        # Atualizar valores dos displays continuamente
        if action_handler:
            action_handler.update_display_values()
        
        if action_handler and action_handler.new_feedback_available:
            # Pega o texto
            new_msg = action_handler.ui_feedback_text
            # Atualiza a dialog box
            self.set_dialog_text(new_msg)
            # Baixa a flag para não atualizar repetidamente
            action_handler.new_feedback_available = False

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

        # Desenhar displays dinâmicos baseados nos valores calculados
        self._draw_dynamic_displays(screen)

        # Desenhar grade de 5x5 pixels para facilitar posicionamento
        # self._draw_grid(screen)

        self._draw_phase_zone_info(screen)

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

        for zone_name in phase_zones:
            zone_config = zones_by_name.get(zone_name)
            if not zone_config: continue

            detected_obj = zone_objects.get(zone_name)
            if detected_obj:
                marker_pos = phase_manager.get_zone_marker_position(zone_config)
                if marker_pos:
                    m_rect = pygame.Rect(0, 0, 26, 26)
                    m_rect.center = marker_pos
                    pygame.draw.rect(screen, BRANCO, m_rect)

            # if show_results and zone_name in validation_results:
            #     val = validation_results[zone_name]
            #     if val is not None:
            #         res_pos = phase_manager.get_zone_result_position(zone_config)
            #         if res_pos:
            #             txt_col = VERDE if val == 1 else VERMELHO
            #             txt_surf = self.result_font.render(str(val), True, txt_col)
            #             txt_rect = txt_surf.get_rect(center=res_pos)

            #             bg_rect = txt_rect.inflate(20, 20)
            #             pygame.draw.rect(screen, PRETO, bg_rect)
            #             pygame.draw.rect(screen, BRANCO, bg_rect, 2)
            #             screen.blit(txt_surf, txt_rect)

    def set_dialog_text(self, new_text):
        """Reinicia a animação de texto com uma nova mensagem."""
        self.full_dialog_text = new_text
        self.shown_chars = 0
        self.last_text_update = pygame.time.get_ticks()
        self.typewriter_started = False

    def _draw_grid(self, screen):
        """Desenha uma grade de 5x5 pixels para facilitar posicionamento."""
        grid_color = (100, 100, 100)  # Cinza escuro
        grid_color_10 = (150, 150, 150)  # Cinza mais claro para linhas de 10 em 10
        
        # Linhas verticais
        for x in range(0, LARGURA, 5):
            color = grid_color_10 if x % 10 == 0 else grid_color
            thickness = 1 if x % 10 == 0 else 1
            pygame.draw.line(screen, color, (x, 0), (x, ALTURA), thickness)
        
        # Linhas horizontais
        for y in range(0, ALTURA, 5):
            color = grid_color_10 if y % 10 == 0 else grid_color
            thickness = 1 if y % 10 == 0 else 1
            pygame.draw.line(screen, color, (0, y), (LARGURA, y), thickness)
        
        # Desenhar números nas coordenadas principais (a cada 20 pixels)
        font = pygame.font.SysFont("arial", 8)
        for x in range(0, LARGURA, 20):
            text = font.render(str(x), True, (255, 255, 0))
            screen.blit(text, (x + 2, 2))
        
        for y in range(20, ALTURA, 20):
            text = font.render(str(y), True, (255, 255, 0))
            screen.blit(text, (2, y + 2))

    def _get_action_handler(self):
        """Recupera o action_handler de forma segura."""
        if hasattr(self.game, 'game_controller') and self.game.game_controller:
            if hasattr(self.game.game_controller, 'camera') and self.game.game_controller.camera:
                return self.game.game_controller.camera.action_handler
        return None
    
    def _draw_dynamic_displays(self, screen):
        """Desenha os displays com os valores dinâmicos calculados pelo circuito."""
        action_handler = self._get_action_handler()
        if not action_handler:
            # Se não há action_handler, desenha displays vazios
            self._draw_empty_displays(screen)
            return
        
        phase_manager = action_handler.get_phase_manager()
        if not phase_manager:
            self._draw_empty_displays(screen)
            return
        
        # Obter valores calculados das zonas
        zone_values = phase_manager.get_validation_results()
        
        # Mapeamento de zonas para tipos de display
        display_mapping = {
            'INPUT1': 'val_sup',      # Display superior (INPUT1)
            'INPUT2': 'val_inf',      # Display inferior (INPUT2)
            'GATE1': 'portaLog',      # Display da porta lógica (AND)
            'GATE2': 'portaNot',      # Display da porta NOT
        }
        
        # Desenhar cada display baseado no valor calculado
        for zone_name, display_prefix in display_mapping.items():
            rect_key = f'{zone_name}_display'
            
            if rect_key not in self.rects:
                continue
            
            # Obter o valor da zona
            value = zone_values.get(zone_name)
            
            # Selecionar o asset correto baseado no valor
            if value is None:
                # Sem valor calculado = display vazio
                image_key = f'{display_prefix}_display_vazio'
            elif value == 0:
                # Valor 0
                image_key = f'{display_prefix}_display_0'
            elif value == 1:
                # Valor 1
                image_key = f'{display_prefix}_display_1'
            else:
                # Valor inválido = display vazio
                image_key = f'{display_prefix}_display_vazio'
            
            # Desenhar o display se a imagem existir
            if image_key in self.images:
                screen.blit(self.images[image_key], self.rects[rect_key])
    
    def _draw_empty_displays(self, screen):
        """Desenha todos os displays vazios (quando não há valores calculados)."""
        empty_displays = [
            ('INPUT1_display', 'val_sup_display_vazio'),
            ('INPUT2_display', 'val_inf_display_vazio'),
            ('GATE1_display', 'portaLog_display_vazio'),
            ('GATE2_display', 'portaNot_display_vazio'),
        ]
        
        for rect_key, image_key in empty_displays:
            if rect_key in self.rects and image_key in self.images:
                screen.blit(self.images[image_key], self.rects[rect_key])
