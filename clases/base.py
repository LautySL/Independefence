import pygame
import math

class Base(pygame.sprite.Sprite):
    
    def __init__(self, vidas=20):
        # Inicializacion obligatoria como Sprite de Pygame
        super().__init__()
        
        # 1. CONFIGURACIÓN DE ATRIBUTOS DE SALUD Y RECOMPENSAS
        self.vidas_maximas = vidas
        self.vidas = vidas
        self.emergencia_disponible = True
        
        # 2. CONFIGURACIÓN DE ATAQUE PASIVO (Línea 44 de tu update)
        self.ultima_defensa = pygame.time.get_ticks()
        self.cadencia_ataque = 1500  # Dispara cada 1.5 segundos
        self.rango_defensa = 150     # Radio de proteccion de la base
        self.poder_ataque = 5        # Danio pasivo a los realistas cercanos

        # 3. CONTENEDOR GRÁFICO (Requerido para que funcione el .rect en tu main y mapa)
        # Creamos una superficie transparente de 80x80 pixeles
        self.image = pygame.Surface((80, 80), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        
        # Llamamos al metodo que tenías para pintar los bloques patrios iniciales
        self.dibujar_base()

    def dibujar_base(self):
        """Mantiene la superficie limpia para no tapar el mapa del fondo."""
        # Limpiamos la superficie dejandola 100% transparente
        self.image.fill((0, 0, 0, 0))
        
    def recibir_danio(self, cantidad, grupo_enemigos):
        """Resta vida a la edificación y evalúa el ataque de emergencia del GDD."""
        self.vidas -= cantidad
        if self.vidas < 0:
            self.vidas = 0
            
        # Habilidad de Emergencia (Sección 1.13): Se activa al llegar a estado crítico (<= 25% de vida)
        if self.vidas <= (self.vidas_maximas * 0.25) and self.emergencia_disponible and self.vidas > 0:
            self.activar_grito_de_la_patria(grupo_enemigos)

    def activar_grito_de_la_patria(self, grupo_enemigos):
        """Limpia la plaza de Mayo activando las animaciones de muerte nativas de los enemigos."""
        self.emergencia_disponible = False
        print("¡Habilidad de Emergencia Activada: El Grito de la Patria!")
        
        # Recorremos la lista de invasores realistas activos
        for enemigo in list(grupo_enemigos):
            if enemigo.tipo in ["soldado_raso", "soldado_experimentado", "artillero"]:
                # === CORRECCIÓN DEFINITIVA CONTRA EL BORRADO EN SECO ===
                # Sincronizamos con la variable real de tu update de enemigo: 'esta_muerto'
                enemigo.vida = 0
                enemigo.esta_muerto = True # <-- ¡Cambiamos 'esta_muriendo' por tu bandera real!
                
                # Reiniciamos su animador para que arranque prolijo desde el cuadro 1 de caida
                enemigo.frame_actual = 0
                enemigo.ultimo_refresco = pygame.time.get_ticks()
            else:
                # A los jefes o generales les quita el 50% de su vida actual
                enemigo.vida = int(enemigo.vida * 0.5)

    def entrenar_ingeniero(self, grupo_ingenieros, grupo_torres):
        """Instancia un Ingeniero Militar en las puertas de la base si hay estructuras rotas o hackeadas."""
        # (Se mantiene intacto segun tu codigo, asumiendo que IngenieroMilitar esta importado en tu proyecto)
        try:
            from clases.ingeniero import IngenieroMilitar
            torre_objetivo = None
            for torre in grupo_torres:
                if torre.deshabilitada or torre.nivel < 2:
                    torre_objetivo = torre
                    break
                    
            if torre_objetivo:
                nuevo_ingeniero = IngenieroMilitar(self.rect.center, torre_objetivo)
                grupo_ingenieros.add(nuevo_ingeniero)
        except Exception as e:
            print(f"Aviso en entrenamiento de ingeniero: {e}")

    def update(self, grupo_enemigos, tiempo_actual):
        """Lógica de autodefensa pasiva del Cabildo/Fortín frente a las hordas españolas."""
        if tiempo_actual - self.ultima_defensa > self.cadencia_ataque:
            # Buscar el enemigo más cercano a las puertas de la base
            for enemigo in grupo_enemigos:
                # Comprobacion de seguridad para evitar crashes con enemigos que no tengan rect
                if hasattr(enemigo, "rect"):
                    dx = enemigo.rect.centerx - self.rect.centerx
                    dy = enemigo.rect.centery - self.rect.centery
                    if math.hypot(dx, dy) <= self.rango_defensa:
                        enemigo.recibir_danio(self.poder_ataque, grupo_enemigos)
                        self.ultima_defensa = tiempo_actual
                        break