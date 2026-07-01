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