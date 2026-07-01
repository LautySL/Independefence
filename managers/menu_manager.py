import pygame
import math
import random
from config import constants as cte

class MenuManager:
    
    def __init__(self):
        self.ultimo_sonido_hover_global = 0
        
        # --- CARGA INTEGRADA DE RECURSOS EN LA MEMORIA DEL OBJETO ---
        try:
            # 1. Cargamos y escalamos el logotipo oficial de Independefence
            img_logo = pygame.image.load("assets/Independefence.png").convert_alpha()
            self.logo_juego = pygame.transform.scale(img_logo, (450, 150))
            
            # 2. Cargamos y escalamos el fondo grande para el paneo cinemático
            img_fondo = pygame.image.load("assets/interfaces/menu_principal.png").convert()
            self.fondo_menu_grande = pygame.transform.scale(img_fondo, (1124, 868))

            # --- INYECCIÓN: FONDOS ESTÁTICOS DE PANTALLAS FINALES Y MAPAS ---
            # Victoria Definitiva
            img_vic = pygame.image.load("assets/interfaces/mision_cumplida.png").convert()
            self.fondo_victoria = pygame.transform.scale(img_vic, (cte.ANCHO_DE_PANTALLA, cte.ALTO_DE_PANTALLA))
            
            # Selección de Niveles
            img_sel = pygame.image.load("assets/interfaces/seleccion_de_nivel.png").convert()
            self.fondo_seleccion = pygame.transform.scale(img_sel, (cte.ANCHO_DE_PANTALLA, cte.ALTO_DE_PANTALLA))
            
            # Derrota Definitiva
            img_gov = pygame.image.load("assets/interfaces/game_over.png").convert()
            self.fondo_game_over = pygame.transform.scale(img_gov, (cte.ANCHO_DE_PANTALLA, cte.ALTO_DE_PANTALLA))

            # Bienvenida
            img_bien = pygame.image.load("assets/interfaces/Pantalla_de_bienvenida.png").convert()
            self.fondo_bienvenida = pygame.transform.scale(img_bien, (cte.ANCHO_DE_PANTALLA, cte.ALTO_DE_PANTALLA))
            
        except Exception as e:
            print(f"Error al cargar recursos estéticos en el MenuManager: {e}")
            self.logo_juego = self.fondo_menu_grande = None
            self.fondo_victoria = self.fondo_seleccion = self.fondo_game_over = None

    # ========================================================
    # FUNCIONES AUXILIARES PARA CADA PANTALLA DEL DIAGRAMA
    # ========================================================

    # CORRECCIÓN DEFINITIVA: Tabulado a la derecha y con 'self' incorporado en el paréntesis
    def dibujar_bienvenida(self, pantalla, f_tit, f_bot):
        # El truco: Leemos la variable directamente desde self de forma interna
        if self.fondo_bienvenida:
            pantalla.blit(self.fondo_bienvenida, (0, 0))
        else:
            pantalla.fill(cte.BLACK)

        # --- INDICADOR INFERIOR CON CONTORNO REAL ---
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            texto_start = "PULSA CUALQUIER TECLA PARA EMPEZAR"
            color_crema = (245, 222, 179) 
            color_borde = (0, 0, 0)       

            surf_borde = f_bot.render(texto_start, True, color_borde)
            surf_frente = f_bot.render(texto_start, True, color_crema)
            rect_final = surf_frente.get_rect(center=(512, 630))

            for dx, dy in [(-2,0), (2,0), (0,-2), (0,2), (-2,-2), (2,-2), (-2,2), (2,2)]:
                pantalla.blit(surf_borde, (rect_final.x + dx, rect_final.y + dy))
            
            pantalla.blit(surf_frente, rect_final)

    # CORRECCIÓN DE CABECERA: Borramos 'ultimo_sonido_hover' del final del parentesis
    def dibujar_menu_principal(self, pantalla, f_tit, pos_mouse, btn_com, btn_glo, btn_cre, btn_sal, click_presionado, tiempo_actual):
        import math 
    
        # El truco: leemos las variables directamente desde self de forma interna
        if self.fondo_menu_grande:
            velocidad_paneo = tiempo_actual / 1500.0
            desvio_x = int(-50 + math.sin(velocidad_paneo) * 50)
            desvio_y = int(-50 + math.cos(velocidad_paneo * 0.8) * 50)
            pantalla.blit(self.fondo_menu_grande, (desvio_x, desvio_y))
        else:
            pantalla.fill((30, 30, 30))
    
        if self.logo_juego:
            pantalla.blit(self.logo_juego, self.logo_juego.get_rect(center=(512, 110)))
        else:
            self.blit_con_contorno(pantalla, "INDEPENDEFENCE", f_tit, (245, 222, 179), (512, 120), es_centro=True)

        # === BOTONERA ULTRA COMPACTA E INTELIGENTE ===
        # Le pasamos la lista entera una sola vez y el método se encarga del resto
        r_jugar = self.dibujar_boton_imagen(pantalla, btn_com, 512, 240, pos_mouse, click_presionado)
        r_glosario = self.dibujar_boton_imagen(pantalla, btn_glo, 512, 340, pos_mouse, click_presionado)
        r_creditos = self.dibujar_boton_imagen(pantalla, btn_cre, 512, 440, pos_mouse, click_presionado)
        r_salir = self.dibujar_boton_imagen(pantalla, btn_sal, 512, 540, pos_mouse, click_presionado)
    
        return r_jugar, r_glosario, r_creditos, r_salir

    def dibujar_seleccion_niveles(self, pantalla, f_tit, f_bot, pos_mouse, nivel_5_desbloqueado, dict_postales, click_presionado):
        """Dibuja la grilla de las postales con tamaño y altura calibrables a gusto por el programador."""
        if self.fondo_seleccion:
            pantalla.blit(self.fondo_seleccion, (0, 0))
        else:
            pantalla.fill((255, 235, 205))
            
        self.blit_con_contorno(pantalla, "SELECCION DE CAMPANAS", f_tit, (255, 215, 0), (512, 60), es_centro=True)
        
        tamano_letra_gusto = 32 
        f_ajustable = pygame.font.Font(None, tamano_letra_gusto) # Si usás un .ttf, cambialo por None

        # 2. ALTURA EN FILA SUPERIOR (Cabildo y Catedral)
        altura_y_superior = 135 

        # 3. ALTURA EN FILA INFERIOR (Fortín y Recova)
        altura_y_inferior = 435 
        
        color_letras = (255, 255, 255) # Blanco puro con contorno negro

        # === APLICACIÓN MILIMÉTRICA EN LA GRILLA ===
        # Nivel 1: El Cabildo (Centro vertical X = 340)
        self.blit_con_contorno(pantalla, "EL CABILDO", f_ajustable, color_letras, (340, altura_y_superior), es_centro=True)
        r_n1 = self.dibujar_postal_nivel(pantalla, dict_postales["c1"], 215, 135, pos_mouse, click_presionado)
        
        # Nivel 2: La Catedral (Centro vertical X = 684)
        self.blit_con_contorno(pantalla, "LA CATEDRAL", f_ajustable, color_letras, (684, altura_y_superior), es_centro=True)
        r_n2 = self.dibujar_postal_nivel(pantalla, dict_postales["c2"], 559, 135, pos_mouse, click_presionado)
        
        # Nivel 3: El Fortín (Centro vertical X = 340)
        self.blit_con_contorno(pantalla, "EL FORTIN", f_ajustable, color_letras, (340, altura_y_inferior), es_centro=True)
        r_n3 = self.dibujar_postal_nivel(pantalla, dict_postales["c3"], 215, 435, pos_mouse, click_presionado)
        
        # Nivel 4: La Recova (Centro vertical X = 684)
        self.blit_con_contorno(pantalla, "LA RECOVA", f_ajustable, color_letras, (684, altura_y_inferior), es_centro=True)
        r_n4 = self.dibujar_postal_nivel(pantalla, dict_postales["c4"], 559, 435, pos_mouse, click_presionado)
        
        # Nivel 5: Especial
        r_n5 = pygame.Rect(750, 220, 250, 50)
        if nivel_5_desbloqueado:
            self.blit_con_contorno(pantalla, "QUINTA DE OLIVOS", f_ajustable, color_letras, (875, 200), es_centro=True)
            r_n5 = self.dibujar_postal_nivel(pantalla, dict_postales["c5"], 750, 220, pos_mouse, click_presionado)
            
        r_volver = self.crear_boton_pixel(pantalla, "VOLVER AL MENU", 120, 715, f_bot, pos_mouse)
        return r_n1, r_n2, r_n3, r_n4, r_volver

    def blit_con_contorno(self, pantalla, texto, fuente, color_frente, posicion, es_centro=False):
        """Renderiza un texto con un borde negro grueso de 2 píxeles para mejorar el contraste."""
        # Renderizamos la capa base negra y la capa de color
        surf_borde = fuente.render(texto, True, (0, 0, 0))
        surf_frente = fuente.render(texto, True, color_frente)
    
        # Calculamos el rectángulo de posicionamiento
        if es_centro:
            rect = surf_frente.get_rect(center=posicion)
        else:
            rect = surf_frente.get_rect(topleft=posicion)
        
        # Dibujamos el contorno en cruz de 2 píxeles de grosor para blindar la lectura
        for dx, dy in [(-2,0), (2,0), (0,-2), (0,2), (-2,-2), (2,-2), (-2,2), (2,2)]:
            pantalla.blit(surf_borde, (rect.x + dx, rect.y + dy))
        
        # Estampamos el texto original de color arriba en el centro
        pantalla.blit(surf_frente, rect)


    def dibujar_pantallas_estaticas(self, pantalla, estado, f_tit, f_bot, pos_mouse):
        # --- 1. MOTOR DE CARGA AUTÓNOMA DE FONDO ---
        if not hasattr(self, "textura_glosario"):
            try:
                img = pygame.image.load("assets/interfaces/glosario.png").convert()
                self.textura_glosario = pygame.transform.scale(img, (1024, 768))
            except Exception as e:
                print(f"Error al cargar assets/interfaces/glosario.png: {e}")
                self.textura_glosario = None

        # --- 2. FUENTES SECUNDARIAS NATIVAS ---
        f_sub = pygame.font.Font(None, 28)
        f_desc = pygame.font.Font(None, 22)

        # ========================================================
        # --- 3. DECLARACIÓN ANTICIPADA DE SPRITES (CORREGIDO DE LUGAR) ---
        # ========================================================
        # Al nacer acá arriba, están disponibles para cualquier pantalla o bucle de abajo
        sprite_vacio = pygame.Surface((48, 48), pygame.SRCALPHA)
        
        tiempo_ahora = pygame.time.get_ticks()
        frame_stance = (tiempo_ahora // 150) % 4 + 1
        try:
            sprite_soldado = pygame.image.load(f"assets/enemigos/soldado/soldadostance{frame_stance}.png").convert_alpha()
            sprite_soldado = pygame.transform.scale(sprite_soldado, (48, 48))
        except:
            sprite_soldado = None

        # ========================================================
        # --- 4. CONTROL DE LAS INTERFACES DEL MANÁGER ---
        # ========================================================
        if estado == cte.ESTADO_GLOSARIO:
            if self.textura_glosario:
                pantalla.blit(self.textura_glosario, (0, 0))
            else:
                pantalla.fill((30, 30, 30))
                
            self.blit_con_contorno(pantalla, "GLOSARIO DE EJERCITOS", f_tit, (255, 255, 0), (512, 50), es_centro=True)
            
            # Al estar definida arriba de todo, la lista va a leer 'sprite_vacio' a la perfección:
            defensas = [
                ("Gauchos:", "Media distancia. Atacan con boleadoras certeras.", sprite_vacio),
                ("Ciudadanos:", "Corto alcance. Lanzan ollas de aceite hirviendo.", sprite_vacio),
                ("Granaderos:", "Jinetes moviles que cargan de arriba a abajo.", sprite_vacio),
                ("Infernales:", "Caballeria de choque que busca jefes realistas.", sprite_vacio),
                ("Ingenieros:", "Sanan estructuras saboteadas y revelan espias.", sprite_vacio)
            ]
            
            self.blit_con_contorno(pantalla, "[ FUERZAS PATRIOTAS ]", f_sub, (135, 206, 250), (80, 110))
            y_def = 150
            for titulo, desc, img_sprite in defensas:
                self.blit_con_contorno(pantalla, titulo, f_desc, (255, 255, 255), (80, y_def + 10))
                self.blit_con_contorno(pantalla, desc, f_desc, (235, 235, 235), (300, y_def + 10))
                pantalla.blit(img_sprite, (220, y_def - 6))       
                y_def += 45                                      

            # ========================================================
            # EJÉRCITO REALISTA (DEFINICIÓN DE LISTA PRIMERO)
            # ========================================================
            # Hacemos lo mismo con los enemigos para que quede super seguro
            enemigos = [
                ("Soldado Raso:", "Infanteria estandard de la corona espanola.", sprite_soldado),
                ("Experimentado:", "Soldado veterano con el doble de resistencia.", sprite_vacio),
                ("A Caballo:", "Rapido. Al caer en combate muta a pie.", sprite_vacio),
                ("Canoneros:", "Lentos y pesados. Al destruirse liberan escoltas.", sprite_vacio),
                ("Espia Realista:", "Camuflado. Deshabilita torres si no es revelado.", sprite_vacio)
            ]
        
            # Pintamos el título rojo de la sección abajo
            self.blit_con_contorno(pantalla, "[ EJERCITO REALISTA ]", f_sub, (255, 127, 127), (80, 380))
        
            y_ene = 420
            for titulo, desc, img_sprite in enemigos:
                self.blit_con_contorno(pantalla, titulo, f_desc, (255, 255, 255), (80, y_ene + 10))
                self.blit_con_contorno(pantalla, desc, f_desc, (235, 235, 235), (300, y_ene + 10))
                if img_sprite:
                    pantalla.blit(img_sprite, (220, y_ene - 6))   
                y_ene += 45                   

        else:
            # ========================================================
            # --- PANTALLA DE CRÉDITOS / REGISTRO DE HEROES (CORREGIDO) ---
            # ========================================================
            # 1. CAPA FONDO: Estampamos el mismo pergamino antiguo para tapar los botones viejos del menu
            if self.textura_glosario:
                # CORRECCIÓN DEFINITIVA: Quitamos '.dibujar_pantallas_estaticas' de la mitad del llamado
                pantalla.blit(self.textura_glosario, (0, 0))
            else:
                pantalla.fill((20, 20, 30)) # Auxilio azul noche

            # 2. TITULO PRINCIPAL (Centrado arriba con contorno amarillo)
            self.blit_con_contorno(pantalla, "REGISTRO DE HEROES", f_tit, (255, 255, 0), (512, 100), es_centro=True)
        
            # 3. TEXTOS INSTITUCIONALES (CORREGIDOS A BLANCO CON BORDE NEGRO)
            # Centramos cada renglon de forma simetrica usando es_centro=True para que quede impecable
            self.blit_con_contorno(
                pantalla, 
                "INDEPENDEFENCE - Juego Historico Nacional", 
                f_sub, 
                (255, 255, 255), # Forzamos el color Blanco Puro (R, G, B)
                (512, 260), 
                es_centro=True
            )
        
            self.blit_con_contorno(
                pantalla, 
                "Desarrollado por: UNLAM - Grupo 7", 
                f_sub, 
                (255, 255, 255), # Blanco Puro
                (512, 340), 
                es_centro=True
            )
        
            self.blit_con_contorno(
                pantalla, 
                "Catedra de Diseno y Desarrollo de Videojuegos 2026", 
                f_desc, 
                (235, 235, 235), # Un blanco sutilmente grisaceo muy prolijo para el subtitulo
                (512, 410), 
                es_centro=True
            )
        # --- BOTON INTERACTIVO PARA REGRESAR ---
        # Mantenemos tu boton amarillo centrado abajo para volver de forma comoda
        r_v = self.crear_boton_pixel(pantalla, "VOLVER AL MILITAR (MENU)", 512, 720, f_bot, pos_mouse)
        return r_v

    def dibujar_game_over(self, pantalla, f_tit, f_bot, pos_mouse):
        if self.fondo_game_over:
            pantalla.blit(self.fondo_game_over, (0, 0))
        else:
            pantalla.fill((50, 10, 10))
            txt_go = f_tit.render("GAME OVER", True, (255, 0, 0))
            pantalla.blit(txt_go, txt_go.get_rect(center=(512, 300)))

        # --- BOTONES INTERACTIVOS INDEPENDIENTES (Abajo centrados) ---
        # Boton izquierdo: REINTENTAR EL NIVEL
        r_reintentar = self.crear_boton_pixel(pantalla, "REINTENTAR NIVEL", 340, 690, f_bot, pos_mouse)
        
        # Boton derecho: REGRESAR AL MENU PRINCIPAL
        r_volver = self.crear_boton_pixel(pantalla, "MENU PRINCIPAL", 684, 690, f_bot, pos_mouse)
        
        return r_reintentar, r_volver

    def dibujar_mision_cumplida(self, pantalla, f_tit, f_bot, pos_mouse, dinero_final, vidas_finales):
        if self.fondo_victoria:
            pantalla.blit(self.fondo_victoria, (0, 0))
        else:
            pantalla.fill((10, 50, 10))
            txt_v = f_tit.render("MISION CUMPLIDA", True, (255, 255, 0))
            pantalla.blit(txt_v, txt_v.get_rect(center=(512, 200)))

        # --- MOTOR DE CARGA AUTÓNOMA DE MONEDA (NUEVO) ---
        if not hasattr(self, "moneda_victoria"):
            try:
                # Modificá esta ruta si tu archivo de moneda/oro real se llama o está en otro lado:
                img_m = pygame.image.load("assets/interfaces/moneda.png").convert_alpha()
                self.moneda_victoria = pygame.transform.scale(img_m, (36, 36))
            except:
                self.moneda_victoria = None

        color_texto = (60, 40, 20)

        # 1. PERGAMINO DE PUNTOS (Izquierda)
        puntos_score = vidas_finales * 100
        txt_puntos = f_tit.render(f"{puntos_score}", True, color_texto)
        pantalla.blit(txt_puntos, txt_puntos.get_rect(center=(265, 550))) 
        
        # 2. PERGAMINO DE DINERO RESTANTE + MONEDA (Derecha)
        txt_dinero = f_tit.render(f"{dinero_final}", True, color_texto)
        rect_dinero = txt_dinero.get_rect(center=(745, 550)) 
        pantalla.blit(txt_dinero, rect_dinero)
        
        # Si la moneda se cargó con éxito de forma autónoma, la estampamos
        if self.moneda_victoria:
            pantalla.blit(self.moneda_victoria, (rect_dinero.x - 45, rect_dinero.y + 4))

        # 3. BOTÓN INTERACTIVO PARA REGRESAR (Abajo al centro)
        r_v_win = self.crear_boton_pixel(pantalla, "REGRESAR AL MENU DE CAMPANA", 512, 715, f_bot, pos_mouse)
        return r_v_win

    def crear_boton_pixel(self, pantalla, texto, centro_x, centro_y, fuente, pos_mouse):
        """Dibuja un texto color crema con contorno negro de 360 grados estilo pixel art."""
        color_crema = (245, 222, 179) # El tono arena de tu captura
        color_borde = (0, 0, 0)       # Negro absoluto para el contorno
        
        # 1. Determinamos si el mouse esta encima para aplicar los corchetes [ ]
        superficie_evaluar = fuente.render(texto, True, color_crema)
        rect_evaluar = superficie_evaluar.get_rect(center=(centro_x, centro_y))
        
        texto_definitivo = texto
        color_activo = color_crema
        
        if rect_evaluar.collidepoint(pos_mouse):
            texto_definitivo = f"[ {texto} ]"
            color_activo = (255, 215, 0) # Brilla en amarillo patrio al pasar el mouse
            
        # 2. RENDERIZAMOS LAS DOS CAPAS DE COLOR
        surf_borde = fuente.render(texto_definitivo, True, color_borde)
        surf_frente = fuente.render(texto_definitivo, True, color_activo)
        rect_final = surf_frente.get_rect(center=(centro_x, centro_y))
        
        # 3. EL TRUCO DEL CONTORNO: Dibujamos el texto negro 8 veces alrededor (en cruz y diagonales)
        # Desplazamiento de 2 píxeles para lograr el grosor exacto de tu imagen
        desplazamientos = [
            (-2, 0), (2, 0), (0, -2), (0, 2),   # Cruz (Izquierda, Derecha, Arriba, Abajo)
            (-2, -2), (-2, 2), (2, -2), (2, 2)  # Diagonales
        ]
        
        for dx, dy in desplazamientos:
            pantalla.blit(surf_borde, (rect_final.x + dx, rect_final.y + dy))
            
        # 4. CAPA FINAL: Pintamos la letra limpia arriba en el centro exacto
        pantalla.blit(surf_frente, rect_final)
        
        return rect_final

    # Declaramos la variable global arriba de todo en el archivo main.py (abajo de los imports)
    ultimo_sonido_hover_global = 0

    def dibujar_boton_imagen(self, pantalla, lista_img, centro_x, centro_y, pos_mouse, click_presionado):
        """Maneja los 3 estados del botón de madera ANCLADO DESDE EL CENTRO (Para el Menú Principal)."""
        img_norm = lista_img[0]
        img_sel = lista_img[1]
        img_pre = lista_img[2]

        # RESTAURADO: Los botones del menú principal vuelven a centrarse milimétricamente
        rect_pantalla = img_norm.get_rect(center=(centro_x, centro_y))
        imagen_activa = img_norm
        
        if rect_pantalla.collidepoint(pos_mouse):
            if click_presionado:
                imagen_activa = img_pre
            else:
                imagen_activa = img_sel
                
        pantalla.blit(imagen_activa, rect_pantalla)
        return rect_pantalla

    def dibujar_postal_nivel(self, pantalla, lista_img, topleft_x, topleft_y, pos_mouse, click_presionado):
        """Maneja los 3 estados de las postales ANCLADAS DESDE ARRIBA A LA IZQUIERDA (Para los Mapas)."""
        img_norm = lista_img[0]
        img_sel = lista_img[1]
        img_pre = lista_img[2]

        # MANTENIDO: Las postales se quedan quietas en su cuadrícula perfecta de la captura
        rect_pantalla = img_norm.get_rect(topleft=(topleft_x, topleft_y))
        imagen_activa = img_norm
        
        if rect_pantalla.collidepoint(pos_mouse):
            if click_presionado:
                imagen_activa = img_pre
            else:
                imagen_activa = img_sel
                
        pantalla.blit(imagen_activa, rect_pantalla)
        return rect_pantalla

    #para no tener líneas de más en el main
    def cargar_pack_boton(self, nombre_base):
        """Carga automáticamente los 3 estados de un botón basándose en su nombre raíz."""
        estados = ["", "_selected", "_pressed"]
        pack = []
        
        try:
            for sufijo in estados:
                ruta = f"assets/interfaces/{nombre_base}{sufijo}.png"
                img = pygame.image.load(ruta).convert_alpha()
                pack.append(img)
            return pack
        except Exception as e:
            print(f"Error al cargar el pack del boton '{nombre_base}': {e}")
            # Auxilio de emergencia: si falla, devuelve superficies vacías para que el juego no crashee
            aux = pygame.Surface((342, 66))
            return [aux, aux, aux]