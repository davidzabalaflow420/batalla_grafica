import random
import numbers

class Tablero:
    """
    Clase para representar un tablero de juego para Batalla Naval.
    """

    def __init__(self, filas, columnas):
        """
        Inicializa un nuevo tablero con las dimensiones dadas.

        Args:
            filas (int): Número de filas en el tablero.
            columnas (int): Número de columnas en el tablero.
        """
        self.validar_dimensiones(filas, columnas)

        self.aciertos = 0
        self.filas = filas
        self.columnas = columnas
        self.matriz = [[' '] * self.columnas for _ in range(self.filas)]
        self.matriz_disparos = []
        self.barcos_hundidos = 0
        self.disparos_realizados = set()
        self.error_disparo = None 

    @staticmethod
    def crear_tablero(filas, columnas):
        """
        Crea un nuevo objeto Tablero con las dimensiones dadas.

        Args:
            filas (int): Número de filas en el tablero.
            columnas (int): Número de columnas en el tablero.

        Returns:
            Tablero: El tablero creado.
        """
        return Tablero(filas, columnas)

    def validar_dimensiones(self, filas, columnas):
        """
        Valida que las dimensiones dadas sean enteras y positivas.

        Args:
            filas (int): Número de filas en el tablero.
            columnas (int): Número de columnas en el tablero.

        Raises:
            ValueError: Si las filas o columnas no son enteras o son negativas.
        """
        if not isinstance(filas, numbers.Integral) or not isinstance(columnas, numbers.Integral):
            raise ValueError("Las filas y columnas deben ser valores enteros y positivos")
        elif filas <= 0 or columnas <= 0:
            raise ValueError("Las filas y columnas deben ser valores positivos")

    def imprimir_separador_horizontal(self):
        """
        Imprime una línea separadora horizontal para el tablero.
        """
        print("+---" * self.columnas + "+")

    def imprimir_fila_de_numeros(self):
        """
        Imprime los números de columna sobre el tablero.
        """
        print("|   " + "|".join(f" {x + 1} " for x in range(self.columnas)) + "|")

    def imprimir_matriz(self, deberia_mostrar_barcos, jugador):
        """
        Imprime la matriz del tablero.

        Args:
            deberia_mostrar_barcos (bool): Indica si los barcos deben ser mostrados o no.
            jugador (int): El número del jugador.

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
                    if celda == 'B':
                        self.barcos_hundidos += 1
                print(f"| {valor_real} ", end="")
            letra = chr(ord(letra) + 1)
            print("|")
        self.imprimir_separador_horizontal()
        self.imprimir_fila_de_numeros()

    def colocar_barcos(self, cantidad_barcos):
        """
        Coloca barcos aleatorios en el tablero.

        Args:
            cantidad_barcos (int): Número de barcos a colocar.
        """
        barcos_colocados = 0
        while barcos_colocados < cantidad_barcos:
            x, y = random.randint(0, self.columnas - 1), random.randint(0, self.filas - 1)
            if self.matriz[y][x] == ' ':
                self.matriz[y][x] = 'S'
                barcos_colocados += 1
            else:
                continue

    def disparar(self, x, y):
        """
        Realiza un disparo en las coordenadas dadas.

        Args:
            x (int): Coordenada x del disparo.
            y (int): Coordenada y del disparo.

        Returns:
            bool: True si el disparo fue un acierto, False de lo contrario.
        """
        if not isinstance(x, numbers.Integral) or not isinstance(y, numbers.Integral):
            return False

        if x < 0 or x >= self.columnas or y < 0 or y >= self.filas:
            return False

        if (x, y) in self.disparos_realizados:
            return False

        if self.matriz[y][x] == ' ':
            self.matriz[y][x] = '-'
            self.matriz_disparos.append((x, y))
            return False
        elif self.matriz[y][x] == '-':
            return False
        else:
            self.matriz[y][x] = '*'
            self.matriz_disparos.append((x, y))
            self.aciertos += 1
            self.disparos_realizados.add((x, y))
            return True
