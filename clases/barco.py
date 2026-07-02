import pygame

class BarcoInvasor(pygame.sprite.Sprite):
    def __init__(self, nivel_activo):
        super().__init__()
        self.nivel = nivel_activo
        
        # --- CARGA ULTRA SEGURA DEL RECURSO DESDE EL DISCO ---
        try:
            img_original = pygame.image.load("assets/interfaces/barco.png").convert_alpha()
            # === CAMBIO DE TAMAÑO: Pasamos de 120x80 a un masivo 190x130 para que sea un verdadero navío ===
            self.image_base = pygame.transform.scale(img_original, (190, 130))
        except Exception as e:
            print(f"Error crítico al cargar barco.png: {e}")
            self.image_base = pygame.Surface((190, 130), pygame.SRCALPHA)
            pygame.draw.rect(self.image_base, (139, 69, 19), (0, 30, 190, 100))

        # --- REGLA DE ORIENTACIÓN SEGÚN EL ESCENARIO (CALIBRACIÓN DE PÍXELES) ---
        if self.nivel == 1:
            # ESCENARIO 1 (CABILDO): Viaja de IZQUIERDA a DERECHA
            self.image = self.image_base
            self.pos_x = -260.0  # Lo tiramos un poco más atrás para compensar el nuevo ancho al nacer
            
            # === CAMBIO DE ALTURA: Bajamos de Y=520 a Y=690 para que navegue 100% sobre el río inferior ===
            self.pos_y = 618.0  
            self.destino_x = 140.0 # Punto donde el casco toca prolijo el muelle izquierdo del Cabildo
            self.velocidad = 1.2 
            
        else:
            # ESCENARIO 2 (CATEDRAL): Viaja de DERECHA a IZQUIERDA (Invertido)
            self.image = pygame.transform.flip(self.image_base, True, False)
            self.pos_x = 1200.0 
            
            # === CAMBIO DE ALTURA CATEDRAL: Calibrado en Y=710 para calzar con tu muelle inferior derecho ===
            self.pos_y = 630.0  
            self.destino_x = 914.0 # Punto exacto de amarre en las maderas de la Catedral
            self.velocidad = -1.2 

        self.rect = self.image.get_rect()
        self.rect.center = (int(self.pos_x), int(self.pos_y))
        self.ha_llegado = False
        self.ultimo_calculo_tiempo = pygame.time.get_ticks() # Guardamos el milisegundo de nacimiento


    # 2. Reemplazá TU método update completo por esta versión industrial:
    def update(self):
        """Maneja el desplazamiento del navío a velocidad constante con freno de inercia final."""
        tiempo_sistema = pygame.time.get_ticks()
        
        # === CANDADO DE ESTABILIZACIÓN VISUAL (MANTENIDO) ===
        if not hasattr(self, "primer_frame_completado"):
            self.primer_frame_completado = True
            self.ultimo_calculo_tiempo = tiempo_sistema
            return
            
        milisegundos_transcurridos = tiempo_sistema - self.ultimo_calculo_tiempo
        self.ultimo_calculo_tiempo = tiempo_sistema
        
        dt = milisegundos_transcurridos / 1000.0
        if dt > 0.05: 
            dt = 0.016

        # --- FÍSICA DE CRUCERO CON INERCIA AL FINAL (NUEVO) ---
        if not self.ha_llegado:
            # 1. Tu velocidad base constante de antes (46 píxeles por segundo real)
            velocidad_base = 46.0 if self.nivel == 1 else -46.0
            
            # 2. Calculamos la distancia absoluta en píxeles que le falta recorrer al casco
            distancia_restante = abs(self.destino_x - self.pos_x)
            
            # === EL FILTRO DE PROXIMIDAD INDUSTRIAL ===
            # Si el barco está a menos de 40 píxeles de tocar el muelle, activamos la desaceleración.
            # Dividimos la distancia restante por 40 para crear un factor que va de 1.0 a 0.0 progresivamente.
            if distancia_restante < 40.0:
                factor_frenado = max(0.2, distancia_restante / 40.0) # Ponemos un piso de 0.2 para que no se congele
                velocidad_dinamica = velocidad_base * factor_frenado
            else:
                # Si está lejos, viaja a tu velocidad constante original perfecta
                velocidad_dinamica = velocidad_base

            # 3. Avanzamos la posición física usando el Delta Time contra los FPS libres
            self.pos_x += velocidad_dinamica * dt
            
            if self.nivel == 1: # Cabildo
                if self.pos_x >= self.destino_x:
                    self.pos_x = self.destino_x
                    self.ha_llegado = True
                    print("[ COMANDANCIA ] ¡El navío español ha encallado suavemente en el puerto del Cabildo!")
            else: # Catedral
                if self.pos_x <= self.destino_x:
                    self.pos_x = self.destino_x
                    self.ha_llegado = True
                    print("[ COMANDANCIA ] ¡El navío español ha encallado suavemente en el puerto de la Catedral!")

            # Sincronizamos las coordenadas físicas con el contenedor de Pygame
            self.rect.centerx = int(self.pos_x)