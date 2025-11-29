"""
Módulo para gerenciar o filtro de cor da interface.
Controla a conversão entre modo colorido e escala de cinza.
"""

import pygame


class ColorFilter:
    """Gerencia o filtro de cor da interface do jogo."""

    def __init__(self, screen_width, screen_height, default_mode="color"):
        """Inicializa o filtro de cor."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_mode = default_mode
        
        # Superfície temporária para aplicar o filtro
        self.temp_surface = pygame.Surface((screen_width, screen_height))

    def set_mode(self, mode):
        """Define o modo de cor."""
        if mode in ["color", "grayscale"]:
            self.current_mode = mode
            mode_name = "COLORIDO" if mode == "color" else "PRETO E BRANCO"
            print(f"[COR] Modo de cor definido para: {mode_name}")
        else:
            print(f"[AVISO] Modo de cor invalido: {mode}")

    def get_mode(self):
        """Retorna o modo de cor atual."""
        return self.current_mode

    def is_grayscale(self):
        """Verifica se está em modo preto e branco."""
        return self.current_mode == "grayscale"

    def is_color(self):
        """Verifica se está em modo colorido."""
        return self.current_mode == "color"

    def apply_filter(self, screen):
        """Aplica o filtro de cor na tela."""
        if self.current_mode == "grayscale":
            # Copiar o conteúdo atual da tela
            self.temp_surface.blit(screen, (0, 0))
            
            # Converter para escala de cinza
            self._convert_to_grayscale(screen, self.temp_surface)

    def _convert_to_grayscale(self, dest_surface, source_surface):
        """Converte uma superfície para escala de cinza."""
        # Obter array de pixels
        width, height = source_surface.get_size()
        
        # Método otimizado usando pygame.transform
        # Criar uma versão em escala de cinza pixel por pixel
        for x in range(width):
            for y in range(height):
                # Obter cor do pixel
                r, g, b, a = source_surface.get_at((x, y))
                
                # Calcular valor de cinza usando fórmula ponderada
                # (mais próxima da percepção humana)
                gray = int(0.299 * r + 0.587 * g + 0.114 * b)
                
                # Definir pixel com valor de cinza
                dest_surface.set_at((x, y), (gray, gray, gray, a))

    def apply_filter_optimized(self, screen):
        """Aplica o filtro de cor na tela de forma otimizada."""
        if self.current_mode == "grayscale":
            try:
                import numpy as np
                
                # Obter array de pixels
                pixels = pygame.surfarray.array3d(screen)
                
                # Calcular escala de cinza usando fórmula ponderada
                # Fórmula: Y = 0.299*R + 0.587*G + 0.114*B
                gray = np.dot(pixels[...,:3], [0.299, 0.587, 0.114])
                
                # Expandir para RGB (mesmo valor em todos os canais)
                gray_rgb = np.zeros_like(pixels)
                gray_rgb[:,:,0] = gray
                gray_rgb[:,:,1] = gray
                gray_rgb[:,:,2] = gray
                
                # Aplicar de volta na tela
                pygame.surfarray.blit_array(screen, gray_rgb)
                
            except ImportError:
                # Se numpy não estiver disponível, usar método padrão
                print("[AVISO] NumPy nao disponivel, usando metodo padrao (mais lento)")
                self.apply_filter(screen)

    def convert_surface_to_grayscale(self, surface):
        """Converte uma superfície específica para escala de cinza."""
        width, height = surface.get_size()
        gray_surface = pygame.Surface((width, height))
        gray_surface = gray_surface.convert_alpha()
        
        for x in range(width):
            for y in range(height):
                r, g, b, a = surface.get_at((x, y))
                gray = int(0.299 * r + 0.587 * g + 0.114 * b)
                gray_surface.set_at((x, y), (gray, gray, gray, a))
        
        return gray_surface

    def reset(self):
        """Reseta o filtro para o modo colorido."""
        self.set_mode("color")

