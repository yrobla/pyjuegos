import pygame
import pygame.draw
from .. import ptext
from ..rect import Rect, ZRect
from .. import loaders
from .. import screen


def lee_posicion(pos):
    return screen.round_pos(pos)


def pon_color(arg):
    screen.make_color(arg)


class PintorPantalla(screen.SurfacePainter):
    def linea(self, start, end, color):
        self.line(start, end, color)

    def circulo(self, pos, radius, color):
        self.circle(pos, radius, color)

    def circulo_relleno(self, pos, radius, color):
        self.filled_circle(pos, radius, color)

    def rectangulo(self, rect, color):
        self.rect(rect, color)

    def rectangulo_relleno(self, rect, color):
        self.filled_rect(rect, color)

    def texto(self, *args, **kwargs):
        self.text(args, kwargs)

    def caja_texto(self, *args, **kwargs):
        self.textbox(args, kwargs)


class Pantalla(screen.Screen):
    def borra(self):
        self.clear()

    def pinta(self, color):
        self.fill(color)

    def coloca(self, image, pos):
        self.blit(image, pos)

    @property
    def dibuja(self):
        return PintorPantalla(self)
