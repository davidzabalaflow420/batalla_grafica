from Logica import Tablero
import unittest

class TestTablero(unittest.TestCase):
    def setUp(self):
        """
        Configura el tablero para las pruebas.
        """
        self.tablero = Tablero(5, 5)

    def test_creacion_con_filas_no_enteras(self):
        """
        Prueba de creación del tablero con filas no enteras.
        """
        with self.assertRaises(ValueError):
            Tablero(2.5, 5)

    def test_creacion_con_columnas_no_enteras(self):
        """
        Prueba de creación del tablero con columnas no enteras.
        """
        with self.assertRaises(ValueError):
            Tablero(4, "B")

    def test_colocar_barcos_sobre_celdas_ocupadas(self):
        """
        Prueba de colocar barcos sobre celdas ya ocupadas.
        """
        self.tablero.matriz[2][2] = 'S'
        with self.assertRaises(ValueError, msg="No se levantó ValueError al colocar barcos sobre celdas ocupadas"):
            self.tablero.colocar_barcos(1)

    def test_colocar_barcos_exitosamente(self):
        """
        Prueba de colocar barcos correctamente.
        """
        cantidad_barcos = 3
        try:
            self.tablero.colocar_barcos(cantidad_barcos)
        except ValueError as e:
            self.fail(f"Se generó un ValueError inesperado: {e}")

        barcos_en_tablero = sum(row.count('S') for row in self.tablero.matriz)
        self.assertEqual(barcos_en_tablero, cantidad_barcos)

    def test_disparar_con_coordenadas_invalidas(self):
        """
        Prueba de disparar con coordenadas fuera de límites.
        """
        self.assertFalse(self.tablero.disparar(6, 2))
        self.assertFalse(self.tablero.disparar(2, 6))

    def test_disparar_con_coordenadas_ya_utilizadas(self):
        """
        Prueba de disparar en celdas ya utilizadas.
        """
        x, y = 2, 2
        self.tablero.disparar(x, y)
        self.assertFalse(self.tablero.disparar(x, y))

    def test_disparar_en_celda_ya_utilizada(self):
        """
        Prueba de disparar en celda ya utilizada.
        """
        x, y = 3, 4
        self.tablero.disparar(x, y)
        self.assertFalse(self.tablero.disparar(1, 1))
        self.assertFalse(self.tablero.disparar(x, y))
            
    def test_disparar_fuera_de_limites(self):
        """
        Prueba de disparar fuera de límites.
        """
        self.assertFalse(self.tablero.disparar(6, 2))
        self.assertFalse(self.tablero.disparar(2, 6))

if __name__ == '__main__':
    # Ejecución de las pruebas unitarias
    testRunner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=testRunner)
