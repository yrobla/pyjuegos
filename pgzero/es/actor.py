import pygame

from .. import game
from .. import loaders
from .. import spellcheck

from pgzero import actor


ES_ANCHORS = {
    'x': {
        'izquierda': 0.0,
        'centro': 0.5,
        'medio': 0.5,
        'derecha': 1.0,
    },
    'y': {
        'arriba': 0.0,
        'centro': 0.5,
        'medio': 0.5,
        'abajo': 1.0,
    }
}


# These are methods (of the same name) on pygame.Rect
SYMBOLIC_POSITIONS = set((
    "arribaizquierda", "abajoizquierda", "arribaderecha",
    "abajoderecha", "medioarriba", "medioizquierda",
    "medioabajo", "medioderecha", "centro",
))

POS_TOPLEFT = None
ANCHOR_CENTER = None

class Personaje(actor.Actor):
    EXPECTED_INIT_KWARGS = SYMBOLIC_POSITIONS

    def __init__(self, image, pos=POS_TOPLEFT, anchor=ANCHOR_CENTER, **kwargs):
        if 'alto' in kwargs:
            kwargs['height'] = kwargs['alto']
            kwargs['alto'] = None

        if 'ancho' in kwargs:
            kwargs['width'] = kwargs['ancho']
            kwargs['ancho'] = None

        super(Personaje, self).__init__(image, pos=pos, anchor=anchor, kwargs=kwargs)

    @property
    def ancla(self):
        return self.anchor()

    @ancla.setter
    def ancla(self, val):
        self.anchor(val)

    @property
    def posicion(self):
        return self.pos()

    @posicion.setter
    def posicion(self, pos):
        self.posicion(pos)

    @property
    def imagen(self):
        return self.image()

    @imagen.setter
    def imagen(self, image):
        self._image_name = image
        p = self.pos
        self._surf = loaders.images.load(image)
        self.width, self.height = self._surf.get_size()
        self._calc_anchor()
        self.pos = p

    @property
    def alto(self):
        return self.height

    @alto.setter
    def alto(self, height):
        self.height = height

    @property
    def ancho(self):
        return self.width

    @ancho.setter
    def ancho(self, width):
        self.width = width

    @property
    def izquierda(self):
        return self.left

    @izquierda.setter
    def izquierda(self, left):
        self.left = left

    @property
    def derecha(self):
        return self.right

    @derecha.setter
    def derecha(self, right):
        self.right = right

    @property
    def arribaizquierda(self):
        return self.topleft

    @arribaizquierda.setter
    def arribaizquierda(self, topleft):
        self.topleft = topleft

    @property
    def abajoizquierda(self):
        return self.bottomleft

    @abajoizquierda.setter
    def abajoizquierda(self, bottomleft):
        self.bottomleft = bottomleft

    @property
    def arribaderecha(self):
        return self.topright

    @arribaderecha.setter
    def arribaderecha(self, topright):
        self.topright = topright

    @property
    def abajoderecha(self):
        return self.bottomright

    @abajoderecha.setter
    def abajoderecha(self, bottomright):
        self.bottomright = bottomright

    @property
    def medioarriba(self):
        return self.midtop

    @medioarriba.setter
    def medioarriba(self, midtop):
        self.midtop = midtop

    @property
    def medioizquierda(self):
        return self.midleft

    @medioizquierda.setter
    def medioizquierda(self, midleft):
        self.midleft = midleft

    @property
    def medioabajo(self):
        return self.midbottom

    @medioabajo.setter
    def medioabajo(self, midbottom):
        self.midbottom = midbottom

    @property
    def medioderecha(self):
        return self.midright

    @medioderecha.setter
    def medioderecha(self, midright):
        self.midright = midright

    @property
    def centro(self):
        return self.center

    @centro.setter
    def centro(self, center):
        self.center = center

    def dibuja(self):
        game.pantalla.blit(self._surf, self.arribaizquierda)

    def coincide(self, pos):
        return self.collidepoint(pos)
