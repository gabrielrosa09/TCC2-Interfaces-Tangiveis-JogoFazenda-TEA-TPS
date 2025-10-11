"""
Processador de objetos para detecção com MediaPipe.
Responsável por processar resultados do MediaPipe e detectar objetos válidos.
"""

import mediapipe as mp
import time
from cv.base_processor import BaseRecognitionProcessor
from cv.config import (
    OBJECT_MODEL_PATH,
    MAX_OBJECT_RESULTS,
    MIN_OBJECT_DETECTION_CONFIDENCE,
    SUPPORTED_OBJECTS,
    CAMERA_WIDTH,
    CAMERA_HEIGHT,
)


class ObjectProcessor(BaseRecognitionProcessor):
    """Processa detecção de objetos usando MediaPipe e gerencia o reconhecimento."""

    def __init__(self, zone_manager=None, action_handler=None):
        super().__init__(zone_manager, action_handler, recognition_type="object")

        # Importações do MediaPipe
        self.BaseOptions = mp.tasks.BaseOptions
        self.ObjectDetector = mp.tasks.vision.ObjectDetector
        self.ObjectDetectorOptions = mp.tasks.vision.ObjectDetectorOptions
        self.VisionRunningMode = mp.tasks.vision.RunningMode

        # Estado atual dos objetos
        self.current_detections = []

        # Configuração do MediaPipe
        self.detector = None
        self._setup_detector()

    def _setup_detector(self):
        """Configura o detector de objetos do MediaPipe."""
        options = self.ObjectDetectorOptions(
            base_options=self.BaseOptions(model_asset_path=OBJECT_MODEL_PATH),
            running_mode=self.VisionRunningMode.LIVE_STREAM,
            max_results=MAX_OBJECT_RESULTS,
            result_callback=self._process_result,
        )

        self.detector = self.ObjectDetector.create_from_options(options)

    def _process_result(self, result, output_image: mp.Image, timestamp_ms: int):
        """
        Callback do MediaPipe para processar resultados de detecção.

        Args:
            result: Resultado da detecção de objetos
            output_image: Imagem de saída do MediaPipe
            timestamp_ms: Timestamp do frame
        """
        # Atualizar estado atual
        self.current_detections = result.detections

        # Processar cada objeto detectado
        self._process_detected_objects(result)

    def _process_detected_objects(self, result):
        """Processa os objetos detectados e executa ações se necessário."""
        current_time = time.time()
        currently_detected_objects = set()

        for i, detection in enumerate(result.detections):
            # Obter categoria e confiança
            if detection.categories:
                category = detection.categories[0]
                object_name = category.category_name
                confidence = category.score

                # Verificar se o objeto é suportado
                if object_name not in SUPPORTED_OBJECTS:
                    continue

                # Filtrar por confiança mínima
                if confidence < MIN_OBJECT_DETECTION_CONFIDENCE:
                    continue

                # Criar chave única para o objeto
                object_key = f"{object_name}_{i}"
                currently_detected_objects.add(object_key)

                # Detectar zona onde o objeto está
                zone_name = self._detect_object_zone(detection)

                # Processar validação de objeto com tempo
                self._process_recognition_validation(
                    object_name, zone_name, object_key, current_time, confidence
                )

        # Limpar rastreamento de objetos que não estão mais sendo detectados
        self._cleanup_undetected_items(currently_detected_objects)

    def _detect_object_zone(self, detection):
        """
        Detecta em qual zona o objeto está localizado.

        Args:
            detection: Detecção do objeto com bounding box

        Returns:
            str or None: Nome da zona ou None se não estiver em nenhuma zona
        """
        if not detection.bounding_box or not self.zone_manager:
            return None

        # Obter coordenadas do centro do bounding box
        bbox = detection.bounding_box
        center_x = int(bbox.origin_x + bbox.width / 2)
        center_y = int(bbox.origin_y + bbox.height / 2)

        zone = self.zone_manager.get_zone_for_point(center_x, center_y)
        return zone["name"] if zone else None

    def detect_async(self, mp_image, timestamp_ms):
        """
        Processa uma imagem de forma assíncrona.

        Args:
            mp_image: Imagem do MediaPipe
            timestamp_ms: Timestamp do frame
        """
        if self.detector:
            self.detector.detect_async(mp_image, timestamp_ms)

    def get_current_detections(self):
        """
        Retorna as detecções atuais de objetos.

        Returns:
            list: Lista de detecções atuais
        """
        return self.current_detections

    def get_filtered_detections(self):
        """
        Retorna apenas as detecções de objetos suportados com confiança suficiente.

        Returns:
            list: Lista de detecções filtradas
        """
        filtered = []
        for detection in self.current_detections:
            if detection.categories:
                category = detection.categories[0]
                object_name = category.category_name
                confidence = category.score

                if (
                    object_name in SUPPORTED_OBJECTS
                    and confidence >= MIN_OBJECT_DETECTION_CONFIDENCE
                ):
                    filtered.append(detection)
        return filtered

    def get_detection_info(self, detection):
        """
        Extrai informações de uma detecção.

        Args:
            detection: Detecção do MediaPipe

        Returns:
            dict: Informações da detecção (nome, confiança, bbox, zona)
        """
        if not detection.categories:
            return None

        category = detection.categories[0]
        bbox = detection.bounding_box

        return {
            "name": category.category_name,
            "confidence": category.score,
            "bbox": {
                "x": int(bbox.origin_x),
                "y": int(bbox.origin_y),
                "width": int(bbox.width),
                "height": int(bbox.height),
            },
            "zone": self._detect_object_zone(detection),
        }

    def cleanup(self):
        """Limpa recursos do processador."""
        if self.detector:
            self.detector.close()
            self.detector = None

        # Limpar detecções
        self.current_detections.clear()

        # Chamar cleanup da classe base
        super().cleanup()

