import pygame
from clases.enemigo import Enemigo

class WaveManager:
    def __init__(self, camino):
        self.camino = camino
        self.oleada_actual = 1
        self.enemigos_pendientes = []

        # === CANDADO DE CAMPAÑA PATRIOTICA (NUEVO) ===
        self.juego_terminado = False # Si pasa a True, el mánager se congela y no procesa más nada

        self.ultimo_spawn = 0
        self.frecuencia_spawn = 2000  
        self.en_descanso = True
        self.tiempo_inicio_descanso = pygame.time.get_ticks()
        self.duracion_descanso = 10000  
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
        # CANDADO INDUSTRIAL DE FRONTERA: Si la campaña ya fue ganada, apagamos el mánager por completo
        if self.juego_terminado:
            return

        # 1. Modo Descanso
        if self.en_descanso:
            if tiempo_actual - self.tiempo_inicio_descanso > self.duracion_descanso:
                self.en_descanso = False
                self.ultimo_spawn = tiempo_actual
            return

        # 2. Modo Asalto: Comienza la salida en fila de las tropas españolas
        if self.enemigos_pendientes:
            if tiempo_actual - self.ultimo_spawn > self.frecuencia_spawn:
                tipo_proximo = self.enemigos_pendientes.pop(0)
                
                # === SENSOR DE BIFURCACIONES INDUSTRIAL (REPARADO) ===
                # Evaluamos si la variable 'self.camino' tiene elementos y si el primer casillero 
                # es otra lista (lo que nos confirma que es la matriz de caminos del Nivel 2)
                if self.camino and isinstance(self.camino[0], list):
                    import random
                    # Sorteamos de forma legítima una de las dos rutas individuales de la Catedral
                    camino_elegido = random.choice(self.camino)
                else:
                    # Si es el nivel 1 o una lista lineal de tuplas común, usa la ruta rígida de siempre
                    camino_elegido = self.camino
                
                # Instanciamos el enemigo pasándole la ruta sorteada limpia de una sola dimensión
                nuevo_soldado = Enemigo(camino=camino_elegido, tipo=tipo_proximo)
                grupo_enemigos.add(nuevo_soldado)
                
                import random
                self.frecuencia_spawn = random.randint(600, 2600)
                self.ultimo_spawn = tiempo_actual
        else:
            # === DETECTOR DE FIN DE OLEADA BLINDADO (CORREGIDO) ===
            if len(grupo_enemigos) == 0 and not self.enemigos_pendientes:
                
                # --- EL CERROJO DEFINITIVO DE LA CAMPAÑA (REPARADO) ---
                if self.oleada_actual == 3:
                    if cabildo:
                        vidas_max = getattr(cabildo, "vidas_maximas", 20)
                        print(f"¡DEFENSA PERFECTA REVOLUCIONARIA! Completaste la horda {self.oleada_actual}.")
                        print(f"Resistencia del Cabildo final: {cabildo.vidas}/{vidas_max}")
                        
                    print("\n¡VICTORIA REVOLUCIONARIA DEFINITIVA! Derrotaste la campana del Cabildo.")
                    
                    # Activamos los candados y clavamos las variables de forma estática
                    self.juego_terminado = True 
                    self.oleada_actual = 4 
                    self.enemigos_pendientes = []
                    return # <-- ¡EL FRENO CLAVE! Salimos del método inmediatamente para no tocar el else de abajo
                    
                else:
                    # --- REPORTES DE HORDAS INTERMEDIAS (1 Y 2) ---
                    if cabildo:
                        vidas_max = getattr(cabildo, "vidas_maximas", 20)
                        print(f"¡ALERTA! Completaste la horda {self.oleada_actual} pero sufriendo bajas.")
                        print(f"Resistencia del Cabildo actual: {cabildo.vidas}/{vidas_max}")
                    else:
                        print(f"¡Horda {self.oleada_actual} completada con éxito!")
                        
                    print(f"Preparando oleada numero: {self.oleada_actual + 1}")
                    self.oleada_actual += 1
                    
                    # Llamamos a tu método dinámico de la ruleta para armar la siguiente tanda
                    self.preparar_oleada()
                    
                    self.en_descanso = True
                    self.tiempo_inicio_descanso = tiempo_actual
                    self.ultimo_spawn = tiempo_actual
