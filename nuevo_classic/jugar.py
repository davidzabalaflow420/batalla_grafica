"""Script principal para el juego de Batalla Naval.
Este script inicializa la ventana del juego, permite al usuario elegir un idioma,
configura los ajustes del juego y ejecuta el bucle del juego hasta que el usuario decida salir.
"""
from barcos import *
from configuracion import *

def main():
    """Función principal para ejecutar el juego de Batalla Naval."""
    init_window()  # Inicializa la ventana del juego

    ##### ELEGIR IDIOMA ####
    # Cargamos el idioma por defecto por si el idioma seleccionado no tiene todas las cadenas definidas
    cargar_idioma('es')
    idioma = elegir_idioma()
    cargar_idioma(idioma)

    configurar()  # Configura los ajustes del juego
    seguir_jugando = True

    while seguir_jugando:
        ##### INTRO ####
        intro()  # Muestra la introducción del juego

        ##### COLOCA LOS BARCOS #####
        tablero1, posiciones_barcos1 = colocar_barcos()  # El jugador coloca sus barcos
        tablero2, posiciones_barcos2 = ordenador_coloca_barcos(tipos_barcos)  # La computadora coloca sus barcos
        print()
        pprint(tablero1)  # Imprime el tablero del jugador
        print(posiciones_barcos1)  # Imprime las posiciones de los barcos del jugador
        pprint(tablero2)  # Imprime el tablero de la computadora
        print(posiciones_barcos2)  # Imprime las posiciones de los barcos de la computadora

        ##### INTRO DISPARAR####
        intro_jugar()  # Muestra la introducción para el turno de disparo

        ##### DISPARAR #####
        jugar(tablero1, tablero2, posiciones_barcos1, posiciones_barcos2)  # Inicia el turno de disparo

        ##### JUGAR OTRA VEZ? #####
        seguir_jugando = volver_a_jugar()  # Pregunta al jugador si desea jugar otra vez

        creditos()  # Muestra los créditos del juego

if __name__ == "__main__":
    main()
