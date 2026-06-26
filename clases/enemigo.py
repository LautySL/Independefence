import pygame
import math

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, camino, tipo="soldado_raso"):
        super().__init__()
        self.camino = camino
        self.indice_camino = 0
        self.tipo = tipo
        self.revelado = True
        
        # Estadísticas del GDD
        self.vida = 15
        self.velocidad = 1.5
        self.recompensa = 10
        self.danio = 1
        
        # Ruta base hacia la nueva carpeta de tus sprites sueltos
        ruta_base = "assets/enemigos/soldado/"
        
        # --- CARGA ULTRA SEGURA DE IMÁGENES SEPARADAS ---
        try:
            # 1. Animación Quietito (Stance) - 4 cuadros
            self.anim_quieto = [pygame.image.load(f"{ruta_base}soldadostance{i}.png").convert_alpha() for i in range(1, 5)]
            
            # 2. Animación Caminar hacia arriba (Up) - 8 cuadros
            self.anim_arriba = [pygame.image.load(f"{ruta_base}soldadoup{i}.png").convert_alpha() for i in range(1, 9)]
            
            # 3. Animación Caminar de costado (Run) - 8 cuadros (Se usa para derecha e izquierda)
            self.anim_correr = [pygame.image.load(f"{ruta_base}soldadorun{i}.png").convert_alpha() for i in range(1, 9)]
            
            # 4. Ataques - 5 y 6 cuadros
            self.anim_ataque1 = [pygame.image.load(f"{ruta_base}soldado1ataque{i}.png").convert_alpha() for i in range(1, 6)]
            self.anim_ataque2 = [pygame.image.load(f"{ruta_base}soldado2ataque{i}.png").convert_alpha() for i in range(1, 7)]
            
            # 5. Muerte (Death) - 6 cuadros
            self.anim_muerte = [pygame.image.load(f"{ruta_base}soldadodeath{i}.png").convert_alpha() for i in range(1, 7)]
            
        except Exception as e:
            print(f"Aviso de carga en sprites sueltos: {e}")
            # Bloque de auxilio gráfico por si te falta pasar o renombrar alguna foto
            aux = pygame.Surface((32, 32), pygame.SRCALPHA)
            pygame.draw.circle(aux, (220, 20, 60), (16, 16), 14)
            self.anim_quieto = self.anim_arriba = self.anim_correr = self.anim_ataque1 = self.anim_ataque2 = self.anim_muerte = [aux]

        # Estado inicial del motor de animación
        self.animacion_actual = self.anim_correr
        self.frame_actual = 0
        self.ultimo_refresco = pygame.time.get_ticks()
        self.velocidad_animacion = 100  # Milisegundos por fotograma
        self.espejar_horizontal = False # Control para el giro a la izquierda
        
        # Sprite activo en pantalla
        self.image = self.animacion_actual[self.frame_actual]
        self.rect = self.image.get_rect()
        
        if self.camino:
            self.rect.center = self.camino[0]
            
        self.pos_x = float(self.rect.centerx)
        self.pos_y = float(self.rect.centery)
        self.ha_llegado_al_final = False
        self.esta_muerto = False

        self.tiempo_ultimo_golpe = 0
        
        # --- VARIABLES PARA EL EFECTO FADE-OUT (DESVANECIMIENTO) ---
        self.opacidad_muerte = 255     # Arranca en 255 (totalmente opaco)
        self.reducir_opacidad = False   # Se activa recién cuando llega al último cuadro tirado


    def update(self):
        """Maneja el movimiento, decide la animacion y procesa el tinte de impacto."""
        if self.esta_muerto:
            self.actualizar_animacion_muerte()
            return

        # --- LÓGICA DE MOVIMIENTO POR WAYPOINTS ---
        if self.indice_camino < len(self.camino):
            objetivo = self.camino[self.indice_camino]
            
            dx = objetivo[0] - self.pos_x
            dy = objetivo[1] - self.pos_y
            distancia = math.hypot(dx, dy)
            
            if distancia > self.velocidad:
                # Determinamos la orientación de la animación en los ejes
                if abs(dy) > abs(dx) and dy < 0:
                    self.animacion_actual = self.anim_arriba
                    self.espejar_horizontal = False
                else:
                    self.animacion_actual = self.anim_correr
                    if dx < 0:
                        self.espejar_horizontal = True  # Fila roja (Mirando a la IZQUIERDA)
                    else:
                        self.espejar_horizontal = False # Puerto o calle alta (Mirando a la DERECHA)
                
                # Avanzamos la posición en base al vector unitario
                self.pos_x += (dx / distancia) * self.velocidad
                self.pos_y += (dy / distancia) * self.velocidad
                self.rect.centerx = int(self.pos_x)
                self.rect.centery = int(self.pos_y)
            else:
                self.indice_camino += 1
        else:
            self.ha_llegado_al_final = True

        # --- PROCESADOR DE ANIMACIÓN EN TIEMPO REAL ---
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_refresco > self.velocidad_animacion:
            self.frame_actual = (self.frame_actual + 1) % len(self.animacion_actual)
            self.ultimo_refresco = tiempo_actual

        # Asignamos el cuadro base segun corresponda el frame
        cuadro_base = self.animacion_actual[self.frame_actual]
        if self.espejar_horizontal:
            self.image = pygame.transform.flip(cuadro_base, True, False)
        else:
            self.image = cuadro_base.copy()

        # --- MOTOR DEL TINTE ROJO TRANSPARENTE EN CALIENTE ---
        if not self.esta_muerto and (tiempo_actual - self.tiempo_ultimo_golpe < 150):
            superficie_tinte = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            superficie_tinte.fill((255, 0, 0, 130))
            self.image.blit(superficie_tinte, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)


    def recibir_danio(self, cantidad, grupo_enemigos):
        """Aplica impacto, activa el flash de danio y gestiona la caida."""
        if self.esta_muerto:
            return
            
        self.vida -= cantidad
        
        # --- ACTIVAMOS EL FLASH DE DAÑO ---
        # Guardamos el fotograma exacto en el que sufrio el golpe para pintar el tinte rojo
        self.tiempo_ultimo_golpe = pygame.time.get_ticks()
        
        if self.vida <= 0:
            self.esta_muerto = True
            self.frame_actual = 0
            self.animacion_actual = self.anim_muerte
            
            # CORRECCIÓN: El cuadro de muerte inicial hereda la orientacion que traia el soldado en la calle
            cuadro_base = self.animacion_actual[self.frame_actual]
            if self.espejar_horizontal:
                self.image = pygame.transform.flip(cuadro_base, True, False)
            else:
                self.image = cuadro_base
                
            self.ultimo_refresco = pygame.time.get_ticks()

    def actualizar_animacion_muerte(self):
        """Muestra los 6 cuadros cayendo al piso y congela el ultimo fotograma para desvanecerlo."""
        tiempo_actual = pygame.time.get_ticks()
        
        # 1. Avanzamos en la lista hasta llegar al ultimo cuadro
        if not self.reducir_opacidad:
            if tiempo_actual - self.ultimo_refresco > self.velocidad_animacion:
                if self.frame_actual < len(self.anim_muerte) - 1:
                    self.frame_actual += 1
                    self.ultimo_refresco = tiempo_actual
                else:
                    # LLEGÓ AL ÚLTIMO CUADRO: Activamos el cerrojo para empezar a desvanecer
                    self.reducir_opacidad = True

        # 2. Forzamos a que mantenga la orientacion que traia en la calle
        cuadro_caida = self.anim_muerte[self.frame_actual]
        if self.espejar_horizontal:
            self.image = pygame.transform.flip(cuadro_caida, True, False).copy()
        else:
            self.image = cuadro_caida.copy()

        # 3. LOGICA DE DESVANECIMIENTO GRADUAL
        if self.reducir_opacidad:
            # Le restamos 5 puntos de opacidad en cada frame (A mayor numero, mas rapido desaparece)
            self.opacidad_muerte -= 5
            
            if self.opacidad_muerte <= 0:
                self.opacidad_muerte = 0
                self.kill() # RECIÉN ACÁ se elimina definitivamente el sprite del juego
            else:
                # El truco: Creamos una capa transparente y la multiplicamos para atenuar el cuerpo
                superficie_alfa = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
                superficie_alfa.fill((255, 255, 255, self.opacidad_muerte))
                self.image.blit(superficie_alfa, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)