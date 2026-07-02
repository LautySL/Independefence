import pygame
from clases.enemigo import Enemigo

class WaveManager:
    def __init__(self, camino):
        self.camino = camino
        self.oleada_actual = 1
        
        # Lista de enemigos pendientes por salir en la oleada activa
        self.enemigos_pendientes = []
        
        # Tiempos de control en milisegundos
        self.ultimo_spawn = 0
        self.frecuencia_spawn = 2000  # Tiempo entre soldados (2 segundos)
        
        self.en_descanso = True
        self.tiempo_inicio_descanso = pygame.time.get_ticks()
        self.duracion_descanso = 10000  # 10 segundos para construir torres antes de la horda
        
        # Cargar la configuracion automatica del primer nivel
        self.preparar_oleada()

    def preparar_oleada(self):
        """Define la composicion del ejercito usando ruleta de probabilidades (Seccion GDD)."""
        self.enemigos_pendientes = []
        self.en_descanso = True
        self.tiempo_inicio_descanso = pygame.time.get_ticks()
        
        # 1. PARAMETRIZACIÓN DE HORDAS SEGÚN DISEÑO DINÁMICO
        if self.oleada_actual == 1:
            cantidad_total = 10
            opciones = ["soldado_raso", "artillero"]
            probabilidades = [0.95, 0.05] # 95% Chance Soldado | 5% Chance Artillero
            
        elif self.oleada_actual == 2:
            cantidad_total = 15
            opciones = ["soldado_raso", "artillero"]
            probabilidades = [0.70, 0.30] # 70% Chance Soldado | 30% Chance Artillero
            
        elif self.oleada_actual == 3:
            cantidad_total = 30
            opciones = ["soldado_raso", "artillero"]
            probabilidades = [0.60, 0.40] # 60% Chance Soldado | 40% Chance Artillero
            
        else:
            # Modo infinito de auxilio posterior
            cantidad_total = 30 + (self.oleada_actual * 2)
            opciones = ["soldado_raso", "artillero"]
            probabilidades = [0.50, 0.50]

        # 2. DISPARO DE LA RULETA DE PYTHON
        # random.choices genera una lista completa eligiendo elementos al azar basados en los pesos
        import random
        self.enemigos_pendientes = random.choices(opciones, weights=probabilidades, k=cantidad_total)
        
        # Seteamos un tiempo de spawn inicial para el primer soldado de la fila
        self.frecuencia_spawn = random.randint(1500, 2500)
        
        # Imprime la fila militar real resultante en la terminal de Sublime Text para auditar las chances
        print(f"[ WaveManager ] Horda {self.oleada_actual} armada al azar. Fila militar real: {self.enemigos_pendientes}")

    def update(self, tiempo_actual, grupo_enemigos, cabildo=None):
        """Monitorea el reloj global para instanciar los sprites en la ruta de campaña."""
        # 1. Modo Descanso: El jugador recolecta o planea sus defensas
        if self.en_descanso:
            if tiempo_actual - self.tiempo_inicio_descanso > self.duracion_descanso:
                self.en_descanso = False
                self.ultimo_spawn = tiempo_actual
            return

        # 2. Modo Asalto: Comienza la salida en fila de las tropas españolas
        if self.enemigos_pendientes:
            if tiempo_actual - self.ultimo_spawn > self.frecuencia_spawn:
                tipo_proximo = self.enemigos_pendientes.pop(0)
                
                # === MECÁNICA DE BIFURCACIÓN ALEATORIA (NUEVO) ===
                # Evaluamos si pasamos una matriz de caminos múltiples (Lista de listas)
                if isinstance(self.camino[0], list):
                    import random
                    # El soldado elige de forma independiente una de las dos rutas del muelle
                    camino_elegido = random.choice(self.camino)
                else:
                    # Si jugás el nivel 1 común, usa el vector rígido único del Cabildo
                    camino_elegido = self.camino
                
                # Instanciamos el enemigo pasándole la ruta sorteada al azar
                nuevo_soldado = Enemigo(camino=camino_elegido, tipo=tipo_proximo)
                grupo_enemigos.add(nuevo_soldado)
                
                import random
                self.frecuencia_spawn = random.randint(600, 2600)
                self.ultimo_spawn = tiempo_actual
        else:
            # === DETECTOR DE FIN DE OLEADA BLINDADO INDUSTRIAL (CORREGIDO) ===
            # El juego SOLO avanza de horda o da la victoria si la pantalla está vacía (len == 0)
            # Y ADEMÁS la lista de espera de la ticketera militar está totalmente vacía de forma legal.
            if len(grupo_enemigos) == 0 and not self.enemigos_pendientes:
                
                # --- REPORTES EN CONSOLA SEGÚN EL DESEMPEÑO DEL GDD (Lo que ya tenías) ---
                if cabildo:
                    vidas_max = getattr(cabildo, "vidas_maximas", 20)
                    if cabildo.vidas < vidas_max:
                        print(f"¡ALERTA! Completaste la horda {self.oleada_actual} pero sufriendo bajas.")
                        print(f"Resistencia del Cabildo actual: {cabildo.vidas}/{vidas_max}")
                    else:
                        print(f"¡DEFENSA PERFECTA! Victoria absoluta en la horda {self.oleada_actual}.")
                else:
                    print(f"¡Horda {self.oleada_actual} completada con éxito!")

                # --- EL CERROJO DEFINITIVO DE LA CAMPAÑA ---
                if self.oleada_actual == 3:
                    print("¡VICTORIA REVOLUCIONARIA DEFINITIVA! Derrotaste la campana del Cabildo.")
                    self.oleada_actual = 4 
                    self.enemigos_pendientes = []
                else:
                    print(f"Preparando oleada numero: {self.oleada_actual + 1}")
                    self.oleada_actual += 1
                    
                    # Llamamos a tu método dinámico de carga para preparar la siguiente ronda
                    self.preparar_oleada()
                    
                    self.en_descanso = True
                    self.tiempo_inicio_descanso = tiempo_actual
                    self.ultimo_spawn = tiempo_actual
