"""
Gerenciador de ações para reconhecimento de gestos.
Responsável por executar ações baseadas em gestos, zonas e estado do jogo.
"""

import time
from cv.config import ACTION_COOLDOWN_TIME, GESTURE_HISTORY_SIZE, GESTURE_ACTIONS


class ActionHandler:
    """Gerencia a execução de ações baseadas em gestos e zonas."""

    def __init__(self, game_controller=None, zone_manager=None):
        self.game_controller = game_controller
        self.zone_manager = zone_manager
        self.action_cooldown = {}
        self.gesture_history = []
        self.cooldown_time = ACTION_COOLDOWN_TIME
        self.max_history = GESTURE_HISTORY_SIZE

    def execute_action(self, gesture_name, zone_name, hand_info):
        """
        Executa ação baseada no gesto, zona e tela atual.

        Args:
            gesture_name (str): Nome do gesto reconhecido
            zone_name (str): Nome da zona onde o gesto foi detectado
            hand_info (str): Informação sobre qual mão (Left/Right)
        """
        # Verificar cooldown
        if self._is_action_on_cooldown(gesture_name, zone_name):
            return

        # Adicionar ao histórico
        self._add_to_history(gesture_name, zone_name, hand_info)

        # Log da ação
        print(
            f"AÇÃO DETECTADA: {gesture_name} | {zone_name} | {hand_info} | Tela: {self.zone_manager.current_game_state}"
        )

        # Executar ação baseada no estado atual
        current_state = self.zone_manager.current_game_state

        if current_state == "menu":
            self._handle_menu_actions(gesture_name, zone_name)
        elif current_state == "tutorial":
            self._handle_tutorial_actions(gesture_name, zone_name)
        elif current_state == "fase1":
            self._handle_game_actions(gesture_name, zone_name)

        # Registrar cooldown
        self._register_cooldown(gesture_name, zone_name)

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

    def _add_to_history(self, gesture_name, zone_name, hand_info):
        """Adiciona gesto ao histórico."""
        gesture_data = {
            "gesture": gesture_name,
            "zone": zone_name,
            "hand": hand_info,
            "timestamp": time.time(),
        }

        self.gesture_history.append(gesture_data)

        # Manter apenas os últimos N gestos
        if len(self.gesture_history) > self.max_history:
            self.gesture_history.pop(0)

    def _is_gesture_valid_for_action(self, gesture_name, action_key):
        """
        Verifica se um gesto é válido para uma ação específica.

        Args:
            gesture_name (str): Nome do gesto
            action_key (str): Chave da ação (ex: "START_GAME")

        Returns:
            bool: True se o gesto é válido para a ação
        """
        if action_key not in GESTURE_ACTIONS:
            return False
        return gesture_name in GESTURE_ACTIONS[action_key]

    def _handle_menu_actions(self, gesture_name, zone_name):
        """Gerencia ações da tela de menu."""
        if zone_name == "GESTOS":
            if self._is_gesture_valid_for_action(gesture_name, "START_GAME"):
                self._start_game()
            elif self._is_gesture_valid_for_action(gesture_name, "OPEN_TUTORIAL"):
                self._open_tutorial()
            elif self._is_gesture_valid_for_action(gesture_name, "EXIT_GAME"):
                self._exit_game()

    def _handle_tutorial_actions(self, gesture_name, zone_name):
        """Gerencia ações da tela de tutorial."""
        if zone_name == "GESTOS":
            if self._is_gesture_valid_for_action(gesture_name, "RETURN_MENU"):
                self._return_to_menu()
            elif self._is_gesture_valid_for_action(gesture_name, "REPEAT_NARRATION"):
                self._repeat_narration()

    def _handle_game_actions(self, gesture_name, zone_name):
        """Gerencia ações da tela de jogo."""
        if zone_name == "GESTOS":
            if self._is_gesture_valid_for_action(gesture_name, "GAME_ACTION"):
                self._execute_game_action()
            elif self._is_gesture_valid_for_action(gesture_name, "REPEAT_NARRATION"):
                self._repeat_narration()
            elif self._is_gesture_valid_for_action(gesture_name, "RETURN_MENU"):
                self._return_to_menu()

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

    def get_gesture_history(self):
        """
        Retorna o histórico de gestos.

        Returns:
            list: Histórico de gestos
        """
        return self.gesture_history.copy()

    def clear_history(self):
        """Limpa o histórico de gestos."""
        self.gesture_history.clear()

    def get_cooldown_status(self, gesture_name, zone_name):
        """
        Retorna o status de cooldown de uma ação.

        Args:
            gesture_name (str): Nome do gesto
            zone_name (str): Nome da zona

        Returns:
            dict: Status do cooldown
        """
        action_key = f"{gesture_name}_{zone_name}"
        current_time = time.time()

        if action_key in self.action_cooldown:
            remaining = self.cooldown_time - (
                current_time - self.action_cooldown[action_key]
            )
            return {"on_cooldown": remaining > 0, "remaining_time": max(0, remaining)}

        return {"on_cooldown": False, "remaining_time": 0}

    def get_gesture_actions_info(self):
        """
        Retorna informações sobre os gestos configurados para cada ação.

        Returns:
            dict: Mapeamento de ações para gestos
        """
        return GESTURE_ACTIONS.copy()

    def get_gestures_for_action(self, action_key):
        """
        Retorna os gestos válidos para uma ação específica.

        Args:
            action_key (str): Chave da ação

        Returns:
            list: Lista de gestos válidos para a ação
        """
        return GESTURE_ACTIONS.get(action_key, [])
