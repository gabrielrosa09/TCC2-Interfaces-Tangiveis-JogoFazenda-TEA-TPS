"""
Módulo para gerenciamento de ações baseadas em objetos detectados.
Contém a classe ObjectAction e funções auxiliares relacionadas.
"""


class ObjectAction:
    """Classe que representa uma ação baseada em detecção de objeto."""

    def __init__(self, name, objects, action_func, description=""):
        """
        Inicializa uma ação de objeto.

        Args:
            name (str): Nome da ação
            objects (list): Lista de objetos que ativam esta ação
            action_func (callable): Função a ser executada quando a ação for ativada
            description (str): Descrição da ação
        """
        self.name = name
        self.objects = objects if isinstance(objects, list) else [objects]
        self.action_func = action_func
        self.description = description

    def is_object_valid(self, object_name):
        """Verifica se um objeto é válido para esta ação."""
        return object_name in self.objects

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


def get_objects_for_actions(object_actions_dict, *action_keys):
    """
    Retorna uma lista de objetos para as ações especificadas.

    Args:
        object_actions_dict (dict): Dicionário de ações de objeto
        *action_keys: Chaves das ações

    Returns:
        list: Lista de objetos únicos
    """
    objects = []
    for action_key in action_keys:
        if action_key in object_actions_dict:
            objects.extend(object_actions_dict[action_key].objects)
    return list(set(objects))  # Remove duplicatas

