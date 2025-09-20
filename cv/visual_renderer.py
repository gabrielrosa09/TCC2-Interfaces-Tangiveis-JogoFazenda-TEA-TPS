"""
Renderizador visual para o sistema de reconhecimento de gestos.
Responsável por desenhar zonas, landmarks e informações na tela.
"""

import cv2
from cv.config import (
    LANDMARK_RADIUS, LANDMARK_COLOR, CONNECTION_THICKNESS, CONNECTION_COLOR,
    ZONE_THICKNESS, TEXT_FONT, TEXT_THICKNESS
)


class VisualRenderer:
    """Renderiza elementos visuais para o reconhecimento de gestos."""
    
    def __init__(self, zone_manager=None):
        self.zone_manager = zone_manager
    
    def render_frame(self, frame, gestures, hand_landmarks, handedness, game_state):
        """
        Renderiza um frame completo com todas as informações visuais.
        
        Args:
            frame: Frame da câmera
            gestures: Lista de gestos detectados
            hand_landmarks: Lista de landmarks das mãos
            handedness: Lista de lateralidade das mãos
            game_state: Estado atual do jogo
            
        Returns:
            numpy.ndarray: Frame renderizado
        """
        height, width, _ = frame.shape
        
        # Desenhar zonas
        self._draw_zones(frame, game_state)
        
        # Desenhar informações do estado
        self._draw_state_info(frame, game_state)
        
        # Desenhar mãos e gestos
        if gestures and hand_landmarks:
            self._draw_hands_and_gestures(frame, gestures, hand_landmarks, handedness)
        
        return frame
    
    def _draw_zones(self, frame, game_state):
        """
        Desenha as zonas de interação na tela.
        
        Args:
            frame: Frame da câmera
            game_state: Estado atual do jogo
        """
        if not self.zone_manager:
            return
        
        current_zones = self.zone_manager.get_current_zones()
        
        for zone in current_zones:
            x1, y1, x2, y2 = zone["rect"]
            color = zone["color"]
            
            # Desenhar retângulo da zona
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, ZONE_THICKNESS)
            
            # Desenhar nome da zona
            cv2.putText(frame, zone["name"], (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, TEXT_FONT, color, TEXT_THICKNESS)
            
            # Desenhar gestos aceitos na zona
            gestures_text = ", ".join(zone["gestures"]) if zone["gestures"] else "Nenhum"
            cv2.putText(frame, f"Gestos: {gestures_text}", (x1, y2 + 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    
    def _draw_state_info(self, frame, game_state):
        """
        Desenha informações do estado atual do jogo.
        
        Args:
            frame: Frame da câmera
            game_state: Estado atual do jogo
        """
        # Desenhar estado atual
        cv2.putText(frame, f"Tela: {game_state.upper()}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), TEXT_THICKNESS)
    
    def _draw_hands_and_gestures(self, frame, gestures, hand_landmarks, handedness):
        """
        Desenha landmarks das mãos e informações dos gestos.
        
        Args:
            frame: Frame da câmera
            gestures: Lista de gestos detectados
            hand_landmarks: Lista de landmarks das mãos
            handedness: Lista de lateralidade das mãos
        """
        height, width, _ = frame.shape
        
        for i, (gesture_list, landmarks_list, handedness_list) in enumerate(
            zip(gestures, hand_landmarks, handedness)):
            
            if gesture_list and landmarks_list:
                # Desenhar landmarks da mão
                self._draw_hand_landmarks(frame, landmarks_list, width, height)
                
                # Desenhar conexões entre landmarks
                self._draw_hand_connections(frame, landmarks_list, width, height)
                
                # Desenhar informações do gesto
                self._draw_gesture_info(frame, gesture_list, handedness_list, 
                                      landmarks_list, width, height)
    
    def _draw_hand_landmarks(self, frame, landmarks_list, width, height):
        """
        Desenha os pontos (landmarks) da mão.
        
        Args:
            frame: Frame da câmera
            landmarks_list: Lista de landmarks da mão
            width: Largura do frame
            height: Altura do frame
        """
        for landmark in landmarks_list:
            x = int(landmark.x * width)
            y = int(landmark.y * height)
            cv2.circle(frame, (x, y), LANDMARK_RADIUS, LANDMARK_COLOR, -1)
    
    def _draw_hand_connections(self, frame, landmarks_list, width, height):
        """
        Desenha as conexões entre os landmarks da mão.
        
        Args:
            frame: Frame da câmera
            landmarks_list: Lista de landmarks da mão
            width: Largura do frame
            height: Altura do frame
        """
        # Definir conexões dos dedos
        connections = [
            # Polegar
            (0, 1), (1, 2), (2, 3), (3, 4),
            # Indicador
            (0, 5), (5, 6), (6, 7), (7, 8),
            # Médio
            (0, 9), (9, 10), (10, 11), (11, 12),
            # Anelar
            (0, 13), (13, 14), (14, 15), (15, 16),
            # Mindinho
            (0, 17), (17, 18), (18, 19), (19, 20)
        ]
        
        for connection in connections:
            if (connection[0] < len(landmarks_list) and 
                connection[1] < len(landmarks_list)):
                
                start_point = landmarks_list[connection[0]]
                end_point = landmarks_list[connection[1]]
                
                start_x = int(start_point.x * width)
                start_y = int(start_point.y * height)
                end_x = int(end_point.x * width)
                end_y = int(end_point.y * height)
                
                cv2.line(frame, (start_x, start_y), (end_x, end_y), 
                        CONNECTION_COLOR, CONNECTION_THICKNESS)
    
    def _draw_gesture_info(self, frame, gesture_list, handedness_list, 
                          landmarks_list, width, height):
        """
        Desenha informações do gesto detectado.
        
        Args:
            frame: Frame da câmera
            gesture_list: Lista de gestos
            handedness_list: Lista de lateralidade
            landmarks_list: Lista de landmarks
            width: Largura do frame
            height: Altura do frame
        """
        if not gesture_list or not landmarks_list:
            return
        
        # Obter informações do gesto
        top_gesture = gesture_list[0]
        gesture_name = top_gesture.category_name
        confidence = top_gesture.score
        
        # Obter informação da mão
        hand_label = handedness_list[0].category_name if handedness_list else "Unknown"
        
        # Calcular posição para o texto (próximo ao pulso)
        wrist = landmarks_list[0]  # Landmark 0 é o pulso
        text_x = int(wrist.x * width)
        text_y = int(wrist.y * height) - 30
        
        # Preparar texto do gesto
        text = f"{hand_label}: {gesture_name} ({confidence:.2f})"
        
        # Desenhar texto com background
        self._draw_text_with_background(frame, text, (text_x, text_y), 
                                      TEXT_FONT, (255, 255, 255), TEXT_THICKNESS)
    
    def _draw_text_with_background(self, frame, text, position, font_scale, 
                                 text_color, thickness, bg_color=(0, 0, 0)):
        """
        Desenha texto com fundo colorido.
        
        Args:
            frame: Frame onde desenhar
            text: Texto a desenhar
            position: Posição (x, y) do texto
            font_scale: Escala da fonte
            text_color: Cor do texto
            thickness: Espessura do texto
            bg_color: Cor do fundo
        """
        x, y = position
        
        # Calcular tamanho do texto
        (text_width, text_height), baseline = cv2.getTextSize(
            text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
        
        # Desenhar background
        cv2.rectangle(frame, (x, y - text_height - 10), 
                     (x + text_width, y + 5), bg_color, -1)
        
        # Desenhar texto
        cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, 
                   font_scale, text_color, thickness)

    def draw_zone_highlight(self, frame, zone_name, color=(0, 255, 255)):
        """
        Destaca uma zona específica.
        
        Args:
            frame: Frame da câmera
            zone_name: Nome da zona a destacar
            color: Cor do destaque
        """
        if not self.zone_manager:
            return
        
        zone = self.zone_manager.get_zone_by_name(zone_name)
        if zone:
            x1, y1, x2, y2 = zone["rect"]
            # Desenhar retângulo destacado
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 4)
    
    def draw_custom_text(self, frame, text, position, color=(255, 255, 255), 
                        font_scale=0.7, thickness=2):
        """
        Desenha texto personalizado no frame.
        
        Args:
            frame: Frame da câmera
            text: Texto a desenhar
            position: Posição (x, y) do texto
            color: Cor do texto
            font_scale: Escala da fonte
            thickness: Espessura do texto
        """
        cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, 
                   font_scale, color, thickness)
    
    def draw_custom_rectangle(self, frame, rect, color, thickness=2):
        """
        Desenha um retângulo personalizado no frame.
        
        Args:
            frame: Frame da câmera
            rect: Tupla (x1, y1, x2, y2) do retângulo
            color: Cor do retângulo
            thickness: Espessura das linhas
        """
        x1, y1, x2, y2 = rect
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
