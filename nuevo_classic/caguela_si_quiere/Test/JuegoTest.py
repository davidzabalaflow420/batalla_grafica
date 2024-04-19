import unittest
from unittest.mock import patch
from Juego import Juego
from Tablero import Tablero
from Sonido import Sonido

class TestJuego(unittest.TestCase):
    
    def setUp(self):
        # Initialize test data
        self.jugador1 = Tablero(10, 10)
        self.jugador2 = Tablero(10, 10)
        self.sonidos = Sonido()
        self.juego = Juego(self.jugador1, self.jugador2, 3, self.sonidos)

    @patch('builtins.input', side_effect=['A', '1'])
    def test_solicitar_coordenadas(self, mock_input):
        x, y = self.juego.solicitar_coordenadas()
        self.assertEqual((x, y), (0, 0))

    def test_disparar_acertado(self):
        x, y = 0, 0
        acertado = self.juego.disparar(x, y, self.jugador2)
        self.assertTrue(acertado)

    def test_disparar_fallado(self):
        x, y = 0, 0
        acertado = self.juego.disparar(x, y, self.jugador2)
        self.assertFalse(acertado)

    def test_indicar_victoria_jugador1(self):
        self.juego.barcos_hundidos_j1 = 5
        self.juego.barcos_hundidos_j2 = 3
        self.juego.indicar_victoria()
        self.assertEqual(self.juego.barcos_hundidos_j1, 5)

    def test_indicar_victoria_jugador2(self):
        self.juego.barcos_hundidos_j1 = 3
        self.juego.barcos_hundidos_j2 = 5
        self.juego.indicar_victoria()
        self.assertEqual(self.juego.barcos_hundidos_j2, 5)

    def test_indicar_empate(self):
        self.juego.barcos_hundidos_j1 = 4
        self.juego.barcos_hundidos_j2 = 4
        self.juego.indicar_victoria()
        self.assertEqual(self.juego.barcos_hundidos_j1, self.juego.barcos_hundidos_j2)

    def test_indicar_fracaso(self):
        self.juego.indicar_fracaso()
        self.assertEqual(self.juego.disparos_restantes_j1, 0)
        self.assertEqual(self.juego.disparos_restantes_j2, 0)

if __name__ == '__main__':
    unittest.main()
