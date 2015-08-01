from pygame.mixer import music as _music
from ..loaders import ResourceLoader
from .. import constants
from pgzero import music


__all__ = [
    'atras', 'para', 'desaparece', 'pon_volumen', 'lee_volumen',
    'lee_posicion', 'pon_posicion', 'suena', 'encola', 'pausa',
    'despausa',
]

def suena(name):
    music.play(name)

def suena_una_vez(name):
    music.play_once(name)

def encola(name):
    music.queue(name)

def esta_sonando(name):
    return music.is_playing(name)

def pausa():
    music.pause()

def despausa():
    music.unpause()

def desaparece(seconds):
    music.fadeout(seconds)

rebobina = _music.rewind
para = _music.stop
lee_volumen = _music.get_volume
pon_volumen = _music.set_volume
lee_posicion = _music.get_pos
pon_posicion = _music.set_pos
