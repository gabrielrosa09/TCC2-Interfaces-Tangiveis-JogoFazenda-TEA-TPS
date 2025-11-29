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
    TUTORIAL_STATES,
    TUTORIAL_ORDER,
)
from core.phase_manager import PhaseManager
from cv.phase_config import OBJECT_TO_GAME_ELEMENT, get_phase_config


class ActionHandler:
    """Gerencia a execução de ações baseadas em gestos e zonas."""

    def __init__(self, game_controller=None, zone_manager=None):
        self.game_controller = game_controller
        self.zone_manager = zone_manager
        self.action_cooldown = {}
        self.recognition_history = []
        self.cooldown_time = ACTION_COOLDOWN_TIME
        self.max_history = GESTURE_HISTORY_SIZE
        
        # Gerenciador de fases
        self.phase_manager = PhaseManager()
        self.current_phase_id = None

    def execute_action(self, recognition_name, zone_name, item_info, recognition_type="gesture"):
        """Executa ação baseada no reconhecimento (gesto/objeto), zona e tela atual."""
        if self._is_action_on_cooldown(recognition_name, zone_name):
            return

        self._add_to_history(recognition_name, zone_name, item_info, recognition_type)

        print(
            f"AÇÃO DETECTADA ({recognition_type}): {recognition_name} | {zone_name} | {item_info} | Tela: {self.zone_manager.current_game_state}"
        )

        # Executar ação baseada no tipo de reconhecimento
        current_state = self.zone_manager.current_game_state
        if recognition_type == "gesture":
            self._handle_gesture_actions(recognition_name, zone_name, current_state)
        elif recognition_type == "object":
            self._handle_object_actions(recognition_name, zone_name, current_state, item_info)

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

        if len(self.recognition_history) > self.max_history:
            self.recognition_history.pop(0)

    def _handle_gesture_actions(self, gesture_name, zone_name, current_state):
        """Gerencia ações baseadas no gesto, zona e estado atual do jogo."""
        state_zone_actions = {}
        
        # Configurar ações para todos os estados de tutorial (cutscenes)
        for tutorial_state in TUTORIAL_STATES:
            state_zone_actions[tutorial_state] = {
                "GESTOS_ESQUERDA": ["TUTORIAL_PREVIOUS", "EXIT_GAME"],
                "GESTOS_DIREITA": ["TUTORIAL_NEXT", "TUTORIAL_SKIP"],
            }
        
        # Configurar ações para a fase 1
        state_zone_actions["fase1"] = {
            "GESTOS_ESQUERDA": ["PHASE_RETURN_TUTORIAL", "EXIT_GAME"],
            "GESTOS_DIREITA": ["PHASE_REPEAT_NARRATION", "PHASE_VALIDATE"],
        }

        # Obter ações válidas para o estado e zona atuais
        valid_actions = []
        if current_state in state_zone_actions:
            zone_actions = state_zone_actions[current_state]
            valid_actions = zone_actions.get(zone_name, [])

        # Verificar cada ação válida para ver se o gesto corresponde
        for action_key in valid_actions:
            if action_key in GESTURE_ACTIONS:
                action = GESTURE_ACTIONS[action_key]
                if action.is_gesture_valid(gesture_name):
                    print(f"[ACAO] Executando acao: {action.description}")
                    action.execute(self, zone_name=zone_name)
                    return

        print(
            f"[AVISO] Gesto '{gesture_name}' na zona '{zone_name}' nao reconhecido para o estado '{current_state}'"
        )

    def _handle_object_actions(self, object_name, zone_name, current_state, item_info=None):
        """Gerencia ações baseadas no objeto, zona e estado atual do jogo."""
        state_actions = {
            "menu": ["CHANGE_BRIGHTNESS", "CHANGE_VOLUME", "CHANGE_COLOR_MODE"],
            "tutorial": ["CHANGE_BRIGHTNESS", "CHANGE_VOLUME", "CHANGE_COLOR_MODE"],
            "fase1": ["FEED_ANIMAL", "USE_TOOL", "PLACE_OBJECT", "CHANGE_BRIGHTNESS", "CHANGE_VOLUME", "CHANGE_COLOR_MODE"],
        }

        # Obter ações válidas para o estado atual
        valid_actions = state_actions.get(current_state, [])

        # Verificar cada ação válida para ver se o objeto corresponde
        for action_key in valid_actions:
            if action_key in OBJECT_ACTIONS:
                action = OBJECT_ACTIONS[action_key]
                if action.is_object_valid(object_name):
                    print(f"[ACAO] Executando acao de objeto: {action.description}")
                    action.execute(self, object_name=object_name, zone_name=zone_name)
                    return

        print(
            f"[AVISO] Objeto '{object_name}' nao reconhecido para o estado '{current_state}'"
        )

    def _start_game(self, zone_name=None):
        """Inicia o jogo."""
        if self.game_controller and hasattr(self.game_controller.game, "state_manager"):
            print("[JOGO] INICIANDO JOGO...")
            self.game_controller.game.state_manager.set_state("fase1")
            self.zone_manager.set_game_state("fase1")

    def _open_tutorial(self, zone_name=None):
        """Abre o tutorial."""
        if self.game_controller and hasattr(self.game_controller.game, "state_manager"):
            print("[TUTORIAL] ABRINDO TUTORIAL...")
            self.game_controller.game.state_manager.set_state("tutorial")
            self.zone_manager.set_game_state("tutorial")

    def _exit_game(self, zone_name=None):
        """Sai do jogo."""
        if self.game_controller:
            print("[JOGO] SAINDO DO JOGO...")
            # Sinalizar para parar o jogo
            self.game_controller.running = False
            # Sinalizar para parar a câmera
            if hasattr(self.game_controller, "camera") and self.game_controller.camera:
                self.game_controller.camera.stop()
            # Sinalizar para parar o jogo pygame
            if hasattr(self.game_controller, "game") and self.game_controller.game:
                self.game_controller.game.running = False

    def _return_to_menu(self, zone_name=None):
        """Volta ao menu principal."""
        if self.game_controller and hasattr(self.game_controller.game, "state_manager"):
            print("[MENU] VOLTANDO AO MENU...")
            self.game_controller.game.state_manager.set_state("menu")
            self.zone_manager.set_game_state("menu")

    def _execute_game_action(self, zone_name=None):
        """Executa ação específica do jogo (validação de fase)."""
        print("[JOGO] EXECUTANDO ACAO DO JOGO...")
        
        # Verificar se estamos em uma fase
        current_state = self.zone_manager.current_game_state
        if current_state not in ["fase1"]:
            print("[AVISO] Acao do jogo so funciona durante as fases")
            return
        
        # Determinar qual fase estamos
        phase_id = 1 if current_state == "fase1" else None
        if phase_id is None:
            print("[AVISO] Fase nao identificada")
            return
        
        # Carregar configuração da fase se necessário
        if self.current_phase_id != phase_id:
            phase_config = get_phase_config(phase_id)
            if phase_config:
                self.phase_manager.set_phase(phase_config)
                self.current_phase_id = phase_id
                print(f"[FASE] Fase {phase_id} carregada: {phase_config.get('description', '')}")
            else:
                print(f"[AVISO] Configuracao da fase {phase_id} nao encontrada")
                return
        
        # Obter objetos detectados nas zonas
        detected_objects = self.zone_manager.get_all_zone_objects()
        
        # Validar a fase
        success, message, zone_values = self.phase_manager.validate_phase(
            detected_objects,
            OBJECT_TO_GAME_ELEMENT
        )
        
        # Exibir resultado no terminal
        print(f"[VALIDACAO] VALIDACAO DA FASE {phase_id}")
        print(f"[VALIDACAO] Resultado: {message}")
        print("[VALIDACAO] Valores das zonas:")
        for zone_name, value in zone_values.items():
            if value is not None:
                print(f"  {zone_name}: {value}")
            else:
                print(f"  {zone_name}: (invalido)")

        if success:
            print("[VALIDACAO] PARABENS! Voce completou a fase!")
        else:
            print("[VALIDACAO] Continue tentando!")
    
    def set_current_phase(self, phase_id: int):
        """Define a fase atual."""
        phase_config = get_phase_config(phase_id)
        if phase_config:
            self.phase_manager.set_phase(phase_config)
            self.current_phase_id = phase_id
            print(f"[FASE] Fase {phase_id} configurada: {phase_config.get('description', '')}")
        else:
            print(f"[AVISO] Configuracao da fase {phase_id} nao encontrada")
    
    def get_phase_manager(self):
        """Retorna o gerenciador de fases."""
        return self.phase_manager

    def _repeat_narration(self, zone_name=None):
        """Repete a narração atual."""
        print("[AUDIO] REPETINDO NARRACAO...")
        pass
    
    def _tutorial_previous_cutscene(self, zone_name=None):
        """Volta para a cutscene anterior do tutorial."""
        if not self.game_controller or not hasattr(self.game_controller.game, "state_manager"):
            return
        
        current_state = self.zone_manager.current_game_state
        
        # Verificar se está em um estado de tutorial
        if current_state not in TUTORIAL_STATES:
            print("[AVISO] Nao esta em uma cutscene do tutorial")
            return
        
        # Encontrar índice da cutscene atual
        try:
            current_index = TUTORIAL_ORDER.index(current_state)
        except ValueError:
            print(f"[AVISO] Estado '{current_state}' nao encontrado na ordem do tutorial")
            return
        
        # Se está na primeira cutscene, não faz nada
        if current_index == 0:
            print("[INFO] Ja esta na primeira cutscene do tutorial")
            return
        
        # Ir para a cutscene anterior
        previous_state = TUTORIAL_ORDER[current_index - 1]
        print(f"[TUTORIAL] VOLTANDO PARA CUTSCENE ANTERIOR: {previous_state}")
        self.game_controller.game.state_manager.set_state(previous_state)
        self.zone_manager.set_game_state(previous_state)
    
    def _tutorial_next_cutscene(self, zone_name=None):
        """Avança para a próxima cutscene do tutorial."""
        if not self.game_controller or not hasattr(self.game_controller.game, "state_manager"):
            return
        
        current_state = self.zone_manager.current_game_state
        
        # Verificar se está em um estado de tutorial
        if current_state not in TUTORIAL_STATES:
            print("[AVISO] Nao esta em uma cutscene do tutorial")
            return
        
        # Encontrar índice da cutscene atual
        try:
            current_index = TUTORIAL_ORDER.index(current_state)
        except ValueError:
            print(f"[AVISO] Estado '{current_state}' nao encontrado na ordem do tutorial")
            return
        
        # Se está na última cutscene, vai para a fase
        if current_index == len(TUTORIAL_ORDER) - 1:
            print("[TUTORIAL] ULTIMA CUTSCENE! Indo para a fase...")
            self.game_controller.game.state_manager.set_state("fase1")
            self.zone_manager.set_game_state("fase1")
            return
        
        # Ir para a próxima cutscene
        next_state = TUTORIAL_ORDER[current_index + 1]
        print(f"[TUTORIAL] AVANCANDO PARA PROXIMA CUTSCENE: {next_state}")
        self.game_controller.game.state_manager.set_state(next_state)
        self.zone_manager.set_game_state(next_state)
    
    def _tutorial_skip(self, zone_name=None):
        """Pula o tutorial e vai direto para a fase."""
        if not self.game_controller or not hasattr(self.game_controller.game, "state_manager"):
            return
        
        current_state = self.zone_manager.current_game_state
        
        # Verificar se está em um estado de tutorial
        if current_state not in TUTORIAL_STATES:
            print("[AVISO] Nao esta em uma cutscene do tutorial")
            return
        
        print("[TUTORIAL] PULANDO TUTORIAL... Indo para a fase!")
        self.game_controller.game.state_manager.set_state("fase1")
        self.zone_manager.set_game_state("fase1")
    
    def _phase_return_to_tutorial(self, zone_name=None):
        """Volta para o tutorial (primeira cutscene)."""
        if not self.game_controller or not hasattr(self.game_controller.game, "state_manager"):
            return
        
        print("[TUTORIAL] VOLTANDO PARA O TUTORIAL (primeira cutscene)...")
        first_tutorial = TUTORIAL_ORDER[0]
        self.game_controller.game.state_manager.set_state(first_tutorial)
        self.zone_manager.set_game_state(first_tutorial)

    def get_gesture_history(self):
        """Retorna o histórico de gestos."""
        return [
            item for item in self.recognition_history if item["type"] == "gesture"
        ]

    def get_recognition_history(self):
        """Retorna o histórico completo de reconhecimentos."""
        return self.recognition_history.copy()

    def _change_brightness(self, object_name=None, zone_name=None):
        """Altera o brilho da tela baseado no objeto detectado."""
        from cv.config import BRIGHTNESS_LEVELS

        if object_name and object_name in BRIGHTNESS_LEVELS:
            opacity = BRIGHTNESS_LEVELS[object_name]

            # Atualizar o brilho no jogo
            if self.game_controller and hasattr(self.game_controller, "game"):
                if hasattr(self.game_controller.game, "brightness_overlay"):
                    # Verificar se o brilho já está no nível desejado
                    current_opacity = self.game_controller.game.brightness_overlay.get_opacity()
                    
                    if current_opacity == opacity:
                        return
                    
                    print(f"[BRILHO] ALTERANDO BRILHO: {object_name} (opacidade: {opacity})")
                    self.game_controller.game.brightness_overlay.set_opacity(opacity)
                    print(f"[BRILHO] Brilho alterado com sucesso!")
                else:
                    print("[AVISO] BrightnessOverlay nao encontrado no jogo")
        else:
            print(f"[AVISO] Objeto '{object_name}' nao possui configuracao de brilho")

    def _change_volume(self, object_name=None, zone_name=None):
        """Altera o volume do som baseado no objeto detectado."""
        from cv.config import VOLUME_LEVELS

        if object_name and object_name in VOLUME_LEVELS:
            volume = VOLUME_LEVELS[object_name]

            # Atualizar o volume no jogo
            if self.game_controller and hasattr(self.game_controller, "game"):
                if hasattr(self.game_controller.game, "audio_manager"):
                    # Verificar se o volume já está no nível desejado
                    current_volume = self.game_controller.game.audio_manager.get_volume()
                    
                    if current_volume == volume:
                        return
                    
                    print(f"[VOLUME] ALTERANDO VOLUME: {object_name} (volume: {volume * 100:.0f}%)")
                    self.game_controller.game.audio_manager.set_volume(volume)
                    print(f"[VOLUME] Volume alterado com sucesso!")
                else:
                    print("[AVISO] AudioManager nao encontrado no jogo")
        else:
            print(f"[AVISO] Objeto '{object_name}' nao possui configuracao de volume")

    def _change_color_mode(self, object_name=None, zone_name=None):
        """Altera o modo de cor da interface baseado no objeto detectado."""
        from cv.config import COLOR_MODES

        if object_name and object_name in COLOR_MODES:
            color_mode = COLOR_MODES[object_name]

            # Atualizar o modo de cor no jogo
            if self.game_controller and hasattr(self.game_controller, "game"):
                if hasattr(self.game_controller.game, "color_filter"):
                    # Verificar se o modo já está configurado
                    current_mode = self.game_controller.game.color_filter.get_mode()
                    
                    if current_mode == color_mode:
                        return
                    
                    mode_name = "COLORIDO" if color_mode == "color" else "PRETO E BRANCO"
                    print(f"[COR] ALTERANDO MODO DE COR: {object_name} -> {mode_name}")
                    self.game_controller.game.color_filter.set_mode(color_mode)
                    print(f"[COR] Modo de cor alterado com sucesso!")
                else:
                    print("[AVISO] ColorFilter nao encontrado no jogo")
        else:
            print(f"[AVISO] Objeto '{object_name}' nao possui configuracao de cor")
