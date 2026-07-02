import pygame
import math
from config import constants as cte
from clases.proyectil import Proyectil  # Asumimos que existirá para las balas/aceite

class Torre(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, tipo="gauchos"):
        super().__init__()
        self.tipo = tipo
        self.nivel = 1  # Máximo nivel 2 según el GDD
        
        # Configuración inicial de estadísticas por tipo
        self.configurar_torre()
        
        # Renderizado del Sprite
        self.image = pygame.Surface((48, 48), pygame.SRCALPHA)
        self.dibujar_marcador_temporal()
        
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        
        # Control de cadencia de disparo (en milisegundos)
        self.ultimo_disparo = pygame.time.get_ticks()
        self.deshabilitada = False
        self.tiempo_deshabilitada = 0

        self.ultima_cadencia = 0

    def configurar_torre(self):
        """Define estadísticas de daño, rango y velocidad basadas en la sección 1.13 del GDD."""
        if self.tipo == "ciudadanos":
            self.rango = 70          # Rango corto (deben pasar por debajo)
            self.cadencia = 2500     # Lento para tirar el aceite (2.5 segundos)
            self.danio = 15
            self.tipo_ataque = "area"
            self.color_test = (139, 69, 19)  # Marrón (Aceite)
            
        elif self.tipo == "gauchos":
            self.rango = 160         # Media distancia para las boleadoras
            self.cadencia = 1200     # Ataque intermedio (1.2 segundos)
            self.danio = 8
            self.tipo_ataque = "directo"
            self.color_test = (30, 144, 255) # Azul Celeste Patria

    def dibujar_marcador_temporal(self):
        """Marcador visual pixelado provisional para desarrollo."""
        pygame.draw.rect(self.image, self.color_test, (4, 4, 40, 40), border_radius=4)
        # Dibujar un pequeño indicador de nivel
        for i in range(self.nivel):
            pygame.draw.circle(self.image, (255, 215, 0), (8 + (i * 8), 10), 3)

    def actualizar_mejoras(self, multiplicador_danio=1.0, multiplicador_cadencia=1.0):
        """Aplica los bonus de la Herrería o Tácticas Belgranianas (Sección 1.15 del GDD)."""
        self.danio = int(self.danio * multiplicador_danio)
        self.cadencia = int(self.cadencia * multiplicador_cadencia)

    def subir_de_nivel(self):
        """Incrementa estadísticas hasta el nivel 2 como especifica el GDD."""
        if self.nivel < 2:
            self.nivel += 1
            self.danio = int(self.danio * 1.4)
            self.rango = int(self.rango * 1.2)
            self.cadencia = int(self.cadencia * 0.8)  # Dispara más rápido
            self.dibujar_marcador_temporal()

    def update(self, grupo_enemigos, grupo_proyectiles, tiempo_actual, administrador_sonidos=None):
        """Busca un objetivo valido en rango y abre fuego segun su cadencia."""
        for enemigo in grupo_enemigos:
            if enemigo.esta_muerto:
                continue
                
            dx = enemigo.rect.centerx - self.rect.centerx
            dy = enemigo.rect.centery - self.rect.centery
            distancia = math.hypot(dx, dy)
            
            if distancia <= self.rango:
                # CORRECCIÓN DEFINITIVA: Le pasamos 'administrador_sonidos' al método atacar
                self.atacar(enemigo, grupo_proyectiles, tiempo_actual, administrador_sonidos)
                break 

    def buscar_objetivo(self, grupo_enemigos):
        """Calcula mediante Pitágoras el enemigo más cercano dentro del radio."""
        enemigo_cercano = None
        distancia_minima = self.rango

        for enemigo in grupo_enemigos:
            dx = enemigo.rect.centerx - self.rect.centerx
            dy = enemigo.rect.centery - self.rect.centery
            distancia = math.hypot(dx, dy)

            # Prioriza el enemigo que esté en rango y más adelantado en su camino
            if distancia <= self.rango:
                if enemigo_cercano is None or enemigo.indice_camino > enemigo_cercano.indice_camino:
                    distancia_minima = distancia
                    enemigo_cercano = enemigo
                    
        return enemigo_cercano

    def atacar(self, enemigo_objetivo, grupo_proyectiles, tiempo_actual, administrador_sonidos):
        """Instancia un nuevo proyectil dirigido al soldado realista respetando la recarga."""
        if tiempo_actual - self.ultima_cadencia > self.cadencia:
            # Formamos la tupla exacta que tu proyectil espera recibir en 'pos_origen'
            nuevo_proyectil = Proyectil((self.rect.centerx, self.rect.centery), enemigo_objetivo, self.danio)
            
            # Agregamos la municion al grupo de sprites activo
            grupo_proyectiles.add(nuevo_proyectil)
            
            self.ultima_cadencia = tiempo_actual

            # === INYECCIÓN ACÚSTICA CALIBRADA (ADENTRO DEL DISPARO) ===
            # Metemos el sonido adentro del if de la recarga para que suene ÚNICAMENTE cuando sale una bala real.
            # Validamos que 'administrador_sonidos' haya llegado bien y que la unidad sea el Gaucho.
            if self.tipo == "gauchos" and administrador_sonidos is not None:
                administrador_sonidos.play_disparo()