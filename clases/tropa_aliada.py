import pygame
import math

class TropaAliada(pygame.sprite.Sprite):
    def __init__(self, pos_origen, tipo="granaderos"):
        super().__init__()
        self.tipo = tipo
        
        # Configurar estadisticas basadas en la sección 1.13 del GDD
        self.configurar_tropa()
        
        # Superficie grafica temporal para desarrollo
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.rect(self.image, self.color_test, (2, 2, 28, 28), border_radius=8)
        
        self.rect = self.image.get_rect()
        self.rect.center = pos_origen
        
        # Coordenadas exactas en punto flotante
        self.pos_x = float(self.rect.centerx)
        self.pos_y = float(self.rect.centery)

    def configurar_tropa(self):
        """Define el comportamiento tactico y velocidad de los jinetes patriotas."""
        if self.tipo == "granaderos":
            self.velocidad_x = 0.0
            self.velocidad_y = 3.0    # Marchan directo hacia el fondo de la pantalla
            self.danio = 12
            self.rango_ataque = 40
            self.cadencia = 500       # Atacan muy rapido al paso (0.5 segundos)
            self.color_test = (0, 0, 139) # Azul oscuro (Regimiento de Granaderos)
            
        elif self.tipo == "infernales":
            self.velocidad = 3.5      # IA de rastreo activo de objetivos prioritarios
            self.danio = 25           # Gran fuerza de ataque
            self.rango_ataque = 30
            self.cadencia = 1000      # 1 segundo
            self.vida = 40            # Tienen resistencia propia antes de desaparecer
            self.color_test = (178, 34, 34) # Rojo punzo (Infernales de Guemes)
            
        self.ultima_accion = pygame.time.get_ticks()

    def update(self, grupo_enemigos, tiempo_actual):
        """Gestiona la navegacion e interaccion en combate de la caballeria."""
        if self.tipo == "granaderos":
            # Logica GDD: Parten desde la torre y se dirigen hacia la parte baja
            self.pos_y += self.velocidad_y
            self.rect.centery = int(self.pos_y)
            
            # Si salen de los limites de la pantalla, se eliminan
            if self.rect.top > 768: # Altura configurada en constants.py
                self.kill()
                return
                
            # Atacan al paso si cruzan a un enemigo cerca
            self.atacar_al_paso(grupo_enemigos, tiempo_actual)
            
        elif self.tipo == "infernales":
            # Logica GDD: Buscan y priorizan unidades de artilleria o jefes
            objetivo = self.buscar_objetivo_prioritario(grupo_enemigos)
            
            if objetivo:
                # Moverse directo hacia el objetivo fijado
                dx = objetivo.rect.centerx - self.pos_x
                dy = objetivo.rect.centery - self.pos_y
                distancia = math.hypot(dx, dy)
                
                if distancia > self.rango_ataque:
                    self.pos_x += (dx / distancia) * self.velocidad
                    self.pos_y += (dy / distancia) * self.velocidad
                    self.rect.centerx = int(self.pos_x)
                    self.rect.centery = int(self.pos_y)
                else:
                    # Rango de combate cuerpo a cuerpo alcanzado
                    if tiempo_actual - self.ultima_accion > self.cadencia:
                        objetivo.recibir_danio(self.danio, grupo_enemigos)
                        self.ultima_accion = tiempo_actual
                        # Los infernales pierden un poco de vida al combatir segun el GDD
                        self.vida -= 10
                        if self.vida <= 0:
                            self.kill()
            else:
                # Si no hay objetivos prioritarios, patrullan hacia adelante o mueren
                self.kill()

    def atacar_al_paso(self, grupo_enemigos, tiempo_actual):
        """Busca enemigos en su trayecto descendente y aplica daño sin detenerse."""
        if tiempo_actual - self.ultima_accion > self.cadencia:
            for enemigo in grupo_enemigos:
                distancia = math.hypot(enemigo.rect.centerx - self.rect.centerx, 
                                       enemigo.rect.centery - self.rect.centery)
                if distancia <= self.rango_ataque:
                    enemigo.recibir_danio(self.danio, grupo_enemigos)
                    self.ultima_accion = tiempo_actual
                    break

    def buscar_objetivo_prioritario(self, grupo_enemigos):
        """Filtra y prioriza cañoneros, artilleros y generales antes que soldados rasos."""
        objetivo_prioritario = None
        distancia_minima = 999999
        
        # Lista de tipos prioritarios en orden descendente segun la seccion 1.13 y 1.14
        prioridades = ["realista", "general", "canoneros", "artillero_pesado", "artillero"]

        for enemigo in grupo_enemigos:
            if enemigo.tipo in prioridades:
                distancia = math.hypot(enemigo.rect.centerx - self.pos_x, enemigo.rect.centery - self.pos_y)
                if distancia < distancia_minima:
                    distancia_minima = distancia
                    objetivo_prioritario = enemigo
                    
        # Si no hay enemigos especiales en pantalla, ataca al mas cercano que encuentre
        if objetivo_prioritario is None and len(grupo_enemigos) > 0:
            for enemigo in grupo_enemigos:
                distancia = math.hypot(enemigo.rect.centerx - self.pos_x, enemigo.rect.centery - self.pos_y)
                if distancia < distancia_minima:
                    distancia_minima = distancia
                    objetivo_prioritario = enemigo

        return objetivo_prioritario