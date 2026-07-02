import pygame
from config import constants as cte

class UIManager:
    def __init__(self):
        self.fuente_hud = pygame.font.Font("fuentes/Jersey10-Regular.ttf", 28)
        
        # CORRECCIÓN: Forzamos la tipografia nativa limpia que tenias originalmente en el juego
        self.fuente_alerta = pygame.font.SysFont("Arial", 16, bold=True)

        try:
            self.icono_moneda = pygame.image.load("assets/Moneda.png").convert_alpha()
            self.icono_moneda = pygame.transform.scale(self.icono_moneda, (24, 24))
        except Exception as e:
            print(f"Aviso: No se pudo cargar Moneda.png: {e}")
            self.icono_moneda = None

    def draw_hud(self, pantalla, dinero, oleada, cabildo, wave_manager, tiempo_actual, pos_barra):
        """Renderiza todo el entorno de datos e interfaces sobre el mapa de juego."""
        
        # ========================================================
        # 1. RECUADRO DE LA HORDA (Superior Izquierda)
        # ========================================================
        # Creamos una caja identica a la de monedas pero a la izquierda
        surf_horda = pygame.Surface((150, 45), pygame.SRCALPHA)
        pygame.draw.rect(surf_horda, (0, 0, 0, 160), (0, 0, 150, 45), border_radius=6)
        pantalla.blit(surf_horda, (20, 20))
        
        texto_oleada = self.fuente_hud.render(f"HORDA: {oleada}/3", True, (245, 222, 179))
        pantalla.blit(texto_oleada, (35, 26))

        # ========================================================
        # 2. RECUADRO DE MONEDAS (Superior Derecha)
        # ========================================================
        pos_x_caja = 1024 - 180 - 20 
        surf_monedas = pygame.Surface((180, 45), pygame.SRCALPHA)
        pygame.draw.rect(surf_monedas, (0, 0, 0, 160), (0, 0, 180, 45), border_radius=6)
        pantalla.blit(surf_monedas, (pos_x_caja, 20))
        
        if self.icono_moneda:
            pantalla.blit(self.icono_moneda, (pos_x_caja + 15, 30))
            
        texto_dinero = self.fuente_hud.render(f"$ {dinero}", True, (255, 255, 255))
        pantalla.blit(texto_dinero, (pos_x_caja + 48, 26))

        # ========================================================
        # 3. CARTEL DE ALERTA CON CONTORNO NEGRO (Centro Superior)
        # ========================================================
        if wave_manager.en_descanso:
            tiempo_restante = max(0, (wave_manager.duracion_descanso - (tiempo_actual - wave_manager.tiempo_inicio_descanso)) // 1000)
            
            # === CAMBIO INTERACTIVO DE TEXTO (NUEVO) ===
            # Si el marcador llegó a cero exacto, mutamos el mensaje colonial
            if tiempo_restante == 0:
                msg_alerta = "¡NUEVA HORDA!"
            else:
                msg_alerta = f"LOS ESPANOLES ATACAN EN: {tiempo_restante}s"
            
            # Renderizamos la capa negra de fondo y la de frente amarilla (Tu lógica original intacta)
            surf_borde = self.fuente_hud.render(msg_alerta, True, (0, 0, 0))
            surf_frente = self.fuente_hud.render(msg_alerta, True, (255, 215, 0))
            rect_alerta = surf_frente.get_rect(center=(512, 42))
            
            for dx, dy in [(-2,0), (2,0), (0,-2), (0,2), (-2,-2), (2,-2), (-2,2), (2,2)]:
                pantalla.blit(surf_borde, (rect_alerta.x + dx, rect_alerta.y + dy))
            pantalla.blit(surf_frente, rect_alerta)

        # 4. Barra de Resistencia del Cabildo (Le pasamos la coordenada viva al constructor de abajo)
        self.dibujar_barra_salud(pantalla, cabildo, pos_barra)

        # 5. Glosario de comandos inferior (Lo que ya tenías)
        self.dibujar_glosario_ayuda(pantalla)

    def dibujar_barra_salud(self, pantalla, cabildo, pos_barra):
        """Genera una barra de vida arriba de la base que vira de verde a rojo según su posición."""
        ancho_total = 140
        alto = 10
        
        # Desempaquetamos la coordenada calculada de forma elegante por el LevelManager
        bx, by = pos_barra
        
        # Centramos el ancho de la barra usando el eje X variable, y calcamos la altura en el eje Y variable
        x = bx - (ancho_total // 2)
        y = by 

        vidas_max = getattr(cabildo, "vidas_maximas", 20)
        porcentaje = max(0.0, min(1.0, cabildo.vidas / vidas_max))
        ancho_actual = int(ancho_total * porcentaje)

        if porcentaje > 0.5:
            color_barra = (int(510 * (1 - porcentaje)), 230, 0)
        else:
            color_barra = (255, int(510 * porcentaje), 0)

        pygame.draw.rect(pantalla, (20, 20, 20), (x - 2, y - 2, ancho_total + 4, alto + 4), border_radius=4)
        if ancho_actual > 0:
            pygame.draw.rect(pantalla, color_barra, (x, y, ancho_actual, alto), border_radius=2)

    def dibujar_glosario_ayuda(self, pantalla):
        """Pinta una guia de comandos en un recuadro negro ceñido que corta en la linea roja."""
        # ========================================================
        # 5. RECUADRO FLOTANTE COMPACTO Y LIMITADO
        # ========================================================
        # CORRECCIÓN: Achicamos el ancho a 580 pixeles exactos para que corte en tu linea roja
        ancho_ayuda = 580
        alto_ayuda = 52
        pos_x = 15
        pos_y = 768 - alto_ayuda - 15  # Separado 15 píxeles del borde inferior
        
        # Creamos el contenedor oscuro transparente ceñido
        surf_ayuda = pygame.Surface((ancho_ayuda, alto_ayuda), pygame.SRCALPHA)
        pygame.draw.rect(surf_ayuda, (0, 0, 0, 160), (0, 0, ancho_ayuda, alto_ayuda), border_radius=6)
        pantalla.blit(surf_ayuda, (pos_x, pos_y))
        
        # Renderizamos los textos con la fuente Arial restaurada
        ayuda_1 = self.fuente_alerta.render("Click Izquierdo: Construir Gauchos ($120) | Mantener 'C' + Click Izquierdo: Ciudadanos ($100)", True, (240, 240, 240))
        ayuda_2 = self.fuente_alerta.render("Click Derecho: Desplegar Ingeniero Militar (Sana torres / Detecta espias ocultos)", True, (240, 240, 240))
        
        # Estampamos las letras con un margen prolijo adentro de su nueva capsula
        pantalla.blit(ayuda_1, (pos_x + 15, pos_y + 6))
        pantalla.blit(ayuda_2, (pos_x + 15, pos_y + 26))