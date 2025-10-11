"""
Processador base para reconhecimento (gestos e objetos).
Contém lógica comum de validação de tempo e rastreamento.
"""

import time
from cv.config import RECOGNITION_VALIDATION_TIME, ACTION_COOLDOWN_TIME


class BaseRecognitionProcessor:
    """
    Classe base para processamento de reconhecimento.
    Unifica a lógica de validação temporal para gestos e objetos.
    """

    def __init__(self, zone_manager=None, action_handler=None, recognition_type="unknown"):
        """
        Inicializa o processador base.

        Args:
            zone_manager: Gerenciador de zonas
            action_handler: Gerenciador de ações
            recognition_type: Tipo de reconhecimento ("gesture" ou "object")
        """
        self.zone_manager = zone_manager
        self.action_handler = action_handler
        self.recognition_type = recognition_type

        # Rastreamento de tempo para validação
        self.recognition_start_times = (
            {}
        )  # {key: (name, zone_name, start_time)}
        self.validated_recognitions = (
            {}
        )  # {key: (name, zone_name, validated_time)}

        # Estado anterior
        self.previous_state = {}

    def _process_recognition_validation(
        self, recognition_name, zone_name, item_key, current_time, confidence=1.0
    ):
        """
        Processa a validação de reconhecimento com base no tempo de detecção.

        Args:
            recognition_name (str): Nome do gesto/objeto detectado
            zone_name (str): Nome da zona onde foi detectado
            item_key (str): Chave do item (ex: "Left_hand" ou "cup_1")
            current_time (float): Timestamp atual
            confidence (float): Confiança da detecção (0-1)
        """
        if not zone_name:
            # Se não está em uma zona válida, limpar rastreamento
            self._clear_recognition_tracking(item_key)
            return

        current_state = (recognition_name, zone_name)

        # Verificar se o reconhecimento mudou
        if item_key in self.recognition_start_times:
            tracked_name, tracked_zone, start_time = self.recognition_start_times[
                item_key
            ]
            tracked_state = (tracked_name, tracked_zone)

            if tracked_state != current_state:
                # Reconhecimento mudou, limpar validações anteriores e reiniciar
                self._clear_recognition_tracking(item_key)
                self.recognition_start_times[item_key] = (
                    recognition_name,
                    zone_name,
                    current_time,
                )
                return

        # Se é um novo reconhecimento ou continua o mesmo
        if item_key not in self.recognition_start_times:
            # Novo reconhecimento detectado
            self.recognition_start_times[item_key] = (
                recognition_name,
                zone_name,
                current_time,
            )
            return

        # Verificar se o reconhecimento foi mantido por tempo suficiente
        start_time = self.recognition_start_times[item_key][2]
        elapsed_time = current_time - start_time

        if elapsed_time >= RECOGNITION_VALIDATION_TIME:
            # Reconhecimento validado! Verificar se já foi executado
            validated_key = f"{item_key}_{recognition_name}_{zone_name}"

            if validated_key not in self.validated_recognitions:
                # Primeira vez que este reconhecimento é validado
                self.validated_recognitions[validated_key] = current_time
                self._execute_validated_recognition(
                    recognition_name, zone_name, item_key, confidence
                )
            else:
                # Reconhecimento já foi validado recentemente, verificar cooldown
                last_validated = self.validated_recognitions[validated_key]
                if current_time - last_validated >= ACTION_COOLDOWN_TIME:
                    self.validated_recognitions[validated_key] = current_time
                    self._execute_validated_recognition(
                        recognition_name, zone_name, item_key, confidence
                    )

    def _execute_validated_recognition(
        self, recognition_name, zone_name, item_key, confidence=1.0
    ):
        """
        Executa um reconhecimento que foi validado.

        Args:
            recognition_name (str): Nome do gesto/objeto
            zone_name (str): Nome da zona
            item_key (str): Chave do item
            confidence (float): Confiança da detecção
        """
        if self.action_handler and self.zone_manager:
            # Verificar se o reconhecimento é válido para a zona
            zone = self.zone_manager.get_zone_by_name(zone_name)
            if zone and self.zone_manager.is_recognition_valid_for_zone(
                recognition_name, zone, self.recognition_type
            ):
                print(
                    f"Executando ação validada ({self.recognition_type}): {recognition_name} | {zone_name} | {item_key} | Confiança: {confidence:.2f}"
                )
                self.action_handler.execute_action(
                    recognition_name, zone_name, item_key, self.recognition_type
                )

    def _clear_recognition_tracking(self, item_key):
        """
        Limpa o rastreamento de reconhecimentos para um item específico.

        Args:
            item_key (str): Chave do item
        """
        if item_key in self.recognition_start_times:
            del self.recognition_start_times[item_key]

        # Limpar reconhecimentos validados relacionados a este item
        keys_to_remove = [
            key
            for key in self.validated_recognitions.keys()
            if key.startswith(item_key)
        ]
        for key in keys_to_remove:
            del self.validated_recognitions[key]

    def _cleanup_undetected_items(self, currently_detected_items):
        """
        Limpa o rastreamento de itens que não estão mais sendo detectados.

        Args:
            currently_detected_items (set): Conjunto de itens atualmente detectados
        """
        # Encontrar itens que estavam sendo rastreados mas não estão mais detectados
        tracked_items = set(self.recognition_start_times.keys())
        items_to_clean = tracked_items - currently_detected_items

        # Limpar rastreamento dos itens não detectados
        for item_key in items_to_clean:
            self._clear_recognition_tracking(item_key)

    def get_validation_progress(self, item_key):
        """
        Retorna o progresso de validação de um item (0.0 a 1.0).

        Args:
            item_key (str): Chave do item

        Returns:
            float: Progresso de validação (0.0 a 1.0)
        """
        if item_key not in self.recognition_start_times:
            return 0.0

        start_time = self.recognition_start_times[item_key][2]
        elapsed_time = time.time() - start_time
        progress = min(elapsed_time / RECOGNITION_VALIDATION_TIME, 1.0)
        return progress

    def cleanup(self):
        """Limpa recursos do processador."""
        # Limpar rastreamento
        self.recognition_start_times.clear()
        self.validated_recognitions.clear()
        self.previous_state.clear()

