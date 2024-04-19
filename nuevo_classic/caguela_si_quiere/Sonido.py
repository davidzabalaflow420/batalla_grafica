import pygame

class Sonido:
    def __init__(self):
        """
        Constructor de la clase Sonido que inicializa objetos de sonido con los archivos especificados.

        Raises:
            FileNotFoundError: Se levanta si hay un error al cargar los archivos de sonido.
        """
        # Rutas de los archivos de sonido
        ruta_acertado = r"Caguela si quiere\acertado.wav"
        ruta_fallado = r"Caguela si quiere\fallado.wav"
        
        try:
            # Carga de los sonidos
            self.acertado = pygame.mixer.Sound(ruta_acertado)
            self.fallado = pygame.mixer.Sound(ruta_fallado)
        except pygame.error as e:
            raise FileNotFoundError(f"No se pudo cargar el archivo de sonido: {str(e)}")
