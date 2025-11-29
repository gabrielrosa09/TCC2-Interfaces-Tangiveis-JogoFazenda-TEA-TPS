"""
Módulo para gerenciamento de ações baseadas em gestos.
Contém a classe GestureAction e funções auxiliares relacionadas.
"""


class GestureAction:
    """Classe que representa uma ação baseada em gesto."""

    def __init__(self, name, gestures, action_func, description=""):
        """Inicializa uma ação de gesto."""
        self.name = name
        self.gestures = gestures if isinstance(gestures, list) else [gestures]
        self.action_func = action_func
        self.description = description

    def is_gesture_valid(self, gesture_name):
        """Verifica se um gesto é válido para esta ação."""
        return gesture_name in self.gestures

    def execute(self, action_handler, *args, **kwargs):
        """Executa a ação."""
        if callable(self.action_func):
            return self.action_func(action_handler, *args, **kwargs)
        elif isinstance(self.action_func, str):
            # Se for uma string, tenta chamar o método do action_handler
            method = getattr(action_handler, self.action_func, None)
            if method and callable(method):
                return method(*args, **kwargs)
        return None


def get_gestures_for_actions(gesture_actions_dict, *action_keys):
    """Retorna uma lista de gestos para as ações especificadas."""
    gestures = []
    for action_key in action_keys:
        if action_key in gesture_actions_dict:
            gestures.extend(gesture_actions_dict[action_key].gestures)
    return list(set(gestures))  # Remove duplicatas
