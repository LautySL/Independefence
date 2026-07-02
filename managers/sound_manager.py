import pygame
import random

class SoundManager:
    def __init__(self):
        # 1. BANDERAS DE CONTROL INTERNO
        self.musica_menu_sonando = False
        self.musica_combate_sonando = False
        
        # === BILLETERA DE VOLUMEN CENTRALIZADA (NUEVO) ===
        # Ambos inicializados en el 40% que me pediste para arrancar simétricos
        self.vol_musica = 0.4
        self.vol_fx = 0.4
        
        # Inicializamos en None para evitar cualquier tipo de AttributeError en la RAM
        self.snd_hover = None
        self.snd_caching = None
        self.snd_victoria = None
        self.snd_gameover = None
        self.snds_siguiente = []
        self.snds_volver = []
        
        # 2. CARGA DE MÚSICA DE FONDO (.mp3 por Streaming)
        pygame.mixer.music.set_volume(self.vol_musica) # Usa tu 40% inicial de forma segura
        self.ruta_musica_menu = "musica/War Plan - Devine-King [Ambient].mp3"
        self.ruta_musica_juego = "musica/March Of The Micmacs - Egan [International].mp3"

        try:
            pygame.mixer.music.load(self.ruta_musica_menu)
        except Exception as e:
            print(f"Aviso de música: No se pudo cargar {self.ruta_musica_menu}: {e}")

        # 3. CARGA DE EFECTOS BASE DEL MENÚ (Aislado de fallas externas)
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
            print(f"Error al cargar efectos FX base del menú: {e}")

        # 4. CARGA AISLADA DEL EFECTO DE COMPRA "CA-CHING"
        try:
            self.snd_caching = pygame.mixer.Sound("assets/sonidos/ca-ching.mp3")
            self.snd_caching.set_volume(0.6)
        except Exception as e:
            print(f"Aviso: No se encontró el archivo ca-ching.mp3: {e}")

        # 5. CARGA AISLADA DE CLÍMAX DE VICTORIA
        try:
            self.snd_victoria = pygame.mixer.Sound("assets/sonidos/victoria.mp3")
            self.snd_victoria.set_volume(0.7) 
        except Exception as e:
            print(f"Aviso: No se pudo cargar assets/sonidos/victoria.mp3: {e}")

        # 6. CARGA AISLADA DE CLÍMAX DE DERROTA
        try:
            self.snd_gameover = pygame.mixer.Sound("assets/sonidos/gameover.mp3")
            self.snd_gameover.set_volume(0.7)
        except Exception as e:
            print(f"Aviso: No se pudo cargar assets/sonidos/gameover.mp3: {e}")

        # 7. CARGA AISLADA DEL EFECTO DEL ENGRANAJE
        self.snd_gear = None
        try:
            self.snd_gear = pygame.mixer.Sound("assets/sonidos/gear.mp3")
            self.snd_gear.set_volume(0.5) 
        except Exception as e:
            print(f"Aviso: No se pudo cargar assets/sonidos/gear.mp3: {e}")

        # 8. CUENTA REGRESIVA
        self.snd_countdown = None
        self.snd_lowcountdown = None

        try:
            self.snd_countdown = pygame.mixer.Sound("assets/sonidos/countdown.mp3")
            self.snd_countdown.set_volume(0.6) # Volumen prudente
        except Exception as e:
            print(f"Aviso: No se pudo cargar assets/sonidos/countdown.mp3: {e}")

        try:
            self.snd_lowcountdown = pygame.mixer.Sound("assets/sonidos/lowcountdown.mp3")
            self.snd_lowcountdown.set_volume(0.7) # Un POCO más fuerte por la urgencia
        except Exception as e:
            print(f"Aviso: No se pudo cargar assets/sonidos/lowcountdown.mp3: {e}")

        # 9. CARGA AISLADA DEL EFECTO DE DISPARO DE TORRES (NUEVO)
        self.snd_disparo = None
        try:
            self.snd_disparo = pygame.mixer.Sound("assets/sonidos/disparo.mp3")
            self.snd_disparo.set_volume(0.4) # Volumen prudente para que no sature si hay muchos gauchos
        except Exception as e:
            print(f"Aviso: No se pudo cargar assets/sonidos/disparo.mp3: {e}")

        # 10. PACK ALEATORIO DE CAÍDA DE ENEMIGOS (NUEVO)
        self.snds_caida = []
        try:
            # Cargamos secuencialmente los 5 archivos caida1.mp3 al 5
            self.snds_caida = [pygame.mixer.Sound(f"assets/sonidos/caida{i}.mp3") for i in range(1, 6)]
            # Ajustamos un volumen sutil para que el golpe contra el suelo no opaque los disparos
            for snd in self.snds_caida: snd.set_volume(self.vol_fx * 0.5)
        except Exception as e:
            print(f"Aviso: No se pudo cargar el pack de caídas: {e}")

        # 11. AUDIO DE IMPACTO INICIAL DE LAS HORDAS POR ESCENARIO (NUEVO)
        self.snd_campana_cabildo = None
        self.snds_catedral = []

        try:
            self.snd_campana_cabildo = pygame.mixer.Sound("assets/sonidos/campana.mp3")
            self.snd_campana_cabildo.set_volume(0.6) # Sonido fuerte e imponente
        except Exception as e:
            print(f"Aviso: No se pudo cargar assets/sonidos/campana.mp3: {e}")

        try:
            # Cargamos tus dos pistas alternativas para la Catedral metropolitana
            self.snds_catedral = [
                pygame.mixer.Sound("assets/sonidos/catedral1.mp3"),
                pygame.mixer.Sound("assets/sonidos/catedral2.mp3")
            ]
            for snd in self.snds_catedral: snd.set_volume(0.6)
        except Exception as e:
            print(f"Aviso: No se pudo cargar el pack de audios de catedral: {e}")

    # ========================================================
    # CONTROLADORES DE VOLUMEN DINÁMICOS EN CALIENTE (NUEVO)
    # ========================================================
    def actualizar_volumen_musica(self, nuevo_volumen):
        """Modifica el volumen del streaming de fondo en tiempo real (0.0 a 1.0)."""
        self.vol_musica = max(0.0, min(1.0, nuevo_volumen))
        pygame.mixer.music.set_volume(self.vol_musica)

    def actualizar_volumen_fx(self, nuevo_volumen):
        """Calibra el volumen de absolutamente todos los audios cortos en caliente."""
        self.vol_fx = max(0.0, min(1.0, nuevo_volumen))
        
        # Le pisamos el volumen individual a cada efecto cargado si existen en la memoria
        if self.snd_hover: self.snd_hover.set_volume(self.vol_fx)
        if self.snd_caching: self.snd_caching.set_volume(self.vol_fx)
        if self.snd_gear: self.snd_gear.set_volume(self.vol_fx)
        if self.snd_victoria: self.snd_victoria.set_volume(self.vol_fx)
        if self.snd_gameover: self.snd_gameover.set_volume(self.vol_fx)
        if self.snd_gameover: self.snd_gameover.set_volume(self.vol_fx)
        if self.snd_disparo: self.snd_disparo.set_volume(self.vol_fx)
        
        # SINCRO DE LISTAS: Recorremos los efectos aleatorios de forma legal contra el spam
        for snd in self.snds_siguiente:
            if snd: snd.set_volume(self.vol_fx)
        for snd in self.snds_volver:
            if snd: snd.set_volume(self.vol_fx)
        for snd in self.snds_caida:
            if snd: snd.set_volume(self.vol_fx * 0.5)

        if self.snd_campana_cabildo: self.snd_campana_cabildo.set_volume(self.vol_fx * 1.2)
        for snd in self.snds_catedral:
            if snd: snd.set_volume(self.vol_fx * 1.2)

    # ========================================================
    # MÉTODOS DE REPRODUCCIÓN (TUS LÍNEAS NATIVAS ACTUALES)
    # ========================================================
    def reproducir_musica_menu(self):
        """Enciende la banda sonora colonial en bucle si no estaba sonando ya."""
        if not self.musica_menu_sonando:
            try:
                pygame.mixer.music.load(self.ruta_musica_menu)
                pygame.mixer.music.play(-1)
                self.musica_menu_sonando = True
                self.musica_combate_sonando = False
            except:
                pass

    def reproducir_musica_combate(self):
        """Activa la marcha militar de guerra en loop infinito en cualquier nivel activo."""
        if not self.musica_combate_sonando:
            try:
                self.musica_combate_sonando = True
                self.musica_menu_sonando = False
                print(f"[ SoundManager ] ¡A las armas! Sonando en loop: {self.ruta_musica_juego}")
                pygame.mixer.music.load(self.ruta_musica_juego)
                pygame.mixer.music.set_volume(self.vol_musica) # Asegura escuchar tu barra de volumen
                pygame.mixer.music.play(-1, 0.0)
            except Exception as e:
                print(f"Error crítico al cargar la marcha de combate: {e}")
                self.musica_combate_sonando = False

    def detener_musica(self):
        """Apaga el streaming de audio por completo de la memoria RAM."""
        pygame.mixer.music.stop()
        self.musica_menu_sonando = False
        self.musica_combate_sonando = False

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

    def play_caching(self):
        """Gatilla el sonido monetario al desplegar tropas patrias en la grilla."""
        if self.snd_caching:
            self.snd_caching.play()

    def play_victoria(self):
        """Gatilla la orquesta triunfal al defender el Cabildo de forma exitosa."""
        if self.snd_victoria:
            self.snd_victoria.play()

    def play_gameover(self):
        """Dispara la melodía de derrota cuando las hordas españolas quiebran tu base."""
        if self.snd_gameover:
            self.snd_gameover.play()

    def play_gear(self):
        """Gatilla el sonido mecánico al presionar el engranaje de opciones."""
        if self.snd_gear:
            self.snd_gear.play()

    def play_countdown(self):
        """Gatilla la alerta regular de preparación (De 8 a 3 segundos)."""
        if self.snd_countdown:
            self.snd_countdown.play()

    def play_lowcountdown(self):
        """Gatilla la alerta crítica de horda inminente (De 3 a 0 segundos)."""
        if self.snd_lowcountdown:
            self.snd_lowcountdown.play()

    def play_disparo(self):
        """Gatilla el sonido de mosquete cuando una torre aliada abre fuego."""
        if self.snd_disparo:
            self.snd_disparo.play()

    def play_caida(self):
        """Dispara un audio de impacto aleatorio forzando un canal libre en el mixer."""
        if self.snds_caida:
            # Elegimos uno de tus 5 mp3 de caídas al azar
            sonido_elegido = random.choice(self.snds_caida)
            
            # TRUCO INDUSTRIAL: Usamos play(loops=0, maxtime=0, fade_ms=0) o buscamos un canal disponible.
            # En Pygame, llamar a pygame.mixer.find_channel(True) busca un canal libre en la RAM 
            # y, si están todos ocupados, corta el sonido más viejo (el disparo viejo) para hacer sonar la caída.
            canal_libre = pygame.mixer.find_channel(True)
            if canal_libre:
                canal_libre.play(sonido_elegido)

    def play_campana_cabildo(self):
        """Gatilla las campanas tradicionales en el segundo cero del Cabildo."""
        if self.snd_campana_cabildo:
            self.snd_campana_cabildo.play()

    def play_alerta_catedral(self):
        """Elige al azar uno de tus dos mp3 de catedral para el segundo cero."""
        if self.snds_catedral:
            random.choice(self.snds_catedral).play()