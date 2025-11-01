"""
Módulo para gerenciar a sobreposição de brilho da tela.
Controla uma camada preta semi-transparente sobre toda a interface.
"""

import pygame


class BrightnessOverlay:
    """Gerencia a sobreposição de brilho da tela do jogo."""

    def __init__(self, screen_width, screen_height, default_opacity=0):
        """
        Inicializa o overlay de brilho.

        Args:
            screen_width (int): Largura da tela
            screen_height (int): Altura da tela
            default_opacity (int): Opacidade inicial (0-255, onde 0 é transparente e 255 é opaco)
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.opacity = default_opacity

        # Criar a superfície preta que será usada como overlay
        self.overlay_surface = pygame.Surface((screen_width, screen_height))
        self.overlay_surface.fill((0, 0, 0))  # Preto
        self.overlay_surface.set_alpha(self.opacity)

    def set_opacity(self, opacity):
        """
        Define a opacidade do overlay.

        Args:
            opacity (int): Valor de opacidade (0-255)
                          0 = totalmente transparente (100% brilho)
                          255 = totalmente opaco (0% brilho)
        """
        # Garantir que o valor está no intervalo válido
        self.opacity = max(0, min(255, opacity))
        self.overlay_surface.set_alpha(self.opacity)
        print(f"🔆 Opacidade do overlay definida para: {self.opacity}/255")

    def get_opacity(self):
        """
        Retorna a opacidade atual do overlay.

        Returns:
            int: Valor de opacidade atual (0-255)
        """
        return self.opacity

    def get_brightness_percentage(self):
        """
        Retorna o percentual de brilho atual.

        Returns:
            float: Percentual de brilho (0-100)
        """
        # Brilho é o inverso da opacidade
        return ((255 - self.opacity) / 255) * 100

    def draw(self, screen):
        """
        Desenha o overlay na tela.

        Args:
            screen (pygame.Surface): Superfície da tela onde o overlay será desenhado
        """
        if self.opacity > 0:
            screen.blit(self.overlay_surface, (0, 0))

    def reset(self):
        """Reseta o overlay para a opacidade padrão (0)."""
        self.set_opacity(0)

