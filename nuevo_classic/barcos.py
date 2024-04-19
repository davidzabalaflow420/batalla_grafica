from random import *
import importlib
import pygame
from configuracion import *
from jugar import *
from time import *
from caguela_si_quiere import * 

# Inicializar Pygame
pygame.init()

# Establecer el reloj para controlar la velocidad de actualización de la pantalla
clock = pygame.time.Clock()

# Inicializar el módulo de fuentes de Pygame
pygame.font.init()

# Cargar la música del juego
pygame.mixer.music.load('sonidos\morse-code-alphabet.ogg')

# Definir el título del juego
título = 'pyBattleship classic'

# Crear la ventana del juego con el tamaño especificado
win = pygame.display.set_mode((TAMAÑO['ANCHO_VENTANA'], TAMAÑO['ALTO_VENTANA']))

def init_window():
    """
    Inicializa la ventana del juego.
    
    Esta función configura el tamaño de la ventana y establece el título del juego.
    """
    # Configurar el tamaño de la ventana y establecer el título
    tamano_ventana_juego()
    win.fill(WHITE)
    pygame.display.set_caption(título)

def tamano_ventana_juego():
    """
    Establece el tamaño de la ventana del juego y las fuentes.
    
    Esta función configura el tamaño de la ventana del juego y carga las fuentes necesarias.
    """
    global monospace_large, monospace_xxl
    # Configurar el tamaño de la ventana
    pygame.display.set_mode((TAMAÑO['ANCHO_VENTANA'], TAMAÑO['ALTO_VENTANA']))
    # Cargar fuentes para texto en diferentes tamaños
    monospace_large = pygame.font.SysFont('Monospace', TAMAÑO['tamaño_letra'])
    monospace_xxl = pygame.font.SysFont('Monospace Bold', TAMAÑO['tamaño_letra_grande'])

    # (Opcional) Llenar la ventana con un color de fondo blanco
    win.fill(WHITE)




def configurar():
    """
    Configura las opciones del juego.
    
    Esta función permite al jugador configurar diferentes opciones del juego, como el idioma o la resolución de pantalla.
    """
    eleccion = configuracion()
    while eleccion > 0:
        if eleccion == 1:
            # Configurar el idioma del juego
            idioma = elegir_idioma()
            cargar_idioma(idioma)
        elif eleccion == 2:
            # Cambiar la resolución de la pantalla
            tamaño = elegir_resolucion_pantalla()
            cambiar_resolucion_pantalla(tamaño)
        elif eleccion == 3:
            pantalla_texto(texto_instrucciones)
        
        eleccion = configuracion()

def trasponer(tablero):
    """
    Transpone una matriz/tablero dado.
    
    Esta función toma una matriz/tablero como entrada y devuelve su transpuesta.
    
    Args:
        tablero (list): La matriz/tablero a transponer.
        
    Returns:
        list: La transpuesta del tablero.
    """
    lado = len(tablero)
    tablero_tras = [[' ']*lado for _ in range(lado)]  # Crear una matriz/tablero vacío con las dimensiones transpuestas
    for i in range(lado):
        for j in range(lado):
            tablero_tras[i][j] = tablero[j][i]  # Copiar los elementos de la matriz original en su posición transpuesta
    return tablero_tras

def pprint(tablero):
    """
    Imprime un tablero de juego de manera legible.
    
    Esta función toma un tablero de juego como entrada y lo imprime en la consola, organizando las filas y columnas de manera legible.
    
    Args:
        tablero (list): El tablero de juego a imprimir.
    """
    tablero_tras = trasponer(tablero)  # Transponer el tablero para imprimir las columnas como filas
    for fila in tablero_tras:
        print(fila)


def dibuja_cuadricula(x0, y0):
    """
    Dibuja la cuadrícula del tablero de juego en la ventana.
    
    Esta función dibuja la cuadrícula del tablero de juego en la posición especificada en la ventana.
    
    Args:
        x0 (int): La coordenada x de la esquina superior izquierda de la cuadrícula.
        y0 (int): La coordenada y de la esquina superior izquierda de la cuadrícula.
    """
    # Dibujar el cuadro exterior de la cuadrícula
    pygame.draw.rect(win, WHITE,
                     (x0, y0,
                      lado*TAMAÑO['LADO_CUADRADO'], lado*TAMAÑO['LADO_CUADRADO']))
    
    # Dibujar líneas horizontales
    for j in range(0,lado+1):
        pygame.draw.line(win, BLACK,
                         (x0, y0 + TAMAÑO['LADO_CUADRADO']*j),
                         (x0 + TAMAÑO['LADO_CUADRADO']*lado, y0 + TAMAÑO['LADO_CUADRADO']*j), 1)
    
    # Dibujar letras en las filas
    for j in range(0,lado):
        letra = monospace_large.render(letras[j], True, BLACK)
        win.blit(letra, (x0 - TAMAÑO['LADO_CUADRADO'], y0 + TAMAÑO['LADO_CUADRADO']*j))

    # Dibujar líneas verticales
    for j in range(0,lado+1):
        pygame.draw.line(win, BLACK,
                         (x0 + TAMAÑO['LADO_CUADRADO']*j, y0),
                         (x0 + TAMAÑO['LADO_CUADRADO']*j, y0 + TAMAÑO['LADO_CUADRADO']*lado), 1)

    # Dibujar números en las columnas
    for j in range(0,lado):
        letra = monospace_large.render(str(j+1), True, BLACK)
        win.blit(letra, (x0 + TAMAÑO['LADO_CUADRADO']*j + (TAMAÑO['LADO_CUADRADO'] - TAMAÑO['tamaño_letra']), y0 + TAMAÑO['LADO_CUADRADO']*lado))


def dibuja_un_tablero(x0, y0, tablero):
    """
    Dibuja un tablero en la ventana del juego.
    
    Esta función dibuja un tablero en la posición especificada en la ventana del juego.
    
    Args:
        x0 (int): La coordenada x de la esquina superior izquierda del tablero.
        y0 (int): La coordenada y de la esquina superior izquierda del tablero.
        tablero (list): El tablero a dibujar.
    """
    # Dibujar la cuadrícula del tablero
    dibuja_cuadricula(x0, y0)
    
    # Iterar sobre cada fila y columna del tablero
    for fila in range(lado):
        for columna in range(lado):
            casilla = tablero[fila][columna]
            # Dibujar las fichas según su tipo
            if casilla in 'BOX':
                if casilla == 'B':
                    color = GREY
                elif casilla == 'O':
                    color = BLUE
                elif casilla == 'X':
                    color = RED
                # Dibujar una ficha circular en la posición correspondiente
                pygame.draw.circle(win, color,
                                   (x0 + TAMAÑO['LADO_CUADRADO']*fila + TAMAÑO['LADO_CUADRADO']//2, y0 + TAMAÑO['LADO_CUADRADO']*columna + TAMAÑO['LADO_CUADRADO']//2),
                                   TAMAÑO['LADO_CUADRADO']//2)
            elif (casilla == ' ') or (casilla == '.'):
                # No hacer nada si la casilla está vacía o es un punto
                pass
            else:
                # Dibujar el contenido de la casilla (letra) en la posición correspondiente
                letra = monospace_large.render(casilla, True, BLACK)
                win.blit(letra, (x0 + TAMAÑO['LADO_CUADRADO']*fila, y0 + TAMAÑO['LADO_CUADRADO']*columna))



def oculta_barcos(tablero):
    """
    Oculta los barcos en el tablero.
    
    Esta función crea un nuevo tablero donde los barcos están ocultos, representados como espacios en blanco.
    
    Args:
        tablero (list): El tablero original con los barcos.
        
    Returns:
        list: El nuevo tablero donde los barcos están ocultos.
    """
    nuevo_tablero = []
    for fila in tablero:
        nueva_fila = [(' ' if casilla=='B' else casilla) for casilla in fila]  # Reemplazar 'B' con espacio en blanco
        nuevo_tablero.append(nueva_fila)
    return nuevo_tablero

def dibuja_tableros(tablero1, tablero2):
    """
    Dibuja dos tableros en la ventana del juego.
    
    Esta función dibuja dos tableros en la ventana del juego, uno al lado del otro, con el tablero 1 visible y el tablero 2 con los barcos ocultos.
    
    Args:
        tablero1 (list): El primer tablero a dibujar.
        tablero2 (list): El segundo tablero a dibujar.
    """
    # Dibujar el tablero 1
    x0 = TAMAÑO['margen']
    y0 = TAMAÑO['margen']
    dibuja_un_tablero(x0, y0, tablero1)
    
    # Dibujar el tablero 2 con los barcos ocultos
    x0 = TAMAÑO['margen'] + TAMAÑO['separacion'] + TAMAÑO['LADO_CUADRADO']*lado
    y0 = TAMAÑO['margen']
    tablero2_oculto = oculta_barcos(tablero2)  # Ocultar los barcos del tablero 2
    dibuja_un_tablero(x0, y0, tablero2_oculto)
    
    # Actualizar la pantalla para mostrar los cambios
    pygame.display.update()


def disparo_ordenador_tonto(tablero):
    """
    Esta función realiza un disparo aleatorio por parte del ordenador en un tablero.
    
    Args:
    - tablero (list): El tablero de juego en el que se realizará el disparo.
    
    Returns:
    - tuple: Las coordenadas (x, y) del disparo realizado por el ordenador.
    """
    x = randint(0, lado - 1)  # Se elige una coordenada x aleatoria dentro del rango del tablero
    y = randint(0, lado - 1)  # Se elige una coordenada y aleatoria dentro del rango del tablero
    print('El ordenador dispara:', traducir_coordenadas_al_reves(x, y))  # Se muestra el disparo realizado
    return x, y

def disparo_ordenador_menos_tonto(tablero):
    """
    Esta función realiza un disparo aleatorio por parte del ordenador en un tablero,
    evitando disparar en casillas que ya han sido atacadas.
    
    Args:
    - tablero (list): El tablero de juego en el que se realizará el disparo.
    
    Returns:
    - tuple: Las coordenadas (x, y) del disparo realizado por el ordenador.
    """
    x = randint(0, lado - 1)  # Se elige una coordenada x aleatoria dentro del rango del tablero
    y = randint(0, lado - 1)  # Se elige una coordenada y aleatoria dentro del rango del tablero
    
    # Puede ser desconocido o barco
    if tablero[x][y] == ' ':  # Si la casilla elegida está vacía, es decir, no ha sido atacada
        print('El ordenador dispara:', traducir_coordenadas_al_reves(x, y))  # Se muestra el disparo realizado
    else:
        print('Aquí ya he disparado, mejor vuelvo a lanzar los dados')  # Si la casilla ya ha sido atacada, se indica
        x, y = disparo_ordenador_menos_tonto(tablero)  # Se vuelve a llamar a la función para elegir otra casilla
    return x, y



def vecinos_de(x, y):
    """
    Encuentra los vecinos de una posición en el tablero.
    
    Esta función devuelve una lista de las posiciones vecinas (arriba, abajo, izquierda, derecha) de una posición dada en el tablero.
    
    Args:
        x (int): La coordenada x de la posición.
        y (int): La coordenada y de la posición.
        
    Returns:
        list: Una lista de tuplas que representan las posiciones de los vecinos.
    """
    vecinos = []
    if x > 0:
        vecinos.append((x - 1, y))
    if x < lado - 1:
        vecinos.append((x + 1, y))
    if y > 0:
        vecinos.append((x, y - 1))
    if y < lado - 1:
        vecinos.append((x, y + 1))
    return vecinos

def algun_vecino_es_X(tablero, x, y):
    """
    Comprueba si alguno de los vecinos de una posición contiene una 'X'.
    
    Esta función verifica si alguno de los vecinos de una posición dada en el tablero contiene una 'X'.
    
    Args:
        tablero (list): El tablero donde se realizará la búsqueda.
        x (int): La coordenada x de la posición.
        y (int): La coordenada y de la posición.
        
    Returns:
        bool: True si alguno de los vecinos contiene una 'X', False en caso contrario.
    """
    vecinos = vecinos_de(x, y)
    return any(tablero[x_vecino][y_vecino] == 'X'
               for (x_vecino, y_vecino) in vecinos)

def disparo_ordenador_medio_listo(tablero):
    """
    Esta función realiza un disparo por parte del ordenador en un tablero, dando prioridad
    a las casillas vecinas de las casillas que contienen un barco conocido.
    
    Args:
    - tablero (list): El tablero de juego en el que se realizará el disparo.
    
    Returns:
    - tuple: Las coordenadas (x, y) del disparo realizado por el ordenador.
    """
    # Se generan las casillas prioritarias, que son aquellas vacías y tienen al menos un vecino con un barco conocido
    casillas_prioritarias = [
        (x, y) for x in range(lado)  # Se recorren todas las coordenadas x del tablero
               for y in range(lado)  # Se recorren todas las coordenadas y del tablero
        if (tablero[x][y] == ' ') and algun_vecino_es_X(tablero, x, y)  # Si la casilla está vacía y tiene al menos un vecino con un barco conocido
    ]
    
    if len(casillas_prioritarias) > 0:  # Si hay casillas prioritarias disponibles
        x, y = choice(casillas_prioritarias)  # Se elige una de forma aleatoria
    else:
        x, y = disparo_ordenador_menos_tonto(tablero)  # Si no hay casillas prioritarias, se procede como en la función menos tonta
    return x, y



def disparo(tablero, x, y):
    """
    Realiza un disparo en una posición específica del tablero.
    
    Esta función simula un disparo en una posición específica del tablero y actualiza el tablero en consecuencia.
    
    Args:
        tablero (list): El tablero donde se realizará el disparo.
        x (int): La coordenada x del disparo.
        y (int): La coordenada y del disparo.
        
    Returns:
        list: El tablero actualizado después del disparo.
    """
    elemento_antiguo = tablero[x][y]
    if elemento_antiguo in ' .':
        elemento_nuevo = 'O'
    elif elemento_antiguo == 'B':
        elemento_nuevo = 'X'
        # Marcar espacios alrededor del barco como 'agua'
        if x > 0 and y > 0 and tablero[x-1][y-1] == ' ':
            tablero[x-1][y-1] = '.'
        if x > 0 and y < lado - 1 and tablero[x-1][y+1] == ' ':
            tablero[x-1][y+1] = '.'
        if x < lado - 1 and y > 0 and tablero[x+1][y-1] == ' ':
            tablero[x+1][y-1] = '.'
        if x < lado - 1 and y < lado - 1 and tablero[x+1][y+1] == ' ':
            tablero[x+1][y+1] = '.'
    else:
        elemento_nuevo = elemento_antiguo
    tablero[x][y] = elemento_nuevo
    return tablero

def dibuja_barco_desde_arriba(largo, x, y, vertical, color=GREY):
    """
    Dibuja un barco en el tablero desde arriba.
    
    Esta función dibuja un barco en el tablero desde arriba, con la opción de dibujarlo vertical u horizontalmente.
    
    Args:
        largo (int): La longitud del barco.
        x (int): La coordenada x de la esquina superior izquierda del barco.
        y (int): La coordenada y de la esquina superior izquierda del barco.
        vertical (bool): True si el barco se dibuja verticalmente, False si se dibuja horizontalmente.
        color (tuple): El color del barco. Por defecto, es GREY.
    """
    if vertical:
        pygame.draw.polygon(win, color, [
            (x, y + TAMAÑO['LADO_CUADRADO']//2),
            (x, y + TAMAÑO['LADO_CUADRADO']//2 + TAMAÑO['LADO_CUADRADO']*(largo-1)),
            (x + TAMAÑO['LADO_CUADRADO']//2, y + TAMAÑO['LADO_CUADRADO']*largo),
            (x + TAMAÑO['LADO_CUADRADO'], y + TAMAÑO['LADO_CUADRADO']//2 + TAMAÑO['LADO_CUADRADO']*(largo-1)),
            (x + TAMAÑO['LADO_CUADRADO'], y + TAMAÑO['LADO_CUADRADO']//2),
            (x + TAMAÑO['LADO_CUADRADO']//2, y)
            ])
    else:
        pygame.draw.polygon(win, color, [
            (x + TAMAÑO['LADO_CUADRADO']//2, y),
            (x + TAMAÑO['LADO_CUADRADO']//2 + TAMAÑO['LADO_CUADRADO']*(largo-1), y),
            (x + TAMAÑO['LADO_CUADRADO']*largo, y + TAMAÑO['LADO_CUADRADO']//2),
            (x + TAMAÑO['LADO_CUADRADO']//2 + TAMAÑO['LADO_CUADRADO']*(largo-1), y + TAMAÑO['LADO_CUADRADO']),
            (x + TAMAÑO['LADO_CUADRADO']//2, y + TAMAÑO['LADO_CUADRADO']),
            (x, y + TAMAÑO['LADO_CUADRADO']//2)
            ])

def dibuja_barcos_en_fila(x, y, barco_seleccionado, barcos_colocados):
    """
    Dibuja los barcos en una fila del panel de selección de barcos.
    
    Esta función dibuja los barcos en una fila del panel de selección de barcos, marcando el barco seleccionado y los barcos ya colocados.
    
    Args:
        x (int): La coordenada x de la esquina superior izquierda del panel.
        y (int): La coordenada y de la esquina superior izquierda del panel.
        barco_seleccionado (int): El índice del barco seleccionado.
        barcos_colocados (list): Una lista que indica qué barcos ya han sido colocados.
        
    Returns:
        list: Una lista que indica qué barcos están en cada columna del panel.
    """
    barco_en_columna = [-1]*(sum(tipos_barcos) + len(tipos_barcos))
    columna = 0
    for j, largo in enumerate(tipos_barcos):
        if j == barco_seleccionado:
            color = BLUE
        elif barcos_colocados[j]:
            color = GREEN
        else:
            color = GREY
        dibuja_barco_desde_arriba(largo, x + columna*TAMAÑO['LADO_CUADRADO'], y, False, color)
        barco_en_columna[columna:columna+largo] = [j]*largo
        columna = columna + largo + 1
    return barco_en_columna

def traducir_coordenadas(disparo):
    """
    Traduce una coordenada de disparo de su formato de entrada a coordenadas de tablero.
    
    Args:
        disparo (str): Coordenada de disparo en formato alfanumérico, por ejemplo 'A1'.
        
    Returns:
        tuple: Coordenadas x, y en formato de tablero (0-indexed).
    """
    if len(disparo) < 2:
        return -1, -1
    letra, numero = disparo[:2]
    x = ord(numero) - ord('1')
    y = ord(letra.upper()) - ord('A')
    return x, y

def traducir_coordenadas_al_reves(x, y):
    """
    Traduce coordenadas de tablero a su formato de disparo alfanumérico.
    
    Args:
        x (int): Coordenada x en formato de tablero.
        y (int): Coordenada y en formato de tablero.
        
    Returns:
        str: Coordenada de disparo en formato alfanumérico, por ejemplo 'A1'.
    """
    numero = str(x + 1)
    letra = chr(ord('A') + y)
    disparo = letra + numero
    return disparo

def ha_terminado(tablero):
    """
    Verifica si todos los barcos han sido hundidos en el tablero.
    
    Args:
        tablero (list): El tablero a verificar.
        
    Returns:
        bool: True si todos los barcos han sido hundidos, False en caso contrario.
    """
    for linea in tablero:
        for elemento in linea:
            if elemento == 'B':
                return False
    return True

def tablero_vacio():
    """
    Crea un tablero vacío lleno de espacios en blanco.
    
    Returns:
        list: Tablero vacío.
    """
    return [[' ']*lado for _ in range(lado)]

def ordenador_coloca_un_barco(tablero, largo):
    """
    Coloca un barco aleatoriamente en el tablero.
    
    Args:
        tablero (list): El tablero donde se colocará el barco.
        largo (int): La longitud del barco a colocar.
        
    Returns:
        tuple: El nuevo tablero con el barco colocado y las posiciones ocupadas por el barco.
    """
    buena_posicion = False
    while not buena_posicion:
        vertical = choice([True, False])
        if vertical:
           columna = randint(0, lado-1)
           fila = randint(0, lado-1-largo)
        else: # if horizontal
            columna = randint(0, lado-1-largo)
            fila = randint(0, lado-1)
        buena_posicion = se_puede_colocar(largo, fila, columna, vertical, tablero)
    nuevo_tablero = coloca_un_barco(tablero, fila, columna, largo, vertical)
    if vertical:
        posiciones_barco = [
            (columna, fila + j) for j in range(largo)
        ]
    else:
        posiciones_barco = [(columna+k, fila) for k in range(largo)]
    return nuevo_tablero, posiciones_barco

def ordenador_coloca_barcos(tipos_barcos):
    """
    Coloca barcos aleatoriamente en el tablero para el ordenador.
    
    Args:
        tipos_barcos (list): Lista de longitudes de los barcos a colocar.
        
    Returns:
        tuple: El tablero con los barcos colocados y un diccionario que mapea índices de barcos a sus posiciones.
    """
    tablero = tablero_vacio()
    posiciones_barcos = {}
    for n, largo in enumerate(tipos_barcos):
        tablero, posiciones_barco = ordenador_coloca_un_barco(tablero, largo)
        posiciones_barcos[n] = posiciones_barco
    return tablero, posiciones_barcos

def texto_jugador(texto):
    """
    Muestra texto para el jugador en la ventana del juego.
    
    Esta función muestra texto para el jugador en la ventana del juego.
    
    Args:
        texto (str): El texto que se mostrará.
    """
    wth = monospace_large.render(texto, True, BLACK)
    pygame.draw.rect(win, WHITE,
                     (TAMAÑO['margen'] + TAMAÑO['tamaño_letra'] + TAMAÑO['LADO_CUADRADO']*lado, TAMAÑO['margen'],
                      2*TAMAÑO['tamaño_letra'], TAMAÑO['tamaño_letra']))
    win.blit(wth, (TAMAÑO['margen'] + TAMAÑO['tamaño_letra'] + TAMAÑO['LADO_CUADRADO']*lado, TAMAÑO['margen']))



def texto_ordenador(texto):
    """
    Muestra texto para el ordenador en la ventana del juego.
    
    Esta función muestra texto para el ordenador en la ventana del juego.
    
    Args:
        texto (str): El texto que se mostrará.
    """
    wth = monospace_large.render(texto, True, RED)
    pygame.draw.rect(win, WHITE,
                     (TAMAÑO['margen'] + TAMAÑO['tamaño_letra'] + TAMAÑO['LADO_CUADRADO']*lado, TAMAÑO['margen'] + TAMAÑO['LADO_CUADRADO'],
                      2*TAMAÑO['tamaño_letra'], TAMAÑO['tamaño_letra']))
    win.blit(wth, (TAMAÑO['margen'] + TAMAÑO['tamaño_letra'] + TAMAÑO['LADO_CUADRADO']*lado, TAMAÑO['margen'] + TAMAÑO['LADO_CUADRADO']))

def texto_victoria(texto):
    """
    Muestra texto de victoria en la ventana del juego.
    
    Esta función muestra texto de victoria en la ventana del juego.
    
    Args:
        texto (str): El texto que se mostrará.
    """
    x = 50
    y = TAMAÑO['ALTO_VENTANA'] - TAMAÑO['tamaño_letra']*4
    dibuja_texto_largo(texto, x, y, monospace_large, TAMAÑO['tamaño_letra'])

def comprueba_hundido(tablero, posiciones_barcos, x, y):
    """
    Comprueba si un disparo ha hundido un barco en el tablero.
    
    Args:
        tablero (list): El tablero donde se ha realizado el disparo.
        posiciones_barcos (dict): Un diccionario que mapea índices de barcos a sus posiciones en el tablero.
        x (int): Coordenada x del disparo.
        y (int): Coordenada y del disparo.
        
    Returns:
        bool: True si el disparo ha hundido un barco, False en caso contrario.
    """
    if tablero[x][y] != 'B':
        return False
    if not algun_vecino_es_X(tablero, x, y):
        return False
    for j, posiciones_barco in posiciones_barcos.items():
        if any((xbarco == x) and (ybarco == y)
               for xbarco, ybarco in posiciones_barco):
            # Estoy disparando al barco j
            daño = sum(1 for xbarco, ybarco in posiciones_barco
                       if tablero[xbarco][ybarco] == 'X')
            largo = len(posiciones_barco)
            if daño == largo - 1:
                x_primer, y_primer = posiciones_barco[0]
                x_ultima, y_ultima = posiciones_barco[-1]
                if x_primer == x_ultima:
                    # Vertical
                    # Primera casilla
                    x = x_primer
                    y = y_primer - 1
                    if y >= 0 and tablero[x][y] == ' ':
                        tablero[x][y] = '.'
                    # Última casilla
                    x = x_primer
                    y = y_ultima + 1
                    if y < lado and tablero[x][y] == ' ':
                        tablero[x][y] = '.'
                else:
                    # Horizontal
                    # Primera casilla
                    x = x_primer - 1
                    y = y_primer
                    if x >= 0 and tablero[x][y] == ' ':
                        tablero[x][y] = '.'
                    # Última casilla
                    x = x_ultima + 1
                    y = y_ultima
                    if x < lado and tablero[x][y] == ' ':
                        tablero[x][y] = '.'
                alerta(texto_alerta_hundido)
                return True


def jugar(tablero1, tablero2, posiciones_barcos1, posiciones_barcos2):
    """
    Función principal que maneja el juego entre el jugador y el ordenador.

    Args:
    - tablero1 (list): El tablero del jugador.
    - tablero2 (list): El tablero del ordenador.
    - posiciones_barcos1 (list): Las posiciones de los barcos del jugador.
    - posiciones_barcos2 (list): Las posiciones de los barcos del ordenador.
    """
    init_window()  # Se inicializa la ventana de juego
    alerta('')  # Se muestra una alerta vacía al principio del juego
    pygame.mixer.music.stop()  # Se detiene la música de fondo
    teclas = []  # Lista para almacenar las teclas presionadas por el jugador
    seguir_jugando = True  # Variable para controlar si se sigue jugando o no

    while seguir_jugando:
        dibuja_tableros(tablero1, tablero2)  # Se dibujan los tableros del jugador y del ordenador
        dibuja_alerta()  # Se dibuja la alerta en la ventana de juego
        sleep(0.1)  # Se realiza una pausa para que el juego no corra demasiado rápido
        events = pygame.event.get()  # Se obtienen los eventos ocurridos en pygame
        for event in events:
            if event.type == pygame.QUIT:  # Si se cierra la ventana, se sale del juego
                exit()
            elif event.type == pygame.KEYDOWN:  # Si se presiona una tecla
                if event.key == pygame.K_F10:  # Si se presiona F10, se abre la configuración del juego
                    configurar()
                    init_window()
                    dibuja_tableros(tablero1, tablero2)
                teclas.append(event.key)  # Se agrega la tecla presionada a la lista de teclas

        # Se comprueba si se han presionado suficientes teclas o si se ha presionado Enter o Esc
        if ((len(teclas) >= 3) or
            (teclas and
             (teclas[-1] in (pygame.K_RETURN, pygame.K_ESCAPE)))
        ):
            if (len(teclas) >= 3) and (teclas[2] == pygame.K_RETURN):  # Si se presionaron al menos tres teclas y la tercera es Enter
                coordenadas = chr(teclas[0]) + chr(teclas[1])  # Se obtienen las coordenadas ingresadas por el jugador

                x, y = traducir_coordenadas(coordenadas)  # Se traducen las coordenadas al formato del tablero
                disparo_ok = ((0 <= x < lado) and  # Se verifica si las coordenadas están dentro del tablero
                              (0 <= y < lado))
            else:
                disparo_ok = False  # Si no se presionaron tres teclas o la tercera no es Enter, el disparo no es válido
            teclas = []  # Se reinicia la lista de teclas

            if disparo_ok:  # Si el disparo es válido
                print()
                pprint(tablero1)  # Se imprime el tablero del jugador
                print()
                pprint(tablero2)  # Se imprime el tablero del ordenador
                texto_jugador(coordenadas)  # Se muestra el texto indicando las coordenadas ingresadas por el jugador
                comprueba_hundido(tablero2, posiciones_barcos2, x, y)  # Se verifica si se ha hundido algún barco del ordenador
                tablero2 = disparo(tablero2, x, y)  # Se realiza el disparo en el tablero del ordenador

                if ha_terminado(tablero2):  # Si el ordenador ha perdido todos sus barcos
                    dibuja_tableros(tablero1, tablero2)  # Se dibujan los tableros
                    texto_victoria(texto_has_ganado)  # Se muestra el texto de victoria para el jugador
                    pygame.display.update()  # Se actualiza la ventana de juego
                    sleep(3)  # Se espera un tiempo antes de salir del juego
                    seguir_jugando = False  # Se termina el juego
                dibuja_tableros(tablero1, tablero2)  # Se dibujan los tableros
                sleep(1)  # Se espera un segundo antes de que juegue el ordenador
                x, y = disparo_ordenador_medio_listo(oculta_barcos(tablero1))  # El ordenador realiza su disparo
                texto_ordenador(traducir_coordenadas_al_reves(x, y))  # Se muestra el texto del disparo del ordenador
                comprueba_hundido(tablero1, posiciones_barcos1, x, y)  # Se verifica si se ha hundido algún barco del jugador
                tablero1 = disparo(tablero1, x, y)  # Se realiza el disparo en el tablero del jugador
                if ha_terminado(tablero1):  # Si el jugador ha perdido todos sus barcos
                    texto_victoria(texto_has_perdido)  # Se muestra el texto de derrota para el jugador
                    pygame.display.update()  # Se actualiza la ventana de juego
                    sleep(3)  # Se espera un tiempo antes de salir del juego
                    dibuja_tableros(tablero1, tablero2)  # Se dibujan los tableros
                    seguir_jugando = False  # Se termina el juego
            else:
                texto_jugador('??')  # Si las coordenadas ingresadas por el jugador son incorrectas, se muestra un texto de error
                alerta(texto_coordenadas_erroneas)  # Se muestra una alerta indicando que las coordenadas son incorrectas


def dibuja_texto_largo(texto, x, y, font, fontsize):
    """
    Dibuja texto largo en la ventana del juego.

    Esta función toma un texto largo, lo divide en líneas y lo dibuja en la ventana del juego.

    Args:
        texto (str): El texto que se va a dibujar.
        x (int): La coordenada x de la posición de inicio del texto.
        y (int): La coordenada y de la posición de inicio del texto.
        font (pygame.font.Font): La fuente a utilizar para el texto.
        fontsize (int): El tamaño de la fuente.

    """
    lineas = texto.splitlines()
    pygame.draw.rect(win, WHITE,
                     (x, y, TAMAÑO['ANCHO_VENTANA'] - x, fontsize*len(lineas)))
    for i, l in enumerate(lineas):
        win.blit(font.render(l, True, BLACK), (x, y + fontsize*i))

def se_puede_colocar(largo, fila, columna, vertical, tablero):
    """
    Comprueba si un barco se puede colocar en una posición determinada del tablero.

    Args:
        largo (int): La longitud del barco.
        fila (int): La fila en la que se va a colocar el barco.
        columna (int): La columna en la que se va a colocar el barco.
        vertical (bool): Indica si el barco se coloca verticalmente o no.
        tablero (list): El tablero de juego.

    Returns:
        bool: True si el barco se puede colocar en la posición dada, False en caso contrario.
    """
    if (vertical and fila+largo > lado):
        alerta(texto_alerta_fuera)
        return False
    if (not vertical and columna+largo > lado):
        alerta(texto_alerta_fuera)
        return False
    if vertical:
        for y in range(max(0, fila-1), min(fila+largo+1, lado)):
            for x in range(max(0, columna-1), min(columna + 2, lado)):
                if tablero[x][y] == 'B':
                    alerta(texto_alerta_barcos_juntos)
                    return False
    else:
        for y in range(max(0, fila-1), min(fila+2, lado)):
            for x in range(max(0, columna-1), min(columna + largo+1, lado)):
                if tablero[x][y] == 'B':
                    alerta(texto_alerta_barcos_juntos)
                    return False
    return True

def coloca_un_barco(tablero, x, y, largo, vertical):
    """
    Coloca un barco en el tablero.

    Args:
        tablero (list): El tablero de juego.
        x (int): La coordenada x de la posición de inicio del barco.
        y (int): La coordenada y de la posición de inicio del barco.
        largo (int): La longitud del barco.
        vertical (bool): Indica si el barco se coloca verticalmente o no.

    Returns:
        list: El tablero con el barco colocado.
    """
    if vertical:
        for j in range(largo):
            tablero = coloca_barcos(tablero, x + j, y)
    else:
        for j in range(largo):
            tablero = coloca_barcos(tablero, x, y + j)
    return tablero

def coloca_barcos(tablero, x, y):
    """
    Coloca un barco en una fila o columna específica del tablero.

    Args:
        tablero (list): El tablero de juego.
        x (int): La coordenada x de la posición de inicio del barco.
        y (int): La coordenada y de la posición de inicio del barco.

    Returns:
        list: El tablero con el barco colocado.
    """
    nuevo_tablero = []
    for numero_fila in range(lado):
        if numero_fila != y:
            fila_antigua = tablero[numero_fila]
            nuevo_tablero.append(fila_antigua)
        else:
            fila_antigua = tablero[numero_fila]
            fila_nueva = []
            for numero_columna in range(lado):
                if numero_columna != x:
                    elemento_antiguo = fila_antigua[numero_columna]
                    fila_nueva.append(elemento_antiguo)
                else:
                    elemento_antiguo = fila_antigua[numero_columna]
                    if elemento_antiguo == ' ':
                        elemento_nuevo = 'B'
                    elif elemento_antiguo == 'B':
                        elemento_nuevo = ' '
                    else:
                        elemento_nuevo = elemento_antiguo
                    fila_nueva.append(elemento_nuevo)
            nuevo_tablero.append(fila_nueva)
    return nuevo_tablero

def colocar_barcos_viejo():
    """
    Coloca los barcos en el tablero en el modo de juego de un jugador.

    Returns:
        list: El tablero con los barcos colocados.
    """
    tablero1 = tablero_vacio()
    tablero2 = tablero_vacio()
    seguir_colocando = True
    while seguir_colocando:
        dibuja_tableros(tablero1, tablero2)
        sleep(0.1)
        events = pygame.event.get()
        # Procesar eventos
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                seguir_colocando = False
            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                print(x, y)
                if ((TAMAÑO['margen'] <= x < TAMAÑO['margen'] + lado*TAMAÑO['LADO_CUADRADO']) and
                        (TAMAÑO['margen'] <= y < TAMAÑO['margen'] + lado*TAMAÑO['LADO_CUADRADO'])):
                    columna = (x - TAMAÑO['margen'])//TAMAÑO['LADO_CUADRADO']
                    fila = (y - TAMAÑO['margen'])//TAMAÑO['LADO_CUADRADO']
                    print(columna, fila)
                    print(traducir_coordenadas_al_reves(fila, columna))
                    tablero1 = coloca_barcos(tablero1, fila, columna)
    return tablero1

tiempo_ultima_alerta = pygame.time.get_ticks()
texto_alerta = ''

def alerta(texto):
    """
    Muestra una alerta en la ventana del juego.

    Esta función muestra una alerta en la ventana del juego y reproduce un sonido.

    Args:
        texto (str): El texto de la alerta.

    """
    pygame.mixer.music.play()
    global texto_alerta, tiempo_ultima_alerta
    tiempo_ultima_alerta = pygame.time.get_ticks()
    texto_alerta = texto

def dibuja_alerta():
    """
    Dibuja la alerta en la ventana del juego.

    Esta función dibuja la alerta en la ventana del juego.

    """
    hasta_aqui = int((pygame.time.get_ticks() - tiempo_ultima_alerta)/velocidad_texto)
    texto = texto_alerta[:hasta_aqui]
    if hasta_aqui > len(texto_alerta):
        pygame.mixer.music.stop()
    x_alerta = 50
    y_alerta = TAMAÑO['ALTO_VENTANA'] - 100
    pygame.draw.rect(win, WHITE,
                     (x_alerta, y_alerta, TAMAÑO['ANCHO_VENTANA'], TAMAÑO['LADO_CUADRADO']))
    win.blit(monospace_large.render(texto, True, BLACK), (x_alerta, y_alerta))



def colocar_barcos():
    """
    Función principal para que el jugador coloque sus barcos en el tablero.

    Returns:
        tuple: Una tupla que contiene el tablero con los barcos colocados y un diccionario de las posiciones de los barcos.
    """
    # Inicializa la ventana del juego y otras variables
    init_window()
    num_barcos = len(tipos_barcos)
    posiciones_barcos = {j:[] for j in range(num_barcos)}
    tablero1 = tablero_vacio()
    tablero2 = tablero_vacio()
    y_coloca_barcos_min = TAMAÑO['margen'] + TAMAÑO['LADO_CUADRADO']*(lado+2)
    y_coloca_barcos_max = y_coloca_barcos_min + TAMAÑO['LADO_CUADRADO']
    x_coloca_barcos_min = TAMAÑO['separacion']
    x_coloca_barcos_max = (x_coloca_barcos_min
        + sum(largo for largo in tipos_barcos)*TAMAÑO['LADO_CUADRADO']
        + sum(1 for largo in tipos_barcos)*TAMAÑO['LADO_CUADRADO']
    )
    seguir_colocando = True
    barco_seleccionado = -1
    barcos_colocados = [False]*len(tipos_barcos)
    vertical = False

    # Bucle principal para colocar los barcos
    while seguir_colocando:
        sleep(0.1)
        dibuja_tableros(tablero1, tablero2)
        dibuja_alerta()
        barco_en_columna = dibuja_barcos_en_fila(
            x_coloca_barcos_min, y_coloca_barcos_min,
            barco_seleccionado, barcos_colocados)

        # Eventos del juego
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Verifica si todos los barcos han sido colocados antes de continuar
                if sum(barcos_colocados) < num_barcos:
                    alerta(texto_alerta_sin_terminar)
                else:
                    seguir_colocando = False
            elif event.type == pygame.MOUSEMOTION:
                x,y = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                x,y = pygame.mouse.get_pos()
                if event.button == 3:  # Botón derecho del ratón
                    vertical = not vertical
                elif ((barco_seleccionado >= 0) and
                      (TAMAÑO['margen'] <= x < TAMAÑO['margen'] + lado*TAMAÑO['LADO_CUADRADO']) and
                      (TAMAÑO['margen'] <= y < TAMAÑO['margen'] + lado*TAMAÑO['LADO_CUADRADO'])):
                    columna = (x - TAMAÑO['margen'])//TAMAÑO['LADO_CUADRADO']
                    fila = (y - TAMAÑO['margen'])//TAMAÑO['LADO_CUADRADO']
                    largo = tipos_barcos[barco_seleccionado]
                    # Verifica si el barco se puede colocar en la posición seleccionada
                    if vertical and (fila+largo <= lado):
                        dibuja_barco_desde_arriba(largo, TAMAÑO['margen']+columna*TAMAÑO['LADO_CUADRADO'], TAMAÑO['margen']+fila*TAMAÑO['LADO_CUADRADO'], vertical, color=GREY)
                    elif (not vertical) and (columna + largo <= lado):
                        dibuja_barco_desde_arriba(largo, TAMAÑO['margen']+columna*TAMAÑO['LADO_CUADRADO'], TAMAÑO['margen']+fila*TAMAÑO['LADO_CUADRADO'], vertical, color=GREY)
                    # Actualiza la ventana del juego
                    pygame.display.update()
                    # Procesa los eventos de ratón
                    if se_puede_colocar(largo, fila, columna, vertical, tablero1):
                        tablero1 = coloca_un_barco(tablero1, fila, columna, largo, vertical)
                        barcos_colocados[barco_seleccionado] = True
                        if vertical:
                            posiciones_barcos[barco_seleccionado] = [
                                (columna, fila + j) for j in range(largo)
                            ]
                        else:
                            posiciones_barcos[barco_seleccionado] = [
                                (columna + j, fila) for j in range(largo)
                            ]
                        barco_seleccionado = -1
                # Verifica si se ha hecho clic en la zona de selección de barcos
                elif ((x_coloca_barcos_min <= x < x_coloca_barcos_max) and
                    (y_coloca_barcos_min <= y < y_coloca_barcos_max)):
                    columna = (x - x_coloca_barcos_min)//TAMAÑO['LADO_CUADRADO']
                    barco_seleccionado = barco_en_columna[columna]
                    # Si el barco seleccionado ya estaba colocado, quita el barco del tablero
                    if barcos_colocados[barco_seleccionado]:
                        for columna, fila in posiciones_barcos[barco_seleccionado]:
                            tablero1[columna][fila] = ' '
                        barcos_colocados[barco_seleccionado] = False

    # Limpia la alerta y detiene la música de alerta
    alerta('')
    pygame.mixer.music.stop()
    return tablero1, posiciones_barcos



def pantalla_texto(texto_total):
    """
    Muestra texto en pantalla con efecto de desplazamiento.

    Args:
        texto_total (str): El texto completo que se va a mostrar en pantalla.

    Returns:
        int: La tecla presionada por el usuario para continuar (ENTER o ESCAPE).
    """
    # Reproduce música de fondo y inicializa la ventana del juego
    pygame.mixer.music.play(-1)
    init_window()
    
    # Renderiza y muestra el título en la ventana
    wth = monospace_xxl.render(título, True, BLACK)
    win.blit(wth, (TAMAÑO['ANCHO_VENTANA']/2 - wth.get_bounding_rect().width/2, 50))
    
    # Inicializa el tiempo de inicio para el efecto de desplazamiento del texto
    tiempo_inicial = pygame.time.get_ticks()
    
    while True:
        clock.tick(40)
        
        # Calcula la posición del texto que se va a mostrar
        hasta_aqui = int((pygame.time.get_ticks() - tiempo_inicial)/velocidad_texto)
        
        # Detiene la música si se ha mostrado todo el texto
        if hasta_aqui > len(texto_total):
            pygame.mixer.music.stop()
        
        # Prepara el texto que se va a mostrar
        texto = texto_total[:hasta_aqui]
        
        # Muestra el texto en la ventana
        dibuja_texto_largo(texto, 100, 200, monospace_large, TAMAÑO['tamaño_letra'])
        pygame.display.update()
        
        # Captura eventos del usuario
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                # Si se presiona ENTER o ESCAPE, se detiene la música y se devuelve la tecla presionada
                if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    pygame.mixer.music.stop()
                    return event.key
                # Si se presiona ESPACIO o ABAJO, se simula el efecto de mostrar todo el texto de inmediato
                elif event.key in (pygame.K_SPACE, pygame.K_DOWN):
                    # Un truco para que muestre todo el texto instantáneamente
                    tiempo_inicial = -100000
                    pygame.mixer.music.stop()




def intro():
    """
    Muestra la introducción del juego con información sobre la longitud de los barcos.

    Genera y muestra el texto de introducción del juego, incluyendo información sobre la longitud de los barcos.

    """
    texto_colocar = '\n'.join(texto_longitud_barco+str(largo)
        for largo in tipos_barcos)
    texto_total = texto_intro + texto_colocar + texto_continuar
    pantalla_texto(texto_total)

def intro_jugar():
    """
    Muestra la introducción para comenzar a jugar.

    Genera y muestra el texto de introducción para empezar a jugar.

    """
    texto_total = texto_intro_jugar + texto_continuar
    pantalla_texto(texto_total)

def creditos():
    """
    Muestra los créditos del juego.

    Genera y muestra el texto de los créditos del juego.

    """
    texto_total = texto_creditos
    pantalla_texto(texto_total)

def elegir_opcion(opciones):
    """
    Permite al jugador elegir entre una lista de opciones.

    Muestra las opciones en la pantalla y espera a que el jugador haga clic en una de ellas.

    Args:
        opciones (list): Una lista de tuplas que contienen el índice de la opción y el texto de la opción.

    Returns:
        int: El índice de la opción seleccionada por el jugador.

    """
    init_window()
    wth = monospace_xxl.render(título, True, BLACK)
    win.blit(wth, (TAMAÑO['ANCHO_VENTANA']/2 - wth.get_bounding_rect().width/2, 50))
    xinicio, yinicio = 100, 200
    linea = 0
    coordenadas_opciones = {}
    espacio = TAMAÑO['tamaño_letra'] + 30
    margen_configuracion = 3
    for indice_opcion, opcion in opciones:
        texto_opcion = monospace_large.render(opcion, True, BLACK)
        r = texto_opcion.get_bounding_rect()
        xtexto = xinicio
        ytexto = yinicio + espacio*linea
        coordenadas_opcion = (
            xinicio + r.left - margen_configuracion,
            ytexto + r.top - margen_configuracion,
            r.width + 2*margen_configuracion,
            r.height + 2*margen_configuracion
        )
        coordenadas_opciones[indice_opcion] = coordenadas_opcion
        pygame.draw.rect(win, BLACK, coordenadas_opcion, 1)
        win.blit(texto_opcion, (xinicio, ytexto))
        linea = linea + 1

    pygame.display.update()
    while True:
        clock.tick(40)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                x,y = pygame.mouse.get_pos()
                print(x,y)
                for opcion, coordenadas in coordenadas_opciones.items():
                    xopcion, yopcion, ancho, alto = coordenadas
                    if ((x > xopcion) and
                        (y > yopcion) and
                        (x < xopcion + ancho) and
                        (y < yopcion + alto)):
                        return opcion

def elegir_idioma():
    """
    Permite al jugador elegir un idioma.

    Muestra una lista de idiomas disponibles y espera a que el jugador seleccione uno.

    Returns:
        int: El índice del idioma seleccionado por el jugador.

    """
    return elegir_opcion(idiomas)

def configuracion():
    """
    Permite al jugador configurar diversas opciones del juego.

    Muestra una lista de opciones de configuración y espera a que el jugador seleccione una.

    Returns:
        int: El índice de la opción de configuración seleccionada por el jugador.
    """
    opciones = [
        (0, texto_config_jugar),
        (1, texto_config_idioma),
        (2, texto_config_pantalla),
        (3, texto_instrucciones),
        
]
    eleccion = elegir_opcion(opciones)

    if eleccion == 3: 
        pantalla_texto(texto_instruccion) 
    

    return eleccion

def elegir_resolucion_pantalla():
    """
    Permite al jugador elegir la resolución de la pantalla del juego.

    Muestra una lista de opciones de resolución de pantalla y espera a que el jugador seleccione una.

    Returns:
        int: El índice de la opción de resolución de pantalla seleccionada por el jugador.

    """
    opciones = [
        (0, texto_resolucion_peque), 
        (1, texto_resolucion_medio), 
        (2, texto_resolucion_grande)
    ]
    return elegir_opcion(opciones)

def cambiar_resolucion_pantalla(indice_tamaño):
    """
    Cambia la resolución de la pantalla del juego.

    Args:
        indice_tamaño (int): El índice del tamaño de pantalla seleccionado.

    """
    global TAMAÑO
    TAMAÑO = tamaños[indice_tamaño]
    tamano_ventana_juego()

def cargar_idioma(idioma):
    """
    Carga un idioma específico para el juego.

    Args:
        idioma (str): El nombre del idioma a cargar.

    """
    mod_idiomas = importlib.import_module('idiomas.' + idioma)
    globals().update(mod_idiomas.__dict__)
    pygame.display.set_caption(título)

def volver_a_jugar():
    """
    Pregunta al jugador si desea volver a jugar.

    Muestra un mensaje al jugador preguntando si desea volver a jugar y espera su respuesta.

    Returns:
        bool: True si el jugador desea volver a jugar, False si no.

    """
    tecla = pantalla_texto(texto_volver_a_jugar)
    if tecla == pygame.K_RETURN:
        return True
    elif tecla == pygame.K_ESCAPE:
        return False

def jugar_por_consola ( ):
    """
    Función que maneja el juego por consola.
    
    Esta función permitirá al usuario jugar el juego de Batalla Naval directamente desde la consola.
    """
    main = Main()
    main.iniciar()
    