import unittest
from unittest.mock import patch
from Tablero import Tablero

class TestTablero(unittest.TestCase):

    def setUp(self):
        self.tablero = Tablero(5, 5)

    def test_colocar_barcos(self):
        self.tablero.colocar_barcos(3)
        barcos_count = sum(row.count('S') for row in self.tablero.matriz)
        self.assertEqual(barcos_count, 3)

    def test_todos_los_barcos_hundidos(self):
        self.tablero.matriz = [['S', ' ', 'S'], ['S', 'S', 'S'], [' ', 'S', ' ']]
        self.assertFalse(self.tablero.todos_los_barcos_hundidos())
        self.tablero.matriz = [['*', '*', '*'], ['*', '*', '*'], ['*', '*', '*']]
        self.assertTrue(self.tablero.todos_los_barcos_hundidos())

    @patch('builtins.print')
    def test_imprimir_separador_horizontal(self, mock_print):
        self.tablero.imprimir_separador_horizontal()
        mock_print.assert_called_once_with('+' + '---+' * 5)

    @patch('builtins.print')
    def test_imprimir_fila_de_numeros(self, mock_print):
        self.tablero.imprimir_fila_de_numeros()
        mock_print.assert_called_once_with('|   | 1 | 2 | 3 | 4 | 5 |')

    @patch('builtins.print')
    def test_imprimir_matriz(self, mock_print):
        self.tablero.matriz = [['S', ' ', 'S'], [' ', 'S', ' '], ['S', 'S', 'S']]
        self.tablero.matriz_disparos = [(0, 0), (1, 1), (2, 2)]
        self.tablero.imprimir_matriz(True, 1)
        expected_calls = [
            'Este es el mar del jugador 1: ',
            '+---+---+---+---+---+',
            '| A | S |   | S |   |',
            '+---+---+---+---+---+',
            '| B |   | S |   |   |',
            '+---+---+---+---+---+',
            '| C | S | S | S |   |',
            '+---+---+---+---+---+',
            '|   | 1 | 2 | 3 | 4 | 5 |'
        ]
        mock_print.assert_has_calls([unittest.mock.call(call) for call in expected_calls])

if __name__ == '__main__':
    unittest.main()
