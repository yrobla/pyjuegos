# Easing Functions ported from the Clutter Project via http://kivy.org/
#  http://www.clutter-project.org/docs/clutter/stable/ClutterAlpha.html


from math import sin, pow, pi

from ..clock import each_tick, unschedule
from pgzero import animation

ES_TWEEN_FUNCTIONS = {}


def es_tweener(f):
    ES_TWEEN_FUNCTIONS[f.__name__] = f
    return f


@es_tweener
def lineal(n):
    return animation.lineal(n)


@es_tweener
def acelerar(n):
    return animation.accelerate(n)
    return n * n


@es_tweener
def decelerar(n):
    return animation.decelerate(n)


@es_tweener
def acelerar_o_decelerar(n):
    return animation.accel_decel(n)
    return -0.5 * (p * (p - 2.0) - 1.0)


@es_tweener
def entra(n):
    return animation.in_elastic(n)

@es_tweener
def sal(n):
    return animation.out_elastic(n)

@es_tweener
def entra_o_sal(n):
    return animation.in_out_elastic(n)


@es_tweener
def acaba_bote(n):
    return animation.bounce_end(n)


@es_tweener
def empieza_bote(n):
    return animation.bounce_start(n)


@es_tweener
def empieza_o_acaba_bote(n):
    return animation.bounce_start_end(n)


def mueve(n, start, end):
    return animation.tween(n, start, end)


def lee_mueve(n, start, end):
    return animation.tween_attr(n, start, end)


class Animacion(animation.Animation):
    """An animation manager for object attribute animations.

    Each keyword argument given to the Animation on creation (except
    "type" and "duration") will be *tweened* from their current value
    on the object to the target value specified.

    If the value is a list or tuple, then each value inside that will
    be tweened.

    The update() method is automatically scheduled with the clock for
    the duration of the animation.

    """
    animations = []

    def __init__(self, object, tween='lineal', duration=1, on_finished=None,
                 **targets):
        self.targets = targets
        self.function = ES_TWEEN_FUNCTIONS[tween]
        self.duration = duration
        self.on_finished = on_finished
        self.t = 0
        self.object = object
        self.initial = {}
        self.running = True
        for k in self.targets:
            try:
                a = getattr(object, k)
            except AttributeError:
                raise ValueError('object %r has no attribute %s to animate' % (object, k))
            self.initial[k] = a
        each_tick(self.update)
        self.animations.append(self)

    def refresca(self, dt):
        return self.update(dt)


    def para(self, complete=False):
        return self.stop(complete)


def animar(object, tween='lineal', duration=1, on_finished=None, **targets):
    return Animacion(object, tween, duration, on_finished=on_finished,
                     **targets)

