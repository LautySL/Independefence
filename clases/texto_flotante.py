import pygame

class TextoFlotante(pygame.sprite.Sprite):
    def __init__(self, texto, pos_x, pos_y, fuente, color=(255, 0, 0)):
        super().__init__()
        self.texto = texto
        self.color = color
        self.fuente = fuente
        
        # Guardamos la posición en variables flotantes para movimientos suaves
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.velocidad_subida = 1.2 # Píxeles que trepa por frame
        
        # Temporizador de vida útil (Alfa inicial al máximo)
        self.alfa_actual = 255
        self.velocidad_desvanecimiento = 4 # Cuánto transparente se vuelve por frame
        
        # Renderizado de la superficie inicial (Le damos un colchón extra de tamaño para el borde)
        surf_frente = self.fuente.render(self.texto, True, self.color)
        self.image = pygame.Surface((surf_frente.get_width() + 8, surf_frente.get_height() + 8), pygame.SRCALPHA)
        
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))
        self.actualizar_superficie_texto()

    def actualizar_superficie_texto(self):
        """Genera el render del texto con su contorno negro grueso de 2 píxeles."""
        # Creamos las dos capas base
        surf_borde = self.fuente.render(self.texto, True, (0, 0, 0))
        surf_frente = self.fuente.render(self.texto, True, self.color)
        
        # Creamos un lienzo limpio transparente del tamaño del texto más el margen del borde
        ancho = surf_frente.get_width() + 8
        alto = surf_frente.get_height() + 8
        surf_final = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        
        # Ubicamos el centro local del texto adentro de nuestro lienzo nuevo
        origen_x = 4
        origen_y = 4
        
        # Dibujamos el contorno negro grueso en cruz y diagonales (2 píxeles de grosor)
        for dx, dy in [(-2,0), (2,0), (0,-2), (0,2), (-2,-2), (2,-2), (-2,2), (2,2)]:
            surf_final.blit(surf_borde, (origen_x + dx, origen_y + dy))
            
        # Capa final: La letra de color (Rojo) arriba en el centro
        surf_final.blit(surf_frente, (origen_x, origen_y))
        
        # === MOTOR DE TRANSPARENCIA ALFA EN CALIENTE ===
        # Aplicamos la desintegración frame a frame leyendo self.alfa_actual
        superficie_alfa = pygame.Surface(surf_final.get_size(), pygame.SRCALPHA)
        superficie_alfa.fill((255, 255, 255, self.alfa_actual))
        surf_final.blit(superficie_alfa, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        self.image = surf_final

    def update(self, *args):
        """Trepa verticalmente hacia el cielo colonial y se desvanece en transparencia."""
        # 1. Desplazamiento hacia arriba en el eje Y
        self.pos_y -= self.velocidad_subida
        self.rect.centery = int(self.pos_y)
        
        # 2. Reducimos el canal alfa de visibilidad
        self.alfa_actual -= self.velocidad_desvanecimiento
        if self.alfa_actual <= 0:
            self.kill() # Se retira solo de la memoria RAM al volverse invisible
            return
            
        # Re-renderizamos el cartel aplicando el nuevo nivel de transparencia
        self.actualizar_superficie_texto()