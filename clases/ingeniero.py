import pygame
import math

class IngenieroMilitar(pygame.sprite.Sprite):
    def __init__(self, pos_inicial, torre_objetivo):
        super().__init__()
        self.torre_objetivo = torre_objetivo
        self.velocidad = 2.2
        self.rango_revelado = 90  # Radio para detectar espias realistas
        
        # Grafico provisional para desarrollo
        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (46, 139, 87), (12, 12), 10) # Verde bosque
        
        self.rect = self.image.get_rect()
        self.rect.center = pos_inicial
        
        self.pos_x = float(self.rect.centerx)
        self.pos_y = float(self.rect.centery)

    def update(self, grupo_enemigos):
        """Desplazamiento directo a reparar y escaneo de espias ocultos."""
        # Si la torre que iba a reparar fue destruida, el ingeniero se retira
        if not self.torre_objetivo.alive():
            self.kill()
            return

        # 1. MECÁNICA DE REVELADO (Seccion 1.14 del GDD)
        # Escanea si hay espias realistas cerca para volverlos visibles a las torres
        for enemigo in grupo_enemigos:
            if enemigo.tipo == "espia_realista" and not enemigo.revelado:
                dist_espia = math.hypot(enemigo.rect.centerx - self.pos_x, enemigo.rect.centery - self.pos_y)
                if dist_espia <= self.rango_revelado:
                    enemigo.revelado = True
                    enemigo.dibujar_marcador_temporal()  # Actualiza su visual a opaco

        # 2. MOVIMIENTO HACIA LA TORRE OBJETIVO
        dx = self.torre_objetivo.rect.centerx - self.pos_x
        dy = self.torre_objetivo.rect.centery - self.pos_y
        distancia = math.hypot(dx, dy)

        if distancia > self.velocidad:
            self.pos_x += (dx / distancia) * self.velocidad
            self.pos_y += (dy / distancia) * self.velocidad
            self.rect.centerx = int(self.pos_x)
            self.rect.centery = int(self.pos_y)
        else:
            # Llegó a la torre: remueve deshabilitaciones causadas por espias
            self.torre_objetivo.deshabilitada = False
            print(f"Ingeniero reparo con exito la torre en {self.torre_objetivo.rect.center}")
            self.kill()  # Cumplio su objetivo y se elimina del grupo