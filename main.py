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
                    
                    # Clic en COMENZAR / JUGAR
                    if r_jugar.collidepoint(pos_mouse):
                        administrador_sonidos.play_siguiente()
                        administrador_menus.dibujar_menu_principal(pantalla, fuente_titulos, pos_mouse, btn_com, btn_glo, btn_cre, btn_sal, True, tiempo_actual)
                        pygame.display.flip()
                        pygame.time.delay(180)
                        estado_actual = cte.ESTADO_JUGAR_SELECCION
                        
                    # Clic en GLOSARIO
                    elif r_glosario.collidepoint(pos_mouse):
                        administrador_sonidos.play_siguiente()
                        administrador_menus.dibujar_menu_principal(pantalla, fuente_titulos, pos_mouse, btn_com, btn_glo, btn_cre, btn_sal, True, tiempo_actual)
                        pygame.display.flip()
                        pygame.time.delay(180)
                        estado_actual = cte.ESTADO_GLOSARIO
                        
                    # Clic en CRÉDITOS
                    elif r_creditos.collidepoint(pos_mouse):
                        administrador_sonidos.play_siguiente()
                        administrador_menus.dibujar_menu_principal(pantalla, fuente_titulos, pos_mouse, btn_com, btn_glo, btn_cre, btn_sal, True, tiempo_actual)
                        pygame.display.flip()
                        pygame.time.delay(180)
                        estado_actual = cte.ESTADO_CREDITOS
                        
                    # Clic en SALIR
                    elif r_salir.collidepoint(pos_mouse):
                        administrador_menus.dibujar_menu_principal(pantalla, fuente_titulos, pos_mouse, btn_com, btn_glo, btn_cre, btn_sal, True, tiempo_actual)
                        pygame.display.flip()
                        pygame.time.delay(150)
                        correr = False

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

                # REMOVEMOS 'administrador_sonidos.reproducir_musica_menu()' de acá arriba.
                # (Ya no hace falta porque la música del menú se mantiene sonando estable por su cuenta)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                    # === 1. CLIC EN EL NIVEL 1: EL CABILDO ===
                    if r_n1.collidepoint(pos_mouse):
                        
                        # --- MOTOR DE AUDIO INDUSTRIAL (NUEVO) ---
                        # Cortamos en seco la orquesta War Plan y encendemos March Of The Micmacs en loop
                        administrador_sonidos.detener_musica()
                        administrador_sonidos.reproducir_musica_combate()
                        
                        # Guardamos las coordenadas fijas del camino colonial
                        camino_nivel_1 = [
                            (105, 615), (230, 615), (230, 480), (860, 480), 
                            (860, 350), (215, 350), (215, 175), (512, 175)
                        ]
                        
                        # Inicialización limpia y unificada de tus entidades (Sin duplicaciones)
                        cabildo = Base(vidas=20)
                        cabildo.nombre = "Cabildo de Buenos Aires"
                        cabildo.rect.center = (512, 175)
                        
                        grupo_torres = pygame.sprite.Group()
                        grupo_enemigos = pygame.sprite.Group()
                        grupo_ingenieros = pygame.sprite.Group()
                        grupo_proyectiles = pygame.sprite.Group()
                        grupo_aliados_moviles = pygame.sprite.Group()
                        
                        # El mánager de hordas lee tu vector de forma nativa
                        administrador_oleadas = WaveManager(camino=camino_nivel_1)
                        administrador_oleadas.enemigos_pendientes = ["soldado_raso"] * 5
                        administrador_oleadas.tiempo_inicio_descanso = tiempo_actual
                        
                        interfaz_grafica = UIManager()
                        dinero_patria = cte.DINERO_INICIAL
                        nivel_activo = 1 # Le avisamos al LevelManager qué ilustración levantar del disco
                        
                        # Saltamos al campo de batalla activos
                        estado_actual = cte.ESTADO_JUEGO_ACTIVO
                    
                    # === 2. CLICS EN CAMPANAS BLOQUEADAS (Catedral, Fortín, Recova) ===
                    elif r_n2.collidepoint(pos_mouse) or r_n3.collidepoint(pos_mouse) or r_n4.collidepoint(pos_mouse):
                        administrador_sonidos.play_siguiente()
                        pygame.time.delay(150)
                        estado_actual = cte.ESTADO_CREDITOS # Desvío provisorio de tu GDD
                        
                    # === 3. CLIC EN EL NIVEL EXCLUSIVO 5 ===
                    elif nivel_5_desbloqueado and r_n5.collidepoint(pos_mouse):
                        administrador_sonidos.play_siguiente()
                        pygame.time.delay(150)
                        estado_actual = cte.ESTADO_CREDITOS
                        
                    # === 4. CLIC EN VOLVER AL MENÚ PRINCIPAL ===
                    elif r_volver.collidepoint(pos_mouse):
                        administrador_sonidos.play_volver()
                        
                        # El mánager redibuja la interfaz limpia usando tu diccionario compacto 'postales'
                        administrador_menus.dibujar_seleccion_niveles(
                            pantalla, fuente_titulos, fuente_botones, pos_mouse, 
                            nivel_5_desbloqueado, postales, True
                        )
                        pygame.display.flip()
                        pygame.time.delay(180) 
                        
                        estado_actual = cte.ESTADO_MENU

            # Clics Adentro de la Partida Activa
            # --- CAPTURA DE EVENTOS DE COMBATE (CORREGIDO ARRIBA EN EL FOR EVENT) ---
            elif estado_actual == cte.ESTADO_JUEGO_ACTIVO:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    # 1. Clic Izquierdo (Botón 1): Construcción Inteligente de Torres Patrias
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


        # --- LOGICA Y RENDERIZADO POR FUNCIÓN ---
        if estado_actual == cte.ESTADO_BIENVENIDA:
            administrador_menus.dibujar_bienvenida(pantalla, fuente_titulos, fuente_botones)
            
        elif estado_actual == cte.ESTADO_MENU:
            click_lista = pygame.mouse.get_pressed()
            click_izquierdo_activo = click_lista
            
            # RECORTE DE LLAMADO: Pasamos el llamado limpio terminando en tiempo_actual
            r_jugar, r_glosario, r_creditos, r_salir = administrador_menus.dibujar_menu_principal(
                pantalla, fuente_titulos, pos_mouse, btn_com, btn_glo, btn_cre, btn_sal, 
                click_izquierdo_activo, tiempo_actual
            )
            
            # 2. CONTROL GLOBAL DE AUDIO ANTI-SPAM (NUEVO)
            # Evaluamos qué botón específico tiene el mouse encima en este frame exacto
            id_boton_actual = -1
            if r_jugar.collidepoint(pos_mouse): id_boton_actual = 0
            elif r_glosario.collidepoint(pos_mouse): id_boton_actual = 1
            elif r_creditos.collidepoint(pos_mouse): id_boton_actual = 2
            elif r_salir.collidepoint(pos_mouse): id_boton_actual = 3
            
            # Si el mouse entró a un botón válido en tu menú principal
            if id_boton_actual != -1:
                if control_hover["activo"] != id_boton_actual:
                    # Validamos el colchón de 200 milisegundos para extinguir la ametralladora
                    if tiempo_actual - ultimo_sonido_hover > 200:
                        
                        # CORRECCIÓN INDUSTRIAL: El mánager ejecuta el point.mp3 de forma segura
                        administrador_sonidos.play_hover()
                        
                        ultimo_sonido_hover = tiempo_actual # Registramos el tiempo del pitido global
                    control_hover["activo"] = id_boton_actual
            else:
                # Si el mouse está en el fondo del pergamino fuera de los botones, liberamos el foco
                control_hover["activo"] = -1

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
            
        elif estado_actual == cte.ESTADO_JUEGO_ACTIVO:
            # 1. CENTRALIZADOR DE DERROTA INDUSTRIAL (Evita pisadas de variables y limpia el buffer)
            if cabildo.vidas <= 0:
                administrador_sonidos.detener_musica() 
                print("\n========================================================")
                print(" ¡EL CABILDO HA CAÍDO! Las hordas realistas tomaron la plaza.")
                print("========================================================\n")
                estado_actual = cte.ESTADO_GAME_OVER
                continue 

            # === CORRECCIÓN DEFINITIVA CONTRA EL SILENCIO ===
            # ¡BORRAMOS COMPLETAMENTE LA LÍNEA DE 'administrador_sonidos.detener_musica()' DE ACÁ!
            # (Ya no se necesita porque apagamos la música del menú en el instante del clic en la postal)

            # 3. ACTUALIZACIÓN DE ENTIDADES CONTINUA (SINCRO TOTAL CON TU CLASE TORRE)
            grupo_enemigos.update()
            grupo_torres.update(grupo_enemigos, grupo_proyectiles, tiempo_actual)  
            grupo_proyectiles.update(grupo_enemigos)
            grupo_aliados_moviles.update(grupo_enemigos, tiempo_actual)
            grupo_ingenieros.update(grupo_enemigos)
            cabildo.update(grupo_enemigos, tiempo_actual)
            grupo_textos_flotantes.update() 

            # 4. PROCESADOR DE IMPACTOS, RECOMPENSAS Y ANIMACIONES DE MUERTE
            # REMOVEMOS el segundo 'enemigo.update()' de acá adentro para que no vayan rápido
            for enemigo in list(grupo_enemigos):
                # Caso A: El invasor esquivó tus defensas y vulneró el Cabildo
                if enemigo.ha_llegado_al_final:
                    cabildo.recibir_danio(enemigo.danio, grupo_enemigos)
                    enemigo.kill() 
                    continue

                # Caso B: El enemigo fue alcanzado por las torres o por el Grito de la Patria
                # Validamos si se quedó sin salud (vida <= 0) pero todavía camina de forma normal
                elif enemigo.vida <= 0 and not getattr(enemigo, "ya_pago_recompensa", False):
                    # 1. Le pagamos la plata de la corona española de forma inmediata al HUD
                    dinero_patria += enemigo.recompensa
                    
                    # 2. Le clavamos el cerrojo para cobrar una sola vez y no duplicar fondos
                    enemigo.ya_pago_recompensa = True
                    
                    # 3. Activamos su bandera nativa para congelar sus vectores y que empiece a caer
                    enemigo.esta_muerto = True
                    enemigo.frame_actual = 0
                    enemigo.ultimo_refresco = pygame.time.get_ticks()

                # Caso C: El soldado ya cobró y está pasando por sus cuadros de desvanecimiento
                # Dejamos que corra libre su render en pantalla sin interferir con su caminata
                elif getattr(enemigo, "esta_muerto", False):
                    pass

            # 5. EL MÁNAGER DE OLEADAS GESTIONA LAS HORDAS DE FORMA SEGURA
            administrador_oleadas.update(tiempo_actual, grupo_enemigos, cabildo)

            # 6. DETECTOR DE VICTORIA REVOLUCIONARIA DEFINITIVA
            if administrador_oleadas.oleada_actual > 3:
                administrador_sonidos.detener_musica() 
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
            interfaz_grafica.draw_hud(pantalla, dinero_patria, administrador_oleadas.oleada_actual, cabildo, administrador_oleadas, tiempo_actual)

        pygame.display.update()
        pygame.display.flip()
        reloj.tick(cte.FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
 
