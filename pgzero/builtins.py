# Expose clock API as a builtin
from . import clock
from .es import reloj
from . import music
from .es import musica
from .actor import Actor
from .es.actor import Personaje
from .es.sonido import Sonido
from .keyboard import keyboard
from .es.teclado import teclado
from .animation import animate
from .es.animacion import animar
from .rect import Rect, ZRect

from .constants import mouse, keys, keymods
from .es.constantes import teclas

from .game import exit
