"""
Renderizador visual para o sistema de reconhecimento de gestos.
Responsável por desenhar zonas, landmarks e informações na tela.
"""

import cv2
from cv.config import (
    LANDMARK_RADIUS,
    LANDMARK_COLOR,
    CONNECTION_THICKNESS,
    CONNECTION_COLOR,
    ZONE_THICKNESS,
    TEXT_FONT,
    TEXT_THICKNESS,
)


class VisualRenderer:
    """Renderiza elementos visuais para o reconhecimento de gestos."""

    def __init__(self, zone_manager=None, action_handler=None):
        self.zone_manager = zone_manager
        self.action_handler = action_handler

    def render_frame(
        self,
        frame,
        gestures,
        hand_landmarks,
        handedness,
        game_state,
        object_detections=None,
    ):
        """Renderiza um frame completo com todas as informações visuais."""
        height, width, _ = frame.shape

        # Desenhar zonas
        self._draw_zones(frame)

        # Desenhar informações do estado
        self._draw_state_info(frame, game_state)

        # Desenhar mãos e gestos
        if gestures and hand_landmarks:
            self._draw_hands_and_gestures(frame, gestures, hand_landmarks, handedness)

        # Desenhar detecções de objetos
        if object_detections:
            self._draw_object_detections(frame, object_detections)

        return frame

    def _draw_zones(self, frame):
        """Desenha as zonas de interação na tela."""
        if not self.zone_manager:
            return

        current_zones = self.zone_manager.get_current_zones()

        for zone in current_zones:
            x1, y1, x2, y2 = zone["rect"]
            color = zone["color"]

            # Desenhar retângulo da zona
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, ZONE_THICKNESS)

            # Desenhar nome da zona
            cv2.putText(
                frame,
                zone["name"],
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                TEXT_FONT,
                color,
                TEXT_THICKNESS,
            )

            # Desenhar gestos aceitos na zona
            gestures_text = ", ".join(zone["gestures"])
            if gestures_text:
                cv2.putText(
                    frame,
                    f"Gestos: {gestures_text}",
                    (x1, y2 + 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    color,
                    1,
                )

            # Desenhar objetos aceitos na zona
            objects_text = ", ".join(zone["objects"])
            if objects_text:
                cv2.putText(
                    frame,
                    f"Objetos: {objects_text}",
                    (x1, y2 + 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    color,
                    1,
                )

    def _draw_state_info(self, frame, game_state):
        """Desenha informações do estado atual do jogo."""
        # Desenhar estado atual
        cv2.putText(
            frame,
            f"Tela: {game_state.upper()}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            TEXT_THICKNESS,
        )

    def _draw_hands_and_gestures(self, frame, gestures, hand_landmarks, handedness):
        """Desenha landmarks das mãos e informações dos gestos."""
        height, width, _ = frame.shape

        for i, (gesture_list, landmarks_list, handedness_list) in enumerate(
            zip(gestures, hand_landmarks, handedness)
        ):

            if gesture_list and landmarks_list:
                # Desenhar landmarks da mão
                self._draw_hand_landmarks(frame, landmarks_list, width, height)

                # Desenhar conexões entre landmarks
                self._draw_hand_connections(frame, landmarks_list, width, height)

                # Desenhar informações do gesto
                self._draw_gesture_info(
                    frame, gesture_list, handedness_list, landmarks_list, width, height
                )

    def _draw_hand_landmarks(self, frame, landmarks_list, width, height):
        """Desenha os pontos (landmarks) da mão."""
        for landmark in landmarks_list:
            x = int(landmark.x * width)
            y = int(landmark.y * height)
            cv2.circle(frame, (x, y), LANDMARK_RADIUS, LANDMARK_COLOR, -1)

    def _draw_hand_connections(self, frame, landmarks_list, width, height):
        """Desenha as conexões entre os landmarks da mão."""
        # Definir conexões dos dedos
        connections = [
            # Polegar
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 4),
            # Indicador
            (0, 5),
            (5, 6),
            (6, 7),
            (7, 8),
            # Médio
            (0, 9),
            (9, 10),
            (10, 11),
            (11, 12),
            # Anelar
            (0, 13),
            (13, 14),
            (14, 15),
            (15, 16),
            # Mindinho
            (0, 17),
            (17, 18),
            (18, 19),
            (19, 20),
        ]

        for connection in connections:
            if connection[0] < len(landmarks_list) and connection[1] < len(
                landmarks_list
            ):

                start_point = landmarks_list[connection[0]]
                end_point = landmarks_list[connection[1]]

                start_x = int(start_point.x * width)
                start_y = int(start_point.y * height)
                end_x = int(end_point.x * width)
                end_y = int(end_point.y * height)

                cv2.line(
                    frame,
                    (start_x, start_y),
                    (end_x, end_y),
                    CONNECTION_COLOR,
                    CONNECTION_THICKNESS,
                )

    def _draw_gesture_info(
        self, frame, gesture_list, handedness_list, landmarks_list, width, height
    ):
        """Desenha informações do gesto detectado."""
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
        self._draw_text_with_background(
            frame, text, (text_x, text_y), TEXT_FONT, (255, 255, 255), TEXT_THICKNESS
        )

    def _draw_text_with_background(
        self,
        frame,
        text,
        position,
        font_scale,
        text_color,
        thickness,
        bg_color=(0, 0, 0),
    ):
        """Desenha texto com fundo colorido."""
        x, y = position

        # Calcular tamanho do texto
        (text_width, text_height), baseline = cv2.getTextSize(
            text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness
        )

        # Desenhar background
        cv2.rectangle(
            frame, (x, y - text_height - 10), (x + text_width, y + 5), bg_color, -1
        )

        # Desenhar texto
        cv2.putText(
            frame,
            text,
            position,
            cv2.FONT_HERSHEY_SIMPLEX,
            font_scale,
            text_color,
            thickness,
        )

    def _draw_object_detections(self, frame, detections):
        """Desenha bounding boxes e labels dos objetos detectados."""
        # Cores para diferentes objetos (BGR)
        colors = [
            (0, 255, 0),  # Verde
            (255, 0, 0),  # Vermelho
            (0, 0, 255),  # Azul
            (255, 255, 0),  # Ciano
            (255, 0, 255),  # Magenta
            (0, 255, 255),  # Amarelo
        ]

        for detection in detections:
            if not detection.categories:
                continue

            # Obter categoria e confiança
            category = detection.categories[0]
            label = category.category_name
            confidence = category.score

            # Obter coordenadas do bounding box
            bbox = detection.bounding_box
            x = int(bbox.origin_x)
            y = int(bbox.origin_y)
            width = int(bbox.width)
            height = int(bbox.height)

            # Coordenadas do retângulo
            x1, y1 = x, y
            x2, y2 = x + width, y + height

            # Escolher cor baseada no hash do label
            color = colors[hash(label) % len(colors)]

            # Desenhar retângulo
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            # Preparar texto do label
            text = f"{label}: {confidence:.2f}"

            # Desenhar texto com background
            self._draw_text_with_background(
                frame,
                text,
                (x1, y1 - 5),
                0.6,
                (255, 255, 255),
                2,
                bg_color=color,
            )
