import pygame
import math

class Proyectil(pygame.sprite.Sprite):
    def __init__(self, pos_origen, enemigo_objetivo, danio, tipo="boleadora"):
        super().__init__()
        self.tipo = tipo
        self.danio = danio
        self.objetivo = enemigo_objetivo
        
        # Configurar estadisticas de movimiento segun el proyectil
        self.configurar_proyectil()
        
        self.color_test = (255, 215, 0) 
        
        # Superficie de dibujo para desarrollo (sin graficos externos aun)
        self.image = pygame.Surface((12, 12), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color_test, (6, 6), 5)
        
        self.rect = self.image.get_rect()
        self.rect.center = pos_origen
        
        # Posicion precisa en punto flotante
        self.pos_x = float(self.rect.centerx)
        self.pos_y = float(self.rect.centery)

    def configurar_proyectil(self):
        """Define la velocidad y color de pruebas del proyectil."""
        if self.tipo == "boleadora":
            self.velocidad = 7.0
            self.color_test = (218, 165, 32) # Dorado / Cuero
        elif self.tipo == "bala_fusil":
            self.velocidad = 10.0
            self.color_test = (50, 50, 50) # Gris oscuro

    def update(self, grupo_enemigos):
        """Maneja el rastreo o la trayectoria lineal hacia el objetivo."""
        # --- EL FILTRO DE SEGURIDAD (CORREGIDO) ---
        # Si el enemigo murio por otra torre o ya esta desvaneciendose mientras el proyectil viajaba,
        # la municion se destruye en el aire de forma limpia en vez de perseguir al cadaver.
        if not self.objetivo.alive() or self.objetivo.esta_muerto:
            self.kill()
            return

        # Calcular vector de direccion hacia el centro del enemigo (Aca abajo se queda todo IGUAL)
        dx = self.objetivo.rect.centerx - self.pos_x
        dy = self.objetivo.rect.centery - self.pos_y
        distancia = math.hypot(dx, dy)

        if distancia > self.velocidad:
            # Avanzar frame a frame acortando la distancia de forma lineal
            self.pos_x += (dx / distancia) * self.velocidad
            self.pos_y += (dy / distancia) * self.velocidad
            self.rect.centerx = int(self.pos_x)
            self.rect.centery = int(self.pos_y)
        else:
            # Impacto exitoso contra el soldado realista
            self.objetivo.recibir_danio(self.danio, grupo_enemigos)
            self.kill()