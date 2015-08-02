ANCHO = 500
ALTO = 100
TITULO = "Verde deslumbrante!"

c = 0


def dibuja():
    pantalla.pinta((0, c, 0))


def refresca(dt):
    global c, ALTO
    c = (c + 1) % 256
    if c == 255:
        ALTO += 10


def cuando_raton_pulsa(button, pos):
    print("Raton ", button, "pulsado en", pos)

