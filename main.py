print("Cargando Pygame...")
import pygame
import sys
import random
print("Cargando Clases...")
from config import constants as cte
from clases.base import Base
from clases.torre import Torre
from clases.texto_flotante import TextoFlotante
print("Cargando Managers...")
from managers.wave_manager import WaveManager
from managers.UI_manager import UIManager
from managers.menu_manager import MenuManager
from managers.sound_manager import SoundManager
from managers.level_manager import LevelManager
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
    administrador_menus = MenuManager()
    administrador_sonidos = SoundManager()
    grupo_textos_flotantes = pygame.sprite.Group()

    administrador_niveles = LevelManager()
    nivel_activo = 1 # Cambiará de forma interactiva según el clic de la grilla

    # --- CONFIGURACIÓN DE LA MÚSICA DE FONDO ---
    pygame.mixer.music.set_volume(0.4) # Arranca a un volumen prudente del 40%
    
    # Ruta directa hacia tu carpeta en la raiz (fuera de assets)
    ruta_musica_menu = "musica/War Plan - Devine-King [Ambient].mp3" 

    # Variables de control para evitar que el sonido de hover suene en bucle infinito
    # Guarda que boton estaba tocando el mouse en el frame anterior
    boton_hover_anterior = -1 

    # --- CARGA AUTOMATIZADA DE BOTONERAS INTERACTIVAS (NUEVO) ---
    # El manager se encarga de buscar los sufijos _selected y _pressed tras bambalinas
    btn_com = administrador_menus.cargar_pack_boton("btn_comenzar")
    btn_glo = administrador_menus.cargar_pack_boton("btn_glosario")
    btn_cre = administrador_menus.cargar_pack_boton("btn_creditos")
    btn_sal = administrador_menus.cargar_pack_boton("btn_salir")

    # Usamos el constructor automático del mánager para armar los packs de 3 estados de un viaje
    postales = {
        "c1": administrador_menus.cargar_pack_boton("cabildo"),
        "c2": administrador_menus.cargar_pack_boton("catedral"),
        "c3": administrador_menus.cargar_pack_boton("elfortin"),
        "c4": administrador_menus.cargar_pack_boton("larecova"),
        "c5": [pygame.Surface((1,1)), pygame.Surface((1,1)), pygame.Surface((1,1))] # Reserva vacía N5
    }

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

    # Buscá estas líneas arriba de tu while correr en el main():
    control_hover = {"activo": -1}
    ultimo_sonido_hover = 0 # Inicializado en 0 como número común y corriente
    tiempo_gear_hundido = 0
    segundo_alerta_anterior = -1

    arrastrando_musica = False
    arrastrando_fx = False

    parcelas_validas = [] 
    pos_barra_vida_activa = (512, 140)

    # === VARIABLES EXCLUSIVAS DEL MODO DEBUG: ESTO NOSE TOCA ===
    juego_en_pausa_debug = False # Se Activa/desactiva la pausa con la tecla P
    puntos_capturados_test = [] 

    r_volver = pygame.Rect(20, 695, 200, 40)

    correr = True

    while correr:
        tiempo_actual = pygame.time.get_ticks()
        pos_mouse = pygame.mouse.get_pos()

        # --- CAPTURA DE EVENTOS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                correr = False

            # 1. Transición: De Bienvenida a Menú Principal
            if estado_actual == cte.ESTADO_BIENVENIDA:
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    administrador_sonidos.reproducir_musica_menu()
                    estado_actual = cte.ESTADO_MENU
                    continue # ¡EL TRUCO! Corta este evento acá para vaciar el clic de la Bienvenida y que no se pase al menú

            # 2. CAPTURA DE EVENTOS DE CLICS EN EL MENÚ PRINCIPAL (SEPARADO Y BLINDADO)
            # Al usar un 'if' o un 'elif' limpio a la misma altura, el juego procesa tu dedo de una
            elif estado_actual == cte.ESTADO_MENU:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    
                    # === 1. CLIC EN COMENZAR / JUGAR ===
                    if r_jugar.collidepoint(pos_mouse):
                        administrador_sonidos.play_siguiente()
                        administrador_menus.dibujar_menu_principal(pantalla, fuente_titulos, pos_mouse, btn_com, btn_glo, btn_cre, btn_sal, True, tiempo_actual)
                        
                        # PARCHE VISUAL: Estampamos el engranaje en este frame exacto para que no desaparezca durante el delay
                        pantalla.blit(administrador_menus.img_gear_nativa, administrador_menus.img_gear_nativa.get_rect(center=rect_gear.center))
                        
                        pygame.display.flip()
                        pygame.time.delay(180)
                        estado_actual = cte.ESTADO_JUGAR_SELECCION
                        
                    # === 2. CLIC EN GLOSARIO ===
                    elif r_glosario.collidepoint(pos_mouse):
                        administrador_sonidos.play_siguiente()
                        administrador_menus.dibujar_menu_principal(pantalla, fuente_titulos, pos_mouse, btn_com, btn_glo, btn_cre, btn_sal, True, tiempo_actual)
                        
                        # PARCHE VISUAL: Estampamos el engranaje antes de congelar la pantalla
                        pantalla.blit(administrador_menus.img_gear_nativa, administrador_menus.img_gear_nativa.get_rect(center=rect_gear.center))
                        
                        pygame.display.flip()
                        pygame.time.delay(180)
                        estado_actual = cte.ESTADO_GLOSARIO
                        
                    # === 3. CLIC EN CRÉDITOS ===
                    elif r_creditos.collidepoint(pos_mouse):
                        administrador_sonidos.play_siguiente()
                        administrador_menus.dibujar_menu_principal(pantalla, fuente_titulos, pos_mouse, btn_com, btn_glo, btn_cre, btn_sal, True, tiempo_actual)
                        
                        # PARCHE VISUAL: Estampamos el engranaje antes de congelar la pantalla
                        pantalla.blit(administrador_menus.img_gear_nativa, administrador_menus.img_gear_nativa.get_rect(center=rect_gear.center))
                        
                        pygame.display.flip()
                        pygame.time.delay(180)
                        estado_actual = cte.ESTADO_CREDITOS
                        
                    # === 4. CLIC EN SALIR ===
                    elif r_salir.collidepoint(pos_mouse):
                        administrador_menus.dibujar_menu_principal(pantalla, fuente_titulos, pos_mouse, btn_com, btn_glo, btn_cre, btn_sal, True, tiempo_actual)
                        
                        # PARCHE VISUAL: Estampamos el engranaje antes de congelar la pantalla
                        pantalla.blit(administrador_menus.img_gear_nativa, administrador_menus.img_gear_nativa.get_rect(center=rect_gear.center))
                        
                        pygame.display.flip()
                        pygame.time.delay(150)
                        correr = False

                    # === 5. CLIC EN EL ENGRANAJE DE CONFIGURACIÓN ===
                    elif rect_gear.collidepoint(pos_mouse):
                        pass

            # Sacamos el bloque afuera transformándolo en un 'elif' independiente al mismo nivel que ESTADO_MENU y evaluamos que ocurra el evento de click (MOUSEBUTTONDOWN) para poder leer 'event.pos' de forma segura.
            elif estado_actual == cte.ESTADO_GLOSARIO or estado_actual == cte.ESTADO_CREDITOS:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    clic_x, clic_y = event.pos
                    
                    if (300 <= clic_x <= 720) and (710 <= clic_y <= 760):
                        
                        # El mánager ejecuta el FX aleatorio de retroceso
                        administrador_sonidos.play_volver()
                            
                        pygame.time.delay(180) # Colchón obligatorio para dejar sonar el mp3
                        
                        # El mánager se asegura de que la música de fondo siga rodando estable
                        administrador_sonidos.reproducir_musica_menu()
                        
                        # Cambia el estado a salvo al menú principal
                        estado_actual = cte.ESTADO_MENU 

            # Clics de la Selección de Niveles
            elif estado_actual == cte.ESTADO_JUGAR_SELECCION:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    
                    # EL SENSOR DEL BOTÓN VOLVER
                    # Evaluamos tanto tu caja física invisible 'r_volver' como el rango explícito de píxeles
                    if r_volver.collidepoint(pos_mouse) or ((20 <= pos_mouse[0] <= 220) and (695 <= pos_mouse[1] <= 735)):
                        # Gatillamos tu efecto aleatorio de retroceso de la ticketera
                        administrador_sonidos.play_volver()
                        
                        pygame.time.delay(150) # Colchón mínimo para dejar sonar el mp3
                        estado_actual = cte.ESTADO_MENU # Regresamos a salvo al menú principal
                        continue # Saltamos el frame para limpiar la cola gráfica
                        
                    # === 2. CLIC EN EL NIVEL 1: CABILDO ===
                    elif r_n1.collidepoint(pos_mouse):
                        administrador_sonidos.detener_musica()
                        administrador_sonidos.reproducir_musica_combate()
                        
                        nivel_activo = 1
                        
                        # === CONTROL DE ATRIBUTOS DINÁMICOS NATIVOS ===
                        # Le pedimos al mánager de forma elegante las estructuras de este mapa
                        camino_activo = administrador_niveles.obtener_camino_nivel(nivel_activo)
                        parcelas_validas = administrador_niveles.obtener_parcelas_nivel(nivel_activo)
                        pos_barra_vida_activa = administrador_niveles.obtener_posicion_barra_vida(nivel_activo)

                        cabildo = Base(vidas=20)
                        cabildo.nombre = "Cabildo de Buenos Aires"
                        cabildo.rect.center = (512, 175)
                        
                        grupo_torres = pygame.sprite.Group()
                        grupo_enemigos = pygame.sprite.Group()
                        grupo_ingenieros = pygame.sprite.Group()
                        grupo_proyectiles = pygame.sprite.Group()
                        grupo_aliados_moviles = pygame.sprite.Group()
                        
                        # Pasamos la ruta limpia al mánager de hordas
                        administrador_oleadas = WaveManager(camino=camino_activo)
                        administrador_oleadas.tiempo_inicio_descanso = tiempo_actual
                        
                        interfaz_grafica = UIManager()
                        dinero_patria = cte.DINERO_INICIAL
                        estado_actual = cte.ESTADO_JUEGO_ACTIVO

                    # NIVEL 2: LA CATEDRAL
                    elif r_n2.collidepoint(pos_mouse):
                        administrador_sonidos.detener_musica()
                        administrador_sonidos.reproducir_musica_combate()
                        
                        nivel_activo = 2
                        
                        # === SINCRO AUTOMÁTICA DE LA CATEDRAL (MUDADO AL MANAGER) ===
                        camino_activo = administrador_niveles.obtener_camino_nivel(nivel_activo)
                        parcelas_validas = administrador_niveles.obtener_parcelas_nivel(nivel_activo)
                        pos_barra_vida_activa = administrador_niveles.obtener_posicion_barra_vida(nivel_activo)
                        
                        cabildo = Base(vidas=20)
                        cabildo.nombre = "Catedral de Buenos Aires"
                        cabildo.rect.center = (455, 240) # Posición del portón de la Catedral
                        
                        grupo_torres = pygame.sprite.Group()
                        grupo_enemigos = pygame.sprite.Group()
                        grupo_ingenieros = pygame.sprite.Group()
                        grupo_proyectiles = pygame.sprite.Group()
                        grupo_aliados_moviles = pygame.sprite.Group()
                        
                        # El mánager de hordas lee tu matriz de bifurcaciones del LevelManager
                        administrador_oleadas = WaveManager(camino=camino_activo)
                        administrador_oleadas.tiempo_inicio_descanso = tiempo_actual
                        
                        interfaz_grafica = UIManager()
                        dinero_patria = cte.DINERO_INICIAL
                        estado_actual = cte.ESTADO_JUEGO_ACTIVO

            # Clics Adentro de la Partida Activa
            # --- CAPTURA DE EVENTOS DE COMBATE (CORREGIDO ARRIBA EN EL FOR EVENT) ---
            elif estado_actual == cte.ESTADO_JUEGO_ACTIVO:
                
                # A. CAPTURA DE TECLADO PARA DIAGNÓSTICO (NUEVO)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        # Invertimos el estado de la pausa al presionar la letra 'P'
                        juego_en_pausa_debug = not juego_en_pausa_debug
                        if juego_en_pausa_debug:
                            print("\n[ DEBUG ] === PARTIDA PAUSADA === Clickear en la calle para obtener Waypoints.")
                        else:
                            print("[ DEBUG ] === PARTIDA REANUDADA ===\n")
                
                # B. CAPTURA DE PÍXELES EN PAUSA
                if juego_en_pausa_debug and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Capturamos la coordenada exacta del mouse bajo tu cursor
                    coord_x, coord_y = event.pos
                    puntos_capturados_test.append((coord_x, coord_y))
                    
                    # Imprime el punto listo con formato de tupla para que lo copies directo a tu lista
                    print(f"({coord_x}, {coord_y}),  # Waypoint {len(puntos_capturados_test)}")
                    continue # Salteamos la lógica de construcción común para que no gaste dinero al probar
                
                if not juego_en_pausa_debug and event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        parcela_seleccionada = None
                        
                        # Sincronizamos con la posición real del impacto (event.pos)
                        for parcela in parcelas_validas:
                            if parcela.collidepoint(event.pos):
                                parcela_seleccionada = parcela
                                break

                        if parcela_seleccionada is not None:
                            # Determinamos el tipo de tropa y su balance según el teclado
                            tipo_torre = "ciudadanos" if pygame.key.get_pressed()[pygame.K_c] else "gauchos"
                            costo = cte.COSTO_CIUDADANOS if tipo_torre == "ciudadanos" else cte.COSTO_GAUCHOS

                            if dinero_patria >= costo:
                                # Creamos un rectángulo virtual idéntico al tamaño de la parcela en esa coordenada
                                caja_sensor_torre = pygame.Rect(parcela_seleccionada.x, parcela_seleccionada.y, parcela_seleccionada.width, parcela_seleccionada.height)
                                
                                # Escaneamos el mapa completo buscando colisiones contra las torres ya construidas
                                torre_ya_existente = False
                                for torre_instalada in grupo_torres:
                                    if caja_sensor_torre.colliderect(torre_instalada.rect):
                                        torre_ya_existente = True
                                        break # Cortamos el escaneo porque ya encontramos una superposición
                                
                                # Validamos el cerrojo de espacio
                                if not torre_ya_existente:
                                    # Si la parcela está 100% vacía y limpia, permitimos la inversión patria
                                    nueva_torre = Torre(parcela_seleccionada.centerx, parcela_seleccionada.centery, tipo=tipo_torre)
                                    grupo_torres.add(nueva_torre)
                                    dinero_patria -= costo

                                    # 2. AUDIO DE COMPRA INDUSTRIAL (NUEVO)
                                    # Disparará tu efecto ca-ching desde su canal suelto FX
                                    administrador_sonidos.play_caching()
                                    
                                    # 3. EFECTO VISUAL DE GASTO EN PANTALLA (NUEVO)
                                    # Fabricamos el cartel de dinero restado (ej: -120 o -150 según la tropa)
                                    cartel_restar = TextoFlotante(
                                        texto=f"-{costo}", 
                                        pos_x=parcela_seleccionada.centerx, 
                                        pos_y=parcela_seleccionada.top, # Nace flotando prolijo arriba de la parcela
                                        fuente=fuente_botones, # Usa tu tipografía nativa grande del juego
                                        color=(255, 0, 0) # Rojo nítido revolucionario
                                    )
                                    grupo_textos_flotantes.add(cartel_restar)

                                    print(f"[ BILLETERA ] Inversión realizada: ¡Desplegados {tipo_torre} en la defensa!")
                                else:
                                    # Feedback de aviso preventivo en la consola por si intenta trampear la grilla
                                    print("[ AVISO MILITAR ] ¡Estrategia inválida! No podés encimar dos batallones en la misma parcela de tierra.")
                                # ========================================================

                    # 2. Clic Derecho (Botón 3): Desplegar Ingeniero Militar
                    elif event.button == 3:
                        cabildo.entrenar_ingeniero(grupo_ingenieros, grupo_torres)

            # --- CAPTURA DE EVENTOS EN PANTALLA DE DERROTA (CORREGIDO) ---
            elif estado_actual == cte.ESTADO_GAME_OVER:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    
                    # Clic en REINTENTAR DEFENSA
                    if r_reintentar.collidepoint(pos_mouse):
                        if snds_siguiente: 
                            random.choice(snds_siguiente).play()
                        
                        print("\n========================================================")
                        print(" ¡REINTENTANDO MISIÓN! Reorganizando las milicias criollas...")
                        print("========================================================\n")
                        
                        grupo_enemigos.empty()
                        grupo_torres.empty()
                        grupo_proyectiles.empty()
                        grupo_ingenieros.empty()
                        grupo_aliados_moviles.empty()
                        
                        cabildo = Base() 
                        cabildo.vidas = 20 
                        
                        # --- CORRECCIÓN CRÍTICA DE OLEADAS ---
                        administrador_oleadas.oleada_actual = 1
                        # Volvemos a inyectar tus 5 soldados de la horda 1 del inicio del juego (GDD)
                        administrador_oleadas.enemigos_pendientes = ["soldado_raso"] * 5
                        
                        administrador_oleadas.en_descanso = True
                        administrador_oleadas.tiempo_inicio_descanso = tiempo_actual
                        dinero_patria = 150 
                        
                        estado_actual = cte.ESTADO_JUEGO_ACTIVO
                        
                    # Clic en VOLVER AL MENÚ PRINCIPAL desde la derrota
                    elif r_v_go.collidepoint(pos_mouse):
                        # 1. El mánager reproduce el audio aleatorio de retroceso
                        administrador_sonidos.play_volver()
                            
                        # 2. El mánager se encarga de recargar y encender la orquesta War Plan de forma autónoma
                        administrador_sonidos.reproducir_musica_menu()
                        
                        estado_actual = cte.ESTADO_MENU # Regresamos a salvo al inicio

            elif estado_actual == cte.ESTADO_FINAL_MISION:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    
                    # Clic en CONTINUAR CAMPAÑA
                    if r_v_win.collidepoint(pos_mouse):
                        # 1. El mánager reproduce el audio aleatorio de avance
                        administrador_sonidos.play_siguiente()
                            
                        pygame.time.delay(180) # Colchón obligatorio para escuchar el mp3
                        
                        # 2. El mánager reactiva la música de los menúes de forma segura
                        administrador_sonidos.reproducir_musica_menu()
                        
                        estado_actual = cte.ESTADO_MENU

            elif estado_actual == cte.ESTADO_OPCIONES:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    
                    # Sincronizado milimétricamente con el sensor del texto de Y = 735 (Rango 710 a 760)
                    if (300 <= pos_mouse[0] <= 720) and (710 <= pos_mouse[1] <= 760):
                        # El mánager reproduce el FX de retroceso aleatorio de tu ticketera
                        administrador_sonidos.play_volver()
                        
                        pygame.time.delay(180) # Colchón reglamentario para dejar sonar el mp3
                        
                        # Cambia el estado de regreso a salvo al menú principal
                        estado_actual = cte.ESTADO_MENU

        # --- LOGICA Y RENDERIZADO POR FUNCIÓN ---
        if estado_actual == cte.ESTADO_BIENVENIDA:
            administrador_menus.dibujar_bienvenida(pantalla, fuente_titulos, fuente_botones)
            
        elif estado_actual == cte.ESTADO_MENU:
            click_lista = pygame.mouse.get_pressed()
            click_izquierdo_activo = click_lista[0]
            
            # RECORTE DE LLAMADO: Pasamos el llamado limpio terminando en tiempo_actual
            r_jugar, r_glosario, r_creditos, r_salir = administrador_menus.dibujar_menu_principal(
                pantalla, fuente_titulos, pos_mouse, btn_com, btn_glo, btn_cre, btn_sal, 
                click_izquierdo_activo, tiempo_actual
            )
            
            # 2. CONTROL GLOBAL DE AUDIO ANTI-SPAM
            id_boton_actual = -1
            if r_jugar.collidepoint(pos_mouse): id_boton_actual = 0
            elif r_glosario.collidepoint(pos_mouse): id_boton_actual = 1
            elif r_creditos.collidepoint(pos_mouse): id_boton_actual = 2
            elif r_salir.collidepoint(pos_mouse): id_boton_actual = 3
            
            if id_boton_actual != -1:
                if control_hover["activo"] != id_boton_actual:
                    if tiempo_actual - ultimo_sonido_hover > 200:
                        administrador_sonidos.play_hover()
                        ultimo_sonido_hover = tiempo_actual 
                    control_hover["activo"] = id_boton_actual
            else:
                control_hover["activo"] = -1

            # ========================================================
            # INYECCIÓN EXTRA: MOTOR INTERACTIVO DEL ENGRANAJE (REPARADO Y FIJADO)
            # ========================================================
            tam_base = 69
            rect_gear = pygame.Rect(930, 670, tam_base, tam_base)
            img_gear_render = administrador_menus.img_gear_nativa
            
            # Inicializamos una variable de disparo arriba de tu while correr si preferís, o acá mismo:
            if 'solto_clic_gear' not in locals():
                solto_clic_gear = False

            if rect_gear.collidepoint(pos_mouse):
                if click_izquierdo_activo:
                    # ESTADO PRESIONADO: Se achica un 15% (Se hunde visiblemente mientras mantengas el dedo apoyado)
                    tam_click = int(tam_base * 0.85)
                    img_gear_render = pygame.transform.scale(img_gear_render, (tam_click, tam_click))
                    solto_clic_gear = True # Activamos el gatillo de que el botón fue hundido
                else:
                    # TRANSICIÓN CINEMÁTICA AL SOLTAR EL CLIC:
                    # Si el botón estuvo hundido y recién ahora levantaste el dedo del mouse
                    if solto_clic_gear:
                        solto_clic_gear = False # Reseteamos el gatillo
                        administrador_sonidos.play_gear() # Suena tu mp3 mecánico
                        pygame.time.delay(80) # Breve colchón que ahora sí es legal para escuchar el click
                        estado_actual = cte.ESTADO_OPCIONES # Viajamos al panel de volumen
                    else:
                        tam_hover = int(tam_base * 1.06)
                        img_gear_render = pygame.transform.scale(img_gear_render, (tam_hover, tam_hover))
                        
                        # === RESPLANDOR GRISÁCEO TENUE NATIVO ===
                        copia_brillo = img_gear_render.copy()
                        mascara_gear = pygame.mask.from_surface(copia_brillo)
                        
                        silueta_gris = pygame.Surface(copia_brillo.get_size(), pygame.SRCALPHA)
                        mascara_gear.to_surface(surface=silueta_gris, setcolor=(200, 200, 200, 255), unsetcolor=(0, 0, 0, 0))
                        
                        silueta_gris.set_alpha(90) 
                        copia_brillo.blit(silueta_gris, (0, 0))
                        img_gear_render = copia_brillo
            else:
                # Si sacás el mouse de la zona, cancelamos el gatillo de cambio de pantalla por seguridad
                solto_clic_gear = False

            # Estampamos el engranaje perfectamente centrado en su caja invisible de colisión
            pantalla.blit(img_gear_render, img_gear_render.get_rect(center=rect_gear.center))

        elif estado_actual == cte.ESTADO_JUGAR_SELECCION:
            click_lista = pygame.mouse.get_pressed()
            click_izquierdo_activo = click_lista
            
            # --- BYPASS INDUSTRIAL CONTRA EL VALUEERROR ---
            # Guardamos TODO lo que escupa la función adentro de una única variable contenedora
            retorno_mapas = administrador_menus.dibujar_seleccion_niveles(
                pantalla, fuente_titulos, fuente_botones, pos_mouse, 
                nivel_5_desbloqueado, postales, click_izquierdo_activo
            )
            
            # Asignamos las variables de forma segura leyendo las posiciones del contenedor.
            # Esto evita que el programa crashee sin importar si la función devuelve 2, 4 o 5 elementos.
            r_n1 = retorno_mapas[0]
            
            # Buscamos el último elemento de la tupla (que siempre es el botón volver en tu UIManager)
            r_volver = retorno_mapas[-1]
            
            # Resguardo preventivo para tus otras portadas de la matriz por si las lee tu captura de clics
            if len(retorno_mapas) >= 5:
                r_n2 = retorno_mapas[1]
                r_n3 = retorno_mapas[2]
                r_n4 = retorno_mapas[3]
            
        elif estado_actual == cte.ESTADO_GAME_OVER:
            # Sincronizamos con tus variables nativas de la derrota: r_reintentar y r_v_go
            r_reintentar, r_v_go = administrador_menus.dibujar_game_over(pantalla, fuente_titulos, fuente_botones, pos_mouse)

        elif estado_actual == cte.ESTADO_FINAL_MISION:
            # RECORTE DE LLAMADO: Dejamos el llamado limpio terminando en cabildo.vidas
            r_v_win = administrador_menus.dibujar_mision_cumplida(
                pantalla, fuente_titulos, fuente_botones, pos_mouse, dinero_patria, cabildo.vidas
            )

        elif estado_actual in [cte.ESTADO_GLOSARIO, cte.ESTADO_CREDITOS]:
            r_v_estatico = administrador_menus.dibujar_pantallas_estaticas(pantalla, estado_actual, fuente_titulos, fuente_botones, pos_mouse)
            # El mánager controla el streaming colonial de fondo
            administrador_sonidos.reproducir_musica_menu()

        elif estado_actual == cte.ESTADO_GLOSARIO:
            r_volver = administrador_menus.dibujar_pantallas_estaticas(pantalla, estado_actual, fuente_titulos, fuente_botones, pos_mouse)
            
        elif estado_actual == cte.ESTADO_CREDITOS:
            r_volver = administrador_menus.dibujar_pantallas_estaticas(pantalla, estado_actual, fuente_titulos, fuente_botones, pos_mouse)

        elif estado_actual == cte.ESTADO_OPCIONES:
            click_lista = pygame.mouse.get_pressed()
            click_izquierdo_sostenido = click_lista[0]
            
            # 1. RENDERIZADO VISUAL EN PANTALLA
            r_v_opciones = administrador_menus.dibujar_pantalla_opciones(
                pantalla, fuente_titulos, fuente_botones, pos_mouse, administrador_sonidos
            )
            
            barra_x = 280
            barra_largo = 500
            
            # 2. PROCESADOR DE FOCO Y SEGURIDAD CONTRA ARRASTRES FANTASMAS
            if click_izquierdo_sostenido:
                # Si el usuario hace clic inicial adentro de la zona de música, capturamos el foco de esa barra
                if administrador_menus.rect_zona_musica.collidepoint(pos_mouse) and not arrastrando_fx:
                    arrastrando_musica = True
                # Si hace clic inicial adentro de la zona de efectos, capturamos su foco exclusivo
                elif administrador_menus.rect_zona_fx.collidepoint(pos_mouse) and not arrastrando_musica:
                    arrastrando_fx = True
            else:
                # En cuanto el usuario levanta físicamente el dedo del mouse, liberamos los candados en el acto
                arrastrando_musica = False
                arrastrando_fx = False

            # 3. EJECUCIÓN HORIZONTAL CONTINUA (IGNORA EL DESVÍO VERTICAL DEL CURSOR)
            if arrastrando_musica:
                # Calculamos el porcentaje basándonos únicamente en la posición X actual del cursor
                pixeles_locales = pos_mouse[0] - barra_x
                porcentaje_nuevo = max(0.0, min(1.0, pixeles_locales / barra_largo))
                administrador_sonidos.actualizar_volumen_musica(porcentaje_nuevo)
                
            elif arrastrando_fx:
                pixeles_locales = pos_mouse[0] - barra_x
                porcentaje_nuevo = max(0.0, min(1.0, pixeles_locales / barra_largo))
                administrador_sonidos.actualizar_volumen_fx(porcentaje_nuevo)
            
        elif estado_actual == cte.ESTADO_JUEGO_ACTIVO:

            bx, by = pos_barra_vida_activa
            
            # Calculamos el ancho verde proporcional a la salud actual del cabildo/catedral
            ancho_barra = 160 # Largo total de la barra en píxeles
            ancho_verde = int((cabildo.vidas / cabildo.vidas_maximas) * ancho_barra)
            
            # 1. Dibujamos el fondo de la barra (Rectángulo negro de contorno)
            pygame.draw.rect(pantalla, (0, 0, 0), (bx - (ancho_barra // 2), by, ancho_barra, 14))
            # 2. Dibujamos la barra de salud (Rectángulo verde interno)
            pygame.draw.rect(pantalla, (0, 255, 0), (bx - (ancho_barra // 2) + 2, by + 2, ancho_verde - 4, 10))

            # 1. CENTRALIZADOR DE DERROTA INDUSTRIAL (MANTENIDO ARRIBA Y POR FUERA)
            if cabildo.vidas <= 0:
                administrador_sonidos.detener_musica() 
                administrador_sonidos.play_gameover()
                print("\n========================================================")
                print(" ¡EL CABILDO HA CAÍDO! Las hordas realistas tomaron la plaza.")
                print("========================================================\n")
                estado_actual = cte.ESTADO_GAME_OVER
                continue  

            # ========================================================
            # ENVOLTORIO DEL MODO DESARROLLADOR (PAUSA DEBUG)
            # ========================================================
            # Si la tecla 'P' NO fue presionada, corre la simulación de guerra con total normalidad
            if not juego_en_pausa_debug:

                # 3. ACTUALIZACIÓN DE ENTIDADES CONTINUA 
                grupo_enemigos.update()
                grupo_torres.update(grupo_enemigos, grupo_proyectiles, tiempo_actual, administrador_sonidos)  
                grupo_proyectiles.update(grupo_enemigos)
                grupo_aliados_moviles.update(grupo_enemigos, tiempo_actual)
                grupo_ingenieros.update(grupo_enemigos)
                cabildo.update(grupo_enemigos, tiempo_actual)
                grupo_textos_flotantes.update() 
                
                # Sincronización con tu mánager de hordas original del main
                administrador_oleadas.update(tiempo_actual, grupo_enemigos, cabildo)

                # 4. PROCESADOR DE IMPACTOS, RECOMPENSAS Y ANIMACIONES DE MUERTE
                for enemigo in list(grupo_enemigos):
                    # Caso A: El invasor esquivó tus defensas y vulneró el Cabildo
                    if enemigo.ha_llegado_al_final:
                        cabildo.recibir_danio(enemigo.danio, grupo_enemigos)
                        enemigo.kill() 
                        continue

                    # Caso B: El enemigo fue alcanzado por las torres o por el Grito de la Patria
                    elif enemigo.vida <= 0 and not getattr(enemigo, "ya_pago_recompensa", False):
                        dinero_patria += enemigo.recompensa
                        enemigo.ya_pago_recompensa = True
                        
                        # === REPARACIÓN DE PASE DE PARÁMETROS ===
                        # Llamamos a tu método nativo pasándole tu 'administrador_sonidos' global del main()
                        enemigo.recibir_danio(0, grupo_enemigos, administrador_sonidos)
                        
                        enemigo.esta_muerto = True
                        enemigo.frame_actual = 0
                        enemigo.ultimo_refresco = pygame.time.get_ticks()

                    # Caso C: El soldado ya cobró y está pasando por sus cuadros de desvanecimiento
                    elif getattr(enemigo, "esta_muerto", False):
                        pass

            # ========================================================
            # ORQUESTADOR DE CUENTA REGRESIVA DE OLEADAS 
            # ========================================================
            # Validamos si el manager de hordas está en tiempo de descanso/espera antes de mandar soldados
            if hasattr(administrador_oleadas, "en_descanso") and administrador_oleadas.en_descanso:
                
                # REPARACIÓN MATEMÁTICA REAL: Sumamos el inicio + la duración y le restamos el tiempo actual
                tiempo_limite = administrador_oleadas.tiempo_inicio_descanso + administrador_oleadas.duracion_descanso
                tiempo_restante_ms = tiempo_limite - tiempo_actual
                
                segundos_restantes = max(0, int(tiempo_restante_ms / 1000))
                # Candado de un solo pulso: evaluamos si cambió el segundo físico en este frame
                if segundos_restantes != segundo_alerta_anterior:
                    segundo_alerta_anterior = segundos_restantes # Seteamos el nuevo registro
                    
                    # Rango A: Alerta Regular de preparación (De 10 a 4 segundos inclusive)
                    if 3 < segundos_restantes <= 10:
                        administrador_sonidos.play_countdown()
                        print(f"[ RELOJ PATRIO ] Quedan {segundos_restantes}s... ¡Preparen la defensa!")
                        
                    # Rango B: Alerta Crítica de invasión inminente (De 3 a 1 segundos inclusive)
                    elif 0 < segundos_restantes <= 3:
                        administrador_sonidos.play_lowcountdown()
                        print(f"[ RELOJ PATRIO ] Quedan {segundos_restantes}s... ¡Realistas a la vista!")
                        
                    # === RANGO C: IMPACTO CRÍTICO SEGUNDO CERO (NUEVO GATILLO) ===
                    elif segundos_restantes == 0:
                        if nivel_activo == 1:
                            # Hacemos sonar campana.mp3 en el Cabildo de Buenos Aires
                            administrador_sonidos.play_campana_cabildo()
                        elif nivel_activo == 2:
                            # Hacemos sonar al azar catedral1 o catedral2.mp3 en la Catedral
                            administrador_sonidos.play_alerta_catedral()
                            
                        print("[ RELOJ PATRIO ] ¡CERO SEGUNDOS! ¡Las campanas anuncian la invasión!")
            else:
                # En cuanto los enemigos empiezan a marchar por el mapa, limpiamos el casillero para la próxima horda
                segundo_alerta_anterior = -1

            # 5. EL MÁNAGER DE OLEADAS GESTIONA LAS HORDAS DE FORMA SEGURA
            administrador_oleadas.update(tiempo_actual, grupo_enemigos, cabildo)

            # 6. DETECTOR DE VICTORIA REVOLUCIONARIA DEFINITIVA
            if administrador_oleadas.oleada_actual > 3:
                administrador_sonidos.detener_musica() 
                administrador_sonidos.play_victoria()
                estado_actual = cte.ESTADO_FINAL_MISION

            # ========================================================
            # 2. CAPAS DE RENDERIZADO VISUAL (CORREGIDO CONTRA EL NAMEERROR)
            # ========================================================
            # Capa Fondo: El LevelManager se encarga de estampar la textura correspondiente de forma dinámica
            mapa_fondo_en_combate = administrador_niveles.cargar_mapa_nivel(nivel_activo)
            pantalla.blit(mapa_fondo_en_combate, (0, 0))

            # Capa Intermedia: El destello blanco de tus parcelas calibradas a ojo (Sigue igual abajo...)
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
            grupo_textos_flotantes.draw(pantalla) 

            # Capa Interfaz: El HUD va arriba de todo para que no lo tapen los personajes
            interfaz_grafica.draw_hud(pantalla, dinero_patria, administrador_oleadas.oleada_actual, cabildo, administrador_oleadas, tiempo_actual, pos_barra_vida_activa)

        pygame.display.update()
        pygame.display.flip()
        reloj.tick(cte.FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
 
