#!/usr/bin/env python

# Copyright 2004-2014 Tom Rothamel <pytom@bishoujo.us>
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

import platform
import sys
import os

# Change to the directory containing this file.
os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))

# Create the gen directory if it doesn't exist.
try:
    os.makedirs("gen")
except:
    pass

# Generate styles.
import generate_styles
generate_styles.generate()


# If RENPY_CC or RENPY_LD are in the environment, and CC or LD are not, use them.
def setup_env(name):
    renpy_name = "RENPY_" + name
    if (renpy_name in os.environ) and (name not in os.environ):
        os.environ[name] = os.environ[renpy_name]

setup_env("CC")
setup_env("LD")

import setuplib
from setuplib import android, include, library, cython, pymodule, copyfile, find_unnecessary_gen

# These control the level of optimization versus debugging.
setuplib.extra_compile_args = [ "-Wno-unused-function" ]
setuplib.extra_link_args = [ ]

# Detect win32.
if platform.win32_ver()[0]:
    windows = True
    setuplib.extra_compile_args.append("-fno-strict-aliasing")
else:
    windows = False

include("zlib.h")
include("png.h")
include("SDL.h", directory="SDL")
include("ft2build.h")
include("freetype/freetype.h", directory="freetype2", optional=True) or include("freetype.h", directory="freetype2")
include("libavutil/avstring.h")
include("libavformat/avformat.h")
include("libavcodec/avcodec.h")
include("libswscale/swscale.h")
include("GL/glew.h")

library("SDL")
library("png")
library("avformat")
library("avcodec")
library("avutil")
has_avresample = library("avresample", optional=True)
has_swscale = library("swscale", optional=True)
library("freetype")
has_fribidi = library("fribidi", optional=True)
library("z")
has_libglew = library("GLEW", optional=True)
has_libglew32 = library("glew32", optional=True)
has_angle = windows and library("EGL", optional=True) and library("GLESv2", optional=True)

if android:
    sdl = [ 'sdl', 'GLESv2', 'log' ]
else:
    sdl = [ 'SDL' ]


# Modules directory.
cython(
    "_renpy",
    [ "IMG_savepng.c", "core.c", "subpixel.c"],
    sdl + [ 'png', 'z', 'm' ])

if has_fribidi and not android:
    cython(
        "_renpybidi",
        [ "renpybidicore.c" ],
        ['fribidi'], define_macros=[ ("FRIBIDI_ENTRY", "") ])

# Sound.
pymodule("pysdlsound.__init__")

if not android:

    sound = [ "avformat", "avcodec", "avutil", "z" ]
    macros = [ ]

    if has_avresample:
        sound.insert(0, "avresample")
        macros.append(("HAS_RESAMPLE", 1))

    if has_swscale:
        sound.insert(0, "swscale")

    cython(
        "pysdlsound.sound",
        [ "pss.c", "ffdecode.c" ],
        libs = sdl + sound,
        define_macros=macros)

# renpy
cython("renpy.style")
cython("renpy.styleclass")

# renpy.display
cython("renpy.display.render", libs=[ 'z', 'm' ])
cython("renpy.display.accelerator", libs=sdl + [ 'z', 'm' ])

# renpy.gl
if android:
    glew_libs = [ 'GLESv2', 'z', 'm' ]
elif has_libglew:
    glew_libs = [ 'GLEW' ]
else:
    glew_libs = [ 'glew32', 'opengl32' ]

cython("renpy.gl.gldraw", libs=glew_libs )
cython("renpy.gl.gltexture", libs=glew_libs)
cython("renpy.gl.glenviron_shader", libs=glew_libs)
cython("renpy.gl.glenviron_fixed", libs=glew_libs, compile_if=not android)
cython("renpy.gl.glenviron_limited", libs=glew_libs, compile_if=not android)
cython("renpy.gl.glrtt_copy", libs=glew_libs)
cython("renpy.gl.glrtt_fbo", libs=glew_libs)

# renpy.angle
def anglecopy(fn):
    if android:
        return

    copyfile("renpy/gl/" + fn, "renpy/angle/" + fn, "DEF ANGLE = False", "DEF ANGLE = True")

anglecopy("glblacklist.py")
anglecopy("gldraw.pxd")
anglecopy("gldraw.pyx")
anglecopy("glenviron_shader.pyx")
anglecopy("gl.pxd")
anglecopy("glrtt_fbo.pyx")
anglecopy("glrtt_copy.pyx")
anglecopy("gltexture.pxd")
anglecopy("gltexture.pyx")

angle_libs = [ "SDL", "EGL", "GLESv2" ]

def anglecython(name, source=[]):
    cython(name, libs=angle_libs, compile_if=has_angle, define_macros=[ ( "ANGLE", None ) ], source=source)

anglecython("renpy.angle.gldraw", source=[ "anglesupport.c" ])
anglecython("renpy.angle.gltexture")
anglecython("renpy.angle.glenviron_shader")
anglecython("renpy.angle.glrtt_fbo")
anglecython("renpy.angle.glrtt_copy")

# renpy.text
cython("renpy.text.textsupport")
cython("renpy.text.texwrap")

cython(
    "renpy.text.ftfont",
    [ "ftsupport.c", "ttgsubtable.c" ],
    libs = sdl + [ 'freetype', 'z', 'm' ])

find_unnecessary_gen()

# Figure out the version, and call setup.
sys.path.insert(0, '..')
import renpy

setuplib.setup("Ren'Py", renpy.version[7:])

if not has_fribidi:
    print "Warning: Did not include fribidi."
