import pygame
from config import constants as cte

class LevelManager:
    def __init__(self):
        # Guardamos el mapa activo cargado en memoria para no ralentizar los FPS
        self.mapa_actual = None
        self.id_nivel_actual = None

    def cargar_mapa_nivel(self, id_nivel):
        """Carga dinámicamente el fondo ilustrado del nivel según su identificador."""
        # Si el nivel solicitado ya está cargado en la RAM, salteamos la carga de disco
        if self.id_nivel_actual == id_nivel and self.mapa_actual is not None:
            return self.mapa_actual

        # Diccionario de rutas automatizado para indexar tus mapas futuros
        rutas_mapas = {
            1: "assets/mapas/nivel_cabildo.png",
            2: "assets/mapas/nivel_catedral.png",
            3: "assets/mapas/nivel_fortin.png",
            4: "assets/mapas/nivel_recova.png"
        }

        # Buscamos la ruta correspondiente. Si no existe, usamos el Cabildo por defecto
        ruta_archivo = rutas_mapas.get(id_nivel, "assets/mapas/nivel_cabildo.png")

        try:
            print(f"[ LevelManager ] Cargando escenario de combate desde: {ruta_archivo}")
            img = pygame.image.load(ruta_archivo).convert()
            self.mapa_actual = pygame.transform.scale(img, (cte.ANCHO_DE_PANTALLA, cte.ALTO_DE_PANTALLA))
            self.id_nivel_actual = id_nivel
        except Exception as e:
            print(f"Error crítico al cargar el mapa del nivel {id_nivel}: {e}")
            # Auxilio gris pizarra en caso de archivos faltantes
            self.mapa_actual = pygame.Surface((cte.ANCHO_DE_PANTALLA, cte.ALTO_DE_PANTALLA))
            self.mapa_actual.fill((50, 50, 50))
            self.id_nivel_actual = id_nivel

        return self.mapa_actual

    def obtener_parcelas_nivel(self, numero_nivel):
        """Devuelve la lista exclusiva de rectangulos de construccion para el escenario activo."""
        # ESCENARIO 1: El Cabildo tradicional (Tus 5 coordenadas intactas)
        if numero_nivel == 1:
            return [
                pygame.Rect(226, 287, 53, 53),   # Parcela 1
                pygame.Rect(307, 417, 53, 53),   # Parcela 2
                pygame.Rect(605, 553, 53, 53),   # Parcela 3
                pygame.Rect(690, 285, 53, 53),   # Parcela 5
                pygame.Rect(323, 73, 53, 53)     # Parcela 6
            ]
            
        # === ESCENARIO 2: LA CATEDRAL ===
        elif numero_nivel == 2:
            return [
                pygame.Rect(741, 549, 45, 45),   # Parcela Catedral 1 
                pygame.Rect(276, 165, 45, 45),   # Parcela Catedral 2 
                pygame.Rect(165, 293, 45, 45),   # Parcela Catedral 3
                pygame.Rect(274, 335, 45, 45),   # Parcela Catedral 4 
                pygame.Rect(251, 448, 45, 45),   # Parcela Catedral 5
                pygame.Rect(204, 592, 45, 45),   # Parcela Catedral 6 
                pygame.Rect(447, 656, 45, 45),   # Parcela Catedral 7 
                pygame.Rect(732, 336, 45, 45)    # Parcela Catedral 8 
            ]
            
        return []

    # Waypoints del orto
    def obtener_camino_nivel(self, numero_nivel):
        """Devuelve la matriz de waypoints (camino unico o bifurcaciones) para el escenario activo."""
        # ESCENARIO 1: El Cabildo de Buenos Aires 
        if numero_nivel == 1:
            return [
                (105, 615), (230, 615), (230, 480), (860, 480), 
                (860, 350), (215, 350), (215, 175), (512, 175)
            ]
            
        # === ESCENARIO 2: LA CATEDRAL METROPOLITANA ===
        elif numero_nivel == 2:
            # Camino A: Sube directo hacia el portón de la Catedral
            camino_catedral_arriba = [
                (966, 608), (846, 608), (846, 498), (770, 495), # Tronco Común
                (770, 395), (260, 395), (260, 216), (496, 216), (496, 161)  # Bifurcación Norte
            ]
            
            # Camino B: Baja por la plaza del mercado usando tus sprites down
            camino_catedral_abajo = [
                (966, 608), (737, 608), (737, 703), (430, 703), # Tronco Común
                (430, 651), (197, 651), (197, 508), (350, 508), (350, 391), (260, 391), (260, 216), (496, 216), (496, 161) # Bifurcación Sur
            ]
            
            # Devolvemos la lista matriz con ambas bifurcaciones combinadas
            return [camino_catedral_arriba, camino_catedral_abajo]
            
        # Por si hay más niveles en el futuro
        return []

    # es obvio lo que esta función hace
    def obtener_posicion_barra_vida(self, numero_nivel):
        """Devuelve las coordenadas (X, Y) superiores para dibujar la barra de salud de la base."""
        # ESCENARIO 1: El Cabildo tradicional 
        if numero_nivel == 1:
            return (512, 70) # (Ajustala al valor que tenías si era diferente)
            
        # === ESCENARIO 2: LA CATEDRAL METROPOLITANA ===
        elif numero_nivel == 2:
            # Calibración milimétrica para la Catedral:
            return (477, 70)
            
        # Auxilio por si sumás más niveles en el futuro
        return (512, 140)