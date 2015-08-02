alien = Personaje('alien')

TITULO = "Paseo del alien"
ANCHO = 500
ALTO = alien.alto + 20


# ponemos la posicion inicial
alien.arribaderecha = 0, 10


def dibuja():
    """Clear the screen and draw the alien."""
    pantalla.borra()
    alien.dibuja()


def refresca():
    """Move the alien by one pixel."""
    alien.x += 1

    # si el alien sale por la derecha
    # lo movemos a la izquierda
    if alien.izquierda > ANCHO:
        alien.derecha = 0
