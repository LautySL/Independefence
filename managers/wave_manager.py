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
        """Define la composicion exacta del ejercito real segun la ronda (Seccion 1.14 del GDD)."""
        self.enemigos_pendientes = []
        self.en_descanso = True
        self.tiempo_inicio_descanso = pygame.time.get_ticks()
        
        # Configuramos la dificultad escalable de forma matematica
        if self.oleada_actual == 1:
            # 5 soldados rasos comunes
            self.enemigos_pendientes = ["soldado_raso"] * 5
            self.frecuencia_spawn = 2500
        elif self.oleada_actual == 2:
            # 6 rasos y se suman 2 jinetes rapidos
            self.enemigos_pendientes = ["soldado_raso"] * 6 + ["soldado_a_caballo"] * 2
            self.frecuencia_spawn = 2000
        elif self.oleada_actual == 3:
            # Introduccion de los cañoneros pesados y un espia saboteador
            self.enemigos_pendientes = ["soldado_raso"] * 4 + ["canoneros"] * 2 + ["espia_realista"]
            self.frecuencia_spawn = 1800
        else:
            # Oleadas infinitas posteriores avanzadas con multiplicadores escalables
            cantidad_basicos = 5 + self.oleada_actual
            cantidad_pesados = self.oleada_actual // 2
            self.enemigos_pendientes = ["soldado_experimentado"] * cantidad_basicos + ["canoneros"] * cantidad_pesados
            self.frecuencia_spawn = max(1000, 2000 - (self.oleada_actual * 100))

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
                # Extraemos el primer enemigo de la fila
                tipo_proximo = self.enemigos_pendientes.pop(0)
                
                # Instanciamos el objeto con el waypoint del mapa
                nuevo_soldado = Enemigo(camino=self.camino, tipo=tipo_proximo)
                grupo_enemigos.add(nuevo_soldado)
                
                self.ultimo_spawn = tiempo_actual
        else:
            # --- DETECTOR DE FIN DE OLEADA BLINDADO ---
            if len(grupo_enemigos) == 0:
                
                # --- REPORTES EN CONSOLA SEGÚN EL DESEMPEÑO DEL GDD ---
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
                # Evaluamos el número de horda ANTES de sumarle, para frenar el bucle en la horda 3
                if self.oleada_actual == 3:
                    print("¡VICTORIA REVOLUCIONARIA DEFINITIVA! Derrotaste la campana del Cabildo.")
                    # Pasamos a 4 en completo silencio para que tu main.py salte a la pantalla de pergaminos
                    self.oleada_actual = 4 
                    self.enemigos_pendientes = []
                else:
                    # Si era la horda 1 o la 2, avisamos en consola la que se está preparando
                    print(f"Preparando oleada numero: {self.oleada_actual + 1}")
                    self.oleada_actual += 1
                    
                    # --- NUEVA INYECCIÓN DE TROPAS PARA LAS SIGUIENTES HORDAS ---
                    if self.oleada_actual == 2:
                        self.enemigos_pendientes = ["soldado_raso"] * 8 + ["soldado_experimentado"] * 3
                    elif self.oleada_actual == 3:
                        self.enemigos_pendientes = ["soldado_raso"] * 10 + ["soldado_experimentado"] * 5 + ["general"] * 1
                    
                    # Activamos el descanso ÚNICAMENTE para las hordas intermedias reales
                    self.en_descanso = True
                    self.tiempo_inicio_descanso = tiempo_actual
                    self.ultimo_spawn = tiempo_actual
