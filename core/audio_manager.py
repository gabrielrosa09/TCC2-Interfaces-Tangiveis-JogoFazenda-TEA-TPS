"""
Módulo para gerenciar o áudio do jogo.
Controla a música de fundo e o volume geral do jogo.
"""

import pygame
import os


class AudioManager:
    """Gerencia o sistema de áudio do jogo."""

    def __init__(self, background_music_path=None, default_volume=1.0, background_music_base_volume=1.0):
        """Inicializa o gerenciador de áudio."""
        # Inicializar o mixer do pygame se ainda não foi inicializado
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        self.background_music_path = background_music_path
        self.current_volume = default_volume  # Volume geral do jogo
        self.background_music_base_volume = background_music_base_volume  # Volume base da música
        self.is_music_loaded = False
        self.is_playing = False
        
        # Dicionário para armazenar volumes base de efeitos sonoros
        self.sound_base_volumes = {}

        # Carregar e tocar música de fundo se o caminho foi fornecido
        if background_music_path:
            self.load_background_music(background_music_path)

    def load_background_music(self, music_path):
        """Carrega a música de fundo."""
        try:
            if os.path.exists(music_path):
                pygame.mixer.music.load(music_path)
                # Aplicar volume: base_volume * volume_geral
                final_volume = self.background_music_base_volume * self.current_volume
                pygame.mixer.music.set_volume(final_volume)
                self.is_music_loaded = True
                self.background_music_path = music_path
                print(f"[AUDIO] Musica de fundo carregada: {music_path}")
                print(f"   Volume base: {self.background_music_base_volume * 100:.1f}% | Volume geral: {self.current_volume * 100:.0f}% | Volume final: {final_volume * 100:.2f}%")
            else:
                print(f"[AVISO] Arquivo de musica nao encontrado: {music_path}")
                self.is_music_loaded = False
        except pygame.error as e:
            print(f"[ERRO] Erro ao carregar musica: {e}")
            self.is_music_loaded = False

    def play_background_music(self, loops=-1, start_position=0.0):
        """Inicia a reprodução da música de fundo."""
        if self.is_music_loaded:
            try:
                pygame.mixer.music.play(loops=loops, start=start_position)
                self.is_playing = True
                print(f"[AUDIO] Musica de fundo iniciada (volume: {self.current_volume * 100:.0f}%)")
            except pygame.error as e:
                print(f"[ERRO] Erro ao tocar musica: {e}")
                self.is_playing = False
        else:
            print("[AVISO] Nenhuma musica carregada para tocar")

    def stop_background_music(self):
        """Para a música de fundo."""
        pygame.mixer.music.stop()
        self.is_playing = False
        print("[AUDIO] Musica de fundo parada")

    def pause_background_music(self):
        """Pausa a música de fundo."""
        if self.is_playing:
            pygame.mixer.music.pause()
            print("[AUDIO] Musica de fundo pausada")

    def unpause_background_music(self):
        """Retoma a música de fundo pausada."""
        pygame.mixer.music.unpause()
        print("[AUDIO] Musica de fundo retomada")

    def set_volume(self, volume):
        """Define o volume geral do jogo. Atualiza o volume da música de fundo e de todos os sons proporcionalmente."""
        # Garantir que o valor está no intervalo válido
        self.current_volume = max(0.0, min(1.0, volume))
        
        # Atualizar volume da música de fundo: base_volume * volume_geral
        final_music_volume = self.background_music_base_volume * self.current_volume
        pygame.mixer.music.set_volume(final_music_volume)
        
        print(f"[VOLUME] Volume geral definido para: {self.current_volume * 100:.0f}%")
        print(f"   Musica de fundo: {final_music_volume * 100:.2f}% (base: {self.background_music_base_volume * 100:.1f}%)")

    def get_volume(self):
        """Retorna o volume atual."""
        return self.current_volume

    def get_volume_percentage(self):
        """Retorna o volume atual em porcentagem."""
        return self.current_volume * 100

    def is_music_playing(self):
        """Verifica se a música está tocando."""
        return pygame.mixer.music.get_busy()

    def fadeout_music(self, milliseconds):
        """Diminui gradualmente o volume da música até parar."""
        pygame.mixer.music.fadeout(milliseconds)
        print(f"🔉 Fadeout da música em {milliseconds}ms")

    def play_sound_effect(self, sound_path, base_volume=1.0):
        """Toca um efeito sonoro."""
        try:
            if os.path.exists(sound_path):
                sound = pygame.mixer.Sound(sound_path)
                # Aplicar volume: base_volume * volume_geral
                final_volume = base_volume * self.current_volume
                sound.set_volume(final_volume)
                sound.play()
                print(f"[AUDIO] Efeito sonoro tocado: {sound_path}")
                print(f"   Volume base: {base_volume * 100:.1f}% | Volume geral: {self.current_volume * 100:.0f}% | Volume final: {final_volume * 100:.2f}%")
                return sound
            else:
                print(f"[AVISO] Arquivo de som nao encontrado: {sound_path}")
                return None
        except pygame.error as e:
            print(f"[ERRO] Erro ao tocar efeito sonoro: {e}")
            return None
    
    def register_sound(self, sound_name, sound_path, base_volume=1.0):
        """Registra um som com seu volume base."""
        self.sound_base_volumes[sound_name] = {
            "path": sound_path,
            "base_volume": base_volume
        }
        print(f"📝 Som registrado: {sound_name} (base: {base_volume * 100:.1f}%)")
    
    def play_registered_sound(self, sound_name):
        """Toca um som previamente registrado."""
        if sound_name in self.sound_base_volumes:
            sound_info = self.sound_base_volumes[sound_name]
            return self.play_sound_effect(sound_info["path"], sound_info["base_volume"])
        else:
            print(f"[AVISO] Som '{sound_name}' nao esta registrado")
            return None

    def cleanup(self):
        """Limpa recursos do gerenciador de áudio."""
        self.stop_background_music()
        pygame.mixer.quit()
        print("[AUDIO] AudioManager limpo")

    def __del__(self):
        """Destrutor para garantir limpeza de recursos."""
        try:
            self.cleanup()
        except:
            pass

