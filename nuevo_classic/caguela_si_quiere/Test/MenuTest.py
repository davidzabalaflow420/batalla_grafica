import unittest
from unittest.mock import patch
from io import StringIO
from Menu import Menu

class TestMenu(unittest.TestCase):

    @patch('builtins.input', side_effect=['1'])
    def test_menu_jugar(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Menu.mostrar_menu()
            output = fake_out.getvalue().strip()
            self.assertIn("Jugar", output)

    @patch('builtins.input', side_effect=['2'])
    def test_menu_acerca_de(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Menu.mostrar_menu()
            output = fake_out.getvalue().strip()
            self.assertIn("David y Andrés UdeM 2024/1", output)

    @patch('builtins.input', side_effect=['3'])
    def test_menu_salir(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            Menu.mostrar_menu()
            output = fake_out.getvalue().strip()
            self.assertNotIn("Jugar", output)
            self.assertNotIn("David y Andrés UdeM 2024/1", output)

if __name__ == '__main__':
    unittest.main()
