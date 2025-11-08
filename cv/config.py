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
MAX_OBJECT_RESULTS = 5
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
    "START_GAME": GestureAction(
        name="START_GAME",
        gestures=["ILoveYou"],
        action_func="_start_game",
        description="Inicia o jogo",
    ),
    "OPEN_TUTORIAL": GestureAction(
        name="OPEN_TUTORIAL",
        gestures=["Closed_Fist"],
        action_func="_open_tutorial",
        description="Abre o tutorial",
    ),
    "EXIT_GAME": GestureAction(
        name="EXIT_GAME",
        gestures=["Victory"],
        action_func="_exit_game",
        description="Sai do jogo",
    ),
    "RETURN_MENU": GestureAction(
        name="RETURN_MENU",
        gestures=["Victory"],
        action_func="_return_to_menu",
        description="Volta ao menu principal",
    ),
    "GAME_ACTION": GestureAction(
        name="GAME_ACTION",
        gestures=["Open_Palm"],
        action_func="_execute_game_action",
        description="Executa ação do jogo",
    ),
    "REPEAT_NARRATION": GestureAction(
        name="REPEAT_NARRATION",
        gestures=["Pointing_Up"],
        action_func="_repeat_narration",
        description="Repete a narração",
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
        "objects": get_objects_for_actions(
            OBJECT_ACTIONS,
            "FEED_ANIMAL",
        ),
    },
    {
        "name": "INPUT2",
        "rect": (450, 650, 750, 950),
        "color": ZONE_COLORS["OBJETOS"],
        "gestures": [],
        "objects": get_objects_for_actions(
            OBJECT_ACTIONS,
            "FEED_ANIMAL",
        ),
    },
    {
        "name": "GATE1",
        "rect": (850, 350, 1150, 650),
        "color": ZONE_COLORS["OBJETOS"],
        "gestures": [],
        "objects": get_objects_for_actions(
            OBJECT_ACTIONS,
            "PLACE_OBJECT",
        ),
    },
    {
        "name": "GATE2",
        "rect": (1250, 350, 1550, 650),
        "color": ZONE_COLORS["OBJETOS"],
        "gestures": [],
        "objects": get_objects_for_actions(
            OBJECT_ACTIONS,
            "USE_TOOL",
        ),
    },
]

# ================================
# CONFIGURAÇÕES DE ZONAS POR TELA
# ================================
SCREEN_ZONES = {
    "menu": [
        {
            "name": "GESTOS",
            "rect": (25, CAMERA_HEIGHT - 300, 400, CAMERA_HEIGHT - 100),
            "color": ZONE_COLORS["GESTOS"],
            "gestures": get_gestures_for_actions(
                GESTURE_ACTIONS, "START_GAME", "OPEN_TUTORIAL", "EXIT_GAME"
            ),
            "objects": [],
        },
        *CONFIG_ZONES,
    ],
    "tutorial": [
        {
            "name": "GESTOS",
            "rect": (25, CAMERA_HEIGHT - 300, 400, CAMERA_HEIGHT - 100),
            "color": ZONE_COLORS["GESTOS"],
            "gestures": get_gestures_for_actions(
                GESTURE_ACTIONS, "RETURN_MENU", "REPEAT_NARRATION"
            ),
            "objects": [],
        },
        *CONFIG_ZONES,
    ],
    "fase1": [
        {
            "name": "GESTOS",
            "rect": (25, CAMERA_HEIGHT - 300, 400, CAMERA_HEIGHT - 100),
            "color": ZONE_COLORS["GESTOS"],
            "gestures": get_gestures_for_actions(
                GESTURE_ACTIONS, "GAME_ACTION", "RETURN_MENU", "REPEAT_NARRATION"
            ),
            "objects": [],
        },
        # *FASE1_MATRIX_ZONES,
        *CONFIG_ZONES,
    ],
}
