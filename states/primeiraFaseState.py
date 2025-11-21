import pygame
from config import *

class Fase1State:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font("assets/fonts/vcr.ttf", 60)
        self.result_font = pygame.font.Font("assets/fonts/vcr.ttf", 120)  # Fonte maior para resultados

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
