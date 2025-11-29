"""
Módulo para gerenciar a sobreposição de brilho da tela.
Controla uma camada preta semi-transparente sobre toda a interface.
"""

import pygame


class BrightnessOverlay:
    """Gerencia a sobreposição de brilho da tela do jogo."""

    def __init__(self, screen_width, screen_height, default_opacity=0):
        """Inicializa o overlay de brilho."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.opacity = default_opacity

        # Criar a superfície preta que será usada como overlay
        self.overlay_surface = pygame.Surface((screen_width, screen_height))
        self.overlay_surface.fill((0, 0, 0))  # Preto
        self.overlay_surface.set_alpha(self.opacity)

    def set_opacity(self, opacity):
        """Define a opacidade do overlay."""
        # Garantir que o valor está no intervalo válido
        self.opacity = max(0, min(255, opacity))
        self.overlay_surface.set_alpha(self.opacity)
        print(f"[BRILHO] Opacidade do overlay definida para: {self.opacity}/255")

    def get_opacity(self):
        """Retorna a opacidade atual do overlay."""
        return self.opacity

    def get_brightness_percentage(self):
        """Retorna o percentual de brilho atual."""
        # Brilho é o inverso da opacidade
        return ((255 - self.opacity) / 255) * 100

    def draw(self, screen):
        """Desenha o overlay na tela."""
        if self.opacity > 0:
            screen.blit(self.overlay_surface, (0, 0))

    def reset(self):
        """Reseta o overlay para a opacidade padrão (0)."""
        self.set_opacity(0)

