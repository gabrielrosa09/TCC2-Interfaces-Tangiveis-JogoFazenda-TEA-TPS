# Configurações para o sistema de reconhecimento de gestos e objetos

from cv.gesture_actions import GestureAction, get_gestures_for_actions
from cv.object_actions import ObjectAction, get_objects_for_actions
from config import *


# ================================
# CONFIGURAÇÕES DA CÂMERA
# ================================
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
CAMERA_INDEX = 1

# ================================
# CONFIGURAÇÕES DO MEDIAPIPE - GESTOS
# ================================
GESTURE_MODEL_PATH = "cv/mediapipe_models/gesture_recognizer.task"
NUM_HANDS = 2
MIN_HAND_DETECTION_CONFIDENCE = 0.5
MIN_HAND_PRESENCE_CONFIDENCE = 0.5
MIN_TRACKING_CONFIDENCE = 0.5

# ================================
# CONFIGURAÇÕES DO MEDIAPIPE - OBJETOS
# ================================
OBJECT_MODEL_PATH = "cv/mediapipe_models/best.pt"
MAX_OBJECT_RESULTS = 17
MIN_OBJECT_DETECTION_CONFIDENCE = 0.3

# ================================
# CONFIGURAÇÕES DE RENDERIZAÇÃO
# ================================
LANDMARK_RADIUS = 5
LANDMARK_COLOR = (0, 0, 255)  # Vermelho
CONNECTION_THICKNESS = 2
CONNECTION_COLOR = (255, 255, 255)  # Branco
ZONE_THICKNESS = 2
TEXT_FONT = 0.7
TEXT_THICKNESS = 2

# ================================
# CONFIGURAÇÕES DE ZONAS
# ================================
ZONE_COLORS = {
    "GESTOS": PRETO,
    "SOM": AZUL,
    "BRILHO": BRANCO,
    "TAMANHO_FONTE": VERMELHO,
    "COR": VERDE,
    "OBJETOS": AMARELO,
    "DEFAULT": CINZA,
}

# ================================
# CONFIGURAÇÕES DE GESTOS
# ================================
SUPPORTED_GESTURES = [
    "Closed_Fist",
    "Open_Palm",
    "Pointing_Up",
    "Thumb_Down",
    "Thumb_Up",
    "Victory",
    "ILoveYou",
]

# ================================
# CONFIGURAÇÕES DE OBJETOS
# ================================
SUPPORTED_OBJECTS = {
    "and_gate",
    "colorful",
    "high_brightness",
    "high_volume",
    "large_font",
    "low_brightness",
    "low_volume",
    "medium_brightness",
    "medium_font",
    "medium_volume",
    "mute_volume",
    "not_colored",
    "not_gate",
    "or_gate",
    "solar_input",
    "wind_input",
}

# ================================
# CONFIGURAÇÕES DE BRILHO
# ================================
BRIGHTNESS_LEVELS = {
    "high_brightness": 0,  # 100% de brilho (sem escurecimento)
    "medium_brightness": 102,  # 60% de brilho (40% de opacidade)
    "low_brightness": 179,  # 30% de brilho (70% de opacidade)
}
DEFAULT_BRIGHTNESS_OBJECT = "high_brightness"

# ================================
# CONFIGURAÇÕES DE VOLUME
# ================================
VOLUME_LEVELS = {
    "high_volume": 0.7,  # 100% de volume
    "medium_volume": 0.5,  # 70% de volume
    "low_volume": 0.3,  # 40% de volume
    "mute_volume": 0.0,  # 0% de volume (mudo)
}
DEFAULT_VOLUME_OBJECT = "high_volume"

# ================================
# CONFIGURAÇÕES DE SONS DO JOGO
# ================================
GAME_SOUNDS = {
    "background_music": {
        "path": "assets/sounds/background-music.mp3",
        "base_volume": 0.2,
        "description": "Música de fundo do jogo",
    },
}

# ================================
# CONFIGURAÇÕES DE COR
# ================================
COLOR_MODES = {
    "colorful": "color",  # Modo colorido (padrão)
    "not_colored": "grayscale",  # Modo preto e branco (escala de cinza)
}
DEFAULT_COLOR_MODE_OBJECT = "colorful"

BACKGROUND_MUSIC_PATH = ""

# ================================
# CONFIGURAÇÕES DE AÇÕES
# ================================
ACTION_COOLDOWN_TIME = 2.0  # segundos
GESTURE_HISTORY_SIZE = 5
RECOGNITION_VALIDATION_TIME = 2.0  # segundos para validar gesto/objeto

# ================================
# AÇÕES DE GESTO CONFIGURADAS
# ================================
GESTURE_ACTIONS = {
    # Ações de Tutorial - Zona Esquerda
    "TUTORIAL_PREVIOUS": GestureAction(
        name="TUTORIAL_PREVIOUS",
        gestures=["Victory"],
        action_func="_tutorial_previous_cutscene",
        description="Volta à cutscene anterior do tutorial",
    ),
    # Ações de Tutorial - Zona Direita
    "TUTORIAL_NEXT": GestureAction(
        name="TUTORIAL_NEXT",
        gestures=["Victory"],
        action_func="_tutorial_next_cutscene",
        description="Avança para a próxima cutscene do tutorial",
    ),
    "TUTORIAL_SKIP": GestureAction(
        name="TUTORIAL_SKIP",
        gestures=["Closed_Fist"],
        action_func="_tutorial_skip",
        description="Pula o tutorial e vai para a fase",
    ),
    # Ações de Fase - Zona Esquerda
    "PHASE_RETURN_TUTORIAL": GestureAction(
        name="PHASE_RETURN_TUTORIAL",
        gestures=["Victory"],
        action_func="_phase_return_to_tutorial",
        description="Volta para o tutorial (primeira cutscene)",
    ),
    # Ações de Fase - Zona Direita
    "PHASE_REPEAT_NARRATION": GestureAction(
        name="PHASE_REPEAT_NARRATION",
        gestures=["Pointing_Up"],
        action_func="_repeat_narration",
        description="Repete a narração da fase",
    ),
    "PHASE_VALIDATE": GestureAction(
        name="PHASE_VALIDATE",
        gestures=["Open_Palm"],
        action_func="_execute_game_action",
        description="Valida a lógica booleana da fase",
    ),
    # Ação Global - Zona Esquerda
    "EXIT_GAME": GestureAction(
        name="EXIT_GAME",
        gestures=["ILoveYou"],
        action_func="_exit_game",
        description="Sai do jogo",
    ),
}

# ================================
# AÇÕES DE OBJETO CONFIGURADAS
# ================================
OBJECT_ACTIONS = {
    "CHANGE_BRIGHTNESS": ObjectAction(
        name="CHANGE_BRIGHTNESS",
        objects=list(BRIGHTNESS_LEVELS.keys()),
        action_func="_change_brightness",
        description="Altera o brilho da tela",
    ),
    "CHANGE_VOLUME": ObjectAction(
        name="CHANGE_VOLUME",
        objects=list(VOLUME_LEVELS.keys()),
        action_func="_change_volume",
        description="Altera o volume do som",
    ),
    "CHANGE_COLOR_MODE": ObjectAction(
        name="CHANGE_COLOR_MODE",
        objects=list(COLOR_MODES.keys()),
        action_func="_change_color_mode",
        description="Altera o modo de cor da interface",
    ),
}

# ================================
# CONFIGURAÇÕES DE ESTADOS DO JOGO
# ================================
GAME_STATES = {"MENU": "menu", "TUTORIAL": "tutorial", "FASE1": "fase1"}

# ================================
# ZONAS DE CONFIGURAÇÕES DO JOGO
# ================================
CONFIG_ZONES = [
    {
        "name": "SOM",
        "rect": (283, 0, 433, 133),
        "color": ZONE_COLORS["SOM"],
        "gestures": [],
        "objects": get_objects_for_actions(
            OBJECT_ACTIONS,
            "CHANGE_VOLUME",
        ),
    },
    {
        "name": "BRILHO",
        "rect": (433, 0, 583, 133),
        "color": ZONE_COLORS["BRILHO"],
        "gestures": [],
        "objects": get_objects_for_actions(
            OBJECT_ACTIONS,
            "CHANGE_BRIGHTNESS",
        ),
    },
    {
        "name": "COR",
        "rect": (583, 0, 733, 133),
        "color": ZONE_COLORS["COR"],
        "gestures": [],
        "objects": get_objects_for_actions(
            OBJECT_ACTIONS,
            "CHANGE_COLOR_MODE",
        ),
    },
    {
        "name": "TAMANHO DA FONTE",
        "rect": (733, 0, 883, 133),
        "color": ZONE_COLORS["TAMANHO_FONTE"],
        "gestures": [],
        "objects": get_objects_for_actions(
            OBJECT_ACTIONS,
            "CHANGE_COLOR_MODE",
        ),
    },
]

FASE1_MATRIX_ZONES = [
    {
        "name": "INPUT1",
        "rect": (370, 335, 500, 460),
        "color": ZONE_COLORS["OBJETOS"],
        "gestures": [],
        "objects": ["solar_input", "wind_input"],
    },
    {
        "name": "INPUT2",
        "rect": (370, 515, 500, 640),
        "color": ZONE_COLORS["OBJETOS"],
        "gestures": [],
        "objects": ["solar_input", "wind_input"],
    },
    {
        "name": "GATE1",
        "rect": (560, 425, 680, 540),
        "color": ZONE_COLORS["OBJETOS"],
        "gestures": [],
        "objects": ["and_gate"],
    },
    {
        "name": "GATE2",
        "rect": (740, 425, 860, 540),
        "color": ZONE_COLORS["OBJETOS"],
        "gestures": [],
        "objects": ["not_gate"],
    },
]

# ================================
# CONFIGURAÇÕES DE ZONAS POR TELA
# ================================

# Zonas para todas as cutscenes do tutorial
TUTORIAL_ZONES = [
    {
        "name": "GESTOS_ESQUERDA",
        "rect": (0, CAMERA_HEIGHT - 300, 300, CAMERA_HEIGHT),
        "color": ZONE_COLORS["GESTOS"],
        "gestures": get_gestures_for_actions(
            GESTURE_ACTIONS, "TUTORIAL_PREVIOUS", "EXIT_GAME"
        ),
        "objects": [],
    },
    {
        "name": "GESTOS_DIREITA",
        "rect": (
            CAMERA_WIDTH - 300,
            CAMERA_HEIGHT - 300,
            CAMERA_WIDTH,
            CAMERA_HEIGHT,
        ),
        "color": ZONE_COLORS["GESTOS"],
        "gestures": get_gestures_for_actions(
            GESTURE_ACTIONS, "TUTORIAL_NEXT", "TUTORIAL_SKIP"
        ),
        "objects": [],
    },
    *CONFIG_ZONES,
]

TUTORIAL_STATES = [
    "cutscene1",
    "cutscene2",
    "cutscene3",
    "cutscene4_tutorial",
    "cutscene5_tutorial_pratico",
    "cutscene6_inicio_missoes",
]

TUTORIAL_ORDER = [
    "cutscene1",
    "cutscene2",
    "cutscene3",
    "cutscene4_tutorial",
    "cutscene5_tutorial_pratico",
    "cutscene6_inicio_missoes",
]

SCREEN_ZONES = {
    # Todas as cutscenes do tutorial usam as mesmas zonas
    "cutscene1": TUTORIAL_ZONES,
    "cutscene2": TUTORIAL_ZONES,
    "cutscene3": TUTORIAL_ZONES,
    "cutscene4_tutorial": TUTORIAL_ZONES,
    "cutscene5_tutorial_pratico": TUTORIAL_ZONES,
    "cutscene6_inicio_missoes": TUTORIAL_ZONES,
    # Fase 1 com duas zonas de gestos
    "fase1": [
        {
            "name": "GESTOS_ESQUERDA",
            "rect": (0, CAMERA_HEIGHT - 300, 300, CAMERA_HEIGHT),
            "color": ZONE_COLORS["GESTOS"],
            "gestures": get_gestures_for_actions(
                GESTURE_ACTIONS, "PHASE_RETURN_TUTORIAL", "EXIT_GAME"
            ),
            "objects": [],
        },
        {
            "name": "GESTOS_DIREITA",
            "rect": (
                CAMERA_WIDTH - 300,
                CAMERA_HEIGHT - 300,
                CAMERA_WIDTH,
                CAMERA_HEIGHT,
            ),
            "color": ZONE_COLORS["GESTOS"],
            "gestures": get_gestures_for_actions(
                GESTURE_ACTIONS, "PHASE_REPEAT_NARRATION", "PHASE_VALIDATE"
            ),
            "objects": [],
        },
        *FASE1_MATRIX_ZONES,
        *CONFIG_ZONES,
    ],
}
