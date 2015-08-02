TITULO = 'Pelota saltarina'
ANCHO = 800
ALTO = 600

AZUL = 0, 128, 255
GRAVEDAD = 2000.0  # pixels per second per second


class Pelota:
    def __init__(self, x_inicial, y_inicial):
        self.x = x_inicial
        self.y = y_inicial
        self.vx = 200
        self.vy = 0
        self.radio = 20

    def dibuja(self):
        pos = (self.x, self.y)
        pantalla.dibuja.filled_circle(pos, self.radio, AZUL)


pelota = Pelota(50, 100)


def draw():
    pantalla.borra()
    pelota.dibuja()


def update(dt):
    # Apply constant acceleration formulae
    uy = pelota.vy
    pelota.vy += GRAVEDAD * dt
    pelota.y += (uy + pelota.vy) * 0.5 * dt

    # detect and handle bounce
    if pelota.y > ALTO - pelota.radio:  # we've bounced!
        pelota.y = ALTO - pelota.radio  # fix the position
        pelota.vy = -pelota.vy * 0.9  # inelastic collision

    # X component doesn't have acceleration
    pelota.x += pelota.vx * dt
    if pelota.x > ANCHO - pelota.radio or pelota.x < pelota.radio:
        pelota.vx = -pelota.vx


def cuando_tecla_pulsa(key):
    """Pressing a key will kick the ball upwards."""
    if key == teclas.SPACE:
        pelota.vy = -500
