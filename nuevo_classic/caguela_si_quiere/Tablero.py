import random

class Tablero:
    def __init__(self, filas, columnas):
        """
        Constructor de la clase Tablero que recibe el número de filas y columnas como parámetros.

        Parameters:
        - filas (int): Número de filas del tablero.
        - columnas (int): Número de columnas del tablero.
        """
        self.filas = filas
        self.columnas = columnas
        self.matriz = [[' ']*self.columnas for _ in range(self.filas)]
        self.matriz_disparos = []
        
    def colocar_barcos(self, cantidad_barcos):
        """
        Coloca una cantidad determinada de barcos en el tablero de manera aleatoria.

        Args:
            tablero (Tablero): Objeto Tablero en el que se colocarán los barcos.
            cantidad_barcos (int): Número de barcos que se colocarán en el tablero.
        """
        barcos_colocados = 0
        while True:
            x, y = random.randint(0, self.columnas - 1), random.randint(0, self.filas - 1)
            if self.matriz[y][x] == ' ':
                self.matriz[y][x] = 'S'
                barcos_colocados += 1
            if barcos_colocados >= cantidad_barcos:
                break
    def todos_los_barcos_hundidos(self):
        """
        Verifica si todos los barcos en el tablero han sido hundidos.

        Returns:
            bool: True si todos los barcos han sido hundidos, False en caso contrario.
        """
        for y in range(self.filas):
            for x in range(self.columnas):
                celda = self.matriz[y][x]
                if celda != ' ' and celda != '*' and celda != '-':
                    return False
        return True

    def imprimir_separador_horizontal(self):
        """
        Método que imprime una línea horizontal separadora en el tablero.
        """
        print("+---" * self.columnas + "+")

    def imprimir_fila_de_numeros(self):
        """
        Método que imprime los números de las columnas en el tablero.
        """
        print("|   " + "|".join(f" {x+1} " for x in range(self.columnas)) + "|")

    def imprimir_matriz(self, deberia_mostrar_barcos, jugador):
        """
        Método que imprime la matriz del tablero, mostrando o no los barcos según el parámetro 'deberia_mostrar_barcos'
        y especificando el jugador al que pertenece el tablero.

        Parameters:
        - deberia_mostrar_barcos (bool): Indica si se deben mostrar los barcos en el tablero.
        - jugador (int): Número del jugador al que pertenece el tablero.
        """
        print(f"Este es el mar del jugador {jugador}: ")
        letra = "A"
        for y in range(self.filas):
            self.imprimir_separador_horizontal()
            print(f"| {letra} ", end="")
            for x in range(self.columnas):
                celda = self.matriz[y][x]
                valor_real = celda if deberia_mostrar_barcos or celda == ' ' else ' '
                if (x, y) in self.matriz_disparos:
                    valor_real = '-' if celda == ' ' else celda
                print(f"| {valor_real} ", end="")
            letra = chr(ord(letra) + 1)
            print("|")
        self.imprimir_separador_horizontal()
        self.imprimir_fila_de_numeros()

