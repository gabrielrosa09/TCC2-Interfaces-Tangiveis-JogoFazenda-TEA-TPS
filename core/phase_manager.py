"""
Gerenciador de fases do jogo.
Responsável por validar a montagem do circuito e verificar se o jogador completou a fase.
"""

from typing import Dict, List, Optional, Tuple, Any
from core.circuit_logic import CircuitEvaluator


class PhaseManager:
    """Gerencia a lógica das fases do jogo."""
    
    def __init__(self):
        self.circuit_evaluator = CircuitEvaluator()
        self.current_phase = None
        self.last_validation_results = {}
        self.last_validation_errors = []
        self.show_results = False
    
    def set_phase(self, phase_config: Dict[str, Any]):
        """
        Define a fase atual.
        
        Args:
            phase_config (dict): Configuração da fase
        """
        self.current_phase = phase_config
        self.clear_validation()
    
    def clear_validation(self):
        """Limpa os resultados da validação anterior."""
        self.last_validation_results = {}
        self.last_validation_errors = []
        self.show_results = False
    
    def validate_phase(
        self,
        detected_objects: Dict[str, Optional[str]],
        object_mapping: Dict[str, str]
    ) -> Tuple[bool, str, Dict[str, Optional[int]]]:
        """
        Valida a fase atual com base nos objetos detectados.
        
        Args:
            detected_objects (dict): Dicionário {zona: objeto_detectado}
            object_mapping (dict): Mapeamento de objetos detectados para elementos do jogo
        
        Returns:
            Tuple[bool, str, Dict]: (sucesso, mensagem, valores das zonas)
        """
        if not self.current_phase:
            return False, "Nenhuma fase configurada", {}
        
        # Limpar validação anterior
        self.clear_validation()
        
        # Obter configurações da fase
        zones_config = self.current_phase.get("zones", [])
        input_values = self.current_phase.get("inputs", {})
        evaluation_order = self.current_phase.get("evaluation_order", [])
        output_zone = self.current_phase.get("output_zone", "")
        expected_value = self.current_phase.get("expected_value", None)
        
        # Avaliar o circuito (mesmo que incompleto)
        zone_values, errors = self.circuit_evaluator.evaluate_circuit(
            zones_config,
            detected_objects,
            input_values,
            object_mapping,
            evaluation_order
        )
        
        # Armazenar resultados para exibição
        self.last_validation_results = zone_values
        self.last_validation_errors = errors
        self.show_results = True
        
        # Verificar se todas as zonas têm objetos
        circuit_complete = True
        for zone in zones_config:
            zone_name = zone["name"]
            if zone_name not in detected_objects or detected_objects[zone_name] is None:
                circuit_complete = False
                break
        
        # Se circuito incompleto, retornar falha mas com valores parciais
        if not circuit_complete:
            return False, "Você ainda não conseguiu! Circuito incompleto.", zone_values
        
        # Se houver erros, a fase não foi completada
        if errors:
            error_summary = "Você ainda não conseguiu! "
            # Verificar se há objetos inválidos
            if any("não é reconhecido" in err for err in errors):
                error_summary += "Objeto inválido detectado."
            elif any("não é permitido" in err for err in errors):
                error_summary += "Objeto não permitido na zona."
            else:
                error_summary += "Verifique a montagem do circuito."
            
            return False, error_summary, zone_values
        
        # Verificar se o resultado final corresponde ao esperado
        final_output = self.circuit_evaluator.get_final_output(output_zone)
        
        if final_output is None:
            return False, "Você ainda não conseguiu! Erro ao calcular saída.", zone_values
        
        if final_output == expected_value:
            return True, "Você conseguiu!", zone_values
        else:
            return False, "Você ainda não conseguiu! Resultado incorreto.", zone_values
    
    def get_validation_results(self) -> Dict[str, Optional[int]]:
        """
        Retorna os resultados da última validação.
        
        Returns:
            Dict[str, Optional[int]]: Valores calculados para cada zona
        """
        return self.last_validation_results.copy()
    
    def should_show_results(self) -> bool:
        """
        Verifica se os resultados devem ser exibidos na tela.
        
        Returns:
            bool: True se deve mostrar resultados
        """
        return self.show_results
    
    def get_zone_result_position(self, zone_config: Dict[str, Any]) -> Optional[Tuple[int, int]]:
        """
        Obtém a posição onde o resultado deve ser exibido para uma zona.
        
        Args:
            zone_config (dict): Configuração da zona
        
        Returns:
            Optional[Tuple[int, int]]: Posição (x, y) ou None se não configurada
        """
        result_pos = zone_config.get("result_position")
        if result_pos:
            return tuple(result_pos)
        
        # Posição padrão: centro da zona
        rect = zone_config.get("rect")
        if rect:
            x1, y1, x2, y2 = rect
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            return (center_x, center_y)
        
        return None
    
    def get_zone_marker_position(self, zone_config: Dict[str, Any]) -> Optional[Tuple[int, int]]:
        """
        Obtém a posição onde o marcador de detecção deve ser exibido para uma zona.
        
        Args:
            zone_config (dict): Configuração da zona
        
        Returns:
            Optional[Tuple[int, int]]: Posição (x, y) ou None se não configurada
        """
        marker_pos = zone_config.get("marker_position")
        if marker_pos:
            return tuple(marker_pos)
        
        # Posição padrão: canto superior esquerdo da zona
        rect = zone_config.get("rect")
        if rect:
            x1, y1, x2, y2 = rect
            return (x1 + 20, y1 + 20)
        
        return None
    
    def get_current_phase_info(self) -> Optional[Dict[str, Any]]:
        """
        Retorna informações da fase atual.
        
        Returns:
            Optional[Dict]: Informações da fase ou None
        """
        return self.current_phase

