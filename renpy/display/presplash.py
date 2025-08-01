# Copyright 2004-2017 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Pre-splash code. The goal of this code is to try to get a pre-splash
# screen up as soon as possible, to let the user know something is
# going on.

import threading
import pygame
import os.path
import sys
import time

import renpy

# The window.
window = None

# Should the event thread keep running?
keep_running = False

# The start time.
start_time = time.time()

PRESPLASHEVENT = pygame.USEREVENT


def run_event_thread():
    """
    Disposes of events while the window is running.
    """

    pygame.time.set_timer(PRESPLASHEVENT, 20)

    while keep_running:
        pygame.event.wait()

    pygame.time.set_timer(PRESPLASHEVENT, 0)


def start(basedir, gamedir):
    """
    Called to display the presplash when necessary.
    """

    if "RENPY_LESS_UPDATES" in os.environ:
        return

    filenames = [ "/presplash.png", "/presplash.jpg" ]
    for fn in filenames:
        fn = gamedir + fn
        if os.path.exists(fn):
            break
    else:
        return

    if renpy.windows:

        import ctypes
        from ctypes import c_void_p, c_int

        ctypes.windll.user32.SetProcessDPIAware()

    pygame.display.init()

    img = pygame.image.load(fn, fn)

    global window

    bounds = pygame.display.get_display_bounds(0)

    sw, sh = img.get_size()
    x = bounds[0] + bounds[2] // 2 - sw // 2
    y = bounds[1] + bounds[3] // 2 - sh // 2

    window = pygame.display.Window(
        sys.argv[0],
        img.get_size(),
        flags=pygame.WINDOW_BORDERLESS,
        pos=(x, y))

    img = img.convert_alpha(window.get_surface())

    window.get_surface().blit(img, (0, 0))
    window.update()

    global event_thread

    event_thread = threading.Thread(target=run_event_thread)
    event_thread.daemon = True
    event_thread.start()

    global start_time
    start_time = time.time()


def end():
    """
    Called just before we initialize the display to hide the presplash.
    """

    global keep_running
    global event_thread
    global window

    if window is None:
        return

    keep_running = False

    event_thread.join()

    window.destroy()
    window = None


def sleep():
    """
    Sleep to the end of config.minimum_presplash_time.
    """

    if not (window or renpy.mobile):
        return

    remaining = start_time + renpy.config.minimum_presplash_time - time.time()

    if remaining > 0:
        time.sleep(remaining)
