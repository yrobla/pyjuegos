import sys
import operator
import time

import pygame
import pgzero.clock
import pgzero.keyboard
import pgzero.screen
import pgzero.es.pantalla

from . import constants


screen = None
pantalla = None
DISPLAY_FLAGS = 0


def exit():
    """Wait for up to a second for all sounds to play out
    and then exit
    """
    t0 = time.time()
    while pygame.mixer.get_busy():
        time.sleep(0.1)
        if time.time() - t0 > 1.0:
            break
    sys.exit()

def salir():
    exit()


def positional_parameters(handler):
    """Get the positional parameters of the given function."""
    code = handler.__code__
    return code.co_varnames[:code.co_argcount]


class PGZeroGame:
    WIDTH_CONSTANT = 'WIDTH'
    HEIGHT_CONSTANT = 'HEIGHT'
    TITLE_CONSTANT = 'TITLE'
    SCREEN_CONSTANT = 'screen'
    ICON_CONSTANT = 'ICON'

    DEFAULT_TITLE = 'Pygame Zero Game'
    DEFAULT_WIDTH = 800
    DEFAULT_HEIGHT = 600

    def __init__(self, mod):
        self.mod = mod
        self.screen = None
        self.width = None
        self.height = None
        self.title = None
        self.icon = None
        self.keyboard = pgzero.keyboard.keyboard
        self.handlers = {}

    def reinit_screen(self):
        global screen
        mod = self.mod
        w = getattr(mod, self.WIDTH_CONSTANT, self.DEFAULT_WIDTH)
        h = getattr(mod, self.HEIGHT_CONSTANT, self.DEFAULT_HEIGHT)
        if w != self.width or h != self.height:
            self.screen = pygame.display.set_mode((w, h), DISPLAY_FLAGS)
            if hasattr(self.mod, self.SCREEN_CONSTANT):
                self.mod.screen.surface = self.screen
            else:
                self.mod.screen = pgzero.screen.Screen(self.screen)
            screen = self.screen     # KILL ME
            self.width = w
            self.height = h

        icon = getattr(mod, self.ICON_CONSTANT, None)
        if icon and icon != self.icon:
            pygame.display.set_icon(pygame.image.load(icon))
            self.icon = icon

        title = getattr(self.mod, self.TITLE_CONSTANT, self.DEFAULT_TITLE)
        if title != self.title:
            pygame.display.set_caption(title)
            self.title = title

    EVENT_HANDLERS = {
        pygame.MOUSEBUTTONDOWN: 'on_mouse_down',
        pygame.MOUSEBUTTONUP: 'on_mouse_up',
        pygame.MOUSEMOTION: 'on_mouse_move',
        pygame.KEYDOWN: 'on_key_down',
        pygame.KEYUP: 'on_key_up',
        constants.MUSIC_END: 'on_music_end'
    }

    EVENT_PARAM_MAPPERS = {
        'button': constants.mouse,
        'key': constants.keys
    }

    def load_handlers(self):
        #from .spellcheck import spellcheck
        #spellcheck(vars(self.mod))
        self.handlers = {}
        for type, name in self.EVENT_HANDLERS.items():
            handler = getattr(self.mod, name, None)
            if callable(handler):
                self.handlers[type] = self.prepare_handler(handler)

    def prepare_handler(self, handler):
        """Adapt a pgzero game's raw handler function to take a Pygame Event.

        Returns a one-argument function of the form ``handler(event)``.
        This will ensure that the correct arguments are passed to the raw
        handler based on its argument spec.

        The wrapped handler will also map certain parameter values using
        callables from EVENT_PARAM_MAPPERS; this ensures that the value of
        'button' inside the handler is a real instance of constants.mouse,
        which means (among other things) that it will print as a symbolic value
        rather than a naive integer.

        """
        code = handler.__code__
        param_names = code.co_varnames[:code.co_argcount]

        def make_getter(mapper, getter):
            if mapper:
                return lambda event: mapper(getter(event))
            return getter

        param_handlers = []
        for name in param_names:
            getter = operator.attrgetter(name)
            mapper = self.EVENT_PARAM_MAPPERS.get(name)
            param_handlers.append((name, make_getter(mapper, getter)))

        def prep_args(event):
            return {name: get(event) for name, get in param_handlers}

        def new_handler(event):
            try:
                prepped = prep_args(event)
            except ValueError:
                # If we couldn't construct the keys/mouse objects representing
                # the button that was pressed, then skip the event handler.
                #
                # This happens because Pygame can generate key codes that it
                # does not have constants for.
                return
            else:
                return handler(**prepped)

        return new_handler

    def dispatch_event(self, event):
        handler = self.handlers.get(event.type)
        if handler:
            self.need_redraw = True
            handler(event)

    def get_update_func(self):
        """Get a one-argument update function.

        If the module defines a function matching ::

            update(dt)

        or ::

            update()

        then this will be called. Otherwise return a no-op function.

        """
        try:
            update = self.mod.update
        except AttributeError:
            return None
        else:
            if update.__code__.co_argcount == 0:
                return lambda dt: update()
            return update

    def get_draw_func(self):
        """Get a draw function.

        If no draw function is define, raise an exception.

        """
        try:
            draw = self.mod.draw
        except AttributeError:
            return lambda: None
        else:
            if draw.__code__.co_argcount != 0:
                raise TypeError(
                    "draw() must not take any arguments."
                )
            return draw

    def run(self):
        clock = pygame.time.Clock()
        self.reinit_screen()

        update = self.get_update_func()
        draw = self.get_draw_func()
        self.load_handlers()

        pgzclock = pgzero.clock.clock

        self.need_redraw = True
        while True:
            dt = clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q and \
                            event.mod & (pygame.KMOD_CTRL | pygame.KMOD_META):
                        sys.exit(0)
                    self.keyboard._press(event.key)
                elif event.type == pygame.KEYUP:
                    self.keyboard._release(event.key)
                self.dispatch_event(event)

            pgzclock.tick(dt)

            if update:
                update(dt)

            if update or pgzclock.fired or self.need_redraw:
                self.reinit_screen()
                draw()
                pygame.display.flip()
                self.need_redraw = False

# spanish version
class Juego(PGZeroGame):
    WIDTH_CONSTANT = 'ANCHO'
    HEIGHT_CONSTANT = 'ALTO'
    TITLE_CONSTANT = 'TITULO'
    SCREEN_CONSTANT = 'pantalla'
    ICON_CONSTANT = 'ICONO'

    DEFAULT_TITLE = 'Juego'

    def __init__(self, mod):
        self.mod = mod
        self.pantalla = None
        self.ancho = None
        self.alto = None
        self.titulo = None
        self.icono = None
        self.teclado = pgzero.keyboard.keyboard
        self.handlers = {}

    def reinit_screen(self):
        global pantalla
        mod = self.mod
        w = getattr(mod, self.WIDTH_CONSTANT, self.DEFAULT_WIDTH)
        h = getattr(mod, self.HEIGHT_CONSTANT, self.DEFAULT_HEIGHT)
        if w != self.ancho or h != self.alto:
            self.pantalla = pygame.display.set_mode((w, h), DISPLAY_FLAGS)
            if hasattr(self.mod, self.SCREEN_CONSTANT):
                self.mod.pantalla.superficie = self.pantalla
            else:
                self.mod.pantalla = pgzero.es.pantalla.Pantalla(self.pantalla)
            pantalla = self.pantalla     # KILL ME
            self.ancho =w
            self.alto = h

        icono = getattr(mod, self.ICON_CONSTANT, None)
        if icono and icono != self.icono:
            pygame.display.set_icon(pygame.image.load(icono))
            self.icono = icono

        titulo = getattr(self.mod, self.TITLE_CONSTANT, self.DEFAULT_TITLE)
        if titulo != self.titulo:
            pygame.display.set_caption(titulo)
            self.titulo = titulo


    EVENT_HANDLERS = {
        pygame.MOUSEBUTTONDOWN: 'cuando_raton_pulsa',
        pygame.MOUSEBUTTONUP: 'cuando_raton_suelta',
        pygame.MOUSEMOTION: 'cuando_raton_mueve',
        pygame.KEYDOWN: 'cuando_tecla_pulsa',
        pygame.KEYUP: 'cuando_tecla_suelta',
        constants.MUSIC_END: 'cuando_acaba_musica'
    }

    def run(self):
        clock = pygame.time.Clock()
        self.reinit_screen()

        update = self.get_update_func()
        draw = self.get_draw_func()
        self.load_handlers()

        pgzclock = pgzero.es.reloj.reloj

        self.need_redraw = True
        while True:
            dt = clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q and \
                            event.mod & (pygame.KMOD_CTRL | pygame.KMOD_META):
                        sys.exit(0)
                    self.teclado._press(event.key)
                elif event.type == pygame.KEYUP:
                    self.teclado._release(event.key)
                self.dispatch_event(event)

            pgzclock.vez(dt)

            if update:
                update(dt)

            if update or pgzclock.fired or self.need_redraw:
                self.reinit_screen()
                draw()
                pygame.display.flip()
                self.need_redraw = False

    def jugar(self):
        self.run()

    def get_update_func(self):
        """Get a one-argument update function.

        If the module defines a function matching ::

            update(dt)

        or ::

            update()

        then this will be called. Otherwise return a no-op function.

        """
        try:
            refresca = self.mod.refresca
        except AttributeError:
            return None
        else:
            if refresca.__code__.co_argcount == 0:
                return lambda dt: refresca()
            return refresca

    def get_draw_func(self):
        """Get a draw function.

        If no draw function is define, raise an exception.

        """
        try:
            dibuja = self.mod.dibuja
        except AttributeError:
            return lambda: None
        else:
            if dibuja.__code__.co_argcount != 0:
                raise TypeError(
                    "draw() must not take any arguments."
                )
            return dibuja

