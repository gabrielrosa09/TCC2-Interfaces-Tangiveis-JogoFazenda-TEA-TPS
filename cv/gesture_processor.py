"""
Processador de gestos para reconhecimento com MediaPipe.
Responsável por processar resultados do MediaPipe e detectar gestos válidos.
"""

import mediapipe as mp
import time
from cv.base_processor import BaseRecognitionProcessor
from cv.config import (
    GESTURE_MODEL_PATH,
    NUM_HANDS,
    MIN_HAND_DETECTION_CONFIDENCE,
    MIN_HAND_PRESENCE_CONFIDENCE,
    MIN_TRACKING_CONFIDENCE,
    SUPPORTED_GESTURES,
    CAMERA_WIDTH,
    CAMERA_HEIGHT,
)


class GestureProcessor(BaseRecognitionProcessor):
    """Processa gestos usando MediaPipe e gerencia o reconhecimento."""

    def __init__(self, zone_manager=None, action_handler=None):
        super().__init__(zone_manager, action_handler, recognition_type="gesture")

        # Importações do MediaPipe
        self.BaseOptions = mp.tasks.BaseOptions
        self.GestureRecognizer = mp.tasks.vision.GestureRecognizer
        self.GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
        self.GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
        self.VisionRunningMode = mp.tasks.vision.RunningMode

        # Estado atual dos gestos
        self.current_gestures = []
        self.current_hand_landmarks = []
        self.current_handedness = []

        # Configuração do MediaPipe
        self.recognizer = None
        self._setup_recognizer()

    def _setup_recognizer(self):
        """Configura o reconhecedor de gestos do MediaPipe."""
        options = self.GestureRecognizerOptions(
            base_options=self.BaseOptions(model_asset_path=GESTURE_MODEL_PATH),
            running_mode=self.VisionRunningMode.LIVE_STREAM,
            num_hands=NUM_HANDS,
            min_hand_detection_confidence=MIN_HAND_DETECTION_CONFIDENCE,
            min_hand_presence_confidence=MIN_HAND_PRESENCE_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
            result_callback=self._process_result,
        )

        self.recognizer = self.GestureRecognizer.create_from_options(options)

    def _process_result(self, result, output_image: mp.Image, timestamp_ms: int):
        """Callback do MediaPipe para processar resultados de gestos."""
        # Atualizar estado atual
        self.current_gestures = result.gestures
        self.current_hand_landmarks = result.hand_landmarks
        self.current_handedness = result.handedness

        # Processar cada mão detectada
        self._process_detected_hands(result)

    def _process_detected_hands(self, result):
        """Processa as mãos detectadas e executa ações se necessário."""
        current_time = time.time()
        currently_detected_hands = set()

        for i, gesture_list in enumerate(result.gestures):
            if gesture_list and result.handedness and result.handedness[i]:
                # Obter informações do gesto e mão
                top_gesture = gesture_list[0]
                gesture_name = top_gesture.category_name
                hand_info = result.handedness[i][0].category_name
                hand_key = f"{hand_info}_hand"
                currently_detected_hands.add(hand_key)

                # Verificar se o gesto é suportado
                if gesture_name not in SUPPORTED_GESTURES:
                    continue

                # Detectar zona onde a mão está
                zone_name = self._detect_hand_zone(result.hand_landmarks[i])

                # Processar validação de gesto com tempo (usando método da classe base)
                self._process_recognition_validation(
                    gesture_name, zone_name, hand_key, current_time
                )

        # Limpar rastreamento de mãos que não estão mais sendo detectadas
        self._cleanup_undetected_items(currently_detected_hands)

    def _detect_hand_zone(self, hand_landmarks):
        """Detecta em qual zona a mão está localizada."""
        if not hand_landmarks or not self.zone_manager:
            return None

        # Usar o pulso (landmark 0) como referência
        wrist = hand_landmarks[0]
        x = int(wrist.x * CAMERA_WIDTH)  # Largura do frame
        y = int(wrist.y * CAMERA_HEIGHT)  # Altura do frame

        zone = self.zone_manager.get_zone_for_point(x, y)
        return zone["name"] if zone else None

    def recognize_async(self, mp_image, timestamp_ms):
        """Processa uma imagem de forma assíncrona."""
        if self.recognizer:
            self.recognizer.recognize_async(mp_image, timestamp_ms)

    def get_current_gestures(self):
        """Retorna os gestos atuais detectados."""
        return self.current_gestures

    def get_current_hand_landmarks(self):
        """Retorna os landmarks das mãos atuais."""
        return self.current_hand_landmarks

    def get_current_handedness(self):
        """Retorna a informação de lateralidade das mãos atuais."""
        return self.current_handedness

    def cleanup(self):
        """Limpa recursos do processador."""
        if self.recognizer:
            self.recognizer.close()
            self.recognizer = None

        # Chamar cleanup da classe base
        super().cleanup()
