"""
Câmera principal para reconhecimento de gestos.
Coordena todas as funcionalidades do sistema de reconhecimento.
"""

import cv2
import time
import mediapipe as mp
from cv.config import CAMERA_WIDTH, CAMERA_HEIGHT, CAMERA_INDEX, SUPPORTED_GESTURES
from cv.zone_manager import ZoneManager
from cv.action_handler import ActionHandler
from cv.gesture_processor import GestureProcessor
from cv.visual_renderer import VisualRenderer


class GestureCamera:
    """
    Classe principal que coordena o reconhecimento de gestos.
    
    Responsabilidades:
    - Gerenciar a câmera e captura de frames
    - Coordenar os componentes do sistema
    - Executar o loop principal de reconhecimento
    """
    
    def __init__(self, game_controller=None):
        """
        Inicializa a câmera de gestos.
        
        Args:
            game_controller: Controlador do jogo para comunicação
        """
        self.game_controller = game_controller
        self.stop_camera = False  # Flag para parar a câmera
        
        # Inicializar componentes
        self.zone_manager = ZoneManager()
        self.action_handler = ActionHandler(game_controller, self.zone_manager)
        self.gesture_processor = GestureProcessor(self.zone_manager, self.action_handler)
        self.visual_renderer = VisualRenderer(self.zone_manager)
        
        # Configurar câmera
        self._setup_camera()
        
        print("Sistema de reconhecimento de gestos inicializado com sucesso!")
        print(f"Gestos suportados: {', '.join(SUPPORTED_GESTURES)}")
    
    def _setup_camera(self):
        """Configura a câmera para captura de vídeo."""
        self.cap = cv2.VideoCapture(CAMERA_INDEX)
        
        if not self.cap.isOpened():
            raise IOError("Não foi possível abrir a câmera.")
        
        # Configurar resolução
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
        
        print(f"Câmera configurada: {CAMERA_WIDTH}x{CAMERA_HEIGHT}")
    
    def set_game_state(self, state):
        """
        Define o estado atual do jogo.
        
        Args:
            state (str): Estado do jogo (menu, tutorial, game)
        """
        self.zone_manager.set_game_state(state)
    
    def get_current_game_state(self):
        """
        Retorna o estado atual do jogo.
        
        Returns:
            str: Estado atual do jogo
        """
        return self.zone_manager.current_game_state
    
    def get_gesture_info(self, hand_index=0):
        """
        Retorna informações sobre um gesto específico.
        
        Args:
            hand_index (int): Índice da mão (0 ou 1)
            
        Returns:
            dict or None: Informações do gesto ou None
        """
        return self.gesture_processor.get_gesture_info(hand_index)
    
    def get_gesture_history(self):
        """
        Retorna o histórico de gestos.
        
        Returns:
            list: Histórico de gestos
        """
        return self.action_handler.get_gesture_history()
    
    def clear_gesture_history(self):
        """Limpa o histórico de gestos."""
        self.action_handler.clear_history()
    
    def get_zone_info(self, zone_name):
        """
        Retorna informações sobre uma zona específica.
        
        Args:
            zone_name (str): Nome da zona
            
        Returns:
            str: Informações da zona
        """
        zone = self.zone_manager.get_zone_by_name(zone_name)
        return self.zone_manager.get_zone_info(zone)
    
    def add_zone(self, screen_state, zone):
        """
        Adiciona uma nova zona para um estado de tela.
        
        Args:
            screen_state (str): Estado da tela
            zone (dict): Dados da zona
        """
        self.zone_manager.add_zone(screen_state, zone)
    
    def remove_zone(self, screen_state, zone_name):
        """
        Remove uma zona de um estado de tela.
        
        Args:
            screen_state (str): Estado da tela
            zone_name (str): Nome da zona a ser removida
        """
        self.zone_manager.remove_zone(screen_state, zone_name)
    
    def run(self):
        """
        Executa o loop principal de reconhecimento de gestos.
        
        Este método:
        1. Captura frames da câmera
        2. Processa gestos com MediaPipe
        3. Renderiza elementos visuais
        4. Exibe o resultado na tela
        """
        print("Iniciando reconhecimento de gestos. Pressione 'q' para sair.")
        
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
                
                # Processar gestos
                frame_timestamp_ms = int(time.time() * 1000)
                self.gesture_processor.recognize_async(mp_image, frame_timestamp_ms)
                
                # Renderizar frame
                frame = self._render_frame(frame)
                
                # Exibir frame
                cv2.imshow('Gesture Recognition', frame)
                
                # Verificar tecla de saída
                if cv2.waitKey(1) & 0xFF == ord('q'):
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
        
        # Obter estado atual do jogo
        game_state = self.get_current_game_state()
        
        # Renderizar frame
        return self.visual_renderer.render_frame(
            frame, gestures, hand_landmarks, handedness, game_state
        )
    
    def run_single_frame(self):
        """
        Processa um único frame e retorna o resultado.
        
        Returns:
            tuple: (frame_processado, gestos_detectados)
        """
        ret, frame = self.cap.read()
        if not ret:
            return None, None
        
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        frame_timestamp_ms = int(time.time() * 1000)
        self.gesture_processor.recognize_async(mp_image, frame_timestamp_ms)
        
        # Aguardar processamento
        time.sleep(0.1)
        
        frame = self._render_frame(frame)
        gestures = self.gesture_processor.get_current_gestures()
        
        return frame, gestures
    
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
        if hasattr(self, 'cap') and self.cap:
            self.cap.release()
        
        # Limpar processador
        if hasattr(self, 'gesture_processor'):
            self.gesture_processor.cleanup()
        
        # Fechar janelas do OpenCV
        cv2.destroyAllWindows()
        
        print("Recursos limpos com sucesso.")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()
    
    def get_system_status(self):
        """
        Retorna o status atual do sistema.
        
        Returns:
            dict: Status do sistema
        """
        return {
            "camera_open": self.cap.isOpened() if hasattr(self, 'cap') else False,
            "current_state": self.get_current_game_state(),
            "gesture_count": len(self.gesture_processor.get_current_gestures()),
            "history_size": len(self.get_gesture_history()),
            "zones_count": len(self.zone_manager.get_current_zones())
        }