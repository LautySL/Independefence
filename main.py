print("Cargando Pygame...")
import pygame
import sys
import random
from config import constants as cte
from clases.base import Base
from clases.torre import Torre
from managers.wave_manager import WaveManager
print("Cargando Managers...")
from managers.UI_manager import UIManager
from managers.menu_manager import MenuManager
print("¡Todos los archivos se cargaron con éxito!")

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
    administrador_menus = MenuManager()

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
                        administrador_menus.dibujar_menu_principal(pantalla, fuente_titulos, pos_mouse, btn_com, btn_glo, btn_cre, btn_sal, True, fondo_menu_grande, logo_juego, tiempo_actual)
                        pygame.display.flip()
                        pygame.time.delay(180)
                        estado_actual = cte.ESTADO_JUGAR_SELECCION
                        
                    # 2. CLIC EN GLOSARIO 
                    elif r_glosario.collidepoint(pos_mouse):
                        if snds_siguiente:
                            random.choice(snds_siguiente).play()
                        # CORRECCIÓN: Dejamos el llamado limpio terminando en tiempo_actual
                        administrador_menus.dibujar_menu_principal(pantalla, fuente_titulos, pos_mouse, btn_com, btn_glo, btn_cre, btn_sal, True, fondo_menu_grande, logo_juego, tiempo_actual)
                        pygame.display.flip()
                        pygame.time.delay(180)
                        estado_actual = cte.ESTADO_GLOSARIO
                        
                    # 3. CLIC EN CRÉDITOS 
                    elif r_creditos.collidepoint(pos_mouse):
                        if snds_siguiente:
                            random.choice(snds_siguiente).play()
                        # CORRECCIÓN: Dejamos el llamado limpio terminando en tiempo_actual
                        administrador_menus.dibujar_menu_principal(pantalla, fuente_titulos, pos_mouse, btn_com, btn_glo, btn_cre, btn_sal, True, fondo_menu_grande, logo_juego, tiempo_actual)
                        pygame.display.flip()
                        pygame.time.delay(180)
                        estado_actual = cte.ESTADO_CREDITOS
                        
                    # 4. CLIC EN SALIR 
                    elif r_salir.collidepoint(pos_mouse):
                        # CORRECCIÓN: Dejamos el llamado limpio terminando en tiempo_actual
                        administrador_menus.dibujar_menu_principal(pantalla, fuente_titulos, pos_mouse, btn_com, btn_glo, btn_cre, btn_sal, True, fondo_menu_grande, logo_juego, tiempo_actual)
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
                        administrador_menus.dibujar_seleccion_niveles(pantalla, fuente_titulos, fuente_botones, pos_mouse, nivel_5_desbloqueado, postales, True, fondo_seleccion)
                        pygame.display.flip()
                        pygame.time.delay(150)
                        estado_actual = cte.ESTADO_CREDITOS
                        
                    elif nivel_5_desbloqueado and r_n5.collidepoint(pos_mouse):
                        administrador_menus.dibujar_seleccion_niveles(pantalla, fuente_titulos, fuente_botones, pos_mouse, nivel_5_desbloqueado, postales, True)
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
            administrador_menus.dibujar_bienvenida(pantalla, fuente_titulos, fuente_botones, fondo_bienvenida)
            
        elif estado_actual == cte.ESTADO_MENU:
            click_lista = pygame.mouse.get_pressed()
            click_izquierdo_activo = click_lista[0]
            
            # 1. Renderizamos la interfaz visual limpia con sus 11 argumentos estándar
            r_jugar, r_glosario, r_creditos, r_salir = administrador_menus.dibujar_menu_principal(
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
            r_n1, r_n2, r_n3, r_n4, r_n5, r_volver = administrador_menus.dibujar_seleccion_niveles(
                pantalla, fuente_titulos, fuente_botones, pos_mouse, 
                nivel_5_desbloqueado, postales, click_izq, fondo_seleccion
            )
            
        elif estado_actual in [cte.ESTADO_GLOSARIO, cte.ESTADO_CREDITOS]:
            # CORRECCIÓN: Asegurate de agregar 'r_v_estatico =' al principio de esta línea
            r_v_estatico = administrador_menus.dibujar_pantallas_estaticas(pantalla, estado_actual, fuente_titulos, fuente_botones, pos_mouse)
            if not musica_menu_sonando:
                pygame.mixer.music.play(-1)
                musica_menu_sonando = True
            
        elif estado_actual == cte.ESTADO_GAME_OVER:
            r_v_go = administrador_menus.dibujar_game_over(pantalla, fuente_titulos, fuente_botones, pos_mouse, fondo_game_over)

        elif estado_actual == cte.ESTADO_GLOSARIO:
            # CORRECCIÓN: Dejamos el llamado original sin arrastrar variables extras
            r_volver = administrador_menus.dibujar_pantallas_estaticas(pantalla, estado_actual, fuente_titulos, fuente_botones, pos_mouse)
            
        elif estado_actual == cte.ESTADO_CREDITOS:
            r_volver = administrador_menus.dibujar_pantallas_estaticas(pantalla, estado_actual, fuente_titulos, fuente_botones, pos_mouse)
            
        elif estado_actual == cte.ESTADO_FINAL_MISION:
            r_v_win = administrador_menus.dibujar_mision_cumplida(
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
 
