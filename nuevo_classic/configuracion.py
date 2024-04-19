# Define constant for 'tamaño_letra'
TAMAÑO_LETRA = 'tamaño_letra'
TAMAÑO_LETRA_GRANDE = 'tamaño_letra_grande'

# Configuraciones de ventana para diferentes tamaños
PEQUEÑO = {
    'LADO_CUADRADO': 30,
    'separacion': 100,
    'margen': 100,  # Debe ser mayor que LADO_CUADRADO
    TAMAÑO_LETRA: 15,  # Usando constante en lugar de literal
    TAMAÑO_LETRA_GRANDE: 30,
    'ANCHO_VENTANA': 800,
    'ALTO_VENTANA': 600,
}
MEDIANO = {
    'LADO_CUADRADO': 40,
    'separacion': 120,
    'margen': 100,  # Debe ser mayor que LADO_CUADRADO
    TAMAÑO_LETRA: 30,  # Usando constante en lugar de literal
    TAMAÑO_LETRA_GRANDE: 60,
    'ANCHO_VENTANA': 1000,
    'ALTO_VENTANA': 800,
}
GRANDE = {
    'LADO_CUADRADO': 60,
    'separacion': 200,
    'margen': 200,  # Debe ser mayor que LADO_CUADRADO
    TAMAÑO_LETRA: 40,  # Usando constante en lugar de literal
    TAMAÑO_LETRA_GRANDE: 80,
    'ANCHO_VENTANA': 1500,
    'ALTO_VENTANA': 1000,
}
TAMAÑO = PEQUEÑO  # Tamaño de ventana por defecto
tamaños = {0: PEQUEÑO, 1: MEDIANO, 2: GRANDE}  # Diccionario de tamaños de ventana disponibles

# Define otras constantes
tipos_barcos = [2, 3, 3, 4]  # Tipos de barcos disponibles con sus respectivas longitudes
lado = 8  # Longitud del lado del tablero
letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # Letras para identificar las columnas del tablero

# Colores definidos
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Velocidad del texto (ms)
velocidad_texto = 100

# Lista de idiomas disponibles
idiomas = [
    ('es', 'español'),
    ('en', 'inglés'),
    ('fr', 'francés')
]
