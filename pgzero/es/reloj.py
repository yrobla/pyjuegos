"""Clock/event scheduler.

This is a Pygame implementation of a scheduler inspired by the clock
classes in Pyglet.

"""
import heapq
from weakref import ref
from functools import total_ordering
from types import MethodType
from pgzero import clock

__all__ = [
    'Reloj', 'pon_alarma', 'repite', 'quita_alarma'
]


@total_ordering
class Evento(clock.Event):
    """An event scheduled for a future time.

    Events are ordered by their scheduled execution time.

    """
    @property
    def ejecuta(self):
        return self.cb()


class Reloj(clock.Clock):
    """A clock used for event scheduling.

    When tick() is called, all events scheduled for before now will be called
    in order.

    tick() would typically be called from the game loop for the default clock.

    Additional clocks could be created - for example, a game clock that could
    be suspended in pause screens. Your code must take care of calling tick()
    or not. You could also run the clock at a different rate if desired, by
    scaling dt before passing it to tick().

    """
    def pon_alarma(self, callback, delay):
        self.schedule(callback, delay)

    def pon_alarma_unica(self, callback, delay):
        self.schedule_unique(callback, delay)

    def repite(self, callback, delay):
        self.schedule_interval(callback, delay)

    def quita_alarma(self, callback):
        self.unschedule(callback, delay)

    def cada_vez(self, callback):
        self.each_tick(callback)

    def vez(self, dt):
        self.tick(dt)


# One instance of a clock is available by default, to simplify the API
reloj = Reloj()
vez = reloj.vez
pon_alarma = reloj.pon_alarma
repite = reloj.repite
pon_alarma_unica = reloj.pon_alarma_unica
quita_alarma = reloj.quita_alarma
cada_vez = reloj.cada_vez
