"""
Gerenciador de zonas de interação para reconhecimento de gestos.
Responsável por gerenciar as zonas ativas, detectar colisões e validar gestos.
"""

from cv.config import SCREEN_ZONES, GAME_STATES


class ZoneManager:
    """Gerencia as zonas de interação para cada tela do jogo."""
    
    def __init__(self):
        self.current_game_state = GAME_STATES["MENU"]
        self.screen_zones = SCREEN_ZONES.copy()
    
    def set_game_state(self, state):
        """
        Define o estado atual do jogo.
        
        Args:
            state (str): Estado do jogo (menu, tutorial, game)
        """
        if state in self.screen_zones:
            self.current_game_state = state
            print(f"Estado do jogo alterado para: {state}")
        else:
            print(f"Estado '{state}' não reconhecido")
    
    def get_current_zones(self):
        """
        Retorna as zonas da tela atual.
        
        Returns:
            list: Lista de zonas da tela atual
        """
        return self.screen_zones.get(self.current_game_state, [])
    
    def get_zone_for_point(self, x, y):
        """
        Verifica em qual zona (se houver) o ponto (x,y) está.
        
        Args:
            x (int): Coordenada X do ponto
            y (int): Coordenada Y do ponto
            
        Returns:
            dict or None: Zona encontrada ou None se não estiver em nenhuma zona
        """
        current_zones = self.get_current_zones()
        for zone in current_zones:
            x1, y1, x2, y2 = zone["rect"]
            if x1 <= x <= x2 and y1 <= y <= y2:
                return zone
        return None
    
    def is_gesture_valid_for_zone(self, gesture_name, zone):
        """
        Verifica se um gesto é válido para uma zona específica.
        
        Args:
            gesture_name (str): Nome do gesto
            zone (dict): Zona a ser verificada
            
        Returns:
            bool: True se o gesto é válido para a zona
        """
        if not zone or "gestures" not in zone:
            return False
        return gesture_name in zone["gestures"]
    
    def get_zone_by_name(self, zone_name):
        """
        Busca uma zona pelo nome na tela atual.
        
        Args:
            zone_name (str): Nome da zona
            
        Returns:
            dict or None: Zona encontrada ou None
        """
        current_zones = self.get_current_zones()
        for zone in current_zones:
            if zone["name"] == zone_name:
                return zone
        return None
    
    def add_zone(self, screen_state, zone):
        """
        Adiciona uma nova zona para um estado de tela.
        
        Args:
            screen_state (str): Estado da tela
            zone (dict): Dados da zona
        """
        if screen_state not in self.screen_zones:
            self.screen_zones[screen_state] = []
        self.screen_zones[screen_state].append(zone)
    
    def remove_zone(self, screen_state, zone_name):
        """
        Remove uma zona de um estado de tela.
        
        Args:
            screen_state (str): Estado da tela
            zone_name (str): Nome da zona a ser removida
        """
        if screen_state in self.screen_zones:
            self.screen_zones[screen_state] = [
                zone for zone in self.screen_zones[screen_state] 
                if zone["name"] != zone_name
            ]
    
    def get_zone_info(self, zone):
        """
        Retorna informações formatadas sobre uma zona.
        
        Args:
            zone (dict): Zona a ser analisada
            
        Returns:
            str: Informações formatadas da zona
        """
        if not zone:
            return "Zona não encontrada"
        
        gestures_text = ", ".join(zone["gestures"]) if zone["gestures"] else "Nenhum"
        x1, y1, x2, y2 = zone["rect"]
        
        return f"Zona: {zone['name']} | Posição: ({x1},{y1})-({x2},{y2}) | Gestos: {gestures_text}"
