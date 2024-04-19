import pygame
    
class Juego:
    def __init__(self, jugador1, jugador2, disparos_iniciales, sonidos):
        """
        Inicializa una instancia de la clase Juego.

        Args:
            jugador1 (Tablero): Objeto Tablero que representa el tablero del jugador 1.
            jugador2 (Tablero): Objeto Tablero que representa el tablero del jugador 2.
            disparos_iniciales (int): Número de disparos iniciales que tendrá cada jugador.
            sonidos (Sonidos): Objeto Sonidos que contiene los sonidos del juego.
        """
        self.tablero_j1 = jugador1
        self.tablero_j2 = jugador2
        self.sonidos = sonidos
        self.disparos_iniciales = disparos_iniciales
        self.turno = 0
        self.disparos_restantes_j1 = disparos_iniciales
        self.disparos_restantes_j2 = disparos_iniciales
        self.jugador_actual = jugador1
        self.max_disparos = disparos_iniciales
        self.coordenadas_disparadas_j1 = set()
        self.coordenadas_disparadas_j2 = set()
        self.barcos_hundidos_j1 = 0
        self.barcos_hundidos_j2 = 0

    def jugar(self):
        """
        Inicia el juego y lo mantiene en ejecución hasta que uno de los jugadores gane o se agoten los disparos.
        """
        self.tablero_j1.colocar_barcos(5)
        self.tablero_j2.colocar_barcos(5)
        print("===============")
        print("¡Comienza el juego! Jugador 1, es tu turno.")

        while True:
            print("Turno del jugador {}".format(self.turno + 1))
            self.imprimir_disparos_restantes()

            if (self.jugador_actual == self.tablero_j1 and self.disparos_restantes_j1 <= 0) or \
                (self.jugador_actual == self.tablero_j2 and self.disparos_restantes_j2 <= 0):
                self.indicar_victoria()
                break

            tablero_oponente = self.tablero_j2 if self.jugador_actual == self.tablero_j1 else self.tablero_j1

            tablero_oponente.imprimir_matriz(False, "J1" if self.jugador_actual == self.tablero_j2 else "J2")
            x, y = self.solicitar_coordenadas()
            acertado = self.disparar(x, y, tablero_oponente)

            if not acertado:
                self.turno = (self.turno + 1) % 2

            if self.jugador_actual == self.tablero_j1:
                self.disparos_restantes_j1 -= 1
            else:
                self.disparos_restantes_j2 -= 1

            tablero_oponente.imprimir_matriz(True, "J1" if self.jugador_actual == self.tablero_j2 else "J2")

            if acertado:
                print("Disparo acertado")
                if self.tablero_j2.todos_los_barcos_hundidos():
                    self.indicar_victoria()
                    break
            else:
                print("Disparo fallado")
                if self.turno >= self.max_disparos:
                    self.indicar_fracaso()
                    break

                self.jugador_actual = self.tablero_j1 if self.jugador_actual == self.tablero_j2 else self.tablero_j2
            print("Barcos hundidos por J1:", self.barcos_hundidos_j1)
            print("Barcos hundidos por J2:", self.barcos_hundidos_j2)

    

    def solicitar_coordenadas(self):
        """
        Solicita al jugador las coordenadas de su disparo y las valida.

        Returns:
            tuple: Tupla que contiene las coordenadas x, y del disparo.
        """
        while True:
            letra_fila = input("Ingresa la letra de la fila tal y como aparece en el tablero: ")
            if len(letra_fila) != 1:
                print("Debes ingresar únicamente una letra")
                continue
            y = ord(letra_fila.upper()) - 65
            if 0 <= y < self.tablero_j1.filas:
                break
            else:
                print("Fila inválida")

        while True:
            try:
                x = int(input("Ingresa el número de columna: ")) - 1
                if 0 <= x < self.tablero_j1.columnas:
                    if self.jugador_actual == self.tablero_j1:
                        if (x, y) in self.coordenadas_disparadas_j1:
                            print("Coordenada ya disparada. Escoge otra.")
                            continue
                        else:
                            self.coordenadas_disparadas_j1.add((x, y))
                    else:
                        if (x, y) in self.coordenadas_disparadas_j2:
                            print("Coordenada ya disparada. Escoge otra.")
                            continue
                        else:
                            self.coordenadas_disparadas_j2.add((x, y))
                    break
                else:
                    print("Columna inválida")
            except ValueError:
                print("Ingresa un número válido")

        return x, y


    def disparar(self, x, y, tablero):
        """
        Realiza un disparo en las coordenadas especificadas y actualiza el tablero en consecuencia.

        Args:
            x (int): Coordenada x del disparo.
            y (int): Coordenada y del disparo.
            tablero (Tablero): Objeto Tablero en el que se realizará el disparo.

        Returns:
            bool: True si el disparo fue acertado, False en caso contrario.
        """
        if tablero.matriz[y][x] == ' ':
            tablero.matriz[y][x] = '-'
            pygame.mixer.Sound.play(self.sonidos.fallado)
            tablero.matriz_disparos.append((x, y))
            return False
        elif tablero.matriz[y][x] == '-':
            return False
        else:
            tablero.matriz[y][x] = '*'
            pygame.mixer.Sound.play(self.sonidos.acertado)
            tablero.matriz_disparos.append((x, y))
            if self.jugador_actual == self.tablero_j1:
                self.barcos_hundidos_j1 += 1
            else:
                self.barcos_hundidos_j2+= 1
            return True

    def imprimir_disparos_restantes(self):
        """
        Imprime el número de disparos restantes para cada jugador.
        """
        print("Disparos restantes de J1: {}  -  Disparos restantes de J2: {}".format(
            self.disparos_restantes_j1, self.disparos_restantes_j2))
        
    def indicar_victoria(self):
        """
        Método que se ejecuta cuando un jugador gana el juego.
        Indica cuál jugador ha ganado basado en la cantidad de barcos hundidos.
        """
        if self.barcos_hundidos_j1 > self.barcos_hundidos_j2:
            print("¡Felicidades! El Jugador 1 ha ganado el juego.")
        elif self.barcos_hundidos_j2 > self.barcos_hundidos_j1:
            print("¡Felicidades! El Jugador 2 ha ganado el juego.")
        else:
            print("¡Empate! Ambos jugadores hundieron la misma cantidad de barcos.")
    
    def indicar_fracaso(self):
        """
        Método que se ejecuta cuando ningún jugador gana y se agotan los disparos.
        """
        print("¡Nadie ha ganado! Se han agotado todos los disparos.")
                
            

