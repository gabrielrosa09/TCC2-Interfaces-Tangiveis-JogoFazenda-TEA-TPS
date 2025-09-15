"""
Processador de gestos para reconhecimento com MediaPipe.
Responsável por processar resultados do MediaPipe e detectar gestos válidos.
"""

import mediapipe as mp
from cv.config import (
    MODEL_PATH, NUM_HANDS, MIN_HAND_DETECTION_CONFIDENCE,
    MIN_HAND_PRESENCE_CONFIDENCE, MIN_TRACKING_CONFIDENCE,
    SUPPORTED_GESTURES
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
            result_callback=self._process_result
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
        
        for i, gesture_list in enumerate(result.gestures):
            if gesture_list and result.handedness and result.handedness[i]:
                # Obter informações do gesto e mão
                top_gesture = gesture_list[0]
                gesture_name = top_gesture.category_name
                hand_info = result.handedness[i][0].category_name
                hand_key = f"{hand_info}_hand"
                
                # Verificar se o gesto é suportado
                if gesture_name not in SUPPORTED_GESTURES:
                    continue
                
                # Detectar zona onde a mão está
                zone_name = self._detect_hand_zone(result.hand_landmarks[i])
                
                # Verificar se deve executar ação
                if self._should_execute_action(gesture_name, zone_name, hand_key):
                    if self.action_handler and self.zone_manager:
                        # Verificar se o gesto é válido para a zona
                        zone = self.zone_manager.get_zone_by_name(zone_name)
                        if zone and self.zone_manager.is_gesture_valid_for_zone(gesture_name, zone):
                            print(f"Executando ação: {gesture_name} | {zone_name} | {hand_info}")
                            self.action_handler.execute_action(gesture_name, zone_name, hand_info)
                
                # Salvar estado atual
                current_state[hand_key] = (gesture_name, zone_name)
        
        # Atualizar estado anterior
        self.previous_gestures_state = current_state.copy()
    
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
        y = int(wrist.y * 720)   # Altura do frame
        
        zone = self.zone_manager.get_zone_for_point(x, y)
        return zone["name"] if zone else None
    
    def _should_execute_action(self, gesture_name, zone_name, hand_key):
        """
        Verifica se deve executar uma ação baseada no estado anterior.
        
        Args:
            gesture_name (str): Nome do gesto
            zone_name (str): Nome da zona
            hand_key (str): Chave da mão
            
        Returns:
            bool: True se deve executar ação
        """
        if not zone_name:
            return False
        
        # Verificar se o estado mudou (evita repetições)
        previous_state = self.previous_gestures_state.get(hand_key)
        current_state = (gesture_name, zone_name)
        
        return previous_state != current_state
    
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
    
    def get_gesture_info(self, hand_index=0):
        """
        Retorna informações detalhadas sobre um gesto específico.
        
        Args:
            hand_index (int): Índice da mão (0 ou 1)
            
        Returns:
            dict or None: Informações do gesto ou None se não encontrado
        """
        if (hand_index < len(self.current_gestures) and 
            self.current_gestures[hand_index] and 
            hand_index < len(self.current_handedness) and 
            self.current_handedness[hand_index]):
            
            gesture = self.current_gestures[hand_index][0]
            handedness = self.current_handedness[hand_index][0]
            
            return {
                "gesture_name": gesture.category_name,
                "confidence": gesture.score,
                "hand": handedness.category_name,
                "zone": self._detect_hand_zone(self.current_hand_landmarks[hand_index])
            }
        
        return None
    
    def cleanup(self):
        """Limpa recursos do processador."""
        if self.recognizer:
            self.recognizer.close()
            self.recognizer = None
