# Configurações para o sistema de reconhecimento de gestos

from cv.gesture_actions import GestureAction, get_gestures_for_actions


# ================================
# CONFIGURAÇÕES DA CÂMERA
# ================================
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
CAMERA_INDEX = 0

# ================================
# CONFIGURAÇÕES DO MEDIAPIPE
# ================================
MODEL_PATH = "cv/gesture_recognizer.task"
NUM_HANDS = 2
MIN_HAND_DETECTION_CONFIDENCE = 0.5
MIN_HAND_PRESENCE_CONFIDENCE = 0.5
MIN_TRACKING_CONFIDENCE = 0.5

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
# CONFIGURAÇÕES DE AÇÕES
# ================================
ACTION_COOLDOWN_TIME = 1.0  # segundos
GESTURE_HISTORY_SIZE = 5
GESTURE_VALIDATION_TIME = 2.0  # segundos para validar gesto

# ================================
# AÇÕES DE GESTO CONFIGURADAS
# ================================
GESTURE_ACTIONS = {
    "START_GAME": GestureAction(
        name="START_GAME",
        gestures=["ILoveYou"],
        action_func="_start_game",
        description="Inicia o jogo"
    ),
    "OPEN_TUTORIAL": GestureAction(
        name="OPEN_TUTORIAL",
        gestures=["Closed_Fist"],
        action_func="_open_tutorial",
        description="Abre o tutorial"
    ),
    "EXIT_GAME": GestureAction(
        name="EXIT_GAME",
        gestures=["Victory"],
        action_func="_exit_game",
        description="Sai do jogo"
    ),
    "RETURN_MENU": GestureAction(
        name="RETURN_MENU",
        gestures=["Victory"],
        action_func="_return_to_menu",
        description="Volta ao menu principal"
    ),
    "GAME_ACTION": GestureAction(
        name="GAME_ACTION",
        gestures=["Open_Palm"],
        action_func="_execute_game_action",
        description="Executa ação do jogo"
    ),
    "REPEAT_NARRATION": GestureAction(
        name="REPEAT_NARRATION",
        gestures=["Pointing_Up"],
        action_func="_repeat_narration",
        description="Repete a narração"
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
    },
    {
        "name": "BRILHO",
        "rect": (CAMERA_WIDTH - 100, 100, CAMERA_WIDTH, 200),
        "color": ZONE_COLORS["BRILHO"],
        "gestures": [],
    },
    {
        "name": "TAMANHO DE FONTE",
        "rect": (CAMERA_WIDTH - 100, 200, CAMERA_WIDTH, 300),
        "color": ZONE_COLORS["TAMANHO_FONTE"],
        "gestures": [],
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
            "gestures": get_gestures_for_actions(GESTURE_ACTIONS, "START_GAME", "OPEN_TUTORIAL", "EXIT_GAME"),
        },
        *CONFIG_ZONES,
    ],
    "tutorial": [
        {
            "name": "GESTOS",
            "rect": (25, 300, 400, 650),
            "color": ZONE_COLORS["GESTOS"],
            "gestures": get_gestures_for_actions(GESTURE_ACTIONS, "RETURN_MENU", "REPEAT_NARRATION"),
        },
        *CONFIG_ZONES,
    ],
    "fase1": [
        {
            "name": "GESTOS",
            "rect": (25, 300, 400, 650),
            "color": ZONE_COLORS["GESTOS"],
            "gestures": get_gestures_for_actions(GESTURE_ACTIONS, "GAME_ACTION", "RETURN_MENU", "REPEAT_NARRATION"),
        },
        *CONFIG_ZONES,
    ],
}
