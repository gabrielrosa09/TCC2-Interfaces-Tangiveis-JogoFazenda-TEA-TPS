"""
Módulo de reconhecimento de gestos com MediaPipe.

Componentes principais:
- GestureCamera: Classe principal para reconhecimento de gestos
- ZoneManager: Gerencia zonas de interação
- ActionHandler: Gerencia execução de ações
- GestureProcessor: Processa gestos com MediaPipe
- VisualRenderer: Renderiza elementos visuais
- config: Configurações do sistema
"""

from .camera import GestureCamera
from .zone_manager import ZoneManager
from .action_handler import ActionHandler
from .gesture_processor import GestureProcessor
from .visual_renderer import VisualRenderer

__all__ = [
    'GestureCamera',
    'ZoneManager', 
    'ActionHandler',
    'GestureProcessor',
    'VisualRenderer'
]
