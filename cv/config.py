# Configurações para o sistema de reconhecimento de gestos

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
# GESTOS POR AÇÃO
# ================================
GESTURE_ACTIONS = {
    "START_GAME": ["ILoveYou"],
    "OPEN_TUTORIAL": ["Closed_Fist"],
    "EXIT_GAME": ["Victory"],
    "RETURN_MENU": ["Victory"],
    "GAME_ACTION": ["Open_Palm"],
    "REPEAT_NARRATION": ["Pointing_Up"],
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
            "gestures": [
                *GESTURE_ACTIONS["START_GAME"],
                *GESTURE_ACTIONS["OPEN_TUTORIAL"],
                *GESTURE_ACTIONS["EXIT_GAME"],
            ],
        },
        *CONFIG_ZONES,
    ],
    "tutorial": [
        {
            "name": "GESTOS",
            "rect": (25, 300, 400, 650),
            "color": ZONE_COLORS["GESTOS"],
            "gestures": [
                *GESTURE_ACTIONS["RETURN_MENU"],
                *GESTURE_ACTIONS["REPEAT_NARRATION"],
            ],
        },
        *CONFIG_ZONES,
    ],
    "fase1": [
        {
            "name": "GESTOS",
            "rect": (25, 300, 400, 650),
            "color": ZONE_COLORS["GESTOS"],
            "gestures": [
                *GESTURE_ACTIONS["GAME_ACTION"],
                *GESTURE_ACTIONS["RETURN_MENU"],
                *GESTURE_ACTIONS["REPEAT_NARRATION"],
            ],
        },
        *CONFIG_ZONES,
    ],
}
