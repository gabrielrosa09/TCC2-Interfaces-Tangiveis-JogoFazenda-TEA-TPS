# Configurações para o sistema de reconhecimento de gestos e objetos

from cv.gesture_actions import GestureAction, get_gestures_for_actions
from cv.object_actions import ObjectAction, get_objects_for_actions


# ================================
# CONFIGURAÇÕES DA CÂMERA
# ================================
CAMERA_WIDTH = 1920
CAMERA_HEIGHT = 1080
CAMERA_INDEX = 0

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
OBJECT_MODEL_PATH = "cv/mediapipe_models/efficientdet_lite0.tflite"
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
    "GESTOS": (0, 0, 0),  # Preto
    "SOM": (255, 0, 0),  # Vermelho
    "BRILHO": (0, 255, 0),  # Verde
    "TAMANHO_FONTE": (0, 0, 255),  # Azul
    "OBJETOS": (0, 255, 255),  # Amarelo
    "DEFAULT": (128, 128, 128),  # Cinza
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
    "cup",
    "fork",
    "knife",
    "spoon",
    "banana",
    "apple",
    "orange",
    "broccoli",
    "carrot",
    "mouse",
    "remote",
    "cell phone",
    "clock",
    "toothbrush",
    "scissors",
}

# ================================
# CONFIGURAÇÕES DE BRILHO
# ================================
BRIGHTNESS_LEVELS = {
    "apple": 0,    # 100% de brilho (sem escurecimento)
    "cup": 102,       # 60% de brilho (40% de opacidade)
    "fork": 179,      # 30% de brilho (70% de opacidade)
}
DEFAULT_BRIGHTNESS_OBJECT = "apple"

# ================================
# CONFIGURAÇÕES DE VOLUME
# ================================
VOLUME_LEVELS = {
    "toothbrush": 0.7,          # 100% de volume
    "orange": 0.5,          # 70% de volume
    "banana": 0.3,      # 40% de volume
    "broccoli": 0.0,        # 0% de volume (mudo)
}
DEFAULT_VOLUME_OBJECT = "banana"

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
    "cell phone": "color",      # Modo colorido (padrão)
    "clock": "grayscale",       # Modo preto e branco (escala de cinza)
}
DEFAULT_COLOR_MODE_OBJECT = "cell phone"

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
GAME_STATES = {
    "CUTSCENE1": "cutscene1",
    "CUTSCENE2": "cutscene2",
    "CUTSCENE3": "cutscene3",
    "CUTSCENE4_TUTORIAL": "cutscene4_tutorial",
    "CUTSCENE5_TUTORIAL_PRATICO": "cutscene5_tutorial_pratico",
    "CUTSCENE6_INICIO_MISSOES": "cutscene6_inicio_missoes",
    "FASE1": "fase1",
}

# Estados que são considerados tutoriais (cutscenes)
TUTORIAL_STATES = [
    "cutscene1",
    "cutscene2",
    "cutscene3",
    "cutscene4_tutorial",
    "cutscene5_tutorial_pratico",
    "cutscene6_inicio_missoes",
]

# Ordem das cutscenes do tutorial
TUTORIAL_ORDER = [
    "cutscene1",
    "cutscene2",
    "cutscene3",
    "cutscene4_tutorial",
    "cutscene5_tutorial_pratico",
    "cutscene6_inicio_missoes",
]

# ================================
# ZONAS DE CONFIGURAÇÕES DO JOGO
# ================================
CONFIG_ZONES = [
    {
        "name": "SOM",
        "rect": (0, 0, 300, 300),
        "color": ZONE_COLORS["SOM"],
        "gestures": [],
        "objects": get_objects_for_actions(
            OBJECT_ACTIONS,
            "CHANGE_VOLUME",
        ),
    },
    {
        "name": "BRILHO",
        "rect": (400, 0, 700, 300),
        "color": ZONE_COLORS["BRILHO"],
        "gestures": [],
        "objects": get_objects_for_actions(
            OBJECT_ACTIONS,
            "CHANGE_BRIGHTNESS",
        ),
    },
    {
        "name": "COR",
        "rect": (800, 0, 1100, 300),
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
        "rect": (450, 50, 750, 350),
        "color": ZONE_COLORS["OBJETOS"],
        "gestures": [],
        "objects": ["cell phone", "clock"],  # Aceita inputs de energia
    },
    {
        "name": "INPUT2",
        "rect": (450, 650, 750, 950),
        "color": ZONE_COLORS["OBJETOS"],
        "gestures": [],
        "objects": ["cell phone", "clock"],  # Aceita inputs de energia
    },
    {
        "name": "GATE1",
        "rect": (850, 350, 1150, 650),
        "color": ZONE_COLORS["OBJETOS"],
        "gestures": [],
        "objects": ["toothbrush"],  # Aceita apenas AND gate
    },
    {
        "name": "GATE2",
        "rect": (1250, 350, 1550, 650),
        "color": ZONE_COLORS["OBJETOS"],
        "gestures": [],
        "objects": ["banana"],  # Aceita apenas NOT gate
    },
]

# ================================
# CONFIGURAÇÕES DE ZONAS POR TELA
# ================================

# Zonas para todas as cutscenes do tutorial
TUTORIAL_ZONES = [
    {
        "name": "GESTOS_ESQUERDA",
        "rect": (25, CAMERA_HEIGHT - 300, 400, CAMERA_HEIGHT - 100),
        "color": ZONE_COLORS["GESTOS"],
        "gestures": get_gestures_for_actions(
            GESTURE_ACTIONS, "TUTORIAL_PREVIOUS", "EXIT_GAME"
        ),
        "objects": [],
    },
    {
        "name": "GESTOS_DIREITA",
        "rect": (CAMERA_WIDTH - 400, CAMERA_HEIGHT - 300, CAMERA_WIDTH - 25, CAMERA_HEIGHT - 100),
        "color": ZONE_COLORS["GESTOS"],
        "gestures": get_gestures_for_actions(
            GESTURE_ACTIONS, "TUTORIAL_NEXT", "TUTORIAL_SKIP"
        ),
        "objects": [],
    },
    *CONFIG_ZONES,
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
            "rect": (25, CAMERA_HEIGHT - 300, 400, CAMERA_HEIGHT - 100),
            "color": ZONE_COLORS["GESTOS"],
            "gestures": get_gestures_for_actions(
                GESTURE_ACTIONS, "PHASE_RETURN_TUTORIAL", "EXIT_GAME"
            ),
            "objects": [],
        },
        {
            "name": "GESTOS_DIREITA",
            "rect": (CAMERA_WIDTH - 400, CAMERA_HEIGHT - 300, CAMERA_WIDTH - 25, CAMERA_HEIGHT - 100),
            "color": ZONE_COLORS["GESTOS"],
            "gestures": get_gestures_for_actions(
                GESTURE_ACTIONS, "PHASE_REPEAT_NARRATION", "PHASE_VALIDATE"
            ),
            "objects": [],
        },
        *FASE1_MATRIX_ZONES,
        # *CONFIG_ZONES,
    ],
}
