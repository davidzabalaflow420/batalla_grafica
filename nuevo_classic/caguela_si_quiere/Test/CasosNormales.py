from Logica import Tablero
import unittest

#Pruebas unitarias
class TestTablero(unittest.TestCase):
    """
    Clase que contiene pruebas unitarias para la clase Tablero.
    """
    def setUp(self):
        """
        Configura el tablero antes de cada prueba.
        """
        self.tablero = Tablero(5, 5)  # Crear un tablero de 5x5

    def test_creacion_tablero(self):
        """
        Prueba la creación del tablero.
        """
        self.assertEqual(self.tablero.filas, 5)
        self.assertEqual(self.tablero.columnas, 5)
        self.assertEqual(len(self.tablero.matriz), 5)
        self.assertEqual(len(self.tablero.matriz[0]), 5)

    def test_inicializacion_matriz(self):
        """
        Prueba la inicialización de la matriz del tablero.
        """
        for fila in self.tablero.matriz:
            for celda in fila:
                self.assertEqual(celda, ' ')

    def test_colocar_barcos(self):
        """
        Prueba la colocación de barcos en el tablero.
        """
        self.tablero.colocar_barcos(3)
        self.assertEqual(self.tablero.barcos_hundidos, 0)

    def test_colocar_barcos_cantidad_correcta(self):
        """
        Prueba que se coloquen la cantidad correcta de barcos.
        """
        cantidad_barcos = 3
        self.tablero.colocar_barcos(cantidad_barcos)
        self.assertEqual(sum(row.count('S') for row in self.tablero.matriz), cantidad_barcos)

    def test_disparar_fallado(self):
        """
        Prueba de un disparo fallido.
        """
        x, y = 2, 2
        self.assertFalse(self.tablero.matriz[y][x] == 'S')
        self.assertFalse(self.tablero.matriz[y][x] == '*')
        self.assertFalse(self.tablero.matriz[y][x] == '-')
        self.tablero.disparar(x, y)
        self.assertEqual(self.tablero.matriz[y][x], '-')

    def test_disparar_acertado(self):
        """
        Prueba de un disparo acertado.
        """
        x, y = 3, 3
        self.assertFalse(self.tablero.matriz[y][x] == '*')
        self.assertFalse(self.tablero.matriz[y][x] == '-')
        self.tablero.matriz[y][x] = 'S'
        self.tablero.disparar(x, y)
        self.assertEqual(self.tablero.matriz[y][x], '*')

if __name__ == '__main__':
    # Ejecución de las pruebas unitarias
    testRunner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=testRunner)
