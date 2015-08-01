# Expose clock API as a builtin
from . import clock
from .es import reloj
from . import music
from .es import musica
from .actor import Actor
from .es.actor import Actor
from .keyboard import keyboard
from .es.teclado import teclado
from .animation import animate
from .es.animacion import animar
from .rect import Rect, ZRect

from .constants import mouse, keys, keymods

from .game import exit
