import pygame
import math
import random
from config import constants as cte

class MenuManager:
    
    def __init__(self):
        self.ultimo_sonido_hover_global = 0

    # ========================================================
    # FUNCIONES AUXILIARES PARA CADA PANTALLA DEL DIAGRAMA
    # ========================================================

    # CORRECCIÓN DEFINITIVA: Tabulado a la derecha y con 'self' incorporado en el paréntesis
    def dibujar_bienvenida(self, pantalla, f_tit, f_bot, imagen_fondo):
        if imagen_fondo:
            pantalla.blit(imagen_fondo, (0, 0))
        else:
            pantalla.fill(cte.BLACK)

        # --- INDICADOR INFERIOR CON CONTORNO REAL ---
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            texto_start = "PULSA CUALQUIER TECLA PARA EMPEZAR"
            color_crema = (245, 222, 179) # Tono arena
            color_borde = (0, 0, 0)       # Negro absoluto

            # Creamos las dos superficies independientes
            surf_borde = f_bot.render(texto_start, True, color_borde)
            surf_frente = f_bot.render(texto_start, True, color_crema)
            
            rect_final = surf_frente.get_rect(center=(512, 630))

            # Dibujamos el texto negro ensanchado en cruz de 2 pixeles (Arriba, Abajo, Izquierda, Derecha)
            pantalla.blit(surf_borde, (rect_final.x - 2, rect_final.y))
            pantalla.blit(surf_borde, (rect_final.x + 2, rect_final.y))
            pantalla.blit(surf_borde, (rect_final.x, rect_final.y - 2))
            pantalla.blit(surf_borde, (rect_final.x, rect_final.y + 2))
            
            # También en las diagonales para rellenar los huecos del pixel art
            pantalla.blit(surf_borde, (rect_final.x - 2, rect_final.y - 2))
            pantalla.blit(surf_borde, (rect_final.x + 2, rect_final.y - 2))
            pantalla.blit(surf_borde, (rect_final.x - 2, rect_final.y + 2))
            pantalla.blit(surf_borde, (rect_final.x + 2, rect_final.y + 2))

            # Capa final: La letra limpia color crema arriba en el centro
            pantalla.blit(surf_frente, rect_final)

    # CORRECCIÓN DE CABECERA: Borramos 'ultimo_sonido_hover' del final del parentesis
    def dibujar_menu_principal(self, pantalla, f_tit, pos_mouse, btn_com, btn_glo, btn_cre, btn_sal, click_presionado, img_fondo, img_logo, tiempo_actual):
        import math 
    
        if img_fondo:
            # Paneo cinemático lento de fondo
            velocidad_paneo = tiempo_actual / 1500.0
            desvío_x = int(-50 + math.sin(velocidad_paneo) * 50)
            desvío_y = int(-50 + math.cos(velocidad_paneo * 0.8) * 50)
            pantalla.blit(img_fondo, (desvío_x, desvío_y))
        else:
            pantalla.fill((30, 30, 30))
    
        if img_logo:
            pantalla.blit(img_logo, img_logo.get_rect(center=(512, 110)))
        else:
            txt_m = f_tit.render("INDEPENDEFENCE", True, (245, 222, 179))
            pantalla.blit(txt_m, txt_m.get_rect(center=(512, 120)))

        # Construimos las 4 zonas interactivas de tu captura
        r_jugar = self.dibujar_boton_imagen(pantalla, btn_com[0], btn_com[1], btn_com[2], 512, 240, pos_mouse, click_presionado)
        r_glosario = self.dibujar_boton_imagen(pantalla, btn_glo[0], btn_glo[1], btn_glo[2], 512, 340, pos_mouse, click_presionado)
        r_creditos = self.dibujar_boton_imagen(pantalla, btn_cre[0], btn_cre[1], btn_cre[2], 512, 440, pos_mouse, click_presionado)
        r_salir = self.dibujar_boton_imagen(pantalla, btn_sal[0], btn_sal[1], btn_sal[2], 512, 540, pos_mouse, click_presionado)
    
        return r_jugar, r_glosario, r_creditos, r_salir

    def dibujar_seleccion_niveles(self, pantalla, f_tit, f_bot, pos_mouse, nivel_5_desbloqueado, postales, click_presionado, imagen_fondo):
        if imagen_fondo:
            # Proyectamos tu ilustracion cubriendo todo el lienzo de 1024x768
            pantalla.blit(imagen_fondo, (0, 0))
        else:
            # Fondo marron de auxilio por si se borra el archivo sin querer
            pantalla.fill((40, 20, 20))
    
        # 1. TITULO PRINCIPAL DE LA PANTALLA
        txt_s = f_tit.render("SELECCIONA LA CAMPAÑA", True, (255, 255, 0))
        pantalla.blit(txt_s, txt_s.get_rect(center=(512, 50)))
    
        # --------------------------------------------------------
        # FILA 1: EL CABILDO (N1) Y LA CATEDRAL (N2)
        # --------------------------------------------------------
        lbl_n1 = f_bot.render("NIVEL 1: EL CABILDO", True, (255, 255, 0))
        pantalla.blit(lbl_n1, lbl_n1.get_rect(center=(340, 110)))
    
        lbl_n2 = f_bot.render("NIVEL 2: LA CATEDRAL", True, (255, 255, 0))
        pantalla.blit(lbl_n2, lbl_n2.get_rect(center=(684, 110)))
    
        rn1 = self.dibujar_postal_nivel(pantalla, postales["c1"][0], postales["c1"][1], postales["c1"][2], 340, 255, pos_mouse, click_presionado)
        rn2 = self.dibujar_postal_nivel(pantalla, postales["c2"][0], postales["c2"][1], postales["c2"][2], 684, 255, pos_mouse, click_presionado)
    
        # --------------------------------------------------------
        # FILA 2: EL FORTIN (N3) Y LA RECOVA (N4)
        # --------------------------------------------------------
        lbl_n3 = f_bot.render("NIVEL 3: EL FORTIN", True, (255, 255, 0))
        pantalla.blit(lbl_n3, lbl_n3.get_rect(center=(340, 410)))
    
        lbl_n4 = f_bot.render("NIVEL 4: LA RECOVA", True, (255, 255, 0))
        pantalla.blit(lbl_n4, lbl_n4.get_rect(center=(684, 410)))
    
        rn3 = self.dibujar_postal_nivel(pantalla, postales["c3"][0], postales["c3"][1], postales["c3"][2], 340, 555, pos_mouse, click_presionado)
        rn4 = self.dibujar_postal_nivel(pantalla, postales["c4"][0], postales["c4"][1], postales["c4"][2], 684, 555, pos_mouse, click_presionado)
    
        # --- ESPACIO RESERVADO NIVEL 5 ---
        rn5 = pygame.Rect(0, 0, 0, 0)
        if nivel_5_desbloqueado:
            rn5 = self.dibujar_postal_nivel(pantalla, postales["c5"][0], postales["c5"][1], postales["c5"][2], 875, 255, pos_mouse, click_presionado)
        
        # --- BOTON VOLVER ABAJO A LA IZQUIERDA ---
        rv = self.crear_boton_pixel(pantalla, "VOLVER AL MENU", 120, 715, f_bot, pos_mouse)
    
        return rn1, rn2, rn3, rn4, rn5, rv

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

    def dibujar_game_over(self, pantalla, f_tit, f_bot, pos_mouse, imagen_fondo):
        if imagen_fondo:
            # Estampamos la ilustracion en pantalla completa
            pantalla.blit(imagen_fondo, (0, 0))
        else:
            pantalla.fill((40, 20, 20))
            txt_go = f_tit.render("GAME OVER", True, (255, 0, 0))
            pantalla.blit(txt_go, txt_go.get_rect(center=(512, 300)))

        # --- BOTONES INTERACTIVOS INDEPENDIENTES (Abajo centrados) ---
        # Boton izquierdo: REINTENTAR EL NIVEL
        r_reintentar = self.crear_boton_pixel(pantalla, "REINTENTAR NIVEL", 340, 690, f_bot, pos_mouse)
        
        # Boton derecho: REGRESAR AL MENU PRINCIPAL
        r_volver = self.crear_boton_pixel(pantalla, "MENU PRINCIPAL", 684, 690, f_bot, pos_mouse)
        
        return r_reintentar, r_volver

    def dibujar_mision_cumplida(self, pantalla, f_tit, f_bot, pos_mouse, imagen_fondo, dinero_final, vidas_finales, icono_moneda=None):
        if imagen_fondo:
            pantalla.blit(imagen_fondo, (0, 0))
        else:
            pantalla.fill((20, 40, 20))
            txt_v = f_tit.render("MISION CUMPLIDA", True, (255, 255, 0))
            pantalla.blit(txt_v, txt_v.get_rect(center=(512, 200)))

        # --- COLOR MARRÓN COLONIAL PARA LA LETRA (Integra mejor en los pergaminos) ---
        color_texto = (60, 40, 20)

        # ========================================================
        # 1. PERGAMINO DE PUNTOS (Izquierda)
        # ========================================================
        puntos_score = vidas_finales * 100
        txt_puntos = f_tit.render(f"{puntos_score}", True, color_texto)
        # MODIFICACIÓN: Cambiamos 600 por 575
        pantalla.blit(txt_puntos, txt_puntos.get_rect(center=(265, 550))) 
        
        # ========================================================
        # 2. PERGAMINO DE DINERO RESTANTE + MONEDA (Derecha)
        # ========================================================
        txt_dinero = f_tit.render(f"{dinero_final}", True, color_texto)
        # MODIFICACIÓN: Cambiamos 600 por 575
        rect_dinero = txt_dinero.get_rect(center=(745, 550)) 
        pantalla.blit(txt_dinero, rect_dinero)
        
        # La moneda se acomoda sola de forma automatica porque lee la posicion del 'rect_dinero'
        if icono_moneda:
            moneda_grande = pygame.transform.scale(icono_moneda, (36, 36))
            pantalla.blit(moneda_grande, (rect_dinero.x - 45, rect_dinero.y + 4))

        # ========================================================
        # 3. BOTÓN INTERACTIVO PARA REGRESAR (Abajo al centro)
        # ========================================================
        # Lo subimos apenas unos pixeles a Y=715 para que no pise la bandera argentina del borde inferior
        r_v = crear_boton_pixel(pantalla, "REGRESAR AL MENU DE CAMPANA", 512, 715, f_bot, pos_mouse)
        return r_v

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

    def dibujar_boton_imagen(self, pantalla, img_norm, img_sel, img_pre, centro_x, centro_y, pos_mouse, click_presionado):
        """Maneja los 3 estados visuales del botón y devuelve su rectángulo de colisión."""
        rect_pantalla = img_norm.get_rect(center=(centro_x, centro_y))
        imagen_activa = img_norm
        
        # Verificamos si el cursor colisiona con el marco de madera
        if rect_pantalla.collidepoint(pos_mouse):
            if click_presionado:
                imagen_activa = img_pre   # Estado: Presionado (Madera hundida)
            else:
                imagen_activa = img_sel   # Estado: Seleccionado (Luz de hover)
                
        pantalla.blit(imagen_activa, rect_pantalla)
        return rect_pantalla

    def dibujar_postal_nivel(self, pantalla, img_norm, img_sel, img_pre, centro_x, centro_y, pos_mouse, click_presionado):
        """Proyecta la imagen de la postal completa en base a la interaccion del mouse."""
        rect_pantalla = img_norm.get_rect()
        rect_pantalla.center = (centro_x, centro_y)
        
        imagen_activa = img_norm
        if rect_pantalla.collidepoint(pos_mouse):
            if click_presionado:
                imagen_activa = img_pre
            else:
                imagen_activa = img_sel
                
        pantalla.blit(imagen_activa, rect_pantalla)
        return rect_pantalla