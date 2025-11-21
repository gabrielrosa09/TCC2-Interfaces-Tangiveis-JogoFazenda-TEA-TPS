"""
Configurações das fases do jogo.
Define os circuitos, contextos e regras de cada fase.
"""

# ================================
# MAPEAMENTO DE OBJETOS DETECTADOS PARA ELEMENTOS DO JOGO
# ================================
# Este mapeamento permite trocar facilmente os objetos físicos
# que representam cada elemento do jogo
OBJECT_TO_GAME_ELEMENT = {
    # Inputs (fontes de energia)
    "remote": "solar_input",    # Energia solar
    "clock": "wind_input",           # Energia eólica
    
    # Portas lógicas
    "orange": "and_gate",        # Porta AND
    "cell phone": "or_gate",              # Porta OR
    "scissors": "not_gate",            # Porta NOT
}

# ================================
# CONFIGURAÇÃO DA FASE 1
# ================================
FASE1_CONFIG = {
    "fase_id": 1,
    "name": "Fase 1",
    "description": "Noite com vento",
    
    # Contexto dos inputs (valores lógicos)
    "inputs": {
        "solar": 0,      # Noite (sem sol)
        "eolico": 1,     # Com vento
    },
    
    # Valor esperado na saída
    "expected_value": 1,
    
    # Zona de saída (resultado final)
    "output_zone": "GATE2",
    
    # Ordem de avaliação das zonas (importante para circuitos sequenciais)
    "evaluation_order": ["INPUT1", "INPUT2", "GATE1", "GATE2"],
    
    # Configuração das zonas
    "zones": [
        {
            "name": "INPUT1",
            "rect": (450, 50, 750, 350),
            "allowed_elements": ["solar_input", "wind_input"],
            "inputs": [],  # Não tem inputs (é uma fonte)
            "marker_position": (470, 70),      # Posição do marcador de detecção
            "result_position": (600, 200),     # Posição do resultado (1/0)
        },
        {
            "name": "INPUT2",
            "rect": (450, 650, 750, 950),
            "allowed_elements": ["solar_input", "wind_input"],
            "inputs": [],  # Não tem inputs (é uma fonte)
            "marker_position": (470, 670),
            "result_position": (600, 800),
        },
        {
            "name": "GATE1",
            "rect": (850, 350, 1150, 650),
            "allowed_elements": ["and_gate"],
            "inputs": ["INPUT1", "INPUT2"],  # Recebe de INPUT1 e INPUT2
            "marker_position": (870, 370),
            "result_position": (1000, 500),
        },
        {
            "name": "GATE2",
            "rect": (1250, 350, 1550, 650),
            "allowed_elements": ["not_gate"],
            "inputs": ["GATE1"],  # Recebe de GATE1
            "marker_position": (1270, 370),
            "result_position": (1400, 500),
        },
    ],
}

# ================================
# EXEMPLO DE FASE 2 (para facilitar expansão futura)
# ================================
FASE2_CONFIG = {
    "fase_id": 2,
    "name": "Fase 2",
    "description": "Dia sem vento",
    
    "inputs": {
        "solar": 1,      # Dia (com sol)
        "eolico": 0,     # Sem vento
    },
    
    "expected_value": 1,
    "output_zone": "GATE2",
    "evaluation_order": ["INPUT1", "INPUT2", "GATE1", "GATE2"],
    
    "zones": [
        {
            "name": "INPUT1",
            "rect": (450, 50, 750, 350),
            "allowed_elements": ["solar_input", "wind_input"],
            "inputs": [],
            "marker_position": (470, 70),
            "result_position": (600, 200),
        },
        {
            "name": "INPUT2",
            "rect": (450, 650, 750, 950),
            "allowed_elements": ["solar_input", "wind_input"],
            "inputs": [],
            "marker_position": (470, 670),
            "result_position": (600, 800),
        },
        {
            "name": "GATE1",
            "rect": (850, 350, 1150, 650),
            "allowed_elements": ["or_gate"],  # Diferente da fase 1
            "inputs": ["INPUT1", "INPUT2"],
            "marker_position": (870, 370),
            "result_position": (1000, 500),
        },
        {
            "name": "GATE2",
            "rect": (1250, 350, 1550, 650),
            "allowed_elements": ["not_gate"],
            "inputs": ["GATE1"],
            "marker_position": (1270, 370),
            "result_position": (1400, 500),
        },
    ],
}

# ================================
# REGISTRO DE TODAS AS FASES
# ================================
PHASES = {
    1: FASE1_CONFIG,
    2: FASE2_CONFIG,
}

def get_phase_config(phase_id: int):
    """
    Obtém a configuração de uma fase específica.
    
    Args:
        phase_id (int): ID da fase
    
    Returns:
        dict: Configuração da fase ou None se não existir
    """
    return PHASES.get(phase_id)

def get_all_phases():
    """
    Retorna todas as fases configuradas.
    
    Returns:
        dict: Dicionário com todas as fases
    """
    return PHASES.copy()

