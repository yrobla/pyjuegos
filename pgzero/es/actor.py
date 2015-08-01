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
ES_SYMBOLIC_POSITIONS = set((
    "arribaizquierda", "abajoizquierda", "arribaderecha",
    "abajoderecha", "medioarriba", "medioizquierda",
    "medioabajo", "medioderecha", "centro",
))

class Actor(actor.Actor):
    EXPECTED_INIT_KWARGS = ES_SYMBOLIC_POSITIONS

    def _init_position(self, pos, anchor, **kwargs):
        if anchor is None:
            anchor = ("center", "center")
        self.anchor = anchor

        symbolic_pos_args = {
            k: kwargs[k] for k in kwargs if k in ES_SYMBOLIC_POSITIONS}

        if not pos and not symbolic_pos_args:
            # No positional information given, use sensible top-left default
            self.topleft = (0, 0)
        elif pos and symbolic_pos_args:
            raise TypeError("'pos' argument cannot be mixed with 'topleft', 'topright' etc. argument.")
        elif pos:
            self.pos = pos
        else:
            self._set_symbolic_pos(symbolic_pos_args)

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
        self.image(image)

    def dibuja(self):
        self.draw()
