"""
Módulo para gerenciar o áudio do jogo.
Controla a música de fundo e o volume geral do jogo.
"""

import pygame
import os


class AudioManager:
    """Gerencia o sistema de áudio do jogo."""

    def __init__(self, background_music_path=None, default_volume=1.0):
        """
        Inicializa o gerenciador de áudio.

        Args:
            background_music_path (str): Caminho para o arquivo de música de fundo
            default_volume (float): Volume inicial (0.0 a 1.0)
        """
        # Inicializar o mixer do pygame se ainda não foi inicializado
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        self.background_music_path = background_music_path
        self.current_volume = default_volume
        self.is_music_loaded = False
        self.is_playing = False

        # Carregar e tocar música de fundo se o caminho foi fornecido
        if background_music_path:
            self.load_background_music(background_music_path)

    def load_background_music(self, music_path):
        """
        Carrega a música de fundo.

        Args:
            music_path (str): Caminho para o arquivo de música
        """
        try:
            if os.path.exists(music_path):
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(self.current_volume)
                self.is_music_loaded = True
                self.background_music_path = music_path
                print(f"🎵 Música de fundo carregada: {music_path}")
            else:
                print(f"⚠️ Arquivo de música não encontrado: {music_path}")
                self.is_music_loaded = False
        except pygame.error as e:
            print(f"❌ Erro ao carregar música: {e}")
            self.is_music_loaded = False

    def play_background_music(self, loops=-1, start_position=0.0):
        """
        Inicia a reprodução da música de fundo.

        Args:
            loops (int): Número de repetições (-1 para loop infinito)
            start_position (float): Posição inicial em segundos
        """
        if self.is_music_loaded:
            try:
                pygame.mixer.music.play(loops=loops, start=start_position)
                self.is_playing = True
                print(f"▶️ Música de fundo iniciada (volume: {self.current_volume * 100:.0f}%)")
            except pygame.error as e:
                print(f"❌ Erro ao tocar música: {e}")
                self.is_playing = False
        else:
            print("⚠️ Nenhuma música carregada para tocar")

    def stop_background_music(self):
        """Para a música de fundo."""
        pygame.mixer.music.stop()
        self.is_playing = False
        print("⏹️ Música de fundo parada")

    def pause_background_music(self):
        """Pausa a música de fundo."""
        if self.is_playing:
            pygame.mixer.music.pause()
            print("⏸️ Música de fundo pausada")

    def unpause_background_music(self):
        """Retoma a música de fundo pausada."""
        pygame.mixer.music.unpause()
        print("▶️ Música de fundo retomada")

    def set_volume(self, volume):
        """
        Define o volume da música de fundo e de todos os sons.

        Args:
            volume (float): Valor de volume (0.0 a 1.0)
        """
        # Garantir que o valor está no intervalo válido
        self.current_volume = max(0.0, min(1.0, volume))
        
        # Atualizar volume da música de fundo
        pygame.mixer.music.set_volume(self.current_volume)
        
        print(f"🔊 Volume definido para: {self.current_volume * 100:.0f}%")

    def get_volume(self):
        """
        Retorna o volume atual.

        Returns:
            float: Volume atual (0.0 a 1.0)
        """
        return self.current_volume

    def get_volume_percentage(self):
        """
        Retorna o volume atual em porcentagem.

        Returns:
            float: Volume em porcentagem (0-100)
        """
        return self.current_volume * 100

    def is_music_playing(self):
        """
        Verifica se a música está tocando.

        Returns:
            bool: True se a música está tocando
        """
        return pygame.mixer.music.get_busy()

    def fadeout_music(self, milliseconds):
        """
        Diminui gradualmente o volume da música até parar.

        Args:
            milliseconds (int): Tempo em milissegundos para o fadeout
        """
        pygame.mixer.music.fadeout(milliseconds)
        print(f"🔉 Fadeout da música em {milliseconds}ms")

    def play_sound_effect(self, sound_path):
        """
        Toca um efeito sonoro.

        Args:
            sound_path (str): Caminho para o arquivo de som

        Returns:
            pygame.mixer.Sound or None: Objeto Sound ou None se houver erro
        """
        try:
            if os.path.exists(sound_path):
                sound = pygame.mixer.Sound(sound_path)
                sound.set_volume(self.current_volume)
                sound.play()
                print(f"🔔 Efeito sonoro tocado: {sound_path}")
                return sound
            else:
                print(f"⚠️ Arquivo de som não encontrado: {sound_path}")
                return None
        except pygame.error as e:
            print(f"❌ Erro ao tocar efeito sonoro: {e}")
            return None

    def cleanup(self):
        """Limpa recursos do gerenciador de áudio."""
        self.stop_background_music()
        pygame.mixer.quit()
        print("🔇 AudioManager limpo")

    def __del__(self):
        """Destrutor para garantir limpeza de recursos."""
        try:
            self.cleanup()
        except:
            pass

