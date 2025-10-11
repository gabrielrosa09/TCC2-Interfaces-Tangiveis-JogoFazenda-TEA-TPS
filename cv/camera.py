"""
Câmera principal para reconhecimento de gestos.
Coordena todas as funcionalidades do sistema de reconhecimento.
"""

import cv2
import time
import mediapipe as mp
from cv.config import (
    CAMERA_WIDTH,
    CAMERA_HEIGHT,
    CAMERA_INDEX,
    SUPPORTED_GESTURES,
    SUPPORTED_OBJECTS,
)
from cv.zone_manager import ZoneManager
from cv.action_handler import ActionHandler
from cv.gesture_processor import GestureProcessor
from cv.object_processor import ObjectProcessor
from cv.visual_renderer import VisualRenderer


class GestureCamera:
    """
    Classe principal que coordena o reconhecimento de gestos e objetos.

    Responsabilidades:
    - Gerenciar a câmera e captura de frames
    - Coordenar os componentes do sistema
    - Executar o loop principal de reconhecimento
    """

    def __init__(self, game_controller=None):
        """
        Inicializa a câmera de reconhecimento.

        Args:
            game_controller: Controlador do jogo para comunicação
        """
        self.game_controller = game_controller
        self.stop_camera = False  # Flag para parar a câmera

        # Inicializar componentes
        self.zone_manager = ZoneManager()
        self.action_handler = ActionHandler(game_controller, self.zone_manager)
        self.gesture_processor = GestureProcessor(
            self.zone_manager, self.action_handler
        )
        self.object_processor = ObjectProcessor(
            self.zone_manager, self.action_handler
        )
        self.visual_renderer = VisualRenderer(self.zone_manager)

        # Configurar câmera
        self._setup_camera()

        print("Sistema de reconhecimento de gestos e objetos inicializado com sucesso!")
        print(f"Gestos suportados: {', '.join(SUPPORTED_GESTURES)}")
        print(f"Objetos suportados: {', '.join(SUPPORTED_OBJECTS)}")

    def _setup_camera(self):
        """Configura a câmera para captura de vídeo."""
        self.cap = cv2.VideoCapture(CAMERA_INDEX)

        if not self.cap.isOpened():
            raise IOError("Não foi possível abrir a câmera.")

        # Configurar resolução
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

        # Obter propriedades reais da câmera
        actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = self.cap.get(cv2.CAP_PROP_FPS)

        print(f"📷 PROPRIEDADES DA CÂMERA:")
        print(f"   📐 Resolução Real: {actual_width}x{actual_height}")
        print(f"   📐 Resolução Configurada: {CAMERA_WIDTH}x{CAMERA_HEIGHT}")
        print(f"   🎬 FPS: {fps}")

    def get_current_game_state(self):
        """
        Retorna o estado atual do jogo.

        Returns:
            str: Estado atual do jogo
        """
        return self.zone_manager.current_game_state

    def get_gesture_history(self):
        """
        Retorna o histórico de gestos.

        Returns:
            list: Histórico de gestos
        """
        return self.action_handler.get_gesture_history()

    def run(self):
        """
        Executa o loop principal de reconhecimento de gestos e objetos.

        Este método:
        1. Captura frames da câmera
        2. Processa gestos e objetos com MediaPipe
        3. Renderiza elementos visuais
        4. Exibe o resultado na tela
        """
        print("Iniciando reconhecimento de gestos e objetos. Pressione 'q' para sair.")

        try:
            while not self.stop_camera:
                # Capturar frame
                ret, frame = self.cap.read()
                if not ret:
                    print("Erro ao capturar frame da câmera.")
                    break

                # Espelhar frame horizontalmente
                frame = cv2.flip(frame, 1)

                # Converter para formato do MediaPipe
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

                # Processar gestos e objetos
                frame_timestamp_ms = int(time.time() * 1000)
                self.gesture_processor.recognize_async(mp_image, frame_timestamp_ms)
                self.object_processor.detect_async(mp_image, frame_timestamp_ms)

                # Renderizar frame
                frame = self._render_frame(frame)

                # Exibir frame
                cv2.imshow("Gesture & Object Recognition", frame)

                # Verificar tecla de saída
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    print("Tecla 'q' pressionada, encerrando...")
                    break

                # Pequeno delay para estabilidade
                time.sleep(0.01)

        except KeyboardInterrupt:
            print("Reconhecimento interrompido pelo usuário.")
        except Exception as e:
            print(f"Erro durante o reconhecimento: {e}")
        finally:
            self.cleanup()

    def _render_frame(self, frame):
        """
        Renderiza o frame com todas as informações visuais.

        Args:
            frame: Frame da câmera

        Returns:
            numpy.ndarray: Frame renderizado
        """
        # Obter dados atuais dos gestos
        gestures = self.gesture_processor.get_current_gestures()
        hand_landmarks = self.gesture_processor.get_current_hand_landmarks()
        handedness = self.gesture_processor.get_current_handedness()

        # Obter dados atuais dos objetos
        object_detections = self.object_processor.get_filtered_detections()

        # Obter estado atual do jogo
        game_state = self.get_current_game_state()

        # Renderizar frame
        return self.visual_renderer.render_frame(
            frame, gestures, hand_landmarks, handedness, game_state, object_detections
        )

    def stop(self):
        """Para a câmera de forma elegante."""
        print("🛑 Parando câmera...")
        self.stop_camera = True

    def cleanup(self):
        """Limpa recursos e fecha a câmera."""
        print("Limpando recursos...")

        # Parar câmera se ainda estiver rodando
        self.stop_camera = True

        # Fechar câmera
        if hasattr(self, "cap") and self.cap:
            self.cap.release()

        # Limpar processadores
        if hasattr(self, "gesture_processor"):
            self.gesture_processor.cleanup()
        if hasattr(self, "object_processor"):
            self.object_processor.cleanup()

        # Fechar janelas do OpenCV
        cv2.destroyAllWindows()

        print("Recursos limpos com sucesso.")

    def get_system_status(self):
        """
        Retorna o status atual do sistema.

        Returns:
            dict: Status do sistema
        """
        return {
            "camera_open": self.cap.isOpened() if hasattr(self, "cap") else False,
            "current_state": self.get_current_game_state(),
            "gesture_count": len(self.gesture_processor.get_current_gestures()),
            "object_count": len(self.object_processor.get_filtered_detections()),
            "history_size": len(self.get_gesture_history()),
            "zones_count": len(self.zone_manager.get_current_zones()),
        }
