# batalla_naval_python:
 Batalla naval programada en Python
## Quien lo hizo: 
    David Zabala y Andrés Arango
## Que es y para que:
    Juego de Batalla Naval para divertirse y ganar la materia
## Como lo hago funcionar:
   Instalar Python: Si aún no tienes Python instalado en tu sistema, necesitarás descargar e instalar la versión adecuada desde el sitio web oficial de Python: https://www.python.org/. Asegúrate de marcar la casilla "Agregar Python al PATH" durante la instalación para que puedas ejecutar Python desde cualquier ubicación en tu sistema.

    Descargar el repositorio o conseguir el archivo del juego: Puedes obtener el código del juego desde un repositorio en línea (como GitHub) o descargar el archivo del juego directamente. Si estás utilizando un repositorio, clona el repositorio o descarga el código como un archivo ZIP y extráelo en tu sistema.

    Descargar los archivos de sonidos: Asegúrate de tener los archivos de sonido necesarios para el juego (acertado.wav y fallado.wav) en tu sistema. Si no los tienes, puedes descargarlos de un sitio confiable en línea o crear tus propios archivos de sonido con los efectos de sonido deseados.

    Modificar las rutas de los archivos de sonido: Abre el archivo Sonido.py en un editor de texto y modifica las rutas de los archivos de sonido para que coincidan con la ubicación en tu sistema donde tienes guardados los archivos acertado.wav y fallado.wav.

    Ejecutar el programa: Abre una terminal o línea de comandos en la ubicación donde tienes guardados los archivos del juego. Luego, ejecuta el archivo Main.py con Python utilizando el siguiente comando: "python Main.py"

    Interactuar con el menú: Una vez que el programa se inicie correctamente, deberías ver el menú principal del juego en tu terminal. Sigue las instrucciones en pantalla para seleccionar una opción del menú, como jugar, ver información acerca de los desarrolladores o salir del juego.

    Jugar al juego: Si seleccionas la opción de jugar, se iniciará el juego de Batalla Naval. Sigue las instrucciones en pantalla para jugar, como ingresar las coordenadas de tus disparos y hundir los barcos de tu oponente.

## Como está hecho:
    Archivos Principales:

    Main.py: Este archivo es el punto de entrada de la aplicación. Se encarga de iniciar el juego creando una instancia de la clase Main y llamando al método iniciar().
    Menu.py: Contiene la clase Menu, que muestra el menú principal del juego y maneja las opciones seleccionadas por el usuario, como jugar, ver información acerca de los desarrolladores o salir del juego.
    Juego.py: Define la clase Juego, que gestiona la lógica del juego. Controla los turnos, la mecánica de disparo, las condiciones de victoria y derrota, y realiza las interacciones entre los tableros y los jugadores.
    Tablero.py: Contiene la clase Tablero, que representa el tablero de juego. Se encarga de manejar la colocación de barcos, verificar si los barcos están hundidos y imprimir el estado del tablero en la consola.
    Sonido.py: Define la clase Sonido, que gestiona los sonidos del juego. Carga archivos de sonido para indicar aciertos y fallos en los disparos.
    Clases y Funcionalidades:

    Menu: Proporciona métodos estáticos para mostrar el menú principal del juego y la información acerca de los desarrolladores. También maneja la lógica para iniciar el juego o salir del programa.
    Juego: Controla el flujo del juego, gestionando los turnos de los jugadores, la interacción con los tableros, los disparos y las condiciones de victoria o derrota.
    Tablero: Representa el tablero de juego donde se colocan los barcos y se realizan los disparos. Maneja la colocación de barcos, verifica si todos los barcos están hundidos y muestra el estado del tablero en la consola.
    Sonido: Administra los archivos de sonido del juego para indicar aciertos y fallos en los disparos.
    Interacción con el Usuario:

    El usuario interactúa con el juego a través de la consola, donde se muestran los mensajes y opciones del menú.
    Se utilizan entradas de teclado para seleccionar opciones del menú y para ingresar las coordenadas de los disparos durante el juego.
    Implementación de la Lógica del Juego:

    La lógica del juego se implementa principalmente en la clase Juego, donde se controlan los turnos, los disparos, la colocación de barcos y las condiciones de victoria o derrota.
    Se utilizan métodos y atributos en las clases Tablero y Juego para realizar las interacciones necesarias durante el juego, como la colocación de barcos, la verificación de disparos acertados y la actualización del estado del tablero.

## Estrucutra sugerida:
POO y SOLID
    
