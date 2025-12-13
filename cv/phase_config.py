"""
Configurações das fases do jogo.
Define os circuitos, contextos e regras de cada fase.
"""

# ================================
# CONFIGURAÇÃO DA FASE 1
# ================================
FASE1_CONFIG = {
    "fase_id": 1,
    "name": "Fase 1",
    "description": "Noite com vento",
    "inputs": {
        "solar": 0,      # Noite (sem sol)
        "eolico": 1,     # Com vento (energia eólica)
    },
    "expected_value": 1, # Valor esperado na saída
    "output_zone": "GATE2", # Zona de saída (resultado final)
    "evaluation_order": ["INPUT1", "INPUT2", "GATE1", "GATE2"], # Ordem de avaliação das zonas (importante para circuitos sequenciais)
    "zones": [
        {
            "name": "INPUT1",
            "rect": (370, 335, 500, 460),
            "allowed_elements": ["solar_input", "wind_input"],
            "inputs": [],  # Não tem inputs (é uma fonte)
            "marker_position": (84, 73),
            "result_position": (50, 40),
        },
        {
            "name": "INPUT2",
            "rect": (370, 515, 500, 640),
            "allowed_elements": ["solar_input", "wind_input"],
            "inputs": [],  # Não tem inputs (é uma fonte)
            "marker_position": (84, 125),     # Ajustado para resolução 256x144
            "result_position": (50, 120),     # Ajustado para resolução 256x144
        },
        {
            "name": "GATE1",
            "rect": (560, 425, 680, 540),
            "allowed_elements": ["and_gate"],
            "inputs": ["INPUT1", "INPUT2"],  # Recebe de INPUT1 e INPUT2
            "marker_position": (136, 99),     # Centro horizontal, ajustado para 256x144
            "result_position": (128, 60),     # Ajustado para resolução 256x144
        },
        {
            "name": "GATE2",
            "rect": (740, 425, 860, 540),
            "allowed_elements": ["not_gate"],
            "inputs": ["GATE1"],  # Recebe de GATE1
            "marker_position": (188, 99),     # Lado direito, ajustado para 256x144
            "result_position": (200, 60),     # Ajustado para resolução 256x144
        },
    ],
}

PHASES = {
    1: FASE1_CONFIG,
}

def get_phase_config(phase_id: int):
    """Obtém a configuração de uma fase específica."""
    return PHASES.get(phase_id)

def get_all_phases():
    """Retorna todas as fases configuradas."""
    return PHASES.copy()

