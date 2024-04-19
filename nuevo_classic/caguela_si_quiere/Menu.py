import pygame
from Tablero import Tablero
from Juego import Juego
from Sonido import Sonido

class Menu:
    @staticmethod
    def acerca_de():
        """
        Método estático que imprime información sobre los desarrolladores del juego.
        """
        print("David y Andrés UdeM 2024/1")

    @staticmethod
    def mostrar_menu():
        """
        Método estático que muestra el menú principal del juego y maneja las opciones seleccionadas por el usuario.

        El menú incluye opciones para jugar, ver información acerca de los desarrolladores y salir del juego.
        """
        pygame.init()
        sonidos = Sonido()  
        while True: 
            eleccion = input("""
1. Jugar
2. Acerca de
3. Salir
Elige: """)  
            try:
                opcion = int(eleccion) 
            except ValueError:
                print("Por favor, ingresa un número válido.")
                continue

            if opcion == 1:
                try:
                    tablero_j1 = Tablero(5, 5)
                    tablero_j2 = Tablero(5, 5)
                    sonidos.acertado
                    sonidos.fallado
                    juego = Juego(tablero_j1, tablero_j2, 10, sonidos)
                    juego.jugar()
                except FileNotFoundError as e:
                    print(f"Error: {str(e)}") 
            elif opcion == 2:
                Menu.acerca_de()
            elif opcion == 3:
                break
            else:
                print("Opción no válida. Por favor, elige una opción del menú.")
