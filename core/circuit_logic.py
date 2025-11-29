"""
Módulo de lógica de circuitos booleanos para o jogo.
Define as portas lógicas e a lógica de avaliação de circuitos.
"""

from typing import Dict, List, Optional, Tuple, Any


class Gate:
    """Classe base para portas lógicas."""
    
    def __init__(self, name: str):
        self.name = name
        self.inputs: List[Optional[int]] = []
    
    def evaluate(self) -> Optional[int]:
        """
        Avalia a porta lógica com base nos inputs.
        
        Returns:
            Optional[int]: Resultado da avaliação (0, 1) ou None se inputs inválidos
        """
        raise NotImplementedError("Subclasses devem implementar evaluate()")
    
    def set_inputs(self, *inputs: Optional[int]):
        """Define os inputs da porta."""
        self.inputs = list(inputs)
    
    def has_valid_inputs(self) -> bool:
        """Verifica se todos os inputs são válidos (0 ou 1)."""
        return all(inp in [0, 1] for inp in self.inputs)


class AndGate(Gate):
    """Porta lógica AND."""
    
    def __init__(self):
        super().__init__("AND")
    
    def evaluate(self) -> Optional[int]:
        """Avalia AND: retorna 1 apenas se todos os inputs forem 1."""
        if not self.inputs or not self.has_valid_inputs():
            return None
        
        return 1 if all(inp == 1 for inp in self.inputs) else 0


class OrGate(Gate):
    """Porta lógica OR."""
    
    def __init__(self):
        super().__init__("OR")
    
    def evaluate(self) -> Optional[int]:
        """Avalia OR: retorna 1 se pelo menos um input for 1."""
        if not self.inputs or not self.has_valid_inputs():
            return None
        
        return 1 if any(inp == 1 for inp in self.inputs) else 0


class NotGate(Gate):
    """Porta lógica NOT."""
    
    def __init__(self):
        super().__init__("NOT")
    
    def evaluate(self) -> Optional[int]:
        """Avalia NOT: inverte o input."""
        if len(self.inputs) != 1 or not self.has_valid_inputs():
            return None
        
        return 1 if self.inputs[0] == 0 else 0


class CircuitEvaluator:
    """Avaliador de circuitos booleanos."""
    
    # Mapeamento de tipos de portas para classes
    GATE_TYPES = {
        "and_gate": AndGate,
        "or_gate": OrGate,
        "not_gate": NotGate,
    }
    
    def __init__(self):
        self.zone_values: Dict[str, Optional[int]] = {}
        self.zone_objects: Dict[str, Optional[str]] = {}
    
    def create_gate(self, gate_type: str) -> Optional[Gate]:
        """Cria uma porta lógica baseada no tipo."""
        gate_class = self.GATE_TYPES.get(gate_type)
        if gate_class:
            return gate_class()
        return None
    
    def evaluate_zone(
        self,
        zone_name: str,
        zone_config: Dict[str, Any],
        detected_object: Optional[str],
        input_values: Dict[str, int],
        object_mapping: Dict[str, str]
    ) -> Tuple[Optional[int], bool, str]:
        """Avalia uma zona específica do circuito."""
        # Verificar se há objeto detectado
        if not detected_object:
            return None, False, f"Zona {zone_name} está vazia"
        
        # Mapear objeto detectado para elemento do jogo
        game_element = object_mapping.get(detected_object)
        if not game_element:
            return None, False, f"Objeto '{detected_object}' não é reconhecido pelo jogo"
        
        # Verificar se o elemento é permitido nesta zona (mas continuar calculando)
        allowed_elements = zone_config.get("allowed_elements", [])
        is_allowed = game_element in allowed_elements
        
        # Se for um input, retornar o valor do contexto
        if game_element in ["solar_input", "wind_input"]:
            input_key = "solar" if game_element == "solar_input" else "eolico"
            value = input_values.get(input_key)
            if value is None:
                return None, False, f"Valor do input '{input_key}' não definido"
            # Retornar valor calculado, mas marcar se não é permitido
            error_msg = "" if is_allowed else f"Elemento '{game_element}' não é permitido na zona {zone_name}"
            return value, is_allowed, error_msg
        
        # Se for uma porta lógica, avaliar baseado nas conexões
        if game_element in self.GATE_TYPES:
            # Obter as zonas de entrada (conexões)
            input_zones = zone_config.get("inputs", [])
            if not input_zones:
                return None, False, f"Zona {zone_name} não tem inputs definidos"
            
            # Coletar valores dos inputs
            input_vals = []
            for input_zone in input_zones:
                if input_zone not in self.zone_values:
                    return None, False, f"Input '{input_zone}' ainda não foi avaliado"
                
                val = self.zone_values[input_zone]
                if val is None:
                    return None, False, f"Input '{input_zone}' tem valor inválido"
                
                input_vals.append(val)
            
            # Criar e avaliar a porta
            gate = self.create_gate(game_element)
            if not gate:
                return None, False, f"Tipo de porta '{game_element}' inválido"
            
            gate.set_inputs(*input_vals)
            result = gate.evaluate()
            
            if result is None:
                return None, False, f"Erro ao avaliar porta {game_element} na zona {zone_name}"
            
            # Retornar valor calculado, mas marcar se não é permitido
            error_msg = "" if is_allowed else f"Elemento '{game_element}' não é permitido na zona {zone_name}"
            return result, is_allowed, error_msg
        
        return None, False, f"Elemento '{game_element}' não é um input nem uma porta válida"
    
    def evaluate_circuit(
        self,
        zones_config: List[Dict[str, Any]],
        detected_objects: Dict[str, Optional[str]],
        input_values: Dict[str, int],
        object_mapping: Dict[str, str],
        evaluation_order: List[str]
    ) -> Tuple[Dict[str, Optional[int]], List[str]]:
        """Avalia todo o circuito seguindo a ordem de avaliação."""
        self.zone_values = {}
        self.zone_objects = detected_objects.copy()
        errors = []
        
        # Criar dicionário de configurações por nome de zona
        zones_by_name = {zone["name"]: zone for zone in zones_config}
        
        # Avaliar cada zona na ordem especificada
        for zone_name in evaluation_order:
            zone_config = zones_by_name.get(zone_name)
            if not zone_config:
                errors.append(f"Zona '{zone_name}' não encontrada na configuração")
                self.zone_values[zone_name] = None
                continue
            
            detected_obj = detected_objects.get(zone_name)
            value, is_valid, error_msg = self.evaluate_zone(
                zone_name,
                zone_config,
                detected_obj,
                input_values,
                object_mapping
            )
            
            self.zone_values[zone_name] = value
            
            if not is_valid:
                errors.append(error_msg)
        
        return self.zone_values, errors
    
    def get_final_output(self, output_zone: str) -> Optional[int]:
        """Obtém o valor final do circuito (zona de saída)."""
        return self.zone_values.get(output_zone)

