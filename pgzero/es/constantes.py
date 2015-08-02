"""Names for constants returned by Pygame."""
from enum import IntEnum
import pygame.locals


# Event type indicating the end of a music track
FINAL_MUSICA = 99


class raton(IntEnum):
    IZQUIERDA = 1
    MEDIO = 2
    DERECHA = 3
    RUEDA_ARRIBA = 4
    RUEDA_ABAJO = 5


# Use a code generation approach to copy Pygame's key constants out into
# a Python 3.4 IntEnum, stripping prefixes where possible
srclines = ["class teclas(IntEnum):"]
for k, v in vars(pygame.locals).items():
    if k.startswith('K_'):
        if k[2].isalpha():
            k = k[2:]
        srclines.append("    %s = %d" % (k.upper(), v))

srclines.append("class teclasmods(IntEnum):")
for k, v in vars(pygame.locals).items():
    if k.startswith('KMOD_'):
        srclines.append("    %s = %d" % (k[5:].upper(), v))

exec('\n'.join(srclines), globals())
del srclines
