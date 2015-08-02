ANCHO = 300
ALTO = 300


def dibuja():
    r = 255
    g = 0
    b = 0

    ancho = ANCHO
    alto = ALTO - 200

    for i in range(20):
        rect = Rect((0, 0), (ancho, alto))
        rect.center = 150, 150
        pantalla.dibuja.rect(rect, (r, g, b))

        r -= 10
        g += 10

        ancho -= 10
        alto += 10
