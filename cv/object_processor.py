"""
Processador de objetos para detecção com YOLO.
Responsável por processar resultados do YOLO e detectar objetos válidos.
"""

import time
import numpy as np
from ultralytics import YOLO
from cv.base_processor import BaseRecognitionProcessor
from cv.config import (
    OBJECT_MODEL_PATH,
    MIN_OBJECT_DETECTION_CONFIDENCE,
    SUPPORTED_OBJECTS,
    CAMERA_WIDTH,
    CAMERA_HEIGHT,
)


class ObjectProcessor(BaseRecognitionProcessor):
    """Processa detecção de objetos usando YOLO e gerencia o reconhecimento."""

    def __init__(self, zone_manager=None, action_handler=None):
        super().__init__(zone_manager, action_handler, recognition_type="object")

        # Estado atual dos objetos
        self.current_detections = []

        # Configuração do YOLO
        self.detector = None
        self._setup_detector()

    def _setup_detector(self):
        """Configura o detector de objetos YOLO."""
        try:
            print(f"[YOLO] Carregando modelo: {OBJECT_MODEL_PATH}")
            self.detector = YOLO(OBJECT_MODEL_PATH)
            print("[YOLO] Modelo carregado com sucesso!")
        except Exception as e:
            print(f"[ERRO] Falha ao carregar modelo YOLO: {e}")
            self.detector = None

    def detect_sync(self, frame):
        """
        Processa uma imagem de forma síncrona usando YOLO.
        
        Args:
            frame: Frame BGR do OpenCV (numpy array)
        """
        if not self.detector:
            return

        try:
            # Executar detecção YOLO
            results = self.detector(frame, conf=MIN_OBJECT_DETECTION_CONFIDENCE, verbose=False)
            
            # Processar resultados
            if results and len(results) > 0:
                self._process_yolo_results(results[0], frame)
        except Exception as e:
            print(f"[ERRO] Erro durante detecção YOLO: {e}")

    def _process_yolo_results(self, result, frame):
        """Processa os resultados do YOLO."""
        # Limpar detecções anteriores
        self.current_detections = []
        
        # Verificar se há detecções
        if result.boxes is None or len(result.boxes) == 0:
            # Nenhum objeto detectado, limpar rastreamento
            self._cleanup_undetected_items(set())
            # Limpar objetos nas zonas
            if self.zone_manager:
                self._update_zone_objects({})
            return

        current_time = time.time()
        currently_detected_objects = set()
        
        # Rastrear objetos por zona (para zonas de fase)
        zone_object_tracking = {}

        # Processar cada detecção
        for i, box in enumerate(result.boxes):
            # Obter informações da detecção
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            xyxy = box.xyxy[0].cpu().numpy()  # [x1, y1, x2, y2]
            
            # Obter nome da classe
            object_name = result.names[class_id]
            
            # Verificar se o objeto é suportado
            if object_name not in SUPPORTED_OBJECTS:
                continue

            # Filtrar por confiança mínima (já filtrado pelo YOLO, mas verificar novamente)
            if confidence < MIN_OBJECT_DETECTION_CONFIDENCE:
                continue

            # Criar estrutura de detecção compatível
            detection = {
                'name': object_name,
                'confidence': confidence,
                'bbox': {
                    'x1': int(xyxy[0]),
                    'y1': int(xyxy[1]),
                    'x2': int(xyxy[2]),
                    'y2': int(xyxy[3]),
                    'center_x': int((xyxy[0] + xyxy[2]) / 2),
                    'center_y': int((xyxy[1] + xyxy[3]) / 2),
                }
            }
            
            self.current_detections.append(detection)

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
        if not self.zone_manager:
            return None

        # Obter coordenadas do centro do bounding box
        center_x = detection['bbox']['center_x']
        center_y = detection['bbox']['center_y']

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

    def get_current_detections(self):
        """Retorna as detecções atuais de objetos."""
        return self.current_detections

    def get_filtered_detections(self):
        """Retorna apenas as detecções de objetos suportados com confiança suficiente."""
        # Já filtrado no _process_yolo_results
        return self.current_detections

    def get_detection_info(self, detection):
        """Extrai informações de uma detecção."""
        return {
            "name": detection['name'],
            "confidence": detection['confidence'],
            "bbox": detection['bbox'],
            "zone": self._detect_object_zone(detection),
        }

    def cleanup(self):
        """Limpa recursos do processador."""
        # Limpar detecções
        self.current_detections.clear()

        # Chamar cleanup da classe base
        super().cleanup()
