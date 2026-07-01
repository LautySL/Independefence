import pygame
import random

class SoundManager:
    def __init__(self):
        # 1. BANDERAS DE CONTROL INTERNO (Añadido control de combate)
        self.musica_menu_sonando = False
        self.musica_combate_sonando = False
        
        # 2. CARGA DE MÚSICA DE FONDO (.mp3 por Streaming)
        pygame.mixer.music.set_volume(0.4) # Volumen inicial al 40%
        self.ruta_musica_menu = "musica/War Plan - Devine-King [Ambient].mp3"
        self.ruta_musica_juego = "musica/March Of The Micmacs - Egan [International].mp3"

        try:
            pygame.mixer.music.load(self.ruta_musica_menu)
        except Exception as e:
            print(f"Aviso de música: No se pudo cargar {self.ruta_musica_menu}: {e}")

        # 3. CARGA DE EFECTOS DE SONIDO FX (Formatos cortos en memoria)
        try:
            self.snd_hover = pygame.mixer.Sound("assets/sonidos/point.mp3")
            self.snd_hover.set_volume(0.5)
            
            # Pack aleatorio de sonidos para avanzar
            self.snds_siguiente = [
                pygame.mixer.Sound("assets/sonidos/siguiente1.mp3"),
                pygame.mixer.Sound("assets/sonidos/siguiente2.mp3"),
                pygame.mixer.Sound("assets/sonidos/siguiente3.mp3")
            ]
            
            # Pack aleatorio de sonidos para retroceder
            self.snds_volver = [
                pygame.mixer.Sound("assets/sonidos/volver1.mp3"),
                pygame.mixer.Sound("assets/sonidos/volver2.mp3"),
                pygame.mixer.Sound("assets/sonidos/volver3.mp3")
            ]
        except Exception as e:
            print(f"Error al cargar efectos FX de sonido: {e}")
            self.snd_hover = None
            self.snds_siguiente = []
            self.snds_volver = []

    def reproducir_musica_menu(self):
        """Enciende la banda sonora colonial en bucle si no estaba sonando ya."""
        if not self.musica_menu_sonando:
            try:
                pygame.mixer.music.load(self.ruta_musica_menu)
                pygame.mixer.music.play(-1)
                self.musica_menu_sonando = True
                self.musica_combate_sonando = False # <-- OBLIGATORIO: Libera el candado de guerra al volver al inicio
            except:
                pass

    def reproducir_musica_combate(self):
        """Activa la marcha militar de guerra en loop infinito en cualquier nivel activo."""
        # El cerrojo: si la bandera ya es True, la función rebota y deja correr el tema libremente
        if not self.musica_combate_sonando:
            try:
                # Forzamos el encendido de la bandera en el microsegundo uno ANTES de la carga
                # Esto blinda el motor para que no haya duplicaciones por frames lentos
                self.musica_combate_sonando = True
                self.musica_menu_sonando = False
                
                print(f"[ SoundManager ] ¡A las armas! Sonando en loop: {self.ruta_musica_juego}")
                pygame.mixer.music.load(self.ruta_musica_juego)
                pygame.mixer.music.play(-1) # Loop infinito de combate
            except Exception as e:
                print(f"Error crítico al cargar la marcha de combate: {e}")
                # Si falló la carga física del disco, liberamos el cerrojo por seguridad
                self.musica_combate_sonando = False 

    def detener_musica(self):
        """Apaga el streaming de audio por completo de la memoria RAM."""
        pygame.mixer.music.stop()
        self.musica_menu_sonando = False
        self.musica_combate_sonando = False # <-- OBLIGATORIO: Apaga ambos hilos en seco

    def play_hover(self):
        """Gatilla el pitido corto al pasar el cursor por los botones."""
        if self.snd_hover:
            self.snd_hover.play()

    def play_siguiente(self):
        """Dispara un audio de avance aleatorio de la ticketera."""
        if self.snds_siguiente:
            random.choice(self.snds_siguiente).play()

    def play_volver(self):
        """Dispara un audio de retroceso aleatorio de la ticketera."""
        if self.snds_volver:
            random.choice(self.snds_volver).play()