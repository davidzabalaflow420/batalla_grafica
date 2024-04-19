from Menu import Menu 

class Main:
    """
    La clase Main es responsable de iniciar el juego y gestionar las interacciones iniciales.
    """

    def __init__(self):
        """
        Inicializa una instancia de la clase Main.

        Crea un objeto de la clase Menu y lo asigna al atributo 'menu'.
        """
        self.menu = Menu()

    def iniciar(self):
        """
        Inicia el juego llamando al método 'mostrar_menu()' del objeto 'menu'.
        """
        self.menu.mostrar_menu()

if __name__ == "__main__":
    """
    Bloque principal que crea una instancia de la clase Main y la inicia.
    """
    main = Main()
    main.iniciar()
