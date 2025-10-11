# Configurações para o sistema de reconhecimento de gestos e objetos

from cv.gesture_actions import GestureAction, get_gestures_for_actions
from cv.object_actions import ObjectAction, get_objects_for_actions


# ================================
# CONFIGURAÇÕES DA CÂMERA
# ================================
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
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
# CONFIGURAÇÕES DE AÇÕES
# ================================
ACTION_COOLDOWN_TIME = 2.0  # segundos
GESTURE_HISTORY_SIZE = 5
RECOGNITION_VALIDATION_TIME = 2.0  # segundos para validar gesto/objeto
# Manter compatibilidade com código existente
GESTURE_VALIDATION_TIME = RECOGNITION_VALIDATION_TIME

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
    "FEED_ANIMAL": ObjectAction(
        name="FEED_ANIMAL",
        objects=["apple", "banana", "orange", "carrot"],
        action_func="_feed_animal",
        description="Alimenta um animal",
    ),
    "USE_TOOL": ObjectAction(
        name="USE_TOOL",
        objects=["fork", "knife", "spoon", "scissors"],
        action_func="_use_tool",
        description="Usa uma ferramenta",
    ),
    "PLACE_OBJECT": ObjectAction(
        name="PLACE_OBJECT",
        objects=["cup", "remote", "cell phone", "clock"],
        action_func="_place_object",
        description="Coloca um objeto",
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
        "rect": (CAMERA_WIDTH - 100, 0, CAMERA_WIDTH, 100),
        "color": ZONE_COLORS["SOM"],
        "gestures": [],
        "objects": [],
    },
    {
        "name": "BRILHO",
        "rect": (CAMERA_WIDTH - 100, 100, CAMERA_WIDTH, 200),
        "color": ZONE_COLORS["BRILHO"],
        "gestures": [],
        "objects": [],
    },
    {
        "name": "TAMANHO DE FONTE",
        "rect": (CAMERA_WIDTH - 100, 200, CAMERA_WIDTH, 300),
        "color": ZONE_COLORS["TAMANHO_FONTE"],
        "gestures": [],
        "objects": [],
    },
]

# ================================
# CONFIGURAÇÕES DE ZONAS POR TELA
# ================================
SCREEN_ZONES = {
    "menu": [
        {
            "name": "GESTOS",
            "rect": (25, 300, 400, 650),
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
            "rect": (25, 300, 400, 650),
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
            "rect": (25, 300, 400, 650),
            "color": ZONE_COLORS["GESTOS"],
            "gestures": get_gestures_for_actions(
                GESTURE_ACTIONS, "GAME_ACTION", "RETURN_MENU", "REPEAT_NARRATION"
            ),
            "objects": [],
        },
        {
            "name": "OBJETOS",
            "rect": (880, 300, 1255, 650),
            "color": ZONE_COLORS["DEFAULT"],
            "gestures": [],
            "objects": get_objects_for_actions(
                OBJECT_ACTIONS, "FEED_ANIMAL", "USE_TOOL", "PLACE_OBJECT"
            ),
        },
        *CONFIG_ZONES,
    ],
}
