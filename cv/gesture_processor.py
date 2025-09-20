"""
Processador de gestos para reconhecimento com MediaPipe.
Responsável por processar resultados do MediaPipe e detectar gestos válidos.
"""

import mediapipe as mp
import time
from cv.config import (
    MODEL_PATH,
    NUM_HANDS,
    MIN_HAND_DETECTION_CONFIDENCE,
    MIN_HAND_PRESENCE_CONFIDENCE,
    MIN_TRACKING_CONFIDENCE,
    SUPPORTED_GESTURES,
    GESTURE_VALIDATION_TIME,
    ACTION_COOLDOWN_TIME,
)


class GestureProcessor:
    """Processa gestos usando MediaPipe e gerencia o reconhecimento."""

    def __init__(self, zone_manager=None, action_handler=None):
        self.zone_manager = zone_manager
        self.action_handler = action_handler

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
        self.previous_gestures_state = {}

        # Rastreamento de tempo para validação de gestos
        self.gesture_start_times = (
            {}
        )  # {hand_key: (gesture_name, zone_name, start_time)}
        self.validated_gestures = (
            {}
        )  # {hand_key: (gesture_name, zone_name, validated_time)}

        # Configuração do MediaPipe
        self.recognizer = None
        self._setup_recognizer()

    def _setup_recognizer(self):
        """Configura o reconhecedor de gestos do MediaPipe."""
        options = self.GestureRecognizerOptions(
            base_options=self.BaseOptions(model_asset_path=MODEL_PATH),
            running_mode=self.VisionRunningMode.LIVE_STREAM,
            num_hands=NUM_HANDS,
            min_hand_detection_confidence=MIN_HAND_DETECTION_CONFIDENCE,
            min_hand_presence_confidence=MIN_HAND_PRESENCE_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
            result_callback=self._process_result,
        )

        self.recognizer = self.GestureRecognizer.create_from_options(options)

    def _process_result(self, result, output_image: mp.Image, timestamp_ms: int):
        """
        Callback do MediaPipe para processar resultados de gestos.

        Args:
            result: Resultado do reconhecimento de gestos
            output_image: Imagem de saída do MediaPipe
            timestamp_ms: Timestamp do frame
        """
        # Atualizar estado atual
        self.current_gestures = result.gestures
        self.current_hand_landmarks = result.hand_landmarks
        self.current_handedness = result.handedness

        # Processar cada mão detectada
        self._process_detected_hands(result)

    def _process_detected_hands(self, result):
        """Processa as mãos detectadas e executa ações se necessário."""
        current_state = {}
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

                # Processar validação de gesto com tempo
                self._process_gesture_validation(
                    gesture_name, zone_name, hand_key, current_time
                )

                # Salvar estado atual
                current_state[hand_key] = (gesture_name, zone_name)

        # Limpar rastreamento de mãos que não estão mais sendo detectadas
        self._cleanup_undetected_hands(currently_detected_hands)

        # Atualizar estado anterior
        self.previous_gestures_state = current_state.copy()

    def _cleanup_undetected_hands(self, currently_detected_hands):
        """
        Limpa o rastreamento de mãos que não estão mais sendo detectadas.

        Args:
            currently_detected_hands (set): Conjunto de mãos atualmente detectadas
        """
        # Encontrar mãos que estavam sendo rastreadas mas não estão mais detectadas
        tracked_hands = set(self.gesture_start_times.keys())
        hands_to_clean = tracked_hands - currently_detected_hands

        # Limpar rastreamento das mãos não detectadas
        for hand_key in hands_to_clean:
            self._clear_gesture_tracking(hand_key)

    def _process_gesture_validation(
        self, gesture_name, zone_name, hand_key, current_time
    ):
        """
        Processa a validação de gestos com base no tempo de detecção.

        Args:
            gesture_name (str): Nome do gesto detectado
            zone_name (str): Nome da zona onde o gesto foi detectado
            hand_key (str): Chave da mão (ex: "Left_hand")
            current_time (float): Timestamp atual
        """
        if not zone_name:
            # Se não está em uma zona válida, limpar rastreamento
            self._clear_gesture_tracking(hand_key)
            return

        current_state = (gesture_name, zone_name)

        # Verificar se o gesto mudou
        if hand_key in self.gesture_start_times:
            tracked_gesture, tracked_zone, start_time = self.gesture_start_times[
                hand_key
            ]
            tracked_state = (tracked_gesture, tracked_zone)

            if tracked_state != current_state:
                # Gesto mudou, limpar validações anteriores e reiniciar rastreamento
                self._clear_gesture_tracking(hand_key)
                self.gesture_start_times[hand_key] = (
                    gesture_name,
                    zone_name,
                    current_time,
                )
                return

        # Se é um novo gesto ou continua o mesmo
        if hand_key not in self.gesture_start_times:
            # Novo gesto detectado
            self.gesture_start_times[hand_key] = (gesture_name, zone_name, current_time)
            return

        # Verificar se o gesto foi mantido por tempo suficiente
        start_time = self.gesture_start_times[hand_key][2]
        elapsed_time = current_time - start_time

        if elapsed_time >= GESTURE_VALIDATION_TIME:
            # Gesto validado! Verificar se já foi executado
            validated_key = f"{hand_key}_{gesture_name}_{zone_name}"

            if validated_key not in self.validated_gestures:
                # Primeira vez que este gesto é validado
                self.validated_gestures[validated_key] = current_time
                self._execute_validated_gesture(gesture_name, zone_name, hand_key)
            else:
                # Gesto já foi validado recentemente, verificar cooldown
                last_validated = self.validated_gestures[validated_key]
                if current_time - last_validated >= ACTION_COOLDOWN_TIME:
                    self.validated_gestures[validated_key] = current_time
                    self._execute_validated_gesture(gesture_name, zone_name, hand_key)

    def _execute_validated_gesture(self, gesture_name, zone_name, hand_key):
        """
        Executa um gesto que foi validado por 2 segundos.

        Args:
            gesture_name (str): Nome do gesto
            zone_name (str): Nome da zona
            hand_key (str): Chave da mão
        """
        if self.action_handler and self.zone_manager:
            # Verificar se o gesto é válido para a zona
            zone = self.zone_manager.get_zone_by_name(zone_name)
            if zone and self.zone_manager.is_gesture_valid_for_zone(gesture_name, zone):
                hand_info = hand_key.replace("_hand", "")
                print(
                    f"Executando ação validada: {gesture_name} | {zone_name} | {hand_info}"
                )
                self.action_handler.execute_action(gesture_name, zone_name, hand_info)

    def _clear_gesture_tracking(self, hand_key):
        """
        Limpa o rastreamento de gestos para uma mão específica.

        Args:
            hand_key (str): Chave da mão
        """
        if hand_key in self.gesture_start_times:
            del self.gesture_start_times[hand_key]

        # Limpar gestos validados relacionados a esta mão
        keys_to_remove = [
            key for key in self.validated_gestures.keys() if key.startswith(hand_key)
        ]
        for key in keys_to_remove:
            del self.validated_gestures[key]

    def _detect_hand_zone(self, hand_landmarks):
        """
        Detecta em qual zona a mão está localizada.

        Args:
            hand_landmarks: Landmarks da mão

        Returns:
            str or None: Nome da zona ou None se não estiver em nenhuma zona
        """
        if not hand_landmarks or not self.zone_manager:
            return None

        # Usar o pulso (landmark 0) como referência
        wrist = hand_landmarks[0]
        x = int(wrist.x * 1280)  # Largura do frame
        y = int(wrist.y * 720)  # Altura do frame

        zone = self.zone_manager.get_zone_for_point(x, y)
        return zone["name"] if zone else None

    def recognize_async(self, mp_image, timestamp_ms):
        """
        Processa uma imagem de forma assíncrona.

        Args:
            mp_image: Imagem do MediaPipe
            timestamp_ms: Timestamp do frame
        """
        if self.recognizer:
            self.recognizer.recognize_async(mp_image, timestamp_ms)

    def get_current_gestures(self):
        """
        Retorna os gestos atuais detectados.

        Returns:
            list: Lista de gestos atuais
        """
        return self.current_gestures

    def get_current_hand_landmarks(self):
        """
        Retorna os landmarks das mãos atuais.

        Returns:
            list: Lista de landmarks das mãos
        """
        return self.current_hand_landmarks

    def get_current_handedness(self):
        """
        Retorna a informação de lateralidade das mãos atuais.

        Returns:
            list: Lista de informação de lateralidade
        """
        return self.current_handedness

    def cleanup(self):
        """Limpa recursos do processador."""
        if self.recognizer:
            self.recognizer.close()
            self.recognizer = None

        # Limpar rastreamento de gestos
        self.gesture_start_times.clear()
        self.validated_gestures.clear()
        self.previous_gestures_state.clear()
