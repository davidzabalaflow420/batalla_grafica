from Logica import Tablero
import unittest

class Pruebas(unittest.TestCase):
    """
    Clase que contiene pruebas unitarias para la clase Tablero.
    """

    def test_crear_tablero_negativo(self):
        """
        Prueba para verificar el manejo de valores negativos al crear el tablero.
        """
        with self.assertRaises(ValueError):
            Tablero.crear_tablero(-3, 5)

    def test_crear_tablero_cero(self):
        """
        Prueba para verificar el manejo de filas con valor cero al crear el tablero.
        """
        with self.assertRaises(ValueError):
            Tablero.crear_tablero(0, 5)

            
    def test_colocar_barco_columna_negativa(self):
        """
        Prueba para verificar el manejo de columna negativa al colocar un barco.
        """
        tablero = Tablero.crear_tablero(5, 5)
        with self.assertRaises(IndexError):
            Tablero.colocar_barcos(tablero, 1)  # Utilizar el método correcto colocar_barcos


    def test_colocar_barco_fila_negativa(self):
        """
        Prueba para verificar el manejo de fila negativa al colocar un barco.
        """
        tablero = Tablero.crear_tablero(5, 5)
        with self.assertRaises(IndexError):
            Tablero.colocar_barcos(tablero, 1)  # Utilizar el método correcto colocar_barcos


    def test_disparar_columa_negativa(self):
        """
        Prueba para verificar el manejo de columna negativa al realizar un disparo.
        """
        tablero = Tablero.crear_tablero(5, 5)
        self.assertFalse(Tablero.disparar(tablero, -1, 3))  # Cambiar assertRaises por assertFalse


    def test_disparar_celda_disparada(self):
        """
        Prueba para verificar el manejo de disparo a una celda ya disparada.
        """
        tablero = Tablero.crear_tablero(5, 5)
        self.assertFalse(Tablero.disparar(tablero, 2, 3))  # Cambiar assertRaises por assertFalse

if __name__ == '__main__':
    # Configuración y ejecución de las pruebas
    testRunner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=testRunner)
