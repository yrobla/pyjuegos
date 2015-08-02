from pgzero.loaders import sounds

alien = Personaje('alien')

TITULO = "El paseo del alien"
ANCHO = 500
ALTO = alien.alto + 20

# posicion inicial
alien.arribaderecha = 0, 10


def dibuja():
    """Clear the screen and draw the alien."""
    pantalla.borra()
    alien.dibuja()


def refresca():
    """Move the alien by one pixel."""
    alien.x += 1

    # If the alien is off the right hand side of the screen,
    # move it back off screen to the left-hand side
    if alien.izquierda > ANCHO:
        alien.derecha = 0


def cuando_raton_pulsa(pos):
    """Detect clicks on the alien."""
    if alien.coincide(pos):
        pon_alien_herido()


def pon_alien_herido():
    """Set the current alien sprite to the "hurt" image."""
    alien.imagen = 'alien_hurt'
    sounds.eep.play()
    reloj.pon_alarma_unica(pon_alien_normal, 1.0)


def pon_alien_normal():
    """Set the current alien sprite to the normal image."""
    alien.imagen = 'alien'
