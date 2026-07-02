import pygame
import math

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, camino, tipo="soldado_raso"):
        super().__init__()
        self.camino = camino
        self.indice_camino = 0
        self.tipo = tipo
        self.revelado = True
        
        # ========================================================
        # DICCIONARIO INDUSTRIAL DE BALANCE DE TROPAS 
        # ========================================================
        # Centralizamos las estadísticas del GDD y los nombres de las carpetas
        balance_unidades = {
            "soldado_raso": {
                "vida": 15,
                "velocidad": 1.5,
                "recompensa": 10,
                "danio": 1,
                "ruta_base": "assets/enemigos/soldado/",
                "prefijo": "soldado"
            },
            "artillero": {
                "vida": 40,            
                "velocidad": 1.6,      
                "recompensa": 35,      
                "danio": 5,            
                "ruta_base": "assets/enemigos/artillero/", 
                "prefijo": "artillero"
            }
        }
        
        # Buscamos la configuración activa. Si no existe, usa el soldado común
        cfg = balance_unidades.get(self.tipo, balance_unidades["soldado_raso"])
        
        # Seteamos de forma dinámica TUS variables del GDD originales
        self.vida = cfg["vida"]
        self.velocidad = cfg["velocidad"]
        self.recompensa = cfg["recompensa"]
        self.danio = cfg["danio"]
        
        # Ruta dinámica hacia la carpeta del sprite correspondiente
        ruta_base = cfg["ruta_base"]
        pfx = cfg["prefijo"]
        # ========================================================
        
        # --- CARGA ULTRA SEGURA DE IMÁGENES SEPARADAS (ADAPTADA) ---
        try:
            # 1. Animación Quietito (Stance) - 4 cuadros
            self.anim_quieto = [pygame.image.load(f"{ruta_base}{pfx}stance{i}.png").convert_alpha() for i in range(1, 5)]
            
            # 2. Animación Caminar hacia arriba (Up) - 8 y 9 cuadros de forma dinámica
            # El soldado raso usa 8, pero tu artillero tiene 9 cuadros (del 1 al 9). Usamos len o rangos elásticos.
            rango_up = 10 if self.tipo == "artillero" else 9
            self.anim_arriba = [pygame.image.load(f"{ruta_base}{pfx}up{i}.png").convert_alpha() for i in range(1, rango_up)]
            
            # 3. Animación Caminar de costado (Run) - 8 y 5 cuadros de forma dinámica
            # Tu soldado raso usa 8, pero el artillerorun tiene 5 cuadros (del 1 al 5).
            rango_run = 6 if self.tipo == "artillero" else 9
            self.anim_correr = [pygame.image.load(f"{ruta_base}{pfx}run{i}.png").convert_alpha() for i in range(1, rango_run)]

            # === NUEVA INYECCIÓN: CAMINATA HACIA ABAJO (DOWN) ===
            # Ambos personajes tienen exactamente 4 cuadros (del 1 al 4)
            self.anim_abajo = [pygame.image.load(f"{ruta_base}{pfx}down{i}.png").convert_alpha() for i in range(1, 5)]
            
            # 4. Ataques (Por las dudas mapeamos los de tu soldado)
            if self.tipo == "artillero":
                # Como el artillero no los usa todavía, le ponemos una copia del run de auxilio técnico
                self.anim_ataque1 = self.anim_correr
                self.anim_ataque2 = self.anim_correr
            else:
                self.anim_ataque1 = [pygame.image.load(f"{ruta_base}{pfx}1ataque{i}.png").convert_alpha() for i in range(1, 6)]
                self.anim_ataque2 = [pygame.image.load(f"{ruta_base}{pfx}2ataque{i}.png").convert_alpha() for i in range(1, 7)]
            
            # 5. Muerte (Death) - 6 cuadros (Ambos soldados usan 6 fotogramas exactos)
            self.anim_muerte = [pygame.image.load(f"{ruta_base}{pfx}death{i}.png").convert_alpha() for i in range(1, 7)]
            
        except Exception as e:
            print(f"Aviso de carga en sprites de {self.tipo}: {e}")
            aux = pygame.Surface((32, 32), pygame.SRCALPHA)
            pygame.draw.circle(aux, (220, 20, 60) if self.tipo == "soldado_raso" else (215, 120, 0), (16, 16), 14)
            self.anim_quieto = self.anim_arriba = self.anim_correr = self.anim_ataque1 = self.anim_ataque2 = self.anim_muerte = [aux]

        # Estado inicial del motor de animación
        self.animacion_actual = self.anim_correr
        self.frame_actual = 0
        self.ultimo_refresco = pygame.time.get_ticks()
        self.velocidad_animacion = 100  
        self.espejar_horizontal = False 
        
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
        self.opacidad_muerte = 255     
        self.reducir_opacidad = False   
        self.tiempo_ultimo_golpe = 0
        
        # === VARIABLES PARA EL EFECTO FADE-IN DE NACIMIENTO ===
        self.opacidad_nacimiento = 0      # Arranca 100% invisible en el muelle/inicio
        self.fade_in_completo = False     # Bandera de control
        
        # === EL CANAL INVISIBLE DE FÁBRICA ===
        # Clonamos el cuadro inicial y le inyectamos opacidad 0 para que no parpadee al aparecer
        copia_nacimiento = self.image.copy()
        superficie_alfa_init = pygame.Surface(copia_nacimiento.get_size(), pygame.SRCALPHA)
        superficie_alfa_init.fill((255, 255, 255, self.opacidad_nacimiento))
        copia_nacimiento.blit(superficie_alfa_init, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.image = copia_nacimiento

        # === CANDADO ACÚSTICO DE CAÍDA ===
        self.ya_sonoc_caida = False # Evita el spam infinito del mp3 en el frame fijo

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
                if abs(dy) > abs(dx):
                    if dy < 0:
                        self.animacion_actual = self.anim_arriba
                        self.espejar_horizontal = False
                    else:
                        # NUEVO: Si dy es positivo, el enemigo está bajando por el mapa
                        self.animacion_actual = self.anim_abajo
                        self.espejar_horizontal = False
                else:
                    self.animacion_actual = self.anim_correr
                    if dx < 0:
                        self.espejar_horizontal = True  
                    else:
                        self.espejar_horizontal = False 
                
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

        # ========================================================
        # CANDADO DE SEGURIDAD CONTRA INDEXERROR 
        # ========================================================
        # Si el frame actual quedó desfasado por un cambio de calle o de tropa, lo reiniciamos a 0 para evitar que desborde el tamaño de la lista activa
        if self.frame_actual >= len(self.animacion_actual):
            self.frame_actual = 0

        # Asignamos el cuadro base de forma 100% segura contra desbordes
        cuadro_base = self.animacion_actual[self.frame_actual]
        if self.espejar_horizontal:
            self.image = pygame.transform.flip(cuadro_base, True, False)
        else:
            self.image = cuadro_base.copy()

        # ========================================================
        # LÓGICA DE FADE-IN EN CALIENTE
        # ========================================================
        if self.opacidad_nacimiento < 255:
            # Va sumando opacidad de forma limpia en cada ciclo
            self.opacidad_nacimiento += 12
            if self.opacidad_nacimiento >= 255:
                self.opacidad_nacimiento = 255
                self.fade_in_completo = True # Habilita tu barra de salud flotante
            
            # Aplicamos la multiplicación alfa de forma dinámica sobre el frame activo
            superficie_alfa_in = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            superficie_alfa_in.fill((255, 255, 255, self.opacidad_nacimiento))
            self.image.blit(superficie_alfa_in, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # ========================================================
        # AJUSTE DE OFFSETS VISUALES PARA EL ARTILLERO 
        # ========================================================
        if self.tipo == "artillero" and self.animacion_actual == self.anim_arriba:
            self.rect.centerx = int(self.pos_x) - 12
        else:
            self.rect.centerx = int(self.pos_x)
            
        self.rect.centery = int(self.pos_y)

        # --- MOTOR DEL TINTE ROJO TRANSPARENTE EN CALIENTE ---
        if not self.esta_muerto and (tiempo_actual - self.tiempo_ultimo_golpe < 150):
            superficie_tinte = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            superficie_tinte.fill((255, 0, 0, 130))
            self.image.blit(superficie_tinte, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # ========================================================
        # MOTOR DE BARRA DE SALUD FLOTANTE PARA ENEMIGOS 
        # ========================================================
        if not self.esta_muerto and self.fade_in_completo:
            ancho_total_barra = 26
            alto_barra = 4
            
            vida_maxima_unidad = 40 if self.tipo == "artillero" else 15
            porcentaje_salud = max(0.0, min(1.0, self.vida / vida_maxima_unidad))
            ancho_verde_actual = int(ancho_total_barra * porcentaje_salud)
            
            if porcentaje_salud > 0.5:
                color_dinamico = (int(510 * (1 - porcentaje_salud)), 235, 20)
            else:
                color_dinamico = (255, int(510 * porcentaje_salud), 20)
            
            ancho_orig, alto_orig = self.image.get_size()
            lienzo_expandido = pygame.Surface((ancho_orig, alto_orig + 10), pygame.SRCALPHA)
            
            # Estampamos el cuerpo 10 píxeles abajo para hacer el colchón de aire
            lienzo_expandido.blit(self.image, (0, 10))
            
            bx = (ancho_orig // 2) - (ancho_total_barra // 2)
            by = 2 
            
            pygame.draw.rect(lienzo_expandido, (10, 10, 20), (bx - 1, by - 1, ancho_total_barra + 2, alto_barra + 2))
            if ancho_verde_actual > 0:
                pygame.draw.rect(lienzo_expandido, color_dinamico, (bx, by, ancho_verde_actual, alto_barra))
                
            self.image = lienzo_expandido
            
            # Compensamos el contenedor en el eje Y para que pise la calle empedrada
            self.rect.centery = int(self.pos_y) - 10

    def recibir_danio(self, cantidad, grupo_enemigos, administrador_sonidos=None):
        """Aplica impacto, activa el flash de danio y gestiona la caida."""
        if self.esta_muerto:
            return
            
        self.vida -= cantidad
        # Guardamos el fotograma exacto en el que sufrio el golpe para pintar el tinte rojo
        self.tiempo_ultimo_golpe = pygame.time.get_ticks()
        
        if self.vida <= 0:
            self.esta_muerto = True
            self.frame_actual = 0
            self.animacion_actual = self.anim_muerte
            
            # === GUARDAMOS EL MÁNAGER EN LA ENTIDAD (NUEVO) ===
            # Almacenamos el canal de sonido en la memoria del objeto soldado
            self.sound_manager_ref = administrador_sonidos
            
            cuadro_base = self.animacion_actual[self.frame_actual]
            if self.espejar_horizontal:
                self.image = pygame.transform.flip(cuadro_base, True, False)
            else:
                self.image = cuadro_base
                
            self.ultimo_refresco = pygame.time.get_ticks()

    def actualizar_animacion_muerte(self):
        """Muestra los 6 cuadros cayendo al piso en sintonía con el eje expandido."""
        tiempo_actual = pygame.time.get_ticks()
        
        if not self.reducir_opacidad:
            if tiempo_actual - self.ultimo_refresco > self.velocidad_animacion:
                if self.frame_actual < len(self.anim_muerte) - 1:
                    self.frame_actual += 1
                    self.ultimo_refresco = tiempo_actual
                    
                    if self.frame_actual == 3 and not self.ya_sonoc_caida:
                        self.ya_sonoc_caida = True 
                        import inspect
                        for frame_info in inspect.stack():
                            if "administrador_sonidos" in frame_info.frame.f_locals:
                                snd_manager = frame_info.frame.f_locals["administrador_sonidos"]
                                if snd_manager is not None:
                                    snd_manager.play_caida()
                                break
                else:
                    self.reducir_opacidad = True

        cuadro_caida = self.anim_muerte[self.frame_actual]
        if self.espejar_horizontal:
            cuadro_final = pygame.transform.flip(cuadro_caida, True, False).copy()
        else:
            cuadro_final = cuadro_caida.copy()

        # === COMPENSACIÓN DE LA TRANSICIÓN DE MUERTE ===
        # Aplicamos el mismo colchón de 10 píxeles a la caída para que enganche perfecto con la caminata
        ancho_orig, alto_orig = cuadro_final.get_size()
        lienzo_muerte_expandido = pygame.Surface((ancho_orig, alto_orig + 10), pygame.SRCALPHA)
        lienzo_muerte_expandido.blit(cuadro_final, (0, 10))
        self.image = lienzo_muerte_expandido
        self.rect.centery = int(self.pos_y) - 10

        if self.reducir_opacidad:
            self.opacidad_muerte -= 5
            if self.opacidad_muerte <= 0:
                self.opacidad_muerte = 0
                self.kill() 
            else:
                superficie_alfa = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
                superficie_alfa.fill((255, 255, 255, self.opacidad_muerte))
                self.image.blit(superficie_alfa, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    def cargar_sprites_unidad(self, config):
        """Busca y levanta secuencialmente las imágenes pixel art de la carpeta."""
        try:
            # Caminata Regular (artillerorun (1).png al 5)
            for i in range(1, config["anim_run"] + 1):
                img = pygame.image.load(f"assets/enemigos/{self.prefijo}run ({i}).png").convert_alpha()
                self.animaciones["run"].append(img)
                
            # Caminata hacia Arriba (artilleroup (1).png al 9)
            for i in range(1, config["anim_up"] + 1):
                img = pygame.image.load(f"assets/enemigos/{self.prefijo}up ({i}).png").convert_alpha()
                self.animaciones["up"].append(img)
                
            # Animación de Caída/Muerte (artillerodeath (1).png al 6)
            for i in range(1, config["anim_death"] + 1):
                img = pygame.image.load(f"assets/enemigos/{self.prefijo}death ({i}).png").convert_alpha()
                self.animaciones["death"].append(img)
        except Exception as e:
            print(f"Aviso de texturas para {self.tipo}: Usando bloques de auxilio. Motivo: {e}")
            # Auxilio visual por si falta acomodar alguna carpeta en el disco
            vacio = pygame.Surface((32, 48), pygame.SRCALPHA)
            pygame.draw.rect(vacio, (200, 0, 0), (0, 0, 32, 48))
            self.animaciones["run"] = [vacio] * config["anim_run"]
            self.animaciones["up"] = [vacio] * config["anim_up"]
            self.animaciones["death"] = [vacio] * config["anim_death"]