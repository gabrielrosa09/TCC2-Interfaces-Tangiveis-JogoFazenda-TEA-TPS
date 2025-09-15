import threading
import time
from core.game import Game
from cv.camera import GestureCamera


class GameController:
    """Controlador principal que coordena o jogo e o sistema de gestos."""
    
    def __init__(self):
        self.game = None
        self.camera = None
        self.running = True
        
    def start_game(self):
        """Inicia o jogo em uma thread separada"""
        try:
            self.game = Game()
            print("🎮 Jogo iniciado")
            self.game.run()
            print("🎮 Jogo encerrado")
        except Exception as e:
            print(f"Erro ao iniciar jogo: {e}")
        
    def start_camera(self):
        """Inicia a câmera em uma thread separada"""
        try:
            # Passar referência do controlador para a câmera
            self.camera = GestureCamera(game_controller=self)
            print("📷 Câmera iniciada")
            self.camera.run()
            print("📷 Câmera encerrada")
        except Exception as e:
            print(f"Erro ao iniciar câmera: {e}")
            
    def run(self):
        """Executa jogo e câmera simultaneamente"""
        print("Iniciando sistema de jogo com reconhecimento de gestos...")
        
        # Criar threads para jogo e câmera
        self.game_thread = threading.Thread(target=self.start_game, daemon=True)
        self.camera_thread = threading.Thread(target=self.start_camera, daemon=True)
        
        # Iniciar as threads
        self.game_thread.start()
        time.sleep(1)  # Pequeno delay para o jogo inicializar
        self.camera_thread.start()
        
        try:
            # Manter o programa rodando
            while self.running:
                time.sleep(0.1)
                
                # Verificar se a câmera foi sinalizada para parar
                if self.camera and hasattr(self.camera, 'stop_camera') and self.camera.stop_camera:
                    print("📷 Câmera sinalizada para parar...")
                    break
                
                # Verificar status do sistema
                if self.camera:
                    status = self.camera.get_system_status()
                    if not status["camera_open"]:
                        print("Câmera foi fechada, encerrando...")
                        break
                        
        except KeyboardInterrupt:
            print("Encerrando programa...")
            self.running = False
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Limpa recursos do controlador"""
        print("Limpando recursos do controlador...")
        
        # Sinalizar para parar tudo
        self.running = False
        
        # Aguardar threads terminarem
        if hasattr(self, 'game_thread') and self.game_thread.is_alive():
            print("Aguardando thread do jogo terminar...")
            self.game_thread.join(timeout=2)
        
        if hasattr(self, 'camera_thread') and self.camera_thread.is_alive():
            print("Aguardando thread da câmera terminar...")
            self.camera_thread.join(timeout=2)
        
        # Limpar recursos da câmera
        if self.camera:
            self.camera.cleanup()
        
        print("Recursos limpos com sucesso.")


if __name__ == "__main__":
    try:
        controller = GameController()
        controller.run()
    except Exception as e:
        print(f"Erro fatal: {e}")
    finally:
        print("Programa encerrado.")