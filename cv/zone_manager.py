"""
Gerenciador de zonas de interação para reconhecimento de gestos.
Responsável por gerenciar as zonas ativas, detectar colisões e validar gestos.
"""

from cv.config import SCREEN_ZONES, GAME_STATES
from typing import Dict, Optional


class ZoneManager:
    """Gerencia as zonas de interação para cada tela do jogo."""

    def __init__(self):
        self.current_game_state = GAME_STATES["CUTSCENE1"]
        self.screen_zones = SCREEN_ZONES.copy()
        # Rastrear objetos detectados em cada zona (para zonas de fase)
        self.zone_objects: Dict[str, Optional[str]] = {}

    def set_game_state(self, state):
        """Define o estado atual do jogo."""
        if state in self.screen_zones:
            self.current_game_state = state
            # Limpar objetos detectados ao trocar de estado
            self.zone_objects.clear()
            print(f"Estado do jogo alterado para: {state}")
        else:
            print(f"Estado '{state}' não reconhecido")

    def get_current_zones(self):
        """Retorna as zonas da tela atual."""
        return self.screen_zones.get(self.current_game_state, [])

    def get_zone_for_point(self, x, y):
        """Verifica em qual zona (se houver) o ponto (x,y) está."""
        current_zones = self.get_current_zones()
        for zone in current_zones:
            x1, y1, x2, y2 = zone["rect"]
            if x1 <= x <= x2 and y1 <= y <= y2:
                return zone
        return None

    def is_gesture_valid_for_zone(self, gesture_name, zone):
        """Verifica se um gesto é válido para uma zona específica."""
        if not zone or "gestures" not in zone:
            return False
        return gesture_name in zone["gestures"]

    def is_object_valid_for_zone(self, object_name, zone):
        """Verifica se um objeto é válido para uma zona específica."""
        if not zone or "objects" not in zone:
            return False
        return object_name in zone["objects"]

    def is_recognition_valid_for_zone(self, recognition_name, zone, recognition_type):
        """Verifica se um reconhecimento (gesto ou objeto) é válido para uma zona."""
        if recognition_type == "gesture":
            return self.is_gesture_valid_for_zone(recognition_name, zone)
        elif recognition_type == "object":
            return self.is_object_valid_for_zone(recognition_name, zone)
        return False

    def get_zone_by_name(self, zone_name):
        """Busca uma zona pelo nome na tela atual."""
        current_zones = self.get_current_zones()
        for zone in current_zones:
            if zone["name"] == zone_name:
                return zone
        return None
    
    def update_zone_object(self, zone_name: str, object_name: Optional[str]):
        """Atualiza o objeto detectado em uma zona."""
        self.zone_objects[zone_name] = object_name
    
    def get_zone_object(self, zone_name: str) -> Optional[str]:
        """Obtém o objeto detectado em uma zona."""
        return self.zone_objects.get(zone_name)
    
    def get_all_zone_objects(self) -> Dict[str, Optional[str]]:
        """Retorna todos os objetos detectados nas zonas."""
        return self.zone_objects.copy()
    
    def clear_zone_objects(self):
        """Limpa todos os objetos detectados nas zonas."""
        self.zone_objects.clear()
