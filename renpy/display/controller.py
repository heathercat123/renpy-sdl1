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

# Oh boy! Stubbing time!

import renpy.display

import pygame

import os


def load_mappings():
        pass


def init():
    return


def make_event(name):
    """
    Creates an EVENTNAME event with `name`, and returns it.
    """
    return None

def exists():
    """
    Returns true if a controller exists, and False otherwise.
    """
    return False


def quit(index):  # @ReservedAssignment
    """
    Quits the controller at index.
    """
    return


def start(index):
    """
    Starts the controller at index.
    """
    return


def event(ev):
    """
    Processes an event and returns the same event, a new event, or None if
    the event has been processed and should be ignored.
    """
    return None
