"""
Módulo de reconhecimento de gestos e objetos com MediaPipe.

Componentes principais:
- GestureCamera: Classe principal para reconhecimento de gestos e objetos
- ZoneManager: Gerencia zonas de interação
- ActionHandler: Gerencia execução de ações
- GestureProcessor: Processa gestos com MediaPipe
- ObjectProcessor: Processa detecção de objetos com MediaPipe
- BaseRecognitionProcessor: Classe base para processadores de reconhecimento
- VisualRenderer: Renderiza elementos visuais
- config: Configurações do sistema
"""

from .camera import GestureCamera
from .zone_manager import ZoneManager
from .action_handler import ActionHandler
from .gesture_processor import GestureProcessor
from .object_processor import ObjectProcessor
from .base_processor import BaseRecognitionProcessor
from .visual_renderer import VisualRenderer

__all__ = [
    'GestureCamera',
    'ZoneManager', 
    'ActionHandler',
    'GestureProcessor',
    'ObjectProcessor',
    'BaseRecognitionProcessor',
    'VisualRenderer'
]
