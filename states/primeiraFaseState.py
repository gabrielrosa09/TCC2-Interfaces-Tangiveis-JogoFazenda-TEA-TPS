import pygame
from config import *

class Fase1State:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font("assets/fonts/MinecraftStandard.otf", 30)
        self.result_font = pygame.font.Font("assets/fonts/MinecraftStandard.otf", 60)

        self.dialog_text = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                            "Nunc odio tellus, congue eget orci sed, convallis "
                            "tincidunt magna. Donec ut libero sed ante dignissim "
                            "aliquet interdum a tellus. Etiam imperdiet sapien quis "
                            "nulla dapibus, at venenatis elit aliquam. Nunc nec "
                            "autor risus.")
        self.text_color = (89, 86, 82)

        try:

            self.background_image = pygame.image.load("assets/images/background.gif").convert()

            self.background_image = pygame.transform.scale(self.background_image, (LARGURA, ALTURA))

            self.dialog_box_image = pygame.image.load("assets/images/caixa_Dialogo.gif").convert_alpha()

            scale = 7.65
            w = int(self.dialog_box_image.get_width() * scale)
            h = int(self.dialog_box_image.get_height() * scale)
            self.dialog_box_image = pygame.transform.scale(self.dialog_box_image, (w, h))

            # Painel de status (com "Dia" e "Com Vento")
            self.panel_image = pygame.image.load("assets/images/painel_dia_comVento.gif").convert_alpha()

            scale = 7.7
            w = int(self.panel_image.get_width() * scale)
            h = int(self.panel_image.get_height() * scale)
            self.panel_image = pygame.transform.scale(self.panel_image, (w, h))

            # Retrato da vaca (para colocar sobre o painel)
            self.cow_portrait_image = pygame.image.load("assets/images/vaca_dia_comVento.gif").convert_alpha()

            scale = 7.75
            w = int(self.cow_portrait_image.get_width() * scale)
            h = int(self.cow_portrait_image.get_height() * scale)
            self.cow_portrait_image = pygame.transform.scale(self.cow_portrait_image, (w, h))

            # Displays de lógica (0 e 1)
            self.display_0_image = pygame.image.load("assets/images/display_0.gif").convert_alpha()
            scale = 7.8
            w = int(self.display_0_image.get_width() * scale)
            h = int(self.display_0_image.get_height() * scale)
            self.display_0_image = pygame.transform.scale(self.display_0_image, (w, h))

            self.display_1_image = pygame.image.load("assets/images/display_1.gif").convert_alpha()
            scale = 7.8
            w = int(self.display_1_image.get_width() * scale)
            h = int(self.display_1_image.get_height() * scale)
            self.display_1_image = pygame.transform.scale(self.display_1_image, (w, h))

        except pygame.error as e:
            print(f"Erro ao carregar uma ou mais imagens: {e}")
            self.background_image = None

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.game.state_manager.set_state("menu")

    def update(self):
        pass

    def draw_text_justified(self, surface, text, font, color, rect, line_spacing=0):
        """
        Desenha texto dentro de um rect com alinhamento JUSTIFICADO.
        Última linha é alinhada à esquerda.
        """
        words = text.split()
        space_width, space_height = font.size(" ")
        lines = []
        current_line = []

        for word in words:
            test_line = " ".join(current_line + [word])
            if font.size(test_line)[0] <= rect.width:
                current_line.append(word)
            else:
                lines.append(current_line)
                current_line = [word]

        if current_line:
            lines.append(current_line)

        y = rect.y

        for i, line_words in enumerate(lines):

            if i == len(lines) - 1:
                line_text = " ".join(line_words)
                surface.blit(font.render(line_text, True, color), (rect.x, y))
                y += font.get_linesize() + line_spacing
                continue

            line_text = " ".join(line_words)
            total_words_width = sum(font.size(w)[0] for w in line_words)
            total_spaces = len(line_words) - 1

            if total_spaces > 0:
                extra_space = (rect.width - total_words_width) // total_spaces
            else:
                extra_space = 0

            x = rect.x
            for j, word in enumerate(line_words):
                surface.blit(font.render(word, True, color), (x, y))
                word_width = font.size(word)[0]

                x += word_width + space_width + extra_space

            y += font.get_linesize() + line_spacing

    def draw(self, screen):
        # Desenhar fundo
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        else:
            screen.fill(PRETO)

        # Desenhar marcadores e resultados das zonas de fase
        self._draw_phase_zone_info(screen)

    def _draw_phase_zone_info(self, screen):
        """
        Desenha marcadores de detecção e resultados para zonas de fase na interface do jogo.

        Args:
            screen: Superfície do Pygame onde desenhar
        """
        # Tentar acessar o phase_manager através do game_controller
        try:
            # Acessar através do game -> game_controller (se existir)
            if not hasattr(self.game, 'game_controller') or not self.game.game_controller:
                return

            game_controller = self.game.game_controller

            # Acessar câmera e action_handler
            if not hasattr(game_controller, 'camera') or not game_controller.camera:
                return

            camera = game_controller.camera

            if not hasattr(camera, 'action_handler') or not camera.action_handler:
                return

            action_handler = camera.action_handler
            phase_manager = action_handler.get_phase_manager()
            zone_manager = camera.zone_manager

            if not phase_manager or not zone_manager:
                return

            # Carregar fase 1 se ainda não foi carregada
            if action_handler.current_phase_id != 1:
                action_handler.set_current_phase(1)

            # Obter configuração da fase atual
            phase_info = phase_manager.get_current_phase_info()
            if not phase_info:
                return

            zones_config = phase_info.get("zones", [])
            zones_by_name = {zone["name"]: zone for zone in zones_config}

            # Obter objetos detectados
            zone_objects = zone_manager.get_all_zone_objects()

            # Obter resultados da validação
            validation_results = phase_manager.get_validation_results()
            show_results = phase_manager.should_show_results()

            # Zonas de fase
            phase_zones = ["INPUT1", "INPUT2", "GATE1", "GATE2"]

            # Desenhar para cada zona de fase
            for zone_name in phase_zones:
                zone_config = zones_by_name.get(zone_name)
                if not zone_config:
                    continue

                # Desenhar marcador de detecção (quadrado preto)
                detected_object = zone_objects.get(zone_name)
                if detected_object:
                    marker_pos = phase_manager.get_zone_marker_position(zone_config)
                    if marker_pos:
                        # Desenhar quadrado preto preenchido (300x300 pixels)
                        marker_rect = pygame.Rect(marker_pos[0], marker_pos[1], 300, 300)
                        pygame.draw.rect(screen, PRETO, marker_rect)

                # Desenhar resultado (1 ou 0) se validação foi executada
                if show_results and zone_name in validation_results:
                    result_value = validation_results[zone_name]
                    if result_value is not None:
                        result_pos = phase_manager.get_zone_result_position(zone_config)
                        if result_pos:
                            # Desenhar o valor (1 ou 0) em fonte grande
                            result_text = str(result_value)

                            # Cor: verde para 1, vermelho para 0
                            text_color = VERDE if result_value == 1 else VERMELHO

                            # Renderizar texto
                            text_surface = self.result_font.render(result_text, True, text_color)
                            text_rect = text_surface.get_rect(center=result_pos)

                            # Desenhar fundo preto para contraste
                            bg_rect = text_rect.inflate(20, 20)
                            pygame.draw.rect(screen, PRETO, bg_rect)
                            pygame.draw.rect(screen, BRANCO, bg_rect, 2)

                            # Desenhar texto
                            screen.blit(text_surface, text_rect)

        except Exception as e:
            # Silenciosamente ignorar erros (fase ainda não inicializada, etc.)
            pass

        if self.dialog_box_image:
            screen.blit(self.dialog_box_image, (10, 10))

            # (x, y, largura, altura) - com uma margem interna
            padding_x = 40
            padding_y = 15
            text_rect = pygame.Rect(
                20 + padding_x,
                20 + padding_y,
                self.dialog_box_image.get_width() - (padding_x * 2),
                self.dialog_box_image.get_height() - (padding_y * 2)
            )

            self.draw_text_justified(screen, self.dialog_text, self.font, self.text_color, text_rect)

        # Painel de status
        if self.panel_image:
            screen.blit(self.panel_image, (10, 420))

        # Retrato da vaca
        if self.cow_portrait_image:
            screen.blit(self.cow_portrait_image, (41, 450))

        # Display '0'
        if self.display_0_image:
            screen.blit(self.display_0_image, (740, 525))

        # Display '1'
        if self.display_1_image:
            screen.blit(self.display_1_image, (740, 915))

    def render_pixel_text(self, text, font, color, scale_factor):
        # Renderiza no tamanho original da fonte
        surf = font.render(text, True, color)

        # Expande sem suavizar (pixel-perfect)
        w = surf.get_width() * scale_factor
        h = surf.get_height() * scale_factor
        return pygame.transform.scale(surf, (w, h))
