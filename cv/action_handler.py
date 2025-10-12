"""
Gerenciador de ações para reconhecimento de gestos.
Responsável por executar ações baseadas em gestos, zonas e estado do jogo.
"""

import time
from cv.config import (
    ACTION_COOLDOWN_TIME,
    GESTURE_HISTORY_SIZE,
    GESTURE_ACTIONS,
    OBJECT_ACTIONS,
)


class ActionHandler:
    """Gerencia a execução de ações baseadas em gestos e zonas."""

    def __init__(self, game_controller=None, zone_manager=None):
        self.game_controller = game_controller
        self.zone_manager = zone_manager
        self.action_cooldown = {}
        self.recognition_history = []
        self.cooldown_time = ACTION_COOLDOWN_TIME
        self.max_history = GESTURE_HISTORY_SIZE

    def execute_action(self, recognition_name, zone_name, item_info, recognition_type="gesture"):
        """
        Executa ação baseada no reconhecimento (gesto/objeto), zona e tela atual.

        Args:
            recognition_name (str): Nome do gesto/objeto reconhecido
            zone_name (str): Nome da zona onde foi detectado
            item_info (str): Informação adicional (mão, id do objeto, etc)
            recognition_type (str): Tipo de reconhecimento ("gesture" ou "object")
        """
        # Verificar cooldown
        if self._is_action_on_cooldown(recognition_name, zone_name):
            return

        # Adicionar ao histórico
        self._add_to_history(recognition_name, zone_name, item_info, recognition_type)

        # Log da ação
        print(
            f"AÇÃO DETECTADA ({recognition_type}): {recognition_name} | {zone_name} | {item_info} | Tela: {self.zone_manager.current_game_state}"
        )

        # Executar ação baseada no tipo de reconhecimento
        current_state = self.zone_manager.current_game_state
        if recognition_type == "gesture":
            self._handle_gesture_actions(recognition_name, zone_name, current_state)
        elif recognition_type == "object":
            self._handle_object_actions(recognition_name, zone_name, current_state)

        # Registrar cooldown
        self._register_cooldown(recognition_name, zone_name)

    def _is_action_on_cooldown(self, gesture_name, zone_name):
        """Verifica se a ação está em cooldown."""
        current_time = time.time()
        action_key = f"{gesture_name}_{zone_name}"

        if action_key in self.action_cooldown:
            if current_time - self.action_cooldown[action_key] < self.cooldown_time:
                return True

        return False

    def _register_cooldown(self, gesture_name, zone_name):
        """Registra o cooldown para uma ação."""
        current_time = time.time()
        action_key = f"{gesture_name}_{zone_name}"
        self.action_cooldown[action_key] = current_time

    def _add_to_history(self, recognition_name, zone_name, item_info, recognition_type="gesture"):
        """Adiciona reconhecimento ao histórico."""
        recognition_data = {
            "type": recognition_type,
            "name": recognition_name,
            "zone": zone_name,
            "item_info": item_info,
            "timestamp": time.time(),
        }

        self.recognition_history.append(recognition_data)

        # Manter apenas os últimos N reconhecimentos
        if len(self.recognition_history) > self.max_history:
            self.recognition_history.pop(0)

    def _handle_gesture_actions(self, gesture_name, zone_name, current_state):
        """
        Gerencia ações baseadas no gesto, zona e estado atual do jogo.

        Args:
            gesture_name (str): Nome do gesto reconhecido
            zone_name (str): Nome da zona onde o gesto foi detectado
            current_state (str): Estado atual do jogo
        """

        # Definir quais ações são válidas para cada estado
        state_actions = {
            "menu": ["START_GAME", "OPEN_TUTORIAL", "EXIT_GAME"],
            "tutorial": ["RETURN_MENU", "REPEAT_NARRATION"],
            "fase1": ["GAME_ACTION", "RETURN_MENU", "REPEAT_NARRATION"],
        }

        # Obter ações válidas para o estado atual
        valid_actions = state_actions.get(current_state, [])

        # Verificar cada ação válida para ver se o gesto corresponde
        for action_key in valid_actions:
            if action_key in GESTURE_ACTIONS:
                action = GESTURE_ACTIONS[action_key]
                if action.is_gesture_valid(gesture_name):
                    print(f"🎯 Executando ação: {action.description}")
                    action.execute(self)
                    return

        print(
            f"⚠️ Gesto '{gesture_name}' não reconhecido para o estado '{current_state}'"
        )

    def _handle_object_actions(self, object_name, zone_name, current_state):
        """
        Gerencia ações baseadas no objeto, zona e estado atual do jogo.

        Args:
            object_name (str): Nome do objeto reconhecido
            zone_name (str): Nome da zona onde o objeto foi detectado
            current_state (str): Estado atual do jogo
        """

        # Definir quais ações são válidas para cada estado
        state_actions = {
            "menu": [],
            "tutorial": [],
            "fase1": ["FEED_ANIMAL", "USE_TOOL", "PLACE_OBJECT"],
        }

        # Obter ações válidas para o estado atual
        valid_actions = state_actions.get(current_state, [])

        # Verificar cada ação válida para ver se o objeto corresponde
        for action_key in valid_actions:
            if action_key in OBJECT_ACTIONS:
                action = OBJECT_ACTIONS[action_key]
                if action.is_object_valid(object_name):
                    print(f"🎯 Executando ação de objeto: {action.description}")
                    action.execute(self)
                    return

        print(
            f"⚠️ Objeto '{object_name}' não reconhecido para o estado '{current_state}'"
        )

    def _start_game(self):
        """Inicia o jogo."""
        if self.game_controller and hasattr(self.game_controller.game, "state_manager"):
            print("🎮 INICIANDO JOGO...")
            self.game_controller.game.state_manager.set_state("fase1")
            self.zone_manager.set_game_state("fase1")

    def _open_tutorial(self):
        """Abre o tutorial."""
        if self.game_controller and hasattr(self.game_controller.game, "state_manager"):
            print("📚 ABRINDO TUTORIAL...")
            self.game_controller.game.state_manager.set_state("tutorial")
            self.zone_manager.set_game_state("tutorial")

    def _exit_game(self):
        """Sai do jogo."""
        if self.game_controller:
            print("👋 SAINDO DO JOGO...")
            # Sinalizar para parar o jogo
            self.game_controller.running = False
            # Sinalizar para parar a câmera
            if hasattr(self.game_controller, "camera") and self.game_controller.camera:
                self.game_controller.camera.stop()
            # Sinalizar para parar o jogo pygame
            if hasattr(self.game_controller, "game") and self.game_controller.game:
                self.game_controller.game.running = False

    def _return_to_menu(self):
        """Volta ao menu principal."""
        if self.game_controller and hasattr(self.game_controller.game, "state_manager"):
            print("🏠 VOLTANDO AO MENU...")
            self.game_controller.game.state_manager.set_state("menu")
            self.zone_manager.set_game_state("menu")

    def _execute_game_action(self):
        """Executa ação específica do jogo."""
        print("✋ EXECUTANDO AÇÃO DO JOGO...")
        # Implementar lógica específica do jogo
        pass

    def _repeat_narration(self):
        """Repete a narração atual."""
        print("🔊 REPETINDO NARRAÇÃO...")
        # Implementar repetição da narração
        pass

    def _feed_animal(self):
        """Alimenta um animal no jogo."""
        print("🍎 ALIMENTANDO ANIMAL...")
        # Implementar lógica de alimentar animal
        pass

    def _use_tool(self):
        """Usa uma ferramenta no jogo."""
        print("🔧 USANDO FERRAMENTA...")
        # Implementar lógica de usar ferramenta
        pass

    def _place_object(self):
        """Coloca um objeto no jogo."""
        print("📦 COLOCANDO OBJETO...")
        # Implementar lógica de colocar objeto
        pass

    def get_gesture_history(self):
        """
        Retorna o histórico de gestos (mantém compatibilidade).

        Returns:
            list: Histórico de gestos
        """
        return [
            item for item in self.recognition_history if item["type"] == "gesture"
        ]

    def get_recognition_history(self):
        """
        Retorna o histórico completo de reconhecimentos.

        Returns:
            list: Histórico de reconhecimentos
        """
        return self.recognition_history.copy()
