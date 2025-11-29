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
        """Callback do MediaPipe para processar resultados de detecção."""
        # Atualizar estado atual
        self.current_detections = result.detections

        # Processar cada objeto detectado
        self._process_detected_objects(result)

    def _process_detected_objects(self, result):
        """Processa os objetos detectados e executa ações se necessário."""
        current_time = time.time()
        currently_detected_objects = set()
        
        # Rastrear objetos por zona (para zonas de fase)
        zone_object_tracking = {}

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
                
                if zone_name:
                    # Rastrear objeto por zona
                    if zone_name not in zone_object_tracking:
                        zone_object_tracking[zone_name] = []
                    zone_object_tracking[zone_name].append({
                        "name": object_name,
                        "confidence": confidence,
                        "key": object_key
                    })

                # Processar validação de objeto com tempo
                self._process_recognition_validation(
                    object_name, zone_name, object_key, current_time, confidence
                )
        
        # Atualizar objetos detectados nas zonas (para zonas de fase)
        if self.zone_manager:
            self._update_zone_objects(zone_object_tracking)

        # Limpar rastreamento de objetos que não estão mais sendo detectados
        self._cleanup_undetected_items(currently_detected_objects)

    def _detect_object_zone(self, detection):
        """Detecta em qual zona o objeto está localizado."""
        if not detection.bounding_box or not self.zone_manager:
            return None

        # Obter coordenadas do centro do bounding box
        bbox = detection.bounding_box
        center_x = int(bbox.origin_x + bbox.width / 2)
        center_y = int(bbox.origin_y + bbox.height / 2)

        zone = self.zone_manager.get_zone_for_point(center_x, center_y)
        return zone["name"] if zone else None
    
    def _update_zone_objects(self, zone_object_tracking):
        """Atualiza os objetos detectados em cada zona no zone_manager. Para zonas de fase (INPUT1, INPUT2, GATE1, GATE2), apenas rastreia sem executar ações."""
        # Zonas de fase (não executam ações imediatas)
        phase_zones = ["INPUT1", "INPUT2", "GATE1", "GATE2"]
        
        # Obter todas as zonas atuais
        current_zones = self.zone_manager.get_current_zones()
        zone_names = [zone["name"] for zone in current_zones]
        
        # Atualizar objetos nas zonas
        for zone_name in zone_names:
            if zone_name in phase_zones:
                # Para zonas de fase, rastrear o objeto mais confiante
                if zone_name in zone_object_tracking:
                    # Pegar o objeto com maior confiança
                    objects = zone_object_tracking[zone_name]
                    best_object = max(objects, key=lambda x: x["confidence"])
                    self.zone_manager.update_zone_object(zone_name, best_object["name"])
                else:
                    # Nenhum objeto detectado nesta zona
                    self.zone_manager.update_zone_object(zone_name, None)

    def detect_async(self, mp_image, timestamp_ms):
        """Processa uma imagem de forma assíncrona."""
        if self.detector:
            self.detector.detect_async(mp_image, timestamp_ms)

    def get_current_detections(self):
        """Retorna as detecções atuais de objetos."""
        return self.current_detections

    def get_filtered_detections(self):
        """Retorna apenas as detecções de objetos suportados com confiança suficiente."""
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
        """Extrai informações de uma detecção."""
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

