print("Cargando Pygame...")
import pygame
import sys
import random

print("Cargando Constantes...")
from config import constants as cte

print("Cargando Base...")
from clases.base import Base

print("Cargando Torre...")
from clases.torre import Torre

print("Cargando WaveManager...")
from managers.wave_manager import WaveManager

print("Cargando UIManager...")
from managers.UI_manager import UIManager

print("¡Todos los archivos se cargaron con éxito!")

# ========================================================
# FUNCIONES AUXILIARES PARA CADA PANTALLA DEL DIAGRAMA
# ========================================================

def dibujar_bienvenida(pantalla, f_tit, f_bot, imagen_fondo):
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
def dibujar_menu_principal(pantalla, f_tit, pos_mouse, btn_com, btn_glo, btn_cre, btn_sal, click_presionado, img_fondo, img_logo, tiempo_actual):
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
    r_jugar = dibujar_boton_imagen(pantalla, btn_com[0], btn_com[1], btn_com[2], 512, 240, pos_mouse, click_presionado)
    r_glosario = dibujar_boton_imagen(pantalla, btn_glo[0], btn_glo[1], btn_glo[2], 512, 340, pos_mouse, click_presionado)
    r_creditos = dibujar_boton_imagen(pantalla, btn_cre[0], btn_cre[1], btn_cre[2], 512, 440, pos_mouse, click_presionado)
    r_salir = dibujar_boton_imagen(pantalla, btn_sal[0], btn_sal[1], btn_sal[2], 512, 540, pos_mouse, click_presionado)
    
    return r_jugar, r_glosario, r_creditos, r_salir

def dibujar_seleccion_niveles(pantalla, f_tit, f_bot, pos_mouse, nivel_5_desbloqueado, postales, click_presionado, imagen_fondo):
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
    
    rn1 = dibujar_postal_nivel(pantalla, postales["c1"][0], postales["c1"][1], postales["c1"][2], 340, 255, pos_mouse, click_presionado)
    rn2 = dibujar_postal_nivel(pantalla, postales["c2"][0], postales["c2"][1], postales["c2"][2], 684, 255, pos_mouse, click_presionado)
    
    # --------------------------------------------------------
    # FILA 2: EL FORTIN (N3) Y LA RECOVA (N4)
    # --------------------------------------------------------
    lbl_n3 = f_bot.render("NIVEL 3: EL FORTIN", True, (255, 255, 0))
    pantalla.blit(lbl_n3, lbl_n3.get_rect(center=(340, 410)))
    
    lbl_n4 = f_bot.render("NIVEL 4: LA RECOVA", True, (255, 255, 0))
    pantalla.blit(lbl_n4, lbl_n4.get_rect(center=(684, 410)))
    
    rn3 = dibujar_postal_nivel(pantalla, postales["c3"][0], postales["c3"][1], postales["c3"][2], 340, 555, pos_mouse, click_presionado)
    rn4 = dibujar_postal_nivel(pantalla, postales["c4"][0], postales["c4"][1], postales["c4"][2], 684, 555, pos_mouse, click_presionado)
    
    # --- ESPACIO RESERVADO NIVEL 5 ---
    rn5 = pygame.Rect(0, 0, 0, 0)
    if nivel_5_desbloqueado:
        rn5 = dibujar_postal_nivel(pantalla, postales["c5"][0], postales["c5"][1], postales["c5"][2], 875, 255, pos_mouse, click_presionado)
        
    # --- BOTON VOLVER ABAJO A LA IZQUIERDA ---
    rv = crear_boton_pixel(pantalla, "VOLVER AL MENU", 120, 715, f_bot, pos_mouse)
    
    return rn1, rn2, rn3, rn4, rn5, rv

def blit_con_contorno(pantalla, texto, fuente, color_frente, posicion, es_centro=False):
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


def dibujar_pantallas_estaticas(pantalla, estado, f_tit, f_bot, pos_mouse):
    # --- 1. MOTOR DE CARGA AUTÓNOMA DE FONDO ---
    if not hasattr(dibujar_pantallas_estaticas, "textura_glosario"):
        try:
            img = pygame.image.load("assets/interfaces/glosario.png").convert()
            dibujar_pantallas_estaticas.textura_glosario = pygame.transform.scale(img, (1024, 768))
        except Exception as e:
            print(f"Error al cargar assets/interfaces/glosario.png: {e}")
            dibujar_pantallas_estaticas.textura_glosario = None

    # --- 2. FUENTES SECUNDARIAS ---
    f_sub = pygame.font.Font(None, 28)
    f_desc = pygame.font.Font(None, 22)

    # ========================================================
    # 3. DECLARACIÓN ANTICIPADA DE SPRITES (CORREGIDO DE LUGAR)
    # ========================================================
    # Declaramos las variables aca arriba para que esten vivas ANTES de armar las listas de abajo
    sprite_vacio = pygame.Surface((48, 48), pygame.SRCALPHA)
    
    tiempo_ahora = pygame.time.get_ticks()
    frame_stance = (tiempo_ahora // 150) % 4 + 1
    
    try:
        sprite_soldado = pygame.image.load(f"assets/enemigos/soldado/soldadostance{frame_stance}.png").convert_alpha()
        sprite_soldado = pygame.transform.scale(sprite_soldado, (48, 48))
    except:
        sprite_soldado = None

    # --- 4. CONTROL DE PANTALLAS ---
    if estado == cte.ESTADO_GLOSARIO:
        if dibujar_pantallas_estaticas.textura_glosario:
            pantalla.blit(dibujar_pantallas_estaticas.textura_glosario, (0, 0))
        else:
            pantalla.fill((30, 30, 30))
            
        # 1. TÍTULO PRINCIPAL
        blit_con_contorno(pantalla, "GLOSARIO DE EJERCITOS", f_tit, (255, 255, 0), (512, 50), es_centro=True)
        
        # ========================================================
        # FUERZAS PATRIOTAS (DEFINICIÓN DE LISTA PRIMERO)
        # ========================================================
        # CORRECCIÓN: Declaramos la lista aca arriba para que exista antes del bucle for
        defensas = [
            ("Gauchos:", "Media distancia. Atacan con boleadoras certeras.", sprite_vacio),
            ("Ciudadanos:", "Corto alcance. Lanzan ollas de aceite hirviendo.", sprite_vacio),
            ("Granaderos:", "Jinetes moviles que cargan de arriba a abajo.", sprite_vacio),
            ("Infernales:", "Caballeria de choque que busca jefes realistas.", sprite_vacio),
            ("Ingenieros:", "Sanan estructuras saboteadas y revelan espias.", sprite_vacio)
        ]
        
        # Pintamos el título celeste de la sección
        blit_con_contorno(pantalla, "[ FUERZAS PATRIOTAS ]", f_sub, (135, 206, 250), (80, 110))
        
        y_def = 150
        for titulo, desc, img_sprite in defensas:
            blit_con_contorno(pantalla, titulo, f_desc, (255, 255, 255), (80, y_def + 10))
            blit_con_contorno(pantalla, desc, f_desc, (235, 235, 235), (300, y_def + 10))
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
        blit_con_contorno(pantalla, "[ EJERCITO REALISTA ]", f_sub, (255, 127, 127), (80, 380))
        
        y_ene = 420
        for titulo, desc, img_sprite in enemigos:
            blit_con_contorno(pantalla, titulo, f_desc, (255, 255, 255), (80, y_ene + 10))
            blit_con_contorno(pantalla, desc, f_desc, (235, 235, 235), (300, y_ene + 10))
            if img_sprite:
                pantalla.blit(img_sprite, (220, y_ene - 6))   
            y_ene += 45                   

    else:
        # --- PANTALLA DE CRÉDITOS / REGISTRO DE HEROES ---
        txt_t = f_tit.render("REGISTRO DE HEROES", True, (255, 255, 0))
        pantalla.blit(txt_t, txt_t.get_rect(center=(512, 100)))
        
        txt_c1 = f_sub.render("INDEPENDEFENCE - Juego Historico Nacional", True, (200, 200, 200))
        txt_c2 = f_sub.render("Desarrollado por: UNLAM - Grupo 7", True, (255, 255, 255))
        txt_c3 = f_desc.render("Catedra de Diseno y Desarrollo de Videojuegos 2026", True, (150, 150, 150))
        
        pantalla.blit(txt_c1, txt_c1.get_rect(center=(512, 250)))
        pantalla.blit(txt_c2, txt_c2.get_rect(center=(512, 320)))
        pantalla.blit(txt_c3, txt_c3.get_rect(center=(512, 384)))

    # --- BOTON INTERACTIVO PARA REGRESAR ---
    # Mantenemos tu boton amarillo centrado abajo para volver de forma comoda
    r_v = crear_boton_pixel(pantalla, "VOLVER AL MILITAR (MENU)", 512, 720, f_bot, pos_mouse)
    return r_v

def dibujar_game_over(pantalla, f_tit, f_bot, pos_mouse, imagen_fondo):
    if imagen_fondo:
        # Estampamos la ilustracion en pantalla completa
        pantalla.blit(imagen_fondo, (0, 0))
    else:
        pantalla.fill((40, 20, 20))
        txt_go = f_tit.render("GAME OVER", True, (255, 0, 0))
        pantalla.blit(txt_go, txt_go.get_rect(center=(512, 300)))

    # --- BOTONES INTERACTIVOS INDEPENDIENTES (Abajo centrados) ---
    # Boton izquierdo: REINTENTAR EL NIVEL
    r_reintentar = crear_boton_pixel(pantalla, "REINTENTAR NIVEL", 340, 690, f_bot, pos_mouse)
    
    # Boton derecho: REGRESAR AL MENU PRINCIPAL
    r_volver = crear_boton_pixel(pantalla, "MENU PRINCIPAL", 684, 690, f_bot, pos_mouse)
    
    return r_reintentar, r_volver

def dibujar_mision_cumplida(pantalla, f_tit, f_bot, pos_mouse, imagen_fondo, dinero_final, vidas_finales, icono_moneda=None):
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

def crear_boton_pixel(pantalla, texto, centro_x, centro_y, fuente, pos_mouse):
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

def dibujar_boton_imagen(pantalla, img_norm, img_sel, img_pre, centro_x, centro_y, pos_mouse, click_presionado):
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

def dibujar_postal_nivel(pantalla, img_norm, img_sel, img_pre, centro_x, centro_y, pos_mouse, click_presionado):
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

# ========================================================
# FUNCIÓN PRINCIPAL DE INICIALIZACIÓN Y BUCLE
# ========================================================

def main():

    import os
    os.environ['SDL_VIDEODRIVER'] = 'windib'
    pygame.mixer.init()
    pygame.init()

    pantalla = pygame.display.set_mode((cte.ANCHO_DE_PANTALLA, cte.ALTO_DE_PANTALLA))    
    pygame.display.set_caption("Independefence")
    reloj = pygame.time.Clock()

    try:
        # 1. Cargamos el nuevo logotipo oficial que reemplaza al texto
        logo_juego = pygame.image.load("assets/Independefence.png").convert_alpha()
        # Escalalo a un tamaño prolijo para tu menu (ej: 450x150 o lo que pida tu diseño)
        logo_juego = pygame.transform.scale(logo_juego, (450, 150))
        
        # 2. Cargamos el fondo ilustrado animado
        fondo_menu_crudo = pygame.image.load("assets/interfaces/menu_principal.png").convert()
        # Lo estiramos un poquito mas de la resolucion nativa para tener margen de movimiento
        fondo_menu_grande = pygame.transform.scale(fondo_menu_crudo, (1124, 868))
    except Exception as e:
        print(f"Error al cargar recursos esteticos del menu: {e}")
        logo_juego = None
        fondo_menu_grande = None

    # --- CONFIGURACIÓN DE LA MÚSICA DE FONDO ---
    pygame.mixer.music.set_volume(0.4) # Arranca a un volumen prudente del 40%
    
    # Ruta directa hacia tu carpeta en la raiz (fuera de assets)
    ruta_musica_menu = "musica/War Plan - Devine-King [Ambient].mp3" # <-- CAMBIÁ ESTO por el nombre exacto de tu archivo
    
    try:
        pygame.mixer.music.load(ruta_musica_menu)
        # BORRAMOS la linea del play() de aca para que NO suene en la carga de la consola
        musica_menu_sonando = False 
    except Exception as e:
        print(f"Aviso de música: No se pudo cargar: {e}")
        musica_menu_sonando = False

    try:
        fondo_bienvenida = pygame.image.load("assets/interfaces/Pantalla_de_bienvenida.png").convert()
        fondo_bienvenida = pygame.transform.scale(fondo_bienvenida, (cte.ANCHO_DE_PANTALLA, cte.ALTO_DE_PANTALLA))
    except Exception as e:
        print(f"Error al cargar la portada de bienvenida: {e}")
        fondo_bienvenida = None
    
    try:
        # Sonido para cuando el mouse pasa por encima
        snd_hover = pygame.mixer.Sound("assets/sonidos/point.mp3")
        
        # Listas para reproduccion aleatoria (Random)
        snds_siguiente = [
            pygame.mixer.Sound("assets/sonidos/siguiente1.mp3"),
            pygame.mixer.Sound("assets/sonidos/siguiente2.mp3"),
            pygame.mixer.Sound("assets/sonidos/siguiente3.mp3")
        ]
        snds_volver = [
            pygame.mixer.Sound("assets/sonidos/volver1.mp3"),
            pygame.mixer.Sound("assets/sonidos/volver2.mp3"),
            pygame.mixer.Sound("assets/sonidos/volver3.mp3")
        ]
    except Exception as e:
        print(f"Aviso de audio: No se pudieron cargar los efectos (.mp3): {e}")
        snd_hover = None
        snds_siguiente = snds_volver = []

    # Variables de control para evitar que el sonido de hover suene en bucle infinito
    # Guarda que boton estaba tocando el mouse en el frame anterior
    boton_hover_anterior = -1 

    try:
        # Carga completa del boton COMENZAR
        btn_com = [
            pygame.image.load("assets/interfaces/btn_comenzar.png").convert_alpha(),
            pygame.image.load("assets/interfaces/btn_comenzar_selected.png").convert_alpha(),
            pygame.image.load("assets/interfaces/btn_comenzar_pressed.png").convert_alpha()
        ]
        # Carga completa del boton GLOSARIO
        btn_glo = [
            pygame.image.load("assets/interfaces/btn_glosario.png").convert_alpha(),
            pygame.image.load("assets/interfaces/btn_glosario_selected.png").convert_alpha(),
            pygame.image.load("assets/interfaces/btn_glosario_pressed.png").convert_alpha()
        ]
        # Carga completa del boton CREDITOS
        btn_cre = [
            pygame.image.load("assets/interfaces/btn_creditos.png").convert_alpha(),
            pygame.image.load("assets/interfaces/btn_creditos_selected.png").convert_alpha(),
            pygame.image.load("assets/interfaces/btn_creditos_pressed.png").convert_alpha()
        ]
        # Carga completa del boton SALIR
        btn_sal = [
            pygame.image.load("assets/interfaces/btn_salir.png").convert_alpha(),
            pygame.image.load("assets/interfaces/btn_salir_selected.png").convert_alpha(),
            pygame.image.load("assets/interfaces/btn_salir_pressed.png").convert_alpha()
        ]

    except Exception as e:

        print(f"Error al cargar imagenes individuales: {e}")
        # Auxilio por si te falta renombrar algun archivo todavia
        aux = pygame.Surface((342, 66))
        btn_com = btn_glo = btn_cre = btn_sal = [aux, aux, aux]

    try:
        # Cargamos el fondo ilustrado para la enciclopedia de ejércitos
        fondo_glosario = pygame.image.load("assets/interfaces/glosario.png").convert()
        fondo_glosario = pygame.transform.scale(fondo_glosario, (cte.ANCHO_DE_PANTALLA, cte.ALTO_DE_PANTALLA))
    except Exception as e:
        print(f"Error al cargar el fondo del glosario: {e}")
        fondo_glosario = None

    try:
        postales = {
            "c1": [
                pygame.image.load("assets/interfaces/cabildo.png").convert_alpha(),
                pygame.image.load("assets/interfaces/cabildo_selected.png").convert_alpha(),
                pygame.image.load("assets/interfaces/cabildo_pressed.png").convert_alpha()
            ],
            "c2": [
                pygame.image.load("assets/interfaces/catedral.png").convert_alpha(),
                pygame.image.load("assets/interfaces/catedral_selected.png").convert_alpha(),
                pygame.image.load("assets/interfaces/catedral_pressed.png").convert_alpha()
            ],
            "c3": [
                pygame.image.load("assets/interfaces/elfortin.png").convert_alpha(),
                pygame.image.load("assets/interfaces/elfortin_selected.png").convert_alpha(),
                pygame.image.load("assets/interfaces/elfortin_pressed.png").convert_alpha()
            ],
            "c4": [
                pygame.image.load("assets/interfaces/larecova.png").convert_alpha(),
                pygame.image.load("assets/interfaces/larecova_selected.png").convert_alpha(),
                pygame.image.load("assets/interfaces/larecova_pressed.png").convert_alpha()
            ],
            "c5": [pygame.Surface((1,1)), pygame.Surface((1,1)), pygame.Surface((1,1))] # Reserva vacia N5
        }

    except Exception as e:
        print(f"Aviso de carga de postales: {e}")
        # Auxilio grafico vacio por si falta recortar alguna todavia
        vacio = pygame.Surface((160, 120))
        postales = {"c1":[vacio]*3, "c2":[vacio]*3, "c3":[vacio]*3, "c4":[vacio]*3, "c5":[vacio]*3}

    try:
        # Cargamos el fondo ilustrado de victoria definitiva
        fondo_victoria = pygame.image.load("assets/interfaces/mision_cumplida.png").convert()
        fondo_victoria = pygame.transform.scale(fondo_victoria, (cte.ANCHO_DE_PANTALLA, cte.ALTO_DE_PANTALLA))
    except Exception as e:
        print(f"Error al cargar la pantalla de victoria: {e}")
        fondo_victoria = None

    try:
        # Cargamos el fondo ilustrado para la pantalla de mapas
        fondo_seleccion = pygame.image.load("assets/interfaces/seleccion_de_nivel.png").convert()
        fondo_seleccion = pygame.transform.scale(fondo_seleccion, (cte.ANCHO_DE_PANTALLA, cte.ALTO_DE_PANTALLA))
    except Exception as e:
        print(f"Error al cargar el fondo de seleccion: {e}")
        fondo_seleccion = None

    try:
        mapa_cabildo = pygame.image.load("assets/mapas/nivel_cabildo.png").convert()
        mapa_cabildo = pygame.transform.scale(mapa_cabildo, (cte.ANCHO_DE_PANTALLA, cte.ALTO_DE_PANTALLA))
    except Exception as e:
        print(f"Error al cargar el mapa del nivel 1: {e}")
        mapa_cabildo = None

    try:
        # Cargamos el fondo ilustrado de derrota definitiva
        fondo_game_over = pygame.image.load("assets/interfaces/game_over.png").convert()
        fondo_game_over = pygame.transform.scale(fondo_game_over, (cte.ANCHO_DE_PANTALLA, cte.ALTO_DE_PANTALLA))
    except Exception as e:
        print(f"Error al cargar la pantalla de derrota: {e}")
        fondo_game_over = None

    fuente_titulos = pygame.font.Font("fuentes/Jersey10-Regular.ttf", 54)
    fuente_botones = pygame.font.Font("fuentes/Jersey10-Regular.ttf", 32)

    estado_actual = cte.ESTADO_BIENVENIDA

    # Contenedores de juego vacios al inicio
    cabildo = None
    grupo_torres = None
    grupo_enemigos = None
    grupo_ingenieros = None
    grupo_proyectiles = None
    grupo_aliados_moviles = None
    administrador_oleadas = None
    interfaz_grafica = None
    dinero_patria = 0

    r_jugar = pygame.Rect(341, 207, 341, 66)
    r_glosario = pygame.Rect(341, 302, 341, 66)
    r_creditos = pygame.Rect(341, 397, 341, 66)
    r_salir = pygame.Rect(341, 492, 341, 66)

    r_v_estatico = pygame.Rect(412, 620, 200, 50)
    r_v_go = pygame.Rect(412, 600, 200, 50)
    r_v_win = pygame.Rect(412, 600, 200, 50)

    # Nuevas coordenadas centradas para la matriz de 2x2
    r_n1 = pygame.Rect(215, 135, 250, 240)
    r_n2 = pygame.Rect(559, 135, 250, 240)
    r_n3 = pygame.Rect(215, 435, 250, 240)
    r_n4 = pygame.Rect(559, 435, 250, 240)
    
    # El nivel 5 se acomodará simétricamente si se activa después
    r_n5 = pygame.Rect(750, 220, 250, 50) 
    
    # Mantener volver abajo a la izquierda
    r_volver = pygame.Rect(20, 695, 200, 40)
    
    # Variable de control del GDD para ocultar o revelar el Nivel 5
    nivel_5_desbloqueado = False

        # --- LISTA DE PARCELAS PERMITIDAS PARA CONSTRUIR TORRES ---
    # Cada Rectangulo tiene el formato: (X_inicial, Y_inicial, Ancho, Alto)
    # Ajustados para calzar encima de los cuadraditos de tierra de tu mapa
    parcelas_validas = [
        pygame.Rect(226, 287, 53, 53),   # Parcela 1: Centro-Izquierda (Al lado de la subida) (NO CAMBIAR)
        pygame.Rect(307, 417, 53, 53),   # Parcela 2: Abajo a la izquierda (Calle inferior) (NO CAMBIAR)
        pygame.Rect(605, 553, 53, 53),   # Parcela 3: Abajo al centro (Cerca del mercado) (NO CAMBIAR)
        pygame.Rect(690, 285, 53, 53),   # Parcela 5: Centro-Derecha (Al lado de la bajada)
        pygame.Rect(323, 73, 53, 53)    # Parcela 6: Superior Izquierda (Al lado del Cabildo) (NO CAMBIAR)
    ]

    # Buscá estas líneas arriba de tu while correr en el main():
    control_hover = {"activo": -1}
    ultimo_sonido_hover = 0 # Inicializado en 0 como número común y corriente

    correr = True

    while correr:
        tiempo_actual = pygame.time.get_ticks()
        pos_mouse = pygame.mouse.get_pos()

        # --- CAPTURA DE EVENTOS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                correr = False

            # Transición: De Bienvenida a Menú Principal (MÚSICA ENCIENDE ACÁ)
            if estado_actual == cte.ESTADO_BIENVENIDA:
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    
                    # CORRECCIÓN: Le agregamos la "a" para que diga 'musica_menu_sonando'
                    if not musica_menu_sonando:
                        try:
                            pygame.mixer.music.play(-1) # Se activa en bucle infinito
                            musica_menu_sonando = True
                        except:
                            pass
                    estado_actual = cte.ESTADO_MENU

            # --- CAPTURA DE EVENTOS DE CLICS EN EL MENÚ PRINCIPAL (CORREGIDO DE 14 A 13 ARGUMENTOS) ---
            elif estado_actual == cte.ESTADO_MENU:
                if not musica_menu_sonando:
                    pygame.mixer.music.play(-1)
                    musica_menu_sonando = True

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    
                    # 1. CLIC EN COMENZAR / JUGAR
                    if r_jugar.collidepoint(pos_mouse):
                        if snds_siguiente: random.choice(snds_siguiente).play()
                        # Llamado limpio de 11 argumentos sin arrastrar variables de reloj
                        dibujar_menu_principal(pantalla, fuente_titulos, pos_mouse, btn_com, btn_glo, btn_cre, btn_sal, True, fondo_menu_grande, logo_juego, tiempo_actual)
                        pygame.display.flip()
                        pygame.time.delay(180)
                        estado_actual = cte.ESTADO_JUGAR_SELECCION
                        
                    # 2. CLIC EN GLOSARIO 
                    elif r_glosario.collidepoint(pos_mouse):
                        if snds_siguiente:
                            random.choice(snds_siguiente).play()
                        # CORRECCIÓN: Dejamos el llamado limpio terminando en tiempo_actual
                        dibujar_menu_principal(pantalla, fuente_titulos, pos_mouse, btn_com, btn_glo, btn_cre, btn_sal, True, fondo_menu_grande, logo_juego, tiempo_actual)
                        pygame.display.flip()
                        pygame.time.delay(180)
                        estado_actual = cte.ESTADO_GLOSARIO
                        
                    # 3. CLIC EN CRÉDITOS 
                    elif r_creditos.collidepoint(pos_mouse):
                        if snds_siguiente:
                            random.choice(snds_siguiente).play()
                        # CORRECCIÓN: Dejamos el llamado limpio terminando en tiempo_actual
                        dibujar_menu_principal(pantalla, fuente_titulos, pos_mouse, btn_com, btn_glo, btn_cre, btn_sal, True, fondo_menu_grande, logo_juego, tiempo_actual)
                        pygame.display.flip()
                        pygame.time.delay(180)
                        estado_actual = cte.ESTADO_CREDITOS
                        
                    # 4. CLIC EN SALIR 
                    elif r_salir.collidepoint(pos_mouse):
                        # CORRECCIÓN: Dejamos el llamado limpio terminando en tiempo_actual
                        dibujar_menu_principal(pantalla, fuente_titulos, pos_mouse, btn_com, btn_glo, btn_cre, btn_sal, True, fondo_menu_grande, logo_juego, tiempo_actual)
                        pygame.display.flip()
                        pygame.time.delay(150)
                        correr = False

            # === ¡CORRECCIÓN CRÍTICA AQUÍ! ===
            # Sacamos el bloque afuera transformándolo en un 'elif' independiente al mismo nivel que ESTADO_MENU.
            # Evaluamos que ocurra el evento de click (MOUSEBUTTONDOWN) para poder leer 'event.pos' de forma segura.
            elif estado_actual == cte.ESTADO_GLOSARIO or estado_actual == cte.ESTADO_CREDITOS:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    clic_x, clic_y = event.pos
                    
                    # Rango masivo calibrado con tus dos capturas (Cubre perfectamente el texto amarillo pegado al piso)
                    if (300 <= clic_x <= 720) and (650 <= clic_y <= 768):
                        if snds_volver:
                            random.choice(snds_volver).play()
                            
                        pygame.time.delay(180)
                        estado_actual = cte.ESTADO_MENU

            # Clics de la Selección de Niveles
            elif estado_actual == cte.ESTADO_JUGAR_SELECCION:

                if not musica_menu_sonando:
                    pygame.mixer.music.play(-1)
                    musica_menu_sonando = True

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                    if r_n1.collidepoint(pos_mouse):
                        camino_nivel_1 = [
                            (105, 615), 
                            (230, 615), 
                            (230, 480), 
                            (860, 480), 
                            (860, 350), 
                            (215, 350), 
                            (215, 175), 
                            (512, 175)
                        ]
                        
                        # CREACIÓN PERFECTA: Le pasamos las vidas y fijamos el centro nativo del .rect
                        cabildo = Base(vidas=20)
                        cabildo.nombre = "Cabildo de Buenos Aires"
                        cabildo.rect.center = (512, 175)
                        
                        # (El resto de tus inicializaciones de grupos se quedan exactamente igual abajo...)
                        grupo_torres = pygame.sprite.Group()
                        grupo_enemigos = pygame.sprite.Group()
                        grupo_ingenieros = pygame.sprite.Group()
                        grupo_proyectiles = pygame.sprite.Group()
                        grupo_aliados_moviles = pygame.sprite.Group()
                        administrador_oleadas = WaveManager(camino=camino_nivel_1)
                        interfaz_grafica = UIManager()
                        dinero_patria = cte.DINERO_INICIAL
                        estado_actual = cte.ESTADO_JUEGO_ACTIVO
                        
                        # 1. Instanciamos la Base pasando únicamente el parámetro de vidas
                        cabildo = Base(vidas=20)
                        
                        # 2. Le inyectamos el nombre como un atributo común si tu HUD lo necesita
                        cabildo.nombre = "Cabildo de Buenos Aires"
                        
                        # 3. Lo posicionamos milimétricamente en la entrada del edificio del mapa
                        cabildo.rect.center = (512, 175)
                        
                        # El wave_manager lee la lista y calcula la direccion (dx, dy) cuadro por cuadro
                        administrador_oleadas = WaveManager(camino=camino_nivel_1)
                        interfaz_grafica = UIManager()
                        dinero_patria = cte.DINERO_INICIAL
                        
                        estado_actual = cte.ESTADO_JUEGO_ACTIVO
                    
                    if r_n2.collidepoint(pos_mouse) or r_n3.collidepoint(pos_mouse) or r_n4.collidepoint(pos_mouse):
                        # CORRECCIÓN: Pasamos fondo_seleccion al final también en la pausa dramática
                        dibujar_seleccion_niveles(pantalla, fuente_titulos, fuente_botones, pos_mouse, nivel_5_desbloqueado, postales, True, fondo_seleccion)
                        pygame.display.flip()
                        pygame.time.delay(150)
                        estado_actual = cte.ESTADO_CREDITOS
                        
                    elif nivel_5_desbloqueado and r_n5.collidepoint(pos_mouse):
                        dibujar_seleccion_niveles(pantalla, fuente_titulos, fuente_botones, pos_mouse, nivel_5_desbloqueado, postales, True)
                        pygame.display.flip()
                        pygame.time.delay(150)
                        estado_actual = cte.ESTADO_CREDITOS
                        
                    elif r_volver.collidepoint(pos_mouse):
                        # 1. REPRODUCCIÓN ALEATORIA DE RETROCESO (Gatilla tu efecto FX corto .mp3)
                        if snds_volver:
                            random.choice(snds_volver).play()
                        
                        # --- REMOVEMOS LAS LÍNEAS DE RECARGA MUSICAL DE ACÁ ---
                        # Al quitarlas de este botón, la banda sonora "War Plan" no se va a rebobinar;
                        # va a seguir sonando de largo de forma continua y fluida mientras regresas al inicio.

                        # 2. Forzamos una pausa de microsegundos para dejar escuchar el FX seco de salida
                        pygame.time.delay(180) 
                        
                        # 3. Saltamos de interfaz de forma limpia
                        estado_actual = cte.ESTADO_MENU

            # Clics Adentro de la Partida Activa
            # --- CAPTURA DE EVENTOS DE COMBATE (CORREGIDO ARRIBA EN EL FOR EVENT) ---
            elif estado_actual == cte.ESTADO_JUEGO_ACTIVO:
                # Validamos el instante exacto del click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    # Clic Izquierdo (Botón 1): Construir Torres patrias
                    if event.button == 1:
                        parcela_seleccionada = None
                        # Sincronizamos con la posicion real del impacto (event.pos)
                        for parcela in parcelas_validas:
                            if parcela.collidepoint(event.pos):
                                parcela_seleccionada = parcela
                                break

                        if parcela_seleccionada is not None:
                            tipo_torre = "ciudadanos" if pygame.key.get_pressed()[pygame.K_c] else "gauchos"
                            costo = cte.COSTO_CIUDADANOS if tipo_torre == "ciudadanos" else cte.COSTO_GAUCHOS

                            if dinero_patria >= costo:
                                # Colocamos la torre fija y balanceada en el centro de tu base calibrada
                                nueva_torre = Torre(parcela_seleccionada.centerx, parcela_seleccionada.centery, tipo=tipo_torre)
                                grupo_torres.add(nueva_torre)
                                dinero_patria -= costo

                    # Clic Derecho (Botón 3): Desplegar Ingeniero Militar
                    elif event.button == 3:
                        cabildo.entrenar_ingeniero(grupo_ingenieros, grupo_torres)

            # Clics en la pantalla de Game Over (CORREGIDO)
            elif estado_actual == cte.ESTADO_GAME_OVER:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    
                    # SI ELIGE REINTENTAR: Revisa la posicion [0] (Izquierda)
                    if r_v_go[0].collidepoint(pos_mouse):
                        camino_nivel_1 = [(105, 615), (210, 615), (210, 480), (820, 480), (820, 320), (185, 320), (185, 175), (512, 175)]
                        cabildo = Base(vidas=20)
                        cabildo.nombre = "Cabildo de Buenos Aires"
                        cabildo.rect.center = (512, 175)
                        grupo_torres = pygame.sprite.Group()
                        grupo_enemigos = pygame.sprite.Group()
                        grupo_ingenieros = pygame.sprite.Group()
                        grupo_proyectiles = pygame.sprite.Group()
                        grupo_aliados_moviles = pygame.sprite.Group()
                        administrador_oleadas = WaveManager(camino=camino_nivel_1)
                        dinero_patria = cte.DINERO_INICIAL
                        estado_actual = cte.ESTADO_JUEGO_ACTIVO
                        
                    # SI ELIGE VOLVER: ¡CORRECCIÓN! Cambiamos a la posicion [1] (Derecha)
                    elif r_v_go[1].collidepoint(pos_mouse):
                        estado_actual = cte.ESTADO_MENU

            elif estado_actual == cte.ESTADO_FINAL_MISION:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Si haces clic adentro del rectangulo virtual del boton volver, regresas a salvo al menu
                    if r_v_win.collidepoint(pos_mouse):
                        estado_actual = cte.ESTADO_MENU


        # --- LOGICA Y RENDERIZADO POR FUNCIÓN ---
        if estado_actual == cte.ESTADO_BIENVENIDA:
            dibujar_bienvenida(pantalla, fuente_titulos, fuente_botones, fondo_bienvenida)
            
        elif estado_actual == cte.ESTADO_MENU:
            click_lista = pygame.mouse.get_pressed()
            click_izquierdo_activo = click_lista[0]
            
            # 1. Renderizamos la interfaz visual limpia con sus 11 argumentos estándar
            r_jugar, r_glosario, r_creditos, r_salir = dibujar_menu_principal(
                pantalla, fuente_titulos, pos_mouse, btn_com, btn_glo, btn_cre, btn_sal, 
                click_izquierdo_activo, fondo_menu_grande, logo_juego, tiempo_actual
            )
            
            # 2. CONTROL GLOBAL DE AUDIO ANTI-SPAM (NUEVO)
            # Evaluamos qué botón específico tiene el mouse encima en este frame exacto
            id_boton_actual = -1
            if r_jugar.collidepoint(pos_mouse): id_boton_actual = 0
            elif r_glosario.collidepoint(pos_mouse): id_boton_actual = 1
            elif r_creditos.collidepoint(pos_mouse): id_boton_actual = 2
            elif r_salir.collidepoint(pos_mouse): id_boton_actual = 3
            
            # Si el mouse entró a un botón válido
            if id_boton_actual != -1:
                # Nos aseguramos de tener inicializadas estas variables arriba de tu while correr:
                # control_hover = {"activo": -1} y ultimo_sonido_hover = 0
                if control_hover["activo"] != id_boton_actual:
                    # Validamos que hayan pasado más de 200ms desde el último point.mp3 del sistema
                    if tiempo_actual - ultimo_sonido_hover > 200:
                        if snd_hover:
                            snd_hover.play() # Suena impecable una sola vez
                        ultimo_sonido_hover = tiempo_actual # Registramos el tiempo del pitido
                    control_hover["activo"] = id_boton_actual
            else:
                # Si el mouse está en el fondo del pergamino fuera de los botones, liberamos el foco
                control_hover["activo"] = -1

        elif estado_actual == cte.ESTADO_JUGAR_SELECCION:
            click_lista = pygame.mouse.get_pressed()
            click_izq = click_lista[0]
            
            # CORRECCIÓN: Agregamos 'fondo_seleccion' al final del llamado
            r_n1, r_n2, r_n3, r_n4, r_n5, r_volver = dibujar_seleccion_niveles(
                pantalla, fuente_titulos, fuente_botones, pos_mouse, 
                nivel_5_desbloqueado, postales, click_izq, fondo_seleccion
            )
            
        elif estado_actual in [cte.ESTADO_GLOSARIO, cte.ESTADO_CREDITOS]:
            # CORRECCIÓN: Asegurate de agregar 'r_v_estatico =' al principio de esta línea
            r_v_estatico = dibujar_pantallas_estaticas(pantalla, estado_actual, fuente_titulos, fuente_botones, pos_mouse)
            if not musica_menu_sonando:
                pygame.mixer.music.play(-1)
                musica_menu_sonando = True
            
        elif estado_actual == cte.ESTADO_GAME_OVER:
            r_v_go = dibujar_game_over(pantalla, fuente_titulos, fuente_botones, pos_mouse, fondo_game_over)

        elif estado_actual == cte.ESTADO_GLOSARIO:
            # CORRECCIÓN: Dejamos el llamado original sin arrastrar variables extras
            r_volver = dibujar_pantallas_estaticas(pantalla, estado_actual, fuente_titulos, fuente_botones, pos_mouse)
            
        elif estado_actual == cte.ESTADO_CREDITOS:
            r_volver = dibujar_pantallas_estaticas(pantalla, estado_actual, fuente_titulos, fuente_botones, pos_mouse)
            
        elif estado_actual == cte.ESTADO_FINAL_MISION:
            r_v_win = dibujar_mision_cumplida(
                pantalla, fuente_titulos, fuente_botones, pos_mouse, 
                fondo_victoria, dinero_patria, cabildo.vidas if cabildo else 20,
                interfaz_grafica.icono_moneda if interfaz_grafica else None
            )
            
        elif estado_actual == cte.ESTADO_JUEGO_ACTIVO:
            # 1. CONTROL DE TIEMPO Y LÓGICA INTERNA (Se ejecutan una sola vez)
            grupo_torres.update(grupo_enemigos, grupo_proyectiles, tiempo_actual)
            grupo_proyectiles.update(grupo_enemigos)
            grupo_aliados_moviles.update(grupo_enemigos, tiempo_actual)
            grupo_ingenieros.update(grupo_enemigos)
            cabildo.update(grupo_enemigos, tiempo_actual)

            if musica_menu_sonando:
                pygame.mixer.music.stop() # Apaga el streaming del mp3 al instante
                musica_menu_sonando = False

            # Recorrido de los soldados invasores por los waypoints
            for enemigo in list(grupo_enemigos):
                enemigo.update()
                if enemigo.ha_llegado_al_final:
                    cabildo.recibir_danio(enemigo.danio, group_enemigos if 'group_enemigos' in locals() else grupo_enemigos)
                    enemigo.kill()
                elif not enemigo.alive():
                    dinero_patria += enemigo.recompensa

            # Validacion de condiciones de fin de partida
            if cabildo.vidas <= 0:
                estado_actual = cte.ESTADO_GAME_OVER
            else:
                # El manager corre con tu resguardo nativo de hordas
                administrador_oleadas.update(tiempo_actual, grupo_enemigos, cabildo)

            if administrador_oleadas.oleada_actual > 3:
                estado_actual = cte.ESTADO_FINAL_MISION

            # 2. CAPAS DE RENDERIZADO VISUAL (De atras hacia adelante de forma prolija)
            # Capa Fondo: Primero estampamos el mapa pixel art del Cabildo
            if mapa_cabildo:
                pantalla.blit(mapa_cabildo, (0, 0))
            else:
                pantalla.fill((50, 50, 50))

            # Capa Intermedia: El destello blanco transparente de tus parcelas calibradas a ojo
            for parcela in parcelas_validas:
                if parcela.collidepoint(pos_mouse):
                    surf_indicador = pygame.Surface((parcela.width, parcela.height), pygame.SRCALPHA)
                    pygame.draw.rect(surf_indicador, (255, 255, 255, 80), (0, 0, parcela.width, parcela.height), border_radius=4)
                    pantalla.blit(surf_indicador, (parcela.x, parcela.y))

            # Capa Entidades: Dibujamos la base y los sprites de combate sobre el mapa
            pantalla.blit(cabildo.image, cabildo.rect)
            grupo_torres.draw(pantalla)
            grupo_proyectiles.draw(pantalla)
            grupo_aliados_moviles.draw(pantalla)
            grupo_ingenieros.draw(pantalla)
            grupo_enemigos.draw(pantalla)
            
            # Capa Interfaz: El HUD va arriba de todo para que no lo tapen los personajes
            interfaz_grafica.draw_hud(pantalla, dinero_patria, administrador_oleadas.oleada_actual, cabildo, administrador_oleadas, tiempo_actual)

        pygame.display.update()
        pygame.display.flip()
        reloj.tick(cte.FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
 
