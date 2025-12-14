"""
Gerenciador de fontes do jogo.
Controla o tamanho e tipo de fonte usado em todo o jogo.
"""

import pygame


class FontManager:
    """Gerencia as fontes do jogo."""

    def __init__(self):
        """Inicializa o gerenciador de fontes com a fonte padrão."""
        self.current_font_name = None
        self.current_font = None
        self.current_font_config = None
        
        # Carregar fonte padrão
        self._load_default_font()

    def _load_default_font(self):
        """Carrega a fonte padrão do jogo."""
        from cv.config import DEFAULT_FONT_OBJECT, FONT_SIZES
        
        if DEFAULT_FONT_OBJECT in FONT_SIZES:
            font_config = FONT_SIZES[DEFAULT_FONT_OBJECT]
            self.set_font(DEFAULT_FONT_OBJECT, font_config)
        else:
            # Fallback para fonte do sistema
            print("[AVISO] Fonte padrão não encontrada, usando fonte do sistema")
            self.current_font = pygame.font.SysFont("arial", 12)
            self.current_font_name = "system_fallback"
            self.current_font_config = {
                "path": None,
                "size": 12,
                "description": "Fonte do sistema (fallback)"
            }

    def set_font(self, font_name, font_config):
        """
        Define a fonte atual do jogo.
        
        Args:
            font_name: Nome identificador da fonte (ex: "medium_font", "large_font")
            font_config: Dicionário com configurações da fonte:
                - path: Caminho para o arquivo da fonte
                - size: Tamanho da fonte em pixels
                - description: Descrição da fonte
        """
        try:
            # Carregar a fonte
            font_path = font_config.get("path")
            font_size = font_config.get("size", 12)
            
            if font_path:
                new_font = pygame.font.Font(font_path, font_size)
                self.current_font = new_font
                self.current_font_name = font_name
                self.current_font_config = font_config
                print(f"[FONTE] Fonte carregada: {font_config.get('description', font_name)}")
            else:
                print(f"[AVISO] Caminho da fonte não especificado para '{font_name}'")
        except Exception as e:
            print(f"[ERRO] Falha ao carregar fonte '{font_name}': {e}")
            # Manter fonte atual em caso de erro

    def get_font(self):
        """
        Retorna o objeto pygame.font.Font atual.
        
        Returns:
            pygame.font.Font: Fonte atual do jogo
        """
        return self.current_font

    def get_current_font(self):
        """
        Retorna o nome da fonte atual.
        
        Returns:
            str: Nome identificador da fonte atual
        """
        return self.current_font_name

    def get_font_config(self):
        """
        Retorna a configuração da fonte atual.
        
        Returns:
            dict: Configuração da fonte atual
        """
        return self.current_font_config

    def get_font_size(self):
        """
        Retorna o tamanho da fonte atual.
        
        Returns:
            int: Tamanho da fonte em pixels
        """
        if self.current_font_config:
            return self.current_font_config.get("size", 12)
        return 12

    def get_line_spacing(self):
        """
        Retorna o espaçamento entre linhas da fonte atual.
        
        Returns:
            int: Espaçamento entre linhas em pixels
        """
        if self.current_font_config:
            return self.current_font_config.get("line_spacing", 1)
        return 1

